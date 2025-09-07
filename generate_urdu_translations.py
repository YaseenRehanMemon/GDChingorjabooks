import os
import json
import requests
import time
from pathlib import Path

class UrduTranslationGenerator:
    def __init__(self):
        self.config = self.load_config()
        self.api_keys = self.config.get('apiKeys', [])
        self.current_key_index = 0
        self.key_usage_count = [0] * len(self.api_keys)
        self.max_requests_per_key = self.config.get('maxRequestsPerKey', 100)
        self.translations_dir = "urdu_chapters"
        self.create_directories()
        
    def load_config(self):
        """Load API keys from config file"""
        try:
            with open('assets/js/config.js', 'r') as f:
                content = f.read()
                # Extract API keys from config
                import re
                keys_match = re.search(r'apiKeys:\s*\[(.*?)\]', content, re.DOTALL)
                if keys_match:
                    keys_str = keys_match.group(1)
                    keys = re.findall(r'"([^"]+)"', keys_str)
                    return {'apiKeys': keys, 'maxRequestsPerKey': 100}
        except Exception as e:
            print(f"Error loading config: {e}")
        return {'apiKeys': [], 'maxRequestsPerKey': 100}
    
    def create_directories(self):
        """Create directory structure for Urdu translations"""
        base_dirs = [
            'chemistrybooks_urdu',
            'chemistryxiibooks_urdu', 
            'physicsbooks_urdu',
            'physicsxiibooks_urdu',
            'mathbooks_urdu',
            'mathsxiibooks_urdu',
            'biologybooks_urdu',
            'biologyxiibooks_urdu'
        ]
        
        for dir_name in base_dirs:
            os.makedirs(dir_name, exist_ok=True)
            print(f"Created directory: {dir_name}")
    
    def get_next_api_key(self):
        """Get next available API key"""
        for i in range(len(self.api_keys)):
            key_index = (self.current_key_index + i) % len(self.api_keys)
            if self.key_usage_count[key_index] < self.max_requests_per_key:
                self.current_key_index = key_index
                self.key_usage_count[key_index] += 1
                return self.api_keys[key_index]
        return None
    
    def extract_text_content(self, html_file_path):
        """Extract text content from HTML file"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove script tags and other non-content elements
            import re
            # Remove script tags
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            # Remove style tags
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
            # Remove theme toggle elements
            content = re.sub(r'<input[^>]*theme-toggle[^>]*>', '', content)
            content = re.sub(r'<label[^>]*theme-toggle[^>]*>.*?</label>', '', content, flags=re.DOTALL)
            
            # Extract text from main content area
            main_content_match = re.search(r'<main class="content">(.*?)</main>', content, flags=re.DOTALL)
            if main_content_match:
                main_content = main_content_match.group(1)
                # Remove HTML tags but keep structure
                text_content = re.sub(r'<[^>]+>', ' ', main_content)
                # Clean up whitespace
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                return text_content
            
            return ""
        except Exception as e:
            print(f"Error extracting text from {html_file_path}: {e}")
            return ""
    
    def translate_with_gemini(self, text, api_key):
        """Translate text using Gemini API"""
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
        
        prompt = f"""Translate the following educational content from English to Urdu. This is a textbook chapter about science subjects (Chemistry, Physics, Mathematics, Biology).

IMPORTANT INSTRUCTIONS:
1. Translate ALL text content to Urdu
2. Keep mathematical formulas and equations in LaTeX format unchanged (like $E = mc^2$, $$\\frac{a}{b}$$)
3. Keep chemical formulas unchanged (like H2O, CO2, etc.)
4. Keep scientific symbols and units unchanged
5. Maintain the educational tone and structure
6. Use proper Urdu scientific terminology
7. Return ONLY the translated content, no explanations or additional text

Content to translate:
{text}"""

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
            response = requests.post(api_url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        except Exception as e:
            print(f"API request failed: {e}")
            return ""
    
    def create_urdu_html_file(self, original_file_path, urdu_content, subject_class):
        """Create Urdu HTML file"""
        try:
            with open(original_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Determine Urdu directory
            urdu_dir = f"{subject_class}_urdu"
            filename = os.path.basename(original_file_path)
            urdu_file_path = os.path.join(urdu_dir, filename)
            
            # Replace main content with Urdu translation
            import re
            urdu_html = re.sub(
                r'(<main class="content">)(.*?)(</main>)',
                rf'\1{urdu_content}\3',
                original_content,
                flags=re.DOTALL
            )
            
            # Add RTL direction and Urdu styling
            urdu_html = urdu_html.replace(
                '<body>',
                '<body dir="rtl" class="urdu-content">'
            )
            
            # Add Urdu-specific CSS
            urdu_css = """
    <style>
        .urdu-content {
            font-family: 'Noto Sans Urdu', 'Arial', sans-serif;
            direction: rtl;
            text-align: right;
        }
        .urdu-content h1, .urdu-content h2, .urdu-content h3, .urdu-content h4 {
            text-align: right;
        }
        .urdu-content p, .urdu-content li {
            text-align: right;
            line-height: 1.8;
        }
        .urdu-content .card {
            text-align: right;
        }
        .urdu-content table {
            direction: rtl;
        }
        .urdu-content th, .urdu-content td {
            text-align: right;
        }
    </style>"""
            
            urdu_html = urdu_html.replace('</head>', f'{urdu_css}\n</head>')
            
            # Write Urdu file
            with open(urdu_file_path, 'w', encoding='utf-8') as f:
                f.write(urdu_html)
            
            print(f"Created Urdu file: {urdu_file_path}")
            return True
            
        except Exception as e:
            print(f"Error creating Urdu file {urdu_file_path}: {e}")
            return False
    
    def process_chapter(self, file_path, subject_class):
        """Process a single chapter file"""
        filename = os.path.basename(file_path)
        urdu_dir = f"{subject_class}_urdu"
        urdu_file_path = os.path.join(urdu_dir, filename)
        
        # Check if Urdu file already exists
        if os.path.exists(urdu_file_path):
            print(f"Urdu file already exists: {filename}")
            return True
        
        print(f"Processing: {filename}")
        
        # Extract text content
        text_content = self.extract_text_content(file_path)
        if not text_content:
            print(f"No content extracted from {filename}")
            return False
        
        # Get API key
        api_key = self.get_next_api_key()
        if not api_key:
            print("No available API keys")
            return False
        
        # Translate content
        print(f"Translating {filename}...")
        urdu_content = self.translate_with_gemini(text_content, api_key)
        
        if not urdu_content:
            print(f"Translation failed for {filename}")
            return False
        
        # Create Urdu HTML file
        success = self.create_urdu_html_file(file_path, urdu_content, subject_class)
        
        if success:
            print(f"✅ Successfully translated: {filename}")
        else:
            print(f"❌ Failed to create Urdu file: {filename}")
        
        # Add delay to avoid rate limiting
        time.sleep(2)
        return success
    
    def process_all_chapters(self):
        """Process all chapter files"""
        chapter_dirs = [
            'chemistrybooks',
            'chemistryxiibooks', 
            'physicsbooks',
            'physicsxiibooks',
            'mathbooks',
            'mathsxiibooks',
            'biologybooks',
            'biologyxiibooks'
        ]
        
        total_files = 0
        processed_files = 0
        
        for chapter_dir in chapter_dirs:
            if not os.path.exists(chapter_dir):
                print(f"Directory {chapter_dir} does not exist, skipping...")
                continue
            
            html_files = [f for f in os.listdir(chapter_dir) if f.endswith('.html')]
            total_files += len(html_files)
            
            print(f"\n📚 Processing {chapter_dir} ({len(html_files)} files)")
            print("=" * 50)
            
            for filename in html_files:
                file_path = os.path.join(chapter_dir, filename)
                if self.process_chapter(file_path, chapter_dir):
                    processed_files += 1
        
        print(f"\n🎉 Translation Summary:")
        print(f"Total files: {total_files}")
        print(f"Successfully processed: {processed_files}")
        print(f"Failed: {total_files - processed_files}")
        
        if processed_files > 0:
            print(f"\n📁 Urdu translations saved in:")
            for chapter_dir in chapter_dirs:
                urdu_dir = f"{chapter_dir}_urdu"
                if os.path.exists(urdu_dir):
                    file_count = len([f for f in os.listdir(urdu_dir) if f.endswith('.html')])
                    print(f"  - {urdu_dir}/ ({file_count} files)")

if __name__ == '__main__':
    if not os.path.exists('assets/js/config.js'):
        print("❌ Error: config.js file not found!")
        print("Please make sure assets/js/config.js exists with your API keys.")
        exit(1)
    
    generator = UrduTranslationGenerator()
    
    if not generator.api_keys:
        print("❌ Error: No API keys found in config.js!")
        print("Please add your Gemini API keys to assets/js/config.js")
        exit(1)
    
    print(f"🚀 Starting Urdu translation generation...")
    print(f"📊 Found {len(generator.api_keys)} API keys")
    print(f"📁 Will create Urdu directories for all subjects")
    
    generator.process_all_chapters()