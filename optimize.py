#!/usr/bin/env python3
"""
Performance Optimization Script for Our Books
This script helps optimize the website for better loading speeds and AdSense approval.
"""

import os
import re
import json
from pathlib import Path

class WebsiteOptimizer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def minify_css(self, css_content):
        """Basic CSS minification"""
        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        # Remove extra whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        # Remove spaces around selectors
        css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
        return css_content.strip()

    def optimize_css_files(self):
        """Optimize all CSS files in the project"""
        css_files = list(self.root_dir.rglob('*.css'))

        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()

                minified_content = self.minify_css(original_content)

                # Create minified version
                minified_file = css_file.with_suffix('.min.css')
                with open(minified_file, 'w', encoding='utf-8') as f:
                    f.write(minified_content)

                original_size = len(original_content.encode('utf-8'))
                minified_size = len(minified_content.encode('utf-8'))
                savings = original_size - minified_size
                savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

                print(f"✅ Optimized {css_file.name}")
                print(f"   Original: {original_size} bytes, Minified: {minified_size} bytes")
                print(f"   Savings: {savings} bytes ({savings_percent:.1f}%)")
            except Exception as e:
                print(f"❌ Error optimizing {css_file}: {e}")

    def analyze_performance(self):
        """Analyze website performance and provide recommendations"""
        print("\n🔍 PERFORMANCE ANALYSIS REPORT")
        print("=" * 50)

        # Check for large files
        large_files = []
        total_size = 0
        file_count = 0

        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                size = file_path.stat().st_size
                total_size += size
                file_count += 1

                if size > 500000:  # Files larger than 500KB
                    large_files.append((file_path, size))

        print(f"📊 Total files analyzed: {file_count}")
        print(f"📏 Total size: {total_size / 1024 / 1024:.2f} MB")
        if large_files:
            print(f"\n⚠️  Large files found ({len(large_files)}):")
            for file_path, size in large_files:
                print(f"   Size: {size / 1024 / 1024:.2f} MB")
        else:
            print("\n✅ No large files found!")

        # Check for missing optimizations
        html_files = list(self.root_dir.rglob('*.html'))
        missing_compression = []
        missing_lazy_loading = []

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for images without lazy loading
                img_tags = re.findall(r'<img[^>]+>', content)
                for img_tag in img_tags:
                    if 'loading="lazy"' not in img_tag:
                        missing_lazy_loading.append(str(html_file))

                # Check for uncompressed resources
                if '<script' in content and 'async' not in content:
                    missing_compression.append(str(html_file))

            except Exception as e:
                print(f"Error analyzing {html_file}: {e}")

        if missing_lazy_loading:
            print(f"\n🖼️  Images without lazy loading in {len(set(missing_lazy_loading))} files")
            print("   Consider adding loading='lazy' to img tags")

        print("\n🚀 OPTIMIZATION RECOMMENDATIONS:")
        print("1. Use WebP format for images (smaller file size)")
        print("2. Enable gzip compression on your server")
        print("3. Use a CDN for static assets")
        print("4. Implement browser caching headers")
        print("5. Minify JavaScript files")
        print("6. Use CSS sprites for small icons")

    def generate_optimization_report(self):
        """Generate a comprehensive optimization report"""
        report = {
            "timestamp": "2024-09-13",
            "total_files": len(list(self.root_dir.rglob('*.*'))),
            "html_files": len(list(self.root_dir.rglob('*.html'))),
            "css_files": len(list(self.root_dir.rglob('*.css'))),
            "js_files": len(list(self.root_dir.rglob('*.js'))),
            "image_files": len(list(self.root_dir.rglob('*.(jpg|jpeg|png|gif|webp|svg)'))),
            "recommendations": [
                "Enable gzip compression",
                "Use WebP images",
                "Implement lazy loading",
                "Minify CSS and JavaScript",
                "Use browser caching",
                "Optimize font loading"
            ]
        }

        report_file = self.root_dir / "optimization_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📋 Optimization report saved to {report_file}")

def main():
    print("🚀 Our Books Website Optimizer")
    print("=" * 40)

    optimizer = WebsiteOptimizer("/home/yaseen/ourbooks")

    print("\n1. Optimizing CSS files...")
    optimizer.optimize_css_files()

    print("\n2. Analyzing performance...")
    optimizer.analyze_performance()

    print("\n3. Generating optimization report...")
    optimizer.generate_optimization_report()

    print("\n✅ Optimization complete!")
    print("\n📝 Next Steps:")
    print("- Replace CSS links with minified versions in production")
    print("- Implement lazy loading for images")
    print("- Enable gzip compression on your server")
    print("- Use WebP format for images")
    print("- Set up proper caching headers")

if __name__ == "__main__":
    main()