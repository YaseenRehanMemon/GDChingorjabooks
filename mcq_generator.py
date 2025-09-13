#!/usr/bin/env python3
"""
MCQ Generator using Gemini 2.5 Flash API
Generates comprehensive MCQs from PDF textbooks with explanations
Handles 20MB PDF limit and uses multiple API keys for load balancing
"""

import os
import json
import time
import random
import asyncio
from pathlib import Path
from typing import List, Dict, Any
try:
    import google.generativeai as genai
    from google.generativeai.types import RequestOptions
except ImportError:
    print("❌ google-generativeai not installed. Run: pip install google-generativeai")
    exit(1)

try:
    import fitz  # PyMuPDF for PDF compression
except ImportError:
    print("❌ PyMuPDF not installed. Run: pip install PyMuPDF")
    exit(1)

from concurrent.futures import ThreadPoolExecutor, as_completed


class MCQGenerator:
    def __init__(self, api_keys_file: str = "/home/yaseen/apikeys"):
        self.api_keys = self.load_api_keys(api_keys_file)
        self.current_key_index = 0
        self.setup_gemini()

        # MCQ Generation Configuration
        self.target_mcqs_per_chapter = 100
        self.max_pdf_size_mb = 19  # Leave 1MB buffer
        self.max_retries = 3
        self.rate_limit_delay = 2  # seconds between requests

    def load_api_keys(self, filepath: str) -> List[str]:
        """Load API keys from file"""
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract API keys (lines that start with AIzaSy)
        keys = [line.strip() for line in content.split('\n')
                if line.strip().startswith('AIzaSy')]

        print(f"Loaded {len(keys)} API keys")
        return keys

    def setup_gemini(self):
        """Setup Gemini with current API key"""
        if not self.api_keys:
            raise ValueError("No API keys found")

        current_key = self.api_keys[self.current_key_index]
        genai.configure(api_key=current_key)

        # Use the correct model initialization
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Set generation config separately if needed
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

    def rotate_api_key(self):
        """Rotate to next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.setup_gemini()
        print(f"Switched to API key {self.current_key_index + 1}")

    def compress_pdf(self, pdf_path: str, max_size_mb: int = 19) -> str:
        """Compress PDF if it's over the size limit"""
        file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)

        if file_size_mb <= max_size_mb:
            return pdf_path

        print(f"PDF {pdf_path} is {file_size_mb:.1f}MB, compressing...")

        # Open PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        compressed_path = pdf_path.replace('.pdf', '_compressed.pdf')

        # Compress by reducing image quality and removing unnecessary elements
        for page in doc:
            for img in page.get_images(full=True):
                xref = img[0]
                # Reduce image quality
                doc._deleteObject(xref)

        # Save with compression
        doc.save(
            compressed_path,
            garbage=4,  # Remove unused objects
            deflate=True,  # Compress streams
            clean=True,  # Clean content streams
        )
        doc.close()

        new_size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
        print(f"Compressed to {new_size_mb:.1f}MB")

        if new_size_mb > max_size_mb:
            print(f"Still too large after compression. Splitting PDF...")
            return self.split_pdf(compressed_path, max_size_mb)

        return compressed_path

    def split_pdf(self, pdf_path: str, max_size_mb: int) -> str:
        """Split PDF into smaller chunks if still too large"""
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Calculate pages per chunk
        file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        pages_per_chunk = int((max_size_mb / file_size_mb) * total_pages)

        if pages_per_chunk < 1:
            pages_per_chunk = 1

        # Create first chunk
        chunk_doc = fitz.open()
        for i in range(min(pages_per_chunk, total_pages)):
            chunk_doc.insert_pdf(doc, from_page=i, to_page=i)

        chunk_path = pdf_path.replace('.pdf', '_chunk1.pdf')
        chunk_doc.save(chunk_path)
        chunk_doc.close()

        print(f"Split PDF into chunks. Using first chunk: {chunk_path}")
        doc.close()

        return chunk_path

    def generate_mcqs_for_chapter(self, pdf_path: str, subject: str, chapter: str) -> Dict[str, Any]:
        """Generate MCQs for a specific chapter"""

        # Compress/split PDF if needed
        processed_pdf = self.compress_pdf(pdf_path)

        # Upload PDF to Gemini
        sample_file = genai.upload_file(processed_pdf)
        print(f"Uploaded PDF: {processed_pdf}")

        # Wait for processing
        while sample_file.state.name == "PROCESSING":
            time.sleep(2)
            sample_file = genai.get_file(sample_file.name)

        if sample_file.state.name != "ACTIVE":
            raise ValueError(f"File processing failed: {sample_file.state.name}")

        # Generate MCQs
        prompt = self.create_mcq_prompt(subject, chapter)

        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(
                    [sample_file, prompt],
                    request_options=RequestOptions(timeout=300)
                )

                if response.text:
                    mcqs_data = self.parse_mcq_response(response.text, subject, chapter)
                    sample_file.delete()  # Clean up
                    return mcqs_data

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    self.rotate_api_key()
                    time.sleep(self.rate_limit_delay)
                else:
                    raise e

        sample_file.delete()  # Clean up on failure
        raise ValueError("Failed to generate MCQs after all retries")

    def create_mcq_prompt(self, subject: str, chapter: str) -> str:
        """Create detailed prompt for MCQ generation"""
        return f"""You are an expert educator specializing in Pakistani Intermediate ({subject}) curriculum.
Analyze the provided PDF chapter content and generate comprehensive MCQs.

**Requirements:**
- Generate EXACTLY {self.target_mcqs_per_chapter} MCQs
- Cover ALL topics and subtopics from the chapter
- Include variety: factual, conceptual, application, and analytical questions
- Use proper LaTeX formatting for mathematical expressions: $...$ for inline, $$...$$ for display
- Provide detailed explanations for each answer

**MCQ Format (JSON Array):**
[
  {{
    "id": "{subject.lower()}_xi_{chapter}_mcq_001",
    "question": "Question text with $LaTeX$ formulas if needed",
    "question_type": "multiple_choice",
    "options": {{
      "A": "Option A text $with LaTeX$",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation with $LaTeX$ formulas and reasoning",
    "difficulty": "easy|medium|hard|expert",
    "topic": "main_topic_name",
    "subtopic": "specific_subtopic",
    "tags": ["tag1", "tag2", "tag3"],
    "learning_objective": "What student should learn from this question",
    "created_date": "2024-09-11",
    "source": "{chapter}.pdf",
    "ai_generated": true,
    "reviewed": false,
    "quality_score": 0.95
  }}
]

**Guidelines:**
- Questions should test understanding, not just memorization
- Include diagrams descriptions if present in PDF
- Cover numerical problems with step-by-step solutions
- Ensure explanations are comprehensive but concise
- Use proper scientific terminology
- Balance difficulty levels (30% easy, 40% medium, 20% hard, 10% expert)

Generate the MCQs now:"""

    def parse_mcq_response(self, response_text: str, subject: str, chapter: str) -> Dict[str, Any]:
        """Parse and validate the MCQ response from Gemini"""
        try:
            # Extract JSON from response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array found in response")

            json_content = response_text[json_start:json_end]
            mcqs = json.loads(json_content)

            # Validate and enhance MCQs
            validated_mcqs = []
            for i, mcq in enumerate(mcqs):
                # Ensure required fields
                mcq['id'] = f"{subject.lower()}_xi_{chapter}_mcq_{str(i+1).zfill(3)}"
                mcq['created_date'] = "2024-09-11"
                mcq['source'] = f"{chapter}.pdf"
                mcq['ai_generated'] = True
                mcq['reviewed'] = False

                # Ensure quality_score
                if 'quality_score' not in mcq:
                    mcq['quality_score'] = 0.9

                validated_mcqs.append(mcq)

            return {
                'subject': subject,
                'chapter': chapter,
                'total_mcqs': len(validated_mcqs),
                'mcqs': validated_mcqs
            }

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response content: {response_text[:500]}...")
            raise ValueError("Failed to parse MCQ response as JSON")

    def save_mcqs(self, mcq_data: Dict[str, Any], output_dir: str):
        """Save MCQs to JSON file"""
        os.makedirs(output_dir, exist_ok=True)

        subject = mcq_data['subject'].lower()
        chapter = mcq_data['chapter']

        # Create subject directory if needed
        subject_dir = os.path.join(output_dir, f"{subject}_chapters")
        os.makedirs(subject_dir, exist_ok=True)

        filename = f"{chapter}_mcqs.json"
        filepath = os.path.join(subject_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mcq_data['mcqs'], f, indent=2, ensure_ascii=False)

        print(f"Saved {mcq_data['total_mcqs']} MCQs to {filepath}")

    def process_all_chapters(self, books_dir: str, output_dir: str):
        """Process all chapters from all subjects"""
        subjects = {
            'chemistry': 'chemistry_chapters',
            'physics': 'physics_chapters',
            'biology': 'biology_chapters',
            'mathematics': 'math_chapters',
            'chemistry-xii': 'chemistryXII_chapters',
            'physics-xii': 'physicsXII_chapters',
            'biology-xii': 'biologyXII_chapters',
            'mathematics-xii': 'mathsXII_chapters'
        }

        for subject, chapter_dir in subjects.items():
            chapter_path = os.path.join(books_dir, chapter_dir)

            if not os.path.exists(chapter_path):
                print(f"Chapter directory not found: {chapter_path}")
                continue

            print(f"\nProcessing {subject} chapters...")

            # Get all PDF files in chapter directory
            pdf_files = [f for f in os.listdir(chapter_path) if f.endswith('.pdf')]
            pdf_files.sort()  # Sort for consistent processing

            for pdf_file in pdf_files:
                chapter_name = pdf_file.replace('.pdf', '')
                pdf_path = os.path.join(chapter_path, pdf_file)

                print(f"\nGenerating MCQs for {subject} - {chapter_name}")

                try:
                    mcq_data = self.generate_mcqs_for_chapter(pdf_path, subject, chapter_name)
                    self.save_mcqs(mcq_data, output_dir)

                    # Rate limiting and API key rotation
                    time.sleep(self.rate_limit_delay)
                    if random.random() < 0.3:  # 30% chance to rotate key
                        self.rotate_api_key()

                except Exception as e:
                    print(f"Failed to process {chapter_name}: {e}")
                    continue

    async def process_chapter_async(self, pdf_path: str, subject: str, chapter: str, output_dir: str):
        """Async version for better performance"""
        try:
            mcq_data = await asyncio.get_event_loop().run_in_executor(
                None, self.generate_mcqs_for_chapter, pdf_path, subject, chapter
            )
            self.save_mcqs(mcq_data, output_dir)
            return f"✓ {subject} - {chapter}: {mcq_data['total_mcqs']} MCQs"
        except Exception as e:
            return f"✗ {subject} - {chapter}: {e}"


def main():
    # Configuration
    BOOKS_DIR = "/home/yaseen/books"
    OUTPUT_DIR = "/home/yaseen/ourbooks/mcq_output"

    # Initialize generator
    generator = MCQGenerator()

    print("🚀 Starting MCQ Generation Process")
    print(f"📚 Books Directory: {BOOKS_DIR}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print(f"🔑 API Keys Available: {len(generator.api_keys)}")
    print(f"🎯 Target MCQs per Chapter: {generator.target_mcqs_per_chapter}")
    print(f"📏 Max PDF Size: {generator.max_pdf_size_mb}MB")
    print("\n" + "="*50)

    # Process all chapters
    generator.process_all_chapters(BOOKS_DIR, OUTPUT_DIR)

    print("\n✅ MCQ Generation Complete!")
    print(f"📊 Check {OUTPUT_DIR} for generated MCQs")


if __name__ == "__main__":
    main()