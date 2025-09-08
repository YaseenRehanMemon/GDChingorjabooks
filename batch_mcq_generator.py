#!/usr/bin/env python3

import os
import json
import time
import requests
import concurrent.futures
from pathlib import Path
import threading
from datetime import datetime

class BatchMCQGenerator:
    def __init__(self):
        # Your API keys from config.js
        self.api_keys = [
            "AIzaSyATMv5Hjln4OYk_4-rQk1jHuXtuO0y1J8c",
            "AIzaSyC12_noKxy5jJJfGoLUWpAiWPXHnBxD1-Q", 
            "AIzaSyD19bjFIt1fNXI0RQy-3BHtZasX-rdZDqo",
            "AIzaSyBaJWfsgTaXwkNy711OXHIcBNe8dV7fF_8",
            "AIzaSyCJAus6nrOanNRhWu0rkJJ6Z4CecouJE1E",
            "AIzaSyC12_noKxy5jJJfGoLUWpAiWPXHnBxD1-Q",
            "AIzaSyD19bjFIt1fNXI0RQy-3BHtZasX-rdZDqo",
            "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw",
        ]
        
        # Add 3 more API keys if you have them
        # self.api_keys.extend(["key6", "key7", "key8"])
        
        self.current_key_index = 0
        self.key_lock = threading.Lock()
        
        # Subject mapping to API keys
        self.subject_key_mapping = {
            'chemistry_chapters': 0,
            'chemistryXII_chapters': 1,
            'physics_chapters': 2,
            'physicsXII_chapters': 3,
            'math_chapters': 4,
            'mathsXII_chapters': 5,
            'biology_chapters': 0,  # Reuse key 0
            'biologyXII_chapters': 1  # Reuse key 1
        }
        
        # Files larger than 20MB (manual processing)
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
        
        # Load the prompt
        self.prompt = self.load_prompt()
        
    def load_prompt(self):
        """Load the MCQ extraction prompt"""
        try:
            with open('gemini_mcq_extraction_prompt.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print("❌ Prompt file not found! Please make sure 'gemini_mcq_extraction_prompt.txt' exists.")
            return None
    
    def get_next_api_key(self, subject):
        """Get API key for specific subject"""
        with self.key_lock:
            key_index = self.subject_key_mapping.get(subject, 0)
            return self.api_keys[key_index]
    
    def upload_pdf_to_gemini(self, pdf_path, api_key):
        """Upload PDF file to Gemini and get content"""
        try:
            # For now, we'll read the PDF content as text
            # In a real implementation, you'd use Gemini's file upload API
            print(f"📄 Processing: {pdf_path}")
            
            # This is a placeholder - you'll need to implement actual PDF upload
            # For now, we'll simulate the process
            return f"PDF content from {pdf_path}"
            
        except Exception as e:
            print(f"❌ Error uploading PDF {pdf_path}: {e}")
            return None
    
    def generate_mcqs_for_pdf(self, pdf_path, subject, chapter_name, api_key):
        """Generate MCQs for a single PDF"""
        try:
            print(f"🔄 Generating MCQs for: {pdf_path}")
            
            # Upload PDF content
            pdf_content = self.upload_pdf_to_gemini(pdf_path, api_key)
            if not pdf_content:
                return None
            
            # Create the full prompt with PDF content
            full_prompt = self.prompt.replace("[Insert chapter PDF content here]", pdf_content)
            
            # API request
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
            
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
            
            response = requests.post(api_url, json=payload, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                mcq_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                if mcq_text:
                    # Parse JSON from response
                    try:
                        mcqs = json.loads(mcq_text)
                        print(f"✅ Generated {len(mcqs)} MCQs for {chapter_name}")
                        return mcqs
                    except json.JSONDecodeError:
                        print(f"❌ Invalid JSON response for {chapter_name}")
                        return None
                else:
                    print(f"❌ Empty response for {chapter_name}")
                    return None
            else:
                print(f"❌ API error for {chapter_name}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating MCQs for {chapter_name}: {e}")
            return None
    
    def save_mcqs_to_file(self, mcqs, subject, chapter_name):
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
            
            print(f"💾 Saved MCQs to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving MCQs for {chapter_name}: {e}")
            return None
    
    def process_subject_directory(self, subject_dir):
        """Process all PDFs in a subject directory"""
        subject = os.path.basename(subject_dir)
        api_key = self.get_next_api_key(subject)
        
        print(f"\n📚 Processing {subject} with API key ending in: ...{api_key[-4:]}")
        
        if not os.path.exists(subject_dir):
            print(f"❌ Directory not found: {subject_dir}")
            return
        
        # Get all PDF files
        pdf_files = [f for f in os.listdir(subject_dir) if f.endswith('.pdf')]
        
        # Filter out large files (manual processing)
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
            mcqs = self.generate_mcqs_for_pdf(pdf_path, subject, pdf_file, api_key)
            
            if mcqs:
                # Save to file
                self.save_mcqs_to_file(mcqs, subject, pdf_file)
            
            # Add delay to avoid rate limiting
            time.sleep(2)
    
    def process_all_subjects(self, books_directory):
        """Process all subjects in parallel"""
        print("🚀 Starting Batch MCQ Generation")
        print("=" * 50)
        
        # Get all subject directories
        subject_dirs = []
        for item in os.listdir(books_directory):
            item_path = os.path.join(books_directory, item)
            if os.path.isdir(item_path) and item.endswith('_chapters'):
                subject_dirs.append(item_path)
        
        if not subject_dirs:
            print("❌ No subject directories found!")
            return
        
        print(f"📚 Found {len(subject_dirs)} subject directories")
        
        # Process subjects in parallel (limited by number of API keys)
        max_workers = min(len(self.api_keys), len(subject_dirs))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for subject_dir in subject_dirs:
                future = executor.submit(self.process_subject_directory, subject_dir)
                futures.append(future)
            
            # Wait for all to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Error processing subject: {e}")
        
        print("\n🎉 Batch processing completed!")
        self.print_summary()
    
    def print_summary(self):
        """Print processing summary"""
        print("\n📊 Processing Summary:")
        print("=" * 30)
        
        output_dir = "mcq_output"
        if os.path.exists(output_dir):
            total_files = 0
            for subject in os.listdir(output_dir):
                subject_path = os.path.join(output_dir, subject)
                if os.path.isdir(subject_path):
                    files = len([f for f in os.listdir(subject_path) if f.endswith('.json')])
                    total_files += files
                    print(f"  {subject}: {files} MCQ files")
            
            print(f"\nTotal MCQ files created: {total_files}")
        else:
            print("No output directory found")

def main():
    # Change this to your books directory path
    books_directory = "/home/yaseen/books"
    
    if not os.path.exists(books_directory):
        print(f"❌ Books directory not found: {books_directory}")
        print("Please update the path in the script")
        return
    
    # Create MCQ generator
    generator = BatchMCQGenerator()
    
    if not generator.prompt:
        return
    
    # Start processing
    generator.process_all_subjects(books_directory)

if __name__ == "__main__":
    main()