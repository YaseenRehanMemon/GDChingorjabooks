# 🚀 MCQ Generation - Let's Start!

## 🎯 Quick Start Commands

Run these commands in your terminal:

```bash
# 1. Go to books directory
cd /home/yaseen/books

# 2. Activate virtual environment
source myenv/bin/activate

# 3. Install dependencies
pip install google-generativeai PyMuPDF

# 4. Copy the MCQ generator
cp /home/yaseen/ourbooks/simple_mcq_generator.py .

# 5. Make it executable
chmod +x simple_mcq_generator.py

# 6. Test with one chapter
python3 simple_mcq_generator.py
```

## 📊 What to Expect

### First Test Run:
- ✅ Loads your 8 API keys
- ✅ Tests with Chemistry Chapter 1
- ✅ Generates ~50 MCQs (test mode)
- ✅ Saves to `/home/yaseen/ourbooks/mcq_output/chemistry_chapters/ch1_mcqs.json`

### Sample Output:
```
🚀 Simple MCQ Generator
========================================
🔑 Loaded 8 API keys
🧪 Testing MCQ generation...
📄 PDF: /home/yaseen/books/chemistry_chapters/ch1.pdf
📁 Output: /home/yaseen/ourbooks/mcq_output
📤 Uploading PDF: ch1.pdf
⏳ Processing PDF...
🎯 Generating 50 MCQs...
💾 Saved 50 MCQs to /home/yaseen/ourbooks/mcq_output/chemistry_chapters/ch1_mcqs.json
✅ Test successful!
```

## 🎯 Next Steps After Test

### Option 1: Generate All Chemistry Chapters
```bash
cd /home/yaseen/books
source myenv/bin/activate

python3 -c "
from simple_mcq_generator import SimpleMCQGenerator
import os

generator = SimpleMCQGenerator()
books_dir = '/home/yaseen/books'
output_dir = '/home/yaseen/ourbooks/mcq_output'

# Generate all chemistry chapters
chemistry_dir = os.path.join(books_dir, 'chemistry_chapters')
for pdf_file in sorted(os.listdir(chemistry_dir)):
    if pdf_file.endswith('.pdf'):
        chapter = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(chemistry_dir, pdf_file)
        print(f'\\n🎯 Generating MCQs for Chemistry {chapter}')
        mcq_data = generator.generate_mcqs_for_chapter(pdf_path, 'chemistry', chapter)
        generator.save_mcqs(mcq_data, output_dir)
        print(f'✅ {chapter}: {mcq_data[\"total_mcqs\"]} MCQs generated')
"
```

### Option 2: Generate Specific Subject
```bash
cd /home/yaseen/books
source myenv/bin/activate

python3 -c "
from simple_mcq_generator import SimpleMCQGenerator
import os

generator = SimpleMCQGenerator()
books_dir = '/home/yaseen/books'
output_dir = '/home/yaseen/ourbooks/mcq_output'

# Choose subject: 'chemistry', 'physics', 'biology', 'mathematics'
subject = 'biology'
subject_dir = f'{subject}_chapters'

chapter_dir = os.path.join(books_dir, subject_dir)
for pdf_file in sorted(os.listdir(chapter_dir))[:3]:  # First 3 chapters
    if pdf_file.endswith('.pdf'):
        chapter = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(chapter_dir, pdf_file)
        print(f'\\n🎯 Generating MCQs for {subject} {chapter}')
        mcq_data = generator.generate_mcqs_for_chapter(pdf_path, subject, chapter)
        generator.save_mcqs(mcq_data, output_dir)
"
```

## 📈 Scale Up Strategy

### Phase 1: Test & Optimize (Today)
- Generate 2-3 chapters per subject
- Verify MCQ quality and format
- Check LaTeX rendering in your quiz system
- Optimize prompts if needed

### Phase 2: Full Generation (Tomorrow)
- Generate all remaining chapters
- Use all 8 API keys for parallel processing
- Monitor API usage and costs

### Phase 3: Quality Review & Integration
- Review generated MCQs
- Update `reviewed` field to `true` for verified questions
- Integrate into your existing MCQ database

## 🔧 Troubleshooting

### If Test Fails:

1. **API Key Issues:**
```bash
# Check API keys
cat /home/yaseen/apikeys | wc -l  # Should show 8
head -1 /home/yaseen/apikeys     # Should start with AIzaSy
```

2. **Dependencies:**
```bash
cd /home/yaseen/books
source myenv/bin/activate
python3 -c "import google.generativeai as genai; import fitz; print('OK')"
```

3. **PDF Access:**
```bash
ls -la /home/yaseen/books/chemistry_chapters/ch1.pdf
```

## 📊 Progress Tracking

Create a progress file:
```bash
cd /home/yaseen/books
echo "MCQ Generation Progress" > progress.txt
echo "Started: $(date)" >> progress.txt
echo "Chemistry: 0/12 chapters" >> progress.txt
echo "Physics: 0/14 chapters" >> progress.txt
echo "Biology: 0/14 chapters" >> progress.txt
echo "Mathematics: 0/12 chapters" >> progress.txt
```

## 🎯 Expected Timeline

- **Today**: Setup + Test (1-2 hours)
- **Tomorrow**: Generate all XI subjects (4-6 hours)
- **Day 3**: Generate XII subjects + Review (4-6 hours)
- **Total MCQs**: ~10,000 high-quality questions!

## 🚀 Ready to Start?

**Run the 6 commands above and let me know the results!**

The first test should take 2-3 minutes and generate your first batch of MCQs. Once that works, we can scale up to generate thousands of questions automatically! 🎓</content>
</xai:function_call">Create a comprehensive quick-start guide for MCQ generation