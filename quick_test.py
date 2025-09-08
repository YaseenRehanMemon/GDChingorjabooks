#!/usr/bin/env python3

import requests
import json

def test_mcq_generation():
    api_key = "AIzaSyDZ74bZgJw2U8ACz0ncJ4pxhISeBgoosTw"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Simple prompt for testing
    prompt = """Generate exactly 3 MCQs about stoichiometry in this JSON format:

[
  {
    "id": "test_mcq_001",
    "question": "What is the molecular formula of water?",
    "question_type": "multiple_choice",
    "options": {
      "A": "$H_2O$",
      "B": "$H_2O_2$",
      "C": "$HO$",
      "D": "$H_3O$"
    },
    "correct_answer": "A",
    "explanation": "Water has the molecular formula $H_2O$, consisting of 2 hydrogen atoms and 1 oxygen atom.",
    "difficulty": "easy",
    "topic": "molecular_formula",
    "subtopic": "water",
    "tags": ["molecular_formula", "water", "basic_chemistry"],
    "learning_objective": "Understand basic molecular formulas",
    "created_date": "2024-01-01",
    "source": "test",
    "ai_generated": true,
    "reviewed": false,
    "quality_score": 0.8
  }
]

Return ONLY the JSON array, no additional text."""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 4096,
        }
    }

    try:
        print("🔄 Testing MCQ generation...")
        response = requests.post(api_url, json=payload, timeout=60)
        
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
                    
                    mcqs = json.loads(mcq_text)
                    print(f"✅ Success! Generated {len(mcqs)} MCQs")
                    
                    # Show first MCQ
                    if len(mcqs) > 0:
                        print("\n📋 Sample MCQ:")
                        print("-" * 40)
                        sample = mcqs[0]
                        print(f"Question: {sample.get('question', 'N/A')}")
                        print(f"Options: {sample.get('options', {})}")
                        print(f"Correct Answer: {sample.get('correct_answer', 'N/A')}")
                        print(f"Difficulty: {sample.get('difficulty', 'N/A')}")
                        print(f"Explanation: {sample.get('explanation', 'N/A')[:100]}...")
                    
                    # Save to file
                    with open('test_mcqs.json', 'w') as f:
                        json.dump(mcqs, f, indent=2)
                    print(f"\n💾 Saved to test_mcqs.json")
                    
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    print(f"Raw response: {mcq_text[:200]}...")
                    return False
            else:
                print("❌ Empty response")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_mcq_generation()