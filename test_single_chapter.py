#!/usr/bin/env python3

import os
import json
import time
import requests

class SingleChapterTester:
    def __init__(self):
        # Use only one API key for testing
        self.api_key = "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw"
        
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
    
    def read_pdf_as_text(self, pdf_path):
        """Read PDF content as text (simplified version)"""
        try:
            # For testing, return a sample content
            return f"""
            Chapter 1: Stoichiometry
            
            Stoichiometry is the study of quantitative relationships between reactants and products in chemical reactions.
            
            Key Concepts:
            1. Molecular Formula: The actual number of atoms in a molecule (e.g., H2O)
            2. Empirical Formula: The simplest ratio of atoms in a compound
            3. Molar Mass: The mass of one mole of a substance
            4. Avogadro's Number: 6.022 x 10^23 particles per mole
            
            Example Problems:
            - Calculate the molar mass of water (H2O)
            - Determine the number of moles in 18g of water
            - Balance chemical equations
            
            Important Formulas:
            - Moles = Mass / Molar Mass
            - Mass = Moles × Molar Mass
            - Percent Composition = (Mass of Element / Total Mass) × 100
            """
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {e}")
            return None
    
    def generate_mcqs(self, pdf_path, chapter_name):
        """Generate MCQs for a PDF"""
        try:
            print(f"🔄 Testing MCQ generation for: {chapter_name}")
            
            # Read PDF content
            pdf_content = self.read_pdf_as_text(pdf_path)
            if not pdf_content:
                return None
            
            # Create full prompt
            full_prompt = self.prompt.replace("[Insert chapter PDF content here]", pdf_content)
            
            # API request - Using Gemini 2.5 Flash
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
            
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
            
            print(f"📡 Sending request to Gemini 2.5 Flash...")
            response = requests.post(api_url, json=payload, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                mcq_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                if mcq_text:
                    try:
                        mcqs = json.loads(mcq_text)
                        print(f"✅ Generated {len(mcqs)} MCQs successfully!")
                        return mcqs
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON decode error: {e}")
                        # Save raw response for debugging
                        with open(f"debug_response.txt", 'w') as f:
                            f.write(mcq_text)
                        print("📄 Raw response saved to debug_response.txt")
                        return None
                else:
                    print(f"❌ Empty response")
                    return None
            else:
                print(f"❌ API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating MCQs: {e}")
            return None
    
    def save_mcqs(self, mcqs, chapter_name):
        """Save MCQs to JSON file"""
        try:
            # Create output directory
            os.makedirs("test_output", exist_ok=True)
            
            # Generate filename
            filename = f"{chapter_name.replace('.pdf', '')}_mcqs.json"
            filepath = os.path.join("test_output", filename)
            
            # Save MCQs
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mcqs, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved MCQs to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving MCQs: {e}")
            return None
    
    def test_single_chapter(self):
        """Test with a single chapter"""
        print("🧪 Testing Single Chapter MCQ Generation")
        print("=" * 50)
        
        if not self.prompt:
            return
        
        # Test with a sample chapter
        test_pdf = "test_chapter.pdf"
        chapter_name = "ch1_stoichiometry"
        
        # Generate MCQs
        mcqs = self.generate_mcqs(test_pdf, chapter_name)
        
        if mcqs:
            # Save to file
            self.save_mcqs(mcqs, chapter_name)
            
            # Show sample MCQ
            if len(mcqs) > 0:
                print("\n📋 Sample MCQ:")
                print("-" * 30)
                sample = mcqs[0]
                print(f"Question: {sample.get('question', 'N/A')}")
                print(f"Options: {sample.get('options', {})}")
                print(f"Correct Answer: {sample.get('correct_answer', 'N/A')}")
                print(f"Difficulty: {sample.get('difficulty', 'N/A')}")
                print(f"Explanation: {sample.get('explanation', 'N/A')[:100]}...")
            
            print(f"\n🎉 Test completed successfully!")
            print(f"Generated {len(mcqs)} MCQs")
        else:
            print("❌ Test failed - no MCQs generated")

def main():
    tester = SingleChapterTester()
    tester.test_single_chapter()

if __name__ == "__main__":
    main()