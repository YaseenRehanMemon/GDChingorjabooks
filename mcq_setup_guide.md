# MCQ Generation Setup Guide

## Overview
This guide will help you set up and run the comprehensive MCQ generation system using Gemini 2.5 Flash API to generate 100+ MCQs per chapter from your PDF textbooks.

## 📋 Prerequisites Check

### 1. API Keys
```bash
# Check if API keys file exists
ls -la /home/yaseen/apikeys

# View API keys (should show 8 keys starting with AIzaSy)
head -10 /home/yaseen/apikeys
```

### 2. PDF Textbooks Structure
```bash
# Check books directory structure
ls -la /home/yaseen/books/

# Check chapter PDFs
ls /home/yaseen/books/chemistry_chapters/
ls /home/yaseen/books/biology_chapters/
ls /home/yaseen/books/physics_chapters/
ls /home/yaseen/books/mathematics_chapters/
```

### 3. Python Environment
```bash
# Check Python version
python3 --version

# Check if virtual environment exists
ls -la /home/yaseen/books/myenv/
```

## 🛠️ Installation & Setup

### Step 1: Setup Python Virtual Environment
```bash
cd /home/yaseen/books

# Create virtual environment if it doesn't exist
python3 -m venv myenv

# Activate virtual environment
source myenv/bin/activate
```

### Step 2: Install Required Packages
```bash
cd /home/yaseen/books
source myenv/bin/activate

# Install dependencies
pip install google-generativeai PyMuPDF

# Verify installations
python3 -c "import google.generativeai as genai; import fitz; print('✅ All dependencies installed')"
```

### Step 3: Copy MCQ Generator Script
```bash
# Copy the simple MCQ generator to books directory
cp /home/yaseen/ourbooks/simple_mcq_generator.py /home/yaseen/books/
chmod +x /home/yaseen/books/simple_mcq_generator.py
```

### Step 4: Test Setup
```bash
cd /home/yaseen/books
source myenv/bin/activate

# Run test
python3 simple_mcq_generator.py
```

## 🚀 Running MCQ Generation

### Option 1: Generate All Chapters
```bash
cd /home/yaseen/books
source myenv/bin/activate
python3 mcq_generator.py
```

### Option 2: Generate Specific Subject
```bash
cd /home/yaseen/books
source myenv/bin/activate
python3 -c "
from mcq_generator import MCQGenerator
import os

generator = MCQGenerator()
books_dir = '/home/yaseen/books'
output_dir = '/home/yaseen/ourbooks/mcq_output'

# Generate for specific subject
subject = 'chemistry'
chapter_dir = 'chemistry_chapters'
chapter_path = os.path.join(books_dir, chapter_dir)

for pdf_file in os.listdir(chapter_path):
    if pdf_file.endswith('.pdf'):
        chapter_name = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(chapter_path, pdf_file)
        print(f'Generating MCQs for {subject} - {chapter_name}')
        mcq_data = generator.generate_mcqs_for_chapter(pdf_path, subject, chapter_name)
        generator.save_mcqs(mcq_data, output_dir)
"
```

### Option 3: Test Single Chapter
```bash
cd /home/yaseen/books
source myenv/bin/activate
python3 -c "
from mcq_generator import MCQGenerator

generator = MCQGenerator()
pdf_path = '/home/yaseen/books/chemistry_chapters/ch1.pdf'
mcq_data = generator.generate_mcqs_for_chapter(pdf_path, 'chemistry', 'ch1')
generator.save_mcqs(mcq_data, '/home/yaseen/ourbooks/mcq_output')
print('✅ Test MCQ generation completed!')
"
```

## 📊 Expected Output

### MCQ JSON Structure
Each generated MCQ follows this exact format:
```json
{
  "id": "chemistry_xi_ch1_mcq_001",
  "question": "Which of the following is a homogeneous mixture?",
  "question_type": "multiple_choice",
  "options": {
    "A": "Sand and water",
    "B": "Oil and water",
    "C": "Salt solution",
    "D": "Iron filings and sulfur"
  },
  "correct_answer": "C",
  "explanation": "Detailed explanation with reasoning",
  "difficulty": "easy",
  "topic": "basic_definitions",
  "subtopic": "mixtures",
  "tags": ["mixture", "homogeneous", "heterogeneous"],
  "learning_objective": "Differentiate between homogeneous and heterogeneous mixtures",
  "created_date": "2024-09-11",
  "source": "ch1.pdf",
  "ai_generated": true,
  "reviewed": false,
  "quality_score": 0.95
}
```

### Output Directory Structure
```
/home/yaseen/ourbooks/mcq_output/
├── chemistry_chapters/
│   ├── ch1_mcqs.json
│   ├── ch2_mcqs.json
│   └── ...
├── physics_chapters/
│   └── ...
└── biology_chapters/
    └── ...
```

## ⚙️ Configuration Options

### Modify MCQ Generation Settings
Edit the `__init__` method in `MCQGenerator` class:

```python
# In mcq_generator.py
self.target_mcqs_per_chapter = 100  # Change number of MCQs
self.max_pdf_size_mb = 19          # Adjust PDF size limit
self.max_retries = 3               # API retry attempts
self.rate_limit_delay = 2          # Delay between requests
```

### Customize Prompts
Modify the `create_mcq_prompt()` method to adjust:
- Difficulty distribution
- Question types
- LaTeX formatting requirements
- Subject-specific guidelines

## 🔧 Troubleshooting

### Common Issues

1. **PDF Too Large (>20MB)**
   - Script automatically compresses PDFs
   - If still too large, splits into chunks
   - Uses first chunk for MCQ generation

2. **API Rate Limits**
   - Automatic API key rotation
   - Built-in rate limiting delays
   - 8 API keys for load balancing

3. **JSON Parsing Errors**
   - Robust error handling
   - Automatic retry with different API key
   - Detailed error logging

4. **Memory Issues**
   - Processes one chapter at a time
   - Automatic cleanup of uploaded files
   - Efficient PDF processing

### Debug Mode
```bash
cd /home/yaseen/books
source myenv/bin/activate
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from mcq_generator import MCQGenerator
# Run with debug logging
"
```

## 📈 Performance Optimization

### Parallel Processing
For faster generation across multiple chapters:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_parallel(generator, chapters):
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = []
        for chapter in chapters:
            task = asyncio.get_event_loop().run_in_executor(
                executor, generator.generate_mcqs_for_chapter, *chapter
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results
```

### Batch Processing
Process subjects in batches to manage API quotas:
```python
subjects_batch_1 = ['chemistry', 'physics']
subjects_batch_2 = ['biology', 'mathematics']
# Process batch 1, then batch 2
```

## 🎯 Quality Assurance

### MCQ Validation
- Automatic ID generation
- Required field validation
- LaTeX format checking
- Difficulty level balancing

### Manual Review Process
1. Check generated MCQs for accuracy
2. Verify LaTeX rendering
3. Test explanations completeness
4. Update `reviewed` field to `true`

## 📊 Monitoring & Analytics

### Track Generation Progress
```python
# Add to MCQGenerator class
def log_progress(self, subject, chapter, mcq_count, success=True):
    with open('generation_log.txt', 'a') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        status = 'SUCCESS' if success else 'FAILED'
        f.write(f'{timestamp} | {subject} | {chapter} | {mcq_count} MCQs | {status}\\n')
```

### Performance Metrics
- MCQs generated per minute
- API key usage distribution
- Success/failure rates
- Average processing time per chapter

## 🔄 Integration with Existing System

### Update Quiz System
The generated MCQs are automatically compatible with your existing quiz system:
- Same JSON format as current MCQs
- Proper subject/chapter directory structure
- LaTeX support for mathematical expressions
- Detailed explanations for learning

### Database Integration
```python
# Example: Load MCQs into your system
import json
import os

def load_mcqs_to_system(output_dir):
    all_mcqs = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('_mcqs.json'):
                with open(os.path.join(root, file), 'r') as f:
                    mcqs = json.load(f)
                    all_mcqs.extend(mcqs)

    # Integrate with your existing MCQ system
    return all_mcqs
```

## 🚀 Next Steps

1. **Test the System**: Start with one chapter to verify everything works
2. **Scale Up**: Process all chapters systematically
3. **Quality Review**: Manually review generated MCQs
4. **Integration**: Merge with existing MCQ database
5. **Optimization**: Fine-tune prompts and settings based on results

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify API keys are valid and have sufficient quota
3. Ensure PDF files are not corrupted
4. Check network connectivity for API calls

The system is designed to be robust and handle various edge cases automatically. Happy MCQ generation! 🎓</content>
</xai:function_call">Create comprehensive setup and usage guide for the MCQ generation system