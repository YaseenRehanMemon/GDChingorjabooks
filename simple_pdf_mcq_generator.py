#!/usr/bin/env python3

import os
import json
import time
import requests
import concurrent.futures
import threading
from pathlib import Path

class SimplePDFMCQGenerator:
    def __init__(self):
        # Working API keys only
        self.api_keys = [
            "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw",  # Key 1 - Working
            "AIzaSyD19bjFIt1fNXI0RQy-3BHtZasX-rdZDqo",  # Key 3 - Working
            "AIzaSyBaJWfsgTaXwkNy711OXHIcBNe8dV7fF_8",  # Key 4 - Working
            "AIzaSyCJAus6nrOanNRhWu0rkJJ6Z4CecouJE1E"   # Key 5 - Working
        ]
        
        self.current_key_index = 0
        self.key_lock = threading.Lock()
        
        # Subject to API key mapping (using only working keys)
        self.subject_keys = {
            'chemistry_chapters': 0,      # Key 1 (...osTw)
            'chemistryXII_chapters': 1,   # Key 3 (...ZDqo)
            'physics_chapters': 2,        # Key 4 (...fF_8)
            'physicsXII_chapters': 3,     # Key 5 (...JE1E)
            'math_chapters': 0,           # Reuse Key 1
            'mathsXII_chapters': 1,       # Reuse Key 3
            'biology_chapters': 2,        # Reuse Key 4
            'biologyXII_chapters': 3      # Reuse Key 5
        }
        
        # Large files to skip
        self.large_files = {
            'chemistry_chapters': ['ch2.pdf', 'ch3.pdf', 'ch4.pdf', 'ch7.pdf'],
            'mathsXII_chapters': ['ch2_Functions_and_Limits.pdf', 'ch3_Differentiation.pdf', 
                               'ch7_Plane_Analytic_Geometry:_Straight_Line.pdf', 
                               'ch9_Parabola,_Ellipse_and_Hyperbola.pdf'],
            'physicsXII_chapters': ['ch27_Nuclear_Physics.pdf'],
            'chemistryXII_chapters': ['ch1_CHEMISTRY_OF_REPRESENTATIVE_ELEMENTS.pdf',
                                    'ch2_CHEMISTRY_OF_OUTER_TRANSITION_(d_–_BLOCK)_ELEMENTS.pdf',
                                    'ch3_ORGANIC_COMPOUNDS.pdf', 'ch4_NOMENCLATURE_OF_ORGANIC_COMPOUNDS.pdf',
                                    'ch5_HYDROCARBONS.pdf', 'ch6_ALKYL,_HALIDES_AND_AMINES.pdf',
                                    'ch7_ALCOHOLS,_PHENOLS_AND_ETHERS.pdf',
                                    'ch8_CARBONYL_COMPOUNDS_I:_ALDEHYDES_AND_KEYTONES.pdf',
                                    'ch10_BIOCHEMISTRY.pdf', 'ch11_INDUSTRIAL_CHEMISTRY.pdf',
                                    'ch12_ENVIRONMENTAL_CHEMISTRY.pdf'],
            'math_chapters': ['ch2.pdf', 'ch3.pdf', 'ch4.pdf', 'ch6.pdf', 'ch8.pdf', 'ch12.pdf']
        }
        
        # Load prompt
        self.prompt = self.load_prompt()
    
    def load_prompt(self):
        """Load the MCQ extraction prompt"""
        try:
            with open('gemini_mcq_extraction_prompt.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print("❌ Prompt file not found!")
            return None
    
    def get_api_key(self, subject):
        """Get API key for subject"""
        key_index = self.subject_keys.get(subject, 0)
        return self.api_keys[key_index]
    
    def fix_json_issues(self, json_text):
        """Fix common JSON issues"""
        import re
        
        # Fix invalid escape sequences
        json_text = re.sub(r'\\(?!["\\/bfnrt])', r'\\\\', json_text)
        
        # Fix unterminated strings by finding the last complete object
        if json_text.count('{') > json_text.count('}'):
            # Find the last complete object
            brace_count = 0
            last_complete_pos = 0
            for i, char in enumerate(json_text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_complete_pos = i + 1
            
            if last_complete_pos > 0:
                json_text = json_text[:last_complete_pos]
                # If it's not a complete array, try to close it
                if not json_text.strip().endswith(']'):
                    json_text = json_text.rstrip(',') + ']'
        
        return json_text
    
    def read_pdf_as_text(self, pdf_path):
        """Read PDF content as text (simplified version)"""
        try:
            # For now, return a placeholder
            # You can use PyPDF2 or pdfplumber for actual PDF reading
            return f"PDF content from {os.path.basename(pdf_path)}"
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {e}")
            return None
    
    def generate_mcqs(self, pdf_path, subject, chapter_name, api_key):
        """Generate MCQs for a PDF"""
        try:
            print(f"🔄 Processing: {chapter_name}")
            
            # Read PDF content
            pdf_content = self.read_pdf_as_text(pdf_path)
            if not pdf_content:
                return None
            
            # Create full prompt
            full_prompt = self.prompt.replace("[Insert chapter PDF content here]", pdf_content)
            
            # API request - Using Gemini 2.5 Flash for better performance
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 8192,
                }
            }
            
            print(f"📡 Sending request to API...")
            
            # Retry logic for 503 errors
            max_retries = 3
            for attempt in range(max_retries):
                response = requests.post(api_url, json=payload, timeout=300)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 503 and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 30  # 30, 60, 90 seconds
                    print(f"⚠️ Model overloaded (503), waiting {wait_time}s before retry {attempt + 2}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                else:
                    break
            
            if response.status_code == 200:
                result = response.json()
                mcq_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                if mcq_text:
                    try:
                        # Remove markdown formatting if present
                        if mcq_text.startswith('```json'):
                            mcq_text = mcq_text.replace('```json', '').replace('```', '').strip()
                        elif mcq_text.startswith('```'):
                            mcq_text = mcq_text.replace('```', '').strip()
                        
                        # Fix common JSON issues
                        mcq_text = self.fix_json_issues(mcq_text)
                        
                        mcqs = json.loads(mcq_text)
                        print(f"✅ Generated {len(mcqs)} MCQs for {chapter_name}")
                        return mcqs
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON decode error for {chapter_name}: {e}")
                        print(f"Raw response: {mcq_text[:200]}...")
                        # Save raw response for debugging
                        with open(f"debug_{chapter_name}.txt", 'w') as f:
                            f.write(mcq_text)
                        return None
                else:
                    print(f"❌ Empty response for {chapter_name}")
                    print("This might be due to rate limiting or content filtering")
                    return None
            else:
                print(f"❌ API error for {chapter_name}: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating MCQs for {chapter_name}: {e}")
            return None
    
    def save_mcqs(self, mcqs, subject, chapter_name):
        """Save MCQs to JSON file"""
        try:
            # Create output directory
            output_dir = f"mcq_output/{subject}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            filename = f"{chapter_name.replace('.pdf', '')}_mcqs.json"
            filepath = os.path.join(output_dir, filename)
            
            # Save MCQs
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mcqs, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving MCQs for {chapter_name}: {e}")
            return None
    
    def process_subject(self, subject_dir):
        """Process all PDFs in a subject directory"""
        subject = os.path.basename(subject_dir)
        api_key = self.get_api_key(subject)
        
        print(f"\n📚 Processing {subject}")
        print(f"🔑 Using API key: ...{api_key[-4:]}")
        
        if not os.path.exists(subject_dir):
            print(f"❌ Directory not found: {subject_dir}")
            return
        
        # Get PDF files
        pdf_files = [f for f in os.listdir(subject_dir) if f.endswith('.pdf')]
        
        # Filter out large files
        large_files = self.large_files.get(subject, [])
        pdf_files = [f for f in pdf_files if f not in large_files]
        
        if not pdf_files:
            print(f"⚠️ No PDFs to process in {subject}")
            return
        
        print(f"📄 Found {len(pdf_files)} PDFs to process")
        
        # Process each PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(subject_dir, pdf_file)
            
            # Generate MCQs
            mcqs = self.generate_mcqs(pdf_path, subject, pdf_file, api_key)
            
            if mcqs:
                # Save to file
                self.save_mcqs(mcqs, subject, pdf_file)
            
            # Add longer delay to avoid 503 errors
            time.sleep(10)
    
    def run_batch_processing(self, books_directory):
        """Run batch processing for all subjects"""
        print("🚀 Starting Batch MCQ Generation")
        print("=" * 50)
        
        # Get subject directories
        subject_dirs = []
        for item in os.listdir(books_directory):
            item_path = os.path.join(books_directory, item)
            if os.path.isdir(item_path) and item.endswith('_chapters'):
                subject_dirs.append(item_path)
        
        if not subject_dirs:
            print("❌ No subject directories found!")
            return
        
        print(f"📚 Found {len(subject_dirs)} subject directories")
        
        # Process subjects in parallel (limit to 2 to avoid overwhelming API)
        max_workers = min(2, len(subject_dirs))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for subject_dir in subject_dirs:
                future = executor.submit(self.process_subject, subject_dir)
                futures.append(future)
            
            # Wait for completion
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        print("\n🎉 Batch processing completed!")
        self.print_summary()
    
    def print_summary(self):
        """Print processing summary"""
        print("\n📊 Summary:")
        print("=" * 20)
        
        output_dir = "mcq_output"
        if os.path.exists(output_dir):
            total_files = 0
            for subject in os.listdir(output_dir):
                subject_path = os.path.join(output_dir, subject)
                if os.path.isdir(subject_path):
                    files = len([f for f in os.listdir(subject_path) if f.endswith('.json')])
                    total_files += files
                    print(f"  {subject}: {files} files")
            
            print(f"\nTotal MCQ files: {total_files}")
        else:
            print("No output found")

def main():
    # Update this path
    books_directory = "/home/yaseen/books"
    
    if not os.path.exists(books_directory):
        print(f"❌ Directory not found: {books_directory}")
        return
    
    # Create generator
    generator = SimplePDFMCQGenerator()
    
    if not generator.prompt:
        return
    
    # Start processing
    generator.run_batch_processing(books_directory)

if __name__ == "__main__":
    main()