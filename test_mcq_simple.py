import google.generativeai as genai
import time
import json

print('🎯 Testing Simple MCQ Generation...')

genai.configure(api_key='AIzaSyBaJWfsgTaXwkNy711OXHIcBNe8dV7fF_8')

# Upload PDF
pdf_path = '/home/yaseen/books/chemistry_chapters/ch1.pdf'
print('📤 Uploading PDF...')
sample_file = genai.upload_file(pdf_path)

while sample_file.state.name == 'PROCESSING':
    time.sleep(1)
    sample_file = genai.get_file(sample_file.name)

if sample_file.state.name != 'ACTIVE':
    print(f'❌ PDF processing failed: {sample_file.state.name}')
    exit(1)

print('✅ PDF ready')

# Simple MCQ prompt
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = '''Generate 3 simple MCQs from this chemistry chapter.

Return ONLY a JSON array like this:
[
  {
    "question": "What is the main topic?",
    "options": {"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
    "correct_answer": "A",
    "explanation": "Brief explanation"
  }
]'''

print('🎯 Generating MCQs...')
start_time = time.time()
response = model.generate_content([sample_file, prompt])
gen_time = time.time() - start_time

print(f'⏱️ Generation took {gen_time:.1f}s')

if response and response.text:
    print('✅ Response received')
    print(f'📄 Response length: {len(response.text)} characters')
    print(f'📄 Response preview: {response.text[:200]}...')
    
    # Try to parse JSON
    try:
        # Clean response
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        mcqs = json.loads(text)
        print(f'✅ Successfully parsed {len(mcqs)} MCQs')
        
        if mcqs:
            print(f'📝 Sample: {mcqs[0]["question"][:50]}...')
            
    except json.JSONDecodeError as e:
        print(f'❌ JSON parsing failed: {e}')
        print(f'📄 Raw response: {text[:300]}...')
        
else:
    print('❌ No response from API')

# Clean up
sample_file.delete()
print('🧹 Cleaned up')
