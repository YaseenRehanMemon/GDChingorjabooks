#!/usr/bin/env python3
"""
Simple MCQ Generator using Gemini API
A streamlined version for generating MCQs from PDF textbooks
"""

import os
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Any

# Check and import dependencies
try:
    import google.generativeai as genai
    print("✅ google-generativeai imported successfully")
except ImportError:
    print("❌ google-generativeai not installed")
    print("Run: pip install google-generativeai")
    exit(1)

try:
    import fitz
    print("✅ PyMuPDF (fitz) imported successfully")
except ImportError:
    print("❌ PyMuPDF not installed")
    print("Run: pip install PyMuPDF")
    exit(1)


class SimpleMCQGenerator:
    def __init__(self, api_keys_file: str = "/home/yaseen/apikeys"):
        self.api_keys = self.load_api_keys(api_keys_file)
        self.current_key_index = 2  # Start with API key 3 (index 2)

        # Configuration
        self.target_mcqs_per_subject = 500  # Generate minimum 500 MCQs per subject
        self.target_mcqs_per_chapter = 50   # Target MCQs per chapter
        self.max_single_request = 5         # Maximum MCQs per API request (API limit)
        self.max_requests_per_chapter = 10  # Maximum API requests per chapter
        self.max_pdf_size_mb = 19
        self.api_delay = 3                  # Delay between API requests (seconds)

        print(f"🔑 Loaded {len(self.api_keys)} API keys")

    def load_api_keys(self, filepath: str) -> List[str]:
        """Load API keys from file"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            keys = [line.strip() for line in content.split('\n')
                    if line.strip().startswith('AIzaSy')]
            return keys
        except FileNotFoundError:
            print(f"❌ API keys file not found: {filepath}")
            return []

    def setup_gemini(self):
        """Setup Gemini with current API key"""
        if not self.api_keys:
            raise ValueError("No API keys available")

        current_key = self.api_keys[self.current_key_index]
        genai.configure(api_key=current_key)
        print(f"🔄 Using API key {self.current_key_index + 1}")

    def rotate_api_key(self):
        """Rotate to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.setup_gemini()



    def compress_pdf(self, pdf_path: str) -> str:
        """Compress PDF if needed"""
        file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)

        if file_size_mb <= self.max_pdf_size_mb:
            return pdf_path

        print(f"📦 Compressing PDF ({file_size_mb:.1f}MB)...")

        try:
            doc = fitz.open(pdf_path)
            compressed_path = pdf_path.replace('.pdf', '_compressed.pdf')

            doc.save(
                compressed_path,
                garbage=4,
                deflate=True,
                clean=True
            )
            doc.close()

            new_size = os.path.getsize(compressed_path) / (1024 * 1024)
            print(f"✅ Compressed to {new_size:.1f}MB")

            return compressed_path
        except Exception as e:
            print(f"⚠️ Compression failed: {e}")
            return pdf_path

    def generate_mcqs_for_chapter(self, pdf_path: str, subject: str, chapter: str) -> Dict[str, Any]:
        """Generate MCQs for a single chapter"""

        # Setup API
        self.setup_gemini()

        # Compress PDF if needed
        processed_pdf = self.compress_pdf(pdf_path)

        try:
            # Upload PDF
            print(f"📤 Uploading PDF: {os.path.basename(processed_pdf)}")
            sample_file = genai.upload_file(processed_pdf)

            # Wait for processing
            print("⏳ Processing PDF...")
            while sample_file.state.name == "PROCESSING":
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)

            if sample_file.state.name != "ACTIVE":
                raise ValueError(f"PDF processing failed: {sample_file.state.name}")

            # Create model and generate MCQs
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Generate MCQs in multiple requests to reach target
            mcqs = []
            request_count = 0
            max_requests = 15  # Maximum number of API requests
            response = None

            while len(mcqs) < self.target_mcqs_per_chapter and request_count < max_requests:
                request_count += 1
                remaining_needed = self.target_mcqs_per_chapter - len(mcqs)
                request_size = min(self.max_single_request, remaining_needed)

                print(f"🎯 Request {request_count}: Generating {request_size} MCQs (Total needed: {remaining_needed})...")

                if request_count == 1:
                    prompt = self.create_mcq_prompt(subject, chapter)
                else:
                    prompt = self.create_additional_mcq_prompt(subject, chapter, request_size, len(mcqs))

                response = model.generate_content([sample_file, prompt])

                if response and response.text:
                    batch_mcqs = self.parse_response(response.text, subject, chapter)
                    mcqs.extend(batch_mcqs)
                    print(f"✅ Request {request_count}: Got {len(batch_mcqs)} MCQs (Total: {len(mcqs)})")

                    # Add delay between requests to avoid rate limits
                    if request_count < max_requests and len(mcqs) < self.target_mcqs_per_chapter:
                        print("⏳ Waiting 2 seconds before next request...")
                        time.sleep(2)
                else:
                    print(f"❌ Request {request_count} failed")
                    break

            print(f"🏁 Generation complete: {len(mcqs)} MCQs generated in {request_count} requests")

            # Clean up
            sample_file.delete()

            if response and response.text:
                # Debug: Save raw response
                with open(f'/home/yaseen/ourbooks/debug_raw_response_{chapter}.txt', 'w') as f:
                    f.write(response.text)
                print(f"💾 Saved raw response to debug_raw_response_{chapter}.txt")

                mcqs = self.parse_response(response.text, subject, chapter)
                return self.format_mcq_data(mcqs, subject, chapter)
            else:
                raise ValueError("No response from API")

        except Exception as e:
            print(f"❌ Error generating MCQs: {e}")
            # Try with different API key
            if len(self.api_keys) > 1:
                print("🔄 Trying with different API key...")
                self.rotate_api_key()
                return self.generate_mcqs_for_chapter(pdf_path, subject, chapter)
            raise e

    def create_mcq_prompt(self, subject: str, chapter: str) -> str:
        """Create MCQ generation prompt"""
        return f"""You are an expert educator specializing in Pakistani Intermediate ({subject}) curriculum.

Analyze the provided PDF chapter content and generate {self.target_mcqs_per_chapter} comprehensive MCQs.

**Requirements:**
- Generate EXACTLY {self.target_mcqs_per_chapter} MCQs
- Cover ALL topics from the chapter
- Mix of easy, medium, and hard difficulty
- Use LaTeX for math: $x^2$, $\\frac{{a}}{{b}}$, etc.
- Provide detailed explanations

**Output Format (Valid JSON Array):**
[
  {{
    "question": "Question text with $LaTeX$ formulas",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation",
    "difficulty": "easy",
    "topic": "main_topic",
    "subtopic": "specific_subtopic"
  }}
]

Generate the MCQs now. Return ONLY the JSON array, no additional text."""

    def create_batch_mcq_prompt(self, subject: str, chapter: str, batch_size: int, batch_num: int) -> str:
        """Create batch MCQ generation prompt"""
        return f"""You are an expert educator specializing in Pakistani Intermediate ({subject}) curriculum.

Analyze the provided PDF chapter content and generate {batch_size} comprehensive MCQs for batch {batch_num + 1}.

**Requirements:**
- Generate EXACTLY {batch_size} MCQs
- Focus on different topics than previous batches
- Mix of easy, medium, and hard difficulty
- Use LaTeX for math: $x^2$, $\\frac{{a}}{{b}}$, etc.
- Provide detailed explanations

**Output Format (Valid JSON Array):**
[
  {{
    "question": "Question text with $LaTeX$ formulas",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation",
    "difficulty": "easy",
    "topic": "main_topic",
    "subtopic": "specific_subtopic"
  }}
]

Generate the MCQs now. Return ONLY the JSON array, no additional text."""

    def create_additional_mcq_prompt(self, subject: str, chapter: str, count: int, existing_count: int) -> str:
        """Create additional MCQ generation prompt"""
        return f"""You are an expert educator specializing in Pakistani Intermediate ({subject}) curriculum.

Analyze the provided PDF chapter content and generate {count} additional comprehensive MCQs.
You have already generated {existing_count} MCQs, so focus on different topics and questions.

**Requirements:**
- Generate EXACTLY {count} NEW MCQs
- Cover topics not covered in previous MCQs
- Mix of easy, medium, and hard difficulty
- Use LaTeX for math: $x^2$, $\\frac{{a}}{{b}}$, etc.
- Provide detailed explanations

**Output Format (Valid JSON Array):**
[
  {{
    "question": "Question text with $LaTeX$ formulas",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation",
    "difficulty": "easy",
    "topic": "main_topic",
    "subtopic": "specific_subtopic"
  }}
]

Generate the additional MCQs now. Return ONLY the JSON array, no additional text."""

    def parse_response(self, response_text: str, subject: str, chapter: str) -> List[Dict[str, Any]]:
        """Parse API response into structured format"""
        try:
            # Clean the response text
            response_text = response_text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            # Skip LaTeX fixing for now - Gemini returns properly formatted LaTeX
            # response_text = self.fix_latex_in_json(response_text)

            # Try to parse the entire response as JSON first
            try:
                mcqs = json.loads(response_text)
                if isinstance(mcqs, list):
                    print(f"✅ Successfully parsed {len(mcqs)} MCQs")
                    return mcqs
                else:
                    raise ValueError("Response is not a JSON array")
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON array
                print("⚠️ Direct JSON parsing failed, trying extraction...")

                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1

                if start_idx == -1:
                    print(f"❌ No JSON array found in response")
                    print(f"Response preview: {response_text[:300]}...")
                    raise ValueError("No JSON array found")

                json_str = response_text[start_idx:end_idx]

                # Skip LaTeX fixing for extracted JSON too
                # json_str = self.fix_latex_in_json(json_str)

                # Debug: Print the extracted JSON
                print(f"📄 Extracted JSON length: {len(json_str)}")
                print(f"📄 JSON preview: {json_str[:200]}...")

                # Try to fix common JSON issues
                json_str = json_str.strip()

                # If it ends with a comma before closing, remove it
                if json_str.endswith(',]'):
                    json_str = json_str[:-2] + ']'

                try:
                    mcqs = json.loads(json_str)
                    print(f"✅ Successfully parsed {len(mcqs)} MCQs via extraction")
                    return mcqs
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing failed: {e}")
                    print(f"Problem area: {json_str[max(0, 4110):4120]}...")

                    # Try to salvage partial JSON
                    try:
                        # Find the last complete object
                        last_complete = json_str.rfind('},') + 1
                        if last_complete > 1:
                            partial_json = json_str[:last_complete] + ']'
                            partial_json = self.fix_latex_in_json(partial_json)
                            mcqs = json.loads(partial_json)
                            print(f"⚠️ Parsed partial JSON with {len(mcqs)} MCQs")
                            return mcqs
                    except Exception as salvage_error:
                        print(f"❌ Could not salvage partial JSON: {salvage_error}")
                        raise ValueError(f"Failed to parse JSON: {e}")

        except Exception as e:
            print(f"❌ Unexpected error in parse_response: {e}")
            raise ValueError(f"Failed to parse response: {e}")

        # This should never be reached, but needed for type checking
        return []

    def fix_latex_in_json(self, text: str) -> str:
        """Fix LaTeX expressions that cause JSON parsing issues"""
        import re

        # Replace problematic LaTeX commands with safe alternatives
        replacements = {
            r'\\times': '×',  # Multiplication symbol
            r'\\frac{([^}]+)}{([^}]+)}': r'\1/\2',  # Simple fractions
            r'\\text{([^}]+)}': r'\1',  # Remove text commands
            r'\\mathrm{([^}]+)}': r'\1',  # Remove math roman
            r'\\ce{([^}]+)}': r'\1',  # Remove chemistry expressions
            r'\\Delta': 'Δ',  # Delta symbol
            r'\\alpha': 'α',  # Alpha symbol
            r'\\beta': 'β',   # Beta symbol
            r'\\gamma': 'γ',  # Gamma symbol
            r'\\delta': 'δ',  # Delta symbol
            r'\\rightarrow': '→',  # Arrow
            r'\\leftarrow': '←',  # Left arrow
            r'\\leftrightarrow': '↔',  # Double arrow
            r'\\pm': '±',     # Plus minus
            r'\\approx': '≈', # Approximately equal
            r'\\neq': '≠',    # Not equal
            r'\\leq': '≤',    # Less than or equal
            r'\\geq': '≥',    # Greater than or equal
            r'\\infty': '∞',  # Infinity
            r'\\pi': 'π',     # Pi
            r'\\sigma': 'σ',  # Sigma
            r'\\mu': 'μ',     # Mu
            r'\\nu': 'ν',     # Nu
            r'\\tau': 'τ',    # Tau
            r'\\omega': 'ω',  # Omega
            r'\\deg': '°',    # Degree
            r'\\circ': '°',   # Circle (degree)
            r'\\prime': "'",  # Prime
            r'\\cdot': '·',   # Center dot
            r'\\cdots': '...', # Center ellipsis
            r'\\vdots': ':',  # Vertical ellipsis
            r'\\ddots': '...', # Diagonal ellipsis
        }

        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)

        # Handle superscripts and subscripts (basic)
        text = re.sub(r'\^\{([^}]+)\}', r'^\1', text)  # Remove braces from superscripts
        text = re.sub(r'_\{([^}]+)\}', r'_\1', text)   # Remove braces from subscripts

        # Handle double backslashes that might cause issues
        text = re.sub(r'\\\\', r'\\', text)

        return text

    def format_mcq_data(self, mcqs: List[Dict[str, Any]], subject: str, chapter: str) -> Dict[str, Any]:
        """Format MCQs into the expected data structure"""
        # Validate and enhance MCQs
        validated_mcqs = []
        for i, mcq in enumerate(mcqs):
            # Ensure required fields
            mcq['id'] = f"{subject.lower()}_xi_{chapter}_mcq_{str(i+1).zfill(3)}"
            mcq['question_type'] = 'multiple_choice'
            mcq['created_date'] = '2024-09-11'
            mcq['source'] = f"{chapter}.pdf"
            mcq['ai_generated'] = True
            mcq['reviewed'] = False
            mcq['quality_score'] = 0.9
            mcq['tags'] = mcq.get('tags', [mcq.get('topic', 'general')])
            mcq['learning_objective'] = mcq.get('learning_objective', f"Understand {mcq.get('topic', 'topic')}")

            validated_mcqs.append(mcq)

        return {
            'subject': subject,
            'chapter': chapter,
            'total_mcqs': len(validated_mcqs),
            'mcqs': validated_mcqs
        }

    def save_mcqs(self, mcq_data: Dict[str, Any], output_dir: str):
        """Save MCQs to JSON file"""
        os.makedirs(output_dir, exist_ok=True)

        subject_dir = os.path.join(output_dir, f"{mcq_data['subject'].lower()}_chapters")
        os.makedirs(subject_dir, exist_ok=True)

        filename = f"{mcq_data['chapter']}_mcqs.json"
        filepath = os.path.join(subject_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mcq_data['mcqs'], f, indent=2, ensure_ascii=False)

        print(f"💾 Saved {mcq_data['total_mcqs']} MCQs to {filepath}")

    def test_single_chapter(self):
        """Test with a single chapter"""
        pdf_path = "/home/yaseen/books/chemistry_chapters/ch1.pdf"
        output_dir = "/home/yaseen/ourbooks/mcq_output"

        if not os.path.exists(pdf_path):
            print(f"❌ Test PDF not found: {pdf_path}")
            return

        print("🧪 Testing MCQ generation...")
        print(f"📄 PDF: {pdf_path}")
        print(f"📁 Output: {output_dir}")

        try:
            mcq_data = self.generate_mcqs_for_chapter(pdf_path, 'chemistry', 'ch1')
            self.save_mcqs(mcq_data, output_dir)
            print("✅ Test successful!")
            return True
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

    def generate_subject_mcqs(self, subject: str, pdf_base_dir: str, output_dir: str):
        """Generate MCQs for an entire subject to reach 500+ MCQs"""
        print(f"🚀 STARTING MASSIVE MCQ GENERATION FOR {subject.upper()}")
        print(f"🎯 Target: {self.target_mcqs_per_subject} MCQs")
        print(f"📁 PDF Directory: {pdf_base_dir}")
        print(f"💾 Output Directory: {output_dir}")
        print("=" * 60)

        # Get all available chapters
        if not os.path.exists(pdf_base_dir):
            print(f"❌ PDF directory not found: {pdf_base_dir}")
            return []

        chapters = []
        for file in os.listdir(pdf_base_dir):
            if file.endswith('.pdf'):
                chapter_name = file.replace('.pdf', '')
                chapters.append(chapter_name)

        print(f"📚 Found {len(chapters)} chapters: {chapters[:5]}...")

        all_mcqs = []
        total_generated = 0
        processed_chapters = 0

        for i, chapter in enumerate(chapters, 1):
            pdf_path = os.path.join(pdf_base_dir, f"{chapter}.pdf")

            if not os.path.exists(pdf_path):
                print(f"⚠️ PDF not found: {pdf_path}, skipping...")
                continue

            print(f"\\n📖 Chapter {i}/{len(chapters)}: {chapter}")
            print(f"📊 Progress: {total_generated}/{self.target_mcqs_per_subject} MCQs")

            try:
                # Generate multiple batches for this chapter
                chapter_mcqs = self.generate_chapter_batches(pdf_path, subject, chapter)

                if chapter_mcqs:
                    chapter_count = len(chapter_mcqs)
                    all_mcqs.extend(chapter_mcqs)
                    total_generated += chapter_count
                    processed_chapters += 1

                    print(f"✅ Chapter {chapter}: Generated {chapter_count} MCQs")
                    print(f"📊 Running total: {total_generated} MCQs")

                    # Save individual chapter
                    mcq_data = {
                        'subject': subject,
                        'chapter': chapter,
                        'total_mcqs': chapter_count,
                        'mcqs': chapter_mcqs
                    }
                    self.save_mcqs(mcq_data, output_dir)

                    # Check if we've reached the target
                    if total_generated >= self.target_mcqs_per_subject:
                        print(f"🎉 TARGET REACHED: {total_generated} MCQs!")
                        break

                    # Save combined results every 3 chapters
                    if processed_chapters % 3 == 0:
                        self.save_combined_mcqs(all_mcqs, subject, output_dir)
                        print(f"💾 Saved combined results: {total_generated} MCQs so far")

                else:
                    print(f"❌ Chapter {chapter}: No MCQs generated")

            except Exception as e:
                print(f"❌ Chapter {chapter}: Error - {e}")
                continue

        # Final combined save
        self.save_combined_mcqs(all_mcqs, subject, output_dir)

        print(f"\\n🏁 SUBJECT GENERATION COMPLETE: {subject.upper()}")
        print(f"📊 Final Results:")
        print(f"• Chapters processed: {processed_chapters}/{len(chapters)}")
        print(f"• Total MCQs generated: {total_generated}")
        print(f"• Target achieved: {'✅ YES' if total_generated >= self.target_mcqs_per_subject else '❌ NO'}")
        print(f"• Average per chapter: {total_generated / max(1, processed_chapters):.1f}")
        print(f"• Combined file: {output_dir}/{subject}_chapters/{subject}_all_mcqs.json")

        return all_mcqs

    def generate_chapter_batches(self, pdf_path: str, subject: str, chapter: str):
        """Generate multiple batches of MCQs for a single chapter"""
        print(f"🔄 Generating batches for {chapter}...")

        # Upload PDF once for this chapter
        try:
            sample_file = genai.upload_file(pdf_path)
            while sample_file.state.name == "PROCESSING":
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)

            if sample_file.state.name != "ACTIVE":
                print(f"❌ PDF processing failed: {sample_file.state.name}")
                return []
        except Exception as e:
            print(f"❌ PDF upload failed: {e}")
            return []

        chapter_mcqs = []
        batch_num = 0

        try:
            while len(chapter_mcqs) < self.target_mcqs_per_chapter and batch_num < self.max_requests_per_chapter:
                batch_num += 1
                remaining_needed = self.target_mcqs_per_chapter - len(chapter_mcqs)
                request_size = min(self.max_single_request, remaining_needed)

                print(f"🎯 Batch {batch_num}: Requesting {request_size} MCQs (Chapter total: {len(chapter_mcqs)})")

                try:
                    # Create model and generate
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    if batch_num == 1:
                        prompt = self.create_mcq_prompt(subject, chapter)
                    else:
                        prompt = self.create_additional_mcq_prompt(subject, chapter, request_size, len(chapter_mcqs))

                    response = model.generate_content([sample_file, prompt])

                    if response and response.text:
                        batch_mcqs = self.parse_response(response.text, subject, chapter)
                        chapter_mcqs.extend(batch_mcqs)
                        print(f"✅ Batch {batch_num}: Got {len(batch_mcqs)} MCQs")

                        # Success - add delay before next batch
                        if batch_num < self.max_requests_per_chapter:
                            print(f"⏳ Waiting {self.api_delay} seconds...")
                            time.sleep(self.api_delay)
                    else:
                        print(f"❌ Batch {batch_num}: No response")
                        break

                except Exception as e:
                    print(f"❌ Batch {batch_num}: Error - {e}")
                    # Try with different API key
                    try:
                        self.rotate_api_key()
                        print("🔄 Rotated to different API key")
                        time.sleep(self.api_delay)
                    except:
                        break

        finally:
            # Clean up
            try:
                sample_file.delete()
                print("🧹 Cleaned up PDF file")
            except:
                pass

        print(f"🏁 Chapter {chapter} complete: {len(chapter_mcqs)} MCQs in {batch_num} batches")
        return chapter_mcqs

    def generate_subject_boost(self, subject: str, pdf_dir: str, output_dir: str, needed_count: int):
        """Generate additional MCQs to boost a subject to target count"""
        print(f"🔄 Boosting {subject} with {needed_count} additional MCQs...")

        if not os.path.exists(pdf_dir):
            print(f"❌ PDF directory not found: {pdf_dir}")
            return []

        # Get available chapters
        chapters = []
        for file in os.listdir(pdf_dir):
            if file.endswith('.pdf'):
                chapter_name = file.replace('.pdf', '')
                chapters.append(chapter_name)

        print(f"📚 Available chapters: {len(chapters)}")

        boost_mcqs = []
        chapters_processed = 0

        for chapter in chapters:
            if len(boost_mcqs) >= needed_count:
                break

            pdf_path = os.path.join(pdf_dir, f"{chapter}.pdf")
            if not os.path.exists(pdf_path):
                continue

            chapters_processed += 1
            remaining_needed = needed_count - len(boost_mcqs)

            print(f"📖 Processing {chapter} (need {remaining_needed} more)...")

            try:
                chapter_mcqs = self.generate_chapter_batches(pdf_path, subject, chapter)

                if chapter_mcqs:
                    # Only take what we need
                    needed_from_chapter = min(len(chapter_mcqs), remaining_needed)
                    boost_mcqs.extend(chapter_mcqs[:needed_from_chapter])

                    print(f"✅ Got {needed_from_chapter} MCQs from {chapter}")

                    # Save chapter results
                    mcq_data = {
                        'subject': subject,
                        'chapter': chapter,
                        'total_mcqs': len(chapter_mcqs),
                        'mcqs': chapter_mcqs
                    }
                    self.save_mcqs(mcq_data, output_dir)

                if len(boost_mcqs) >= needed_count:
                    break

            except Exception as e:
                print(f"❌ Error processing {chapter}: {e}")
                continue

        print(f"🏁 Boost complete: {len(boost_mcqs)} MCQs generated from {chapters_processed} chapters")
        return boost_mcqs

    def show_final_inventory(self, output_dir: str):
        """Show final inventory of all MCQs"""
        print("\\n📊 FINAL MCQ INVENTORY:")
        print("=" * 50)

        subjects = {}
        total_mcqs = 0

        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('_mcqs.json'):
                    subject = os.path.basename(root)
                    filepath = os.path.join(root, file)

                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            count = len(data) if isinstance(data, list) else 0
                            subjects[subject] = subjects.get(subject, 0) + count
                            total_mcqs += count
                    except:
                        continue

        for subject, count in sorted(subjects.items()):
            target = 500
            status = "✅ ACHIEVED" if count >= target else f"❌ NEED {target - count} MORE"
            print(f"• {subject}: {count} MCQs ({status})")

        print(f"\\n🏆 GRAND TOTAL: {total_mcqs} MCQs across {len(subjects)} subjects")
        overall_target = len(subjects) * 500
        if total_mcqs >= overall_target:
            print("🎉 MISSION ACCOMPLISHED: All targets achieved! 🚀")
        else:
            deficit = overall_target - total_mcqs
            print(f"📈 {deficit} MCQs still needed to reach all targets")

    def save_combined_mcqs(self, all_mcqs: List[Dict[str, Any]], subject: str, output_dir: str):
        """Save combined MCQs from multiple chapters"""
        if not all_mcqs:
            return

        subject_dir = os.path.join(output_dir, f"{subject}_chapters")
        os.makedirs(subject_dir, exist_ok=True)

        combined_data = {
            'subject': subject,
            'total_mcqs': len(all_mcqs),
            'chapters_included': len(set(mcq.get('source', '').replace('.pdf', '') for mcq in all_mcqs)),
            'mcqs': all_mcqs
        }

        filepath = os.path.join(subject_dir, f"{subject}_all_mcqs.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Combined MCQs saved: {filepath}")


def main():
    print("🚀 Simple MCQ Generator")
    print("=" * 40)

    generator = SimpleMCQGenerator()

    if not generator.api_keys:
        print("❌ No API keys found. Please check /home/yaseen/apikeys")
        return

    # Direct MCQ generation approach
    print("🎯 DIRECT MCQ GENERATION")
    print("📚 Subject: Chemistry XI")
    print("🎯 Target: Generate 50 MCQs from Chapter 1")
    print("=" * 50)

    subject = 'chemistry'
    pdf_path = '/home/yaseen/books/chemistry_chapters/ch1.pdf'
    output_dir = '/home/yaseen/ourbooks/mcq_output'

    if os.path.exists(pdf_path):
        print("✅ PDF found, starting generation...")

        try:
            mcq_data = generator.generate_mcqs_for_chapter(pdf_path, subject, 'ch1_direct')
            if mcq_data and mcq_data.get('mcqs'):
                count = len(mcq_data['mcqs'])
                print(f"✅ Generated {count} MCQs")

                # Save results
                generator.save_mcqs(mcq_data, output_dir)
                print("💾 Saved to chemistry_chapters/ch1_direct_mcqs.json")

                # Show sample
                if mcq_data['mcqs']:
                    sample = mcq_data['mcqs'][0]
                    print(f"\\n📝 Sample MCQ:")
                    print(f"Question: {sample['question']}")
                    print(f"Answer: {sample['correct_answer']}")
            else:
                print("❌ No MCQs generated")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ PDF not found: {pdf_path}")

    # Configuration for subject generation
    subjects_config = [
        {
            'name': 'chemistry',
            'pdf_dir': '/home/yaseen/books/chemistry_chapters',
            'grade': 'XI'
        },
        {
            'name': 'physics',
            'pdf_dir': '/home/yaseen/books/physics_chapters',
            'grade': 'XI'
        },
        {
            'name': 'biology',
            'pdf_dir': '/home/yaseen/books/biology_chapters',
            'grade': 'XI'
        },
        {
            'name': 'mathematics',
            'pdf_dir': '/home/yaseen/books/math_chapters',
            'grade': 'XI'
        },
        {
            'name': 'chemistry',
            'pdf_dir': '/home/yaseen/books/chemistryXII_chapters',
            'grade': 'XII'
        },
        {
            'name': 'physics',
            'pdf_dir': '/home/yaseen/books/physicsXII_chapters',
            'grade': 'XII'
        },
        {
            'name': 'biology',
            'pdf_dir': '/home/yaseen/books/biologyXII_chapters',
            'grade': 'XII'
        },
        {
            'name': 'mathematics',
            'pdf_dir': '/home/yaseen/books/mathsXII_chapters',
            'grade': 'XII'
        }
    ]

    output_dir = '/home/yaseen/ourbooks/mcq_output'

    print(f"🎯 Target: {generator.target_mcqs_per_subject} MCQs per subject")
    print(f"📁 Output Directory: {output_dir}")
    print("=" * 50)

    for config in subjects_config:
        subject = config['name']
        pdf_dir = config['pdf_dir']
        grade = config['grade']
        subject_full = f"{subject} {grade}"

        print(f"\n🚀 STARTING: {subject_full.upper()}")
        print("-" * 40)

        try:
            # Generate MCQs for this subject
            mcqs = generator.generate_subject_mcqs(subject, pdf_dir, output_dir)

            if mcqs:
                count = len(mcqs)
                print(f"✅ {subject_full}: Generated {count} MCQs")
            else:
                print(f"❌ {subject_full}: No MCQs generated")

        except Exception as e:
            print(f"❌ {subject_full}: Error - {e}")
            import traceback
            traceback.print_exc()
            continue

    # Show final inventory
    print("\n" + "=" * 60)
    generator.show_final_inventory(output_dir)
    print("\n🏁 All subjects processing complete!")


if __name__ == "__main__":
    main()