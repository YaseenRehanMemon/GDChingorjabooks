# Batch MCQ Generator

This script processes PDF files from your books directory and generates MCQs using Gemini 2.5 Pro API.

## 🚀 Features

- **Parallel Processing**: Uses multiple API keys simultaneously
- **Subject Mapping**: Each subject uses a different API key
- **Large File Handling**: Skips files larger than 20MB
- **Automatic Organization**: Creates organized JSON files
- **Error Handling**: Robust error handling and logging

## 📁 Directory Structure

```
books/
├── chemistry_chapters/
│   ├── ch1.pdf
│   ├── ch2.pdf (skipped - >20MB)
│   └── ...
├── physics_chapters/
├── math_chapters/
└── ...
```

## 🔧 Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Update API Keys**:
   Edit the script and add your API keys:
   ```python
   self.api_keys = [
       "your-api-key-1",
       "your-api-key-2",
       # ... add more keys
   ]
   ```

3. **Update Directory Path**:
   Change the books directory path in the script:
   ```python
   books_directory = "/home/yaseen/books"
   ```

## 🎯 Usage

1. **Run the Script**:
   ```bash
   python simple_pdf_mcq_generator.py
   ```

2. **Monitor Progress**:
   The script will show real-time progress for each subject and chapter.

3. **Check Output**:
   Generated MCQ files will be saved in `mcq_output/` directory.

## 📊 Output Structure

```
mcq_output/
├── chemistry_chapters/
│   ├── ch1_mcqs.json
│   ├── ch5_mcqs.json
│   └── ...
├── physics_chapters/
├── math_chapters/
└── ...
```

## ⚙️ Configuration

### API Key Mapping
- `chemistry_chapters` → API Key 1
- `chemistryXII_chapters` → API Key 2
- `physics_chapters` → API Key 3
- `physicsXII_chapters` → API Key 4
- `math_chapters` → API Key 5
- `mathsXII_chapters` → API Key 1 (reused)
- `biology_chapters` → API Key 2 (reused)
- `biologyXII_chapters` → API Key 3 (reused)

### Large Files (Skipped)
The script automatically skips these large files:
- `chemistry_chapters`: ch2.pdf, ch3.pdf, ch4.pdf, ch7.pdf
- `mathsXII_chapters`: ch2_Functions_and_Limits.pdf, ch3_Differentiation.pdf, etc.
- `physicsXII_chapters`: ch27_Nuclear_Physics.pdf
- `chemistryXII_chapters`: ch1_CHEMISTRY_OF_REPRESENTATIVE_ELEMENTS.pdf, etc.
- `math_chapters`: ch2.pdf, ch3.pdf, ch4.pdf, ch6.pdf, ch8.pdf, ch12.pdf

## 🔍 Troubleshooting

### Common Issues

1. **API Rate Limiting**:
   - The script includes delays between requests
   - Uses different API keys for different subjects

2. **Large Files**:
   - Files >20MB are automatically skipped
   - Process these manually using the MCQ Manager interface

3. **JSON Parsing Errors**:
   - Raw responses are saved as debug files
   - Check `debug_*.txt` files for issues

### Error Messages

- `❌ Directory not found`: Update the books directory path
- `❌ API error`: Check your API keys and internet connection
- `❌ JSON decode error`: Check the debug file for raw response

## 📈 Performance

- **Speed**: ~3-5 minutes per chapter
- **Parallel**: Multiple subjects processed simultaneously
- **Efficiency**: Uses all available API keys

## 🎯 Next Steps

1. **Run the script** to generate MCQs for all chapters
2. **Use MCQ Manager** to manually process large files
3. **Review generated MCQs** for quality
4. **Integrate with your website** for student access

## 💡 Tips

- **Start with one subject** to test the setup
- **Monitor API usage** to avoid rate limits
- **Keep the prompt file** (`gemini_mcq_extraction_prompt.txt`) in the same directory
- **Check output files** regularly for quality