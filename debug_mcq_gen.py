#!/usr/bin/env python3
import os
import json
import time
import google.generativeai as genai

class DebugMCQGenerator:
    def __init__(self):
        # Load API keys
        with open('/home/yaseen/apikeys', 'r') as f:
            content = f.read()
        self.api_keys = [line.strip() for line in content.split('\n') 
                        if line.strip().startswith('AIzaSy')]
        self.current_key_index = 1  # Use working key
        
        print(f"🔑 Loaded {len(self.api_keys)} API keys")
        
    def test_single_chapter_debug(self):
        """Debug version of single chapter test"""
        pdf_path = "/home/yaseen/books/chemistry_chapters/ch1.pdf"
        output_dir = "/home/yaseen/ourbooks/mcq_output"
        
        if not os.path.exists(pdf_path):
            print(f"❌ Test PDF not found: {pdf_path}")
            return
        
        print("🧪 Debug MCQ Generation Test")
        print(f"📄 PDF: {pdf_path}")
        print(f"📁 Output: {output_dir}")
        
        # Setup API
        genai.configure(api_key=self.api_keys[self.current_key_index])
        print(f"🔄 Using API key {self.current_key_index + 1}")
        
        try:
            # Upload PDF
            print("📤 Uploading PDF...")
            sample_file = genai.upload_file(pdf_path)
            
            # Wait for processing
            print("⏳ Processing PDF...")
            while sample_file.state.name == "PROCESSING":
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)
            
            if sample_file.state.name != "ACTIVE":
                print(f"❌ PDF processing failed: {sample_file.state.name}")
                return
            
            print("✅ PDF processed successfully")
            
            # Create model and generate
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = """You are an expert educator specializing in Pakistani Intermediate Chemistry curriculum.

Analyze the provided PDF chapter content and generate 5 comprehensive MCQs.

Requirements:
- Generate EXACTLY 5 MCQs
- Cover main topics from the chapter
- Mix of easy, medium, and hard difficulty
- Use LaTeX for math: $x^2$, $\\frac{a}{b}$, etc.
- Provide detailed explanations

Output Format (Valid JSON Array):
[
  {
    "question": "Question text with $LaTeX$ formulas",
    "options": {
      "A": "Option A",
      "B": "Option B", 
      "C": "Option C",
      "D": "Option D"
    },
    "correct_answer": "A",
    "explanation": "Detailed explanation",
    "difficulty": "easy",
    "topic": "main_topic",
    "subtopic": "specific_subtopic"
  }
]

Generate the MCQs now. Return ONLY the JSON array, no additional text."""
            
            print("🎯 Generating 5 MCQs...")
            response = model.generate_content([sample_file, prompt])
            
            # Clean up file
            sample_file.delete()
            
            if response and response.text:
                print("✅ Response received")
                print(f"📄 Response length: {len(response.text)} chars")
                
                # Debug: Save raw response
                with open('/home/yaseen/ourbooks/debug_response.txt', 'w') as f:
                    f.write(response.text)
                print("💾 Saved raw response to debug_response.txt")
                
                # Parse response
                mcqs = self.parse_response_debug(response.text)
                
                if mcqs:
                    print(f"✅ Successfully parsed {len(mcqs)} MCQs")
                    
                    # Save MCQs
                    os.makedirs(output_dir, exist_ok=True)
                    subject_dir = os.path.join(output_dir, "chemistry_chapters")
                    os.makedirs(subject_dir, exist_ok=True)
                    
                    with open(os.path.join(subject_dir, "ch1_debug_mcqs.json"), 'w', encoding='utf-8') as f:
                        json.dump(mcqs, f, indent=2, ensure_ascii=False)
                    
                    print("💾 Saved debug MCQs to ch1_debug_mcqs.json")
                    
                    # Show sample
                    if mcqs:
                        print(f"📝 Sample MCQ: {mcqs[0]['question'][:100]}...")
                else:
                    print("❌ Failed to parse MCQs")
            else:
                print("❌ No response from API")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def parse_response_debug(self, response_text):
        """Debug version of response parsing"""
        try:
            print("🔍 Parsing response...")
            
            # Clean the response text
            response_text = response_text.strip()
            print(f"📄 Raw response starts with: {response_text[:100]}...")
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
                print("🧹 Removed ```json prefix")
            if response_text.startswith('```'):
                response_text = response_text[3:]
                print("🧹 Removed ``` prefix")
            if response_text.endswith('```'):
                response_text = response_text[:-3]
                print("🧹 Removed ``` suffix")
            
            response_text = response_text.strip()
            print(f"📄 Cleaned response starts with: {response_text[:100]}...")
            
            # Try to parse the entire response as JSON first
            try:
                mcqs = json.loads(response_text)
                if isinstance(mcqs, list):
                    print(f"✅ Direct JSON parsing successful: {len(mcqs)} items")
                    return mcqs
                else:
                    print("❌ Response is not a JSON array")
                    return []
            except json.JSONDecodeError as e:
                print(f"⚠️ Direct JSON parsing failed: {e}")
                
                # Try to extract JSON array
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                
                if start_idx == -1:
                    print("❌ No JSON array found in response")
                    return []
                
                json_str = response_text[start_idx:end_idx]
                print(f"📄 Extracted JSON length: {len(json_str)}")
                
                try:
                    mcqs = json.loads(json_str)
                    print(f"✅ Extracted JSON parsing successful: {len(mcqs)} items")
                    return mcqs
                except json.JSONDecodeError as e:
                    print(f"❌ Extracted JSON parsing failed: {e}")
                    print(f"📄 Problem area: {json_str[max(0, e.pos-50):e.pos+50]}")
                    return []
                    
        except Exception as e:
            print(f"❌ Unexpected error in parse_response_debug: {e}")
            return []

# Run debug test
if __name__ == "__main__":
    generator = DebugMCQGenerator()
    generator.test_single_chapter_debug()
