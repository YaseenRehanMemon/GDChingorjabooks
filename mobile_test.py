#!/usr/bin/env python3
"""
Mobile Compatibility Testing Script for Our Books
This script tests the website for mobile compatibility and provides recommendations.
"""

import os
import json
import re
from pathlib import Path
from urllib.parse import urlparse

class MobileTester:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.warnings = []
        self.passed = []

    def test_viewport_meta(self):
        """Test for proper viewport meta tags"""
        html_files = list(self.root_dir.rglob('*.html'))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if '<meta name="viewport"' in content:
                    if 'width=device-width' in content and 'initial-scale=1' in content:
                        self.passed.append(f"✅ {html_file.name}: Proper viewport meta tag")
                    else:
                        self.issues.append(f"❌ {html_file.name}: Incomplete viewport meta tag")
                else:
                    self.issues.append(f"❌ {html_file.name}: Missing viewport meta tag")

            except Exception as e:
                self.issues.append(f"❌ Error reading {html_file}: {e}")

    def test_responsive_design(self):
        """Test for responsive design elements"""
        html_files = list(self.root_dir.rglob('*.html'))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for responsive classes
                responsive_indicators = [
                    'md:', 'lg:', 'sm:', 'xl:',
                    '@media', 'flex-wrap', 'grid-cols-1',
                    'max-w-screen', 'container'
                ]

                responsive_found = any(indicator in content for indicator in responsive_indicators)

                if responsive_found:
                    self.passed.append(f"✅ {html_file.name}: Responsive design elements found")
                else:
                    self.warnings.append(f"⚠️ {html_file.name}: Limited responsive design indicators")

            except Exception as e:
                self.issues.append(f"❌ Error reading {html_file}: {e}")

    def test_touch_targets(self):
        """Test for adequate touch target sizes"""
        html_files = list(self.root_dir.rglob('*.html'))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for buttons and links
                buttons = re.findall(r'<button[^>]*>.*?</button>', content, re.DOTALL | re.IGNORECASE)
                links = re.findall(r'<a[^>]*class="[^"]*[^>]*>.*?</a>', content, re.DOTALL | re.IGNORECASE)

                small_targets = []

                for button in buttons:
                    if 'class=' in button:
                        classes = re.search(r'class="([^"]*)"', button)
                        if classes:
                            class_list = classes.group(1).split()
                            # Check for small sizing classes
                            if any(cls in ['w-4', 'h-4', 'w-6', 'h-6', 'w-8', 'h-8', 'text-xs', 'text-sm']
                                   for cls in class_list):
                                small_targets.append('button')

                if small_targets:
                    self.warnings.append(f"⚠️ {html_file.name}: Some buttons may have small touch targets")
                else:
                    self.passed.append(f"✅ {html_file.name}: Touch targets look adequate")

            except Exception as e:
                self.issues.append(f"❌ Error reading {html_file}: {e}")

    def test_image_optimization(self):
        """Test for image optimization"""
        html_files = list(self.root_dir.rglob('*.html'))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find images
                images = re.findall(r'<img[^>]+>', content)

                for img in images:
                    # Check for lazy loading
                    if 'loading="lazy"' not in img:
                        self.warnings.append(f"⚠️ {html_file.name}: Image without lazy loading")
                    else:
                        self.passed.append(f"✅ {html_file.name}: Image with lazy loading")

                    # Check for alt text
                    if 'alt=' not in img:
                        self.issues.append(f"❌ {html_file.name}: Image missing alt text")
                    else:
                        self.passed.append(f"✅ {html_file.name}: Image has alt text")

            except Exception as e:
                self.issues.append(f"❌ Error reading {html_file}: {e}")

    def test_font_sizes(self):
        """Test for readable font sizes on mobile"""
        css_files = list(self.root_dir.rglob('*.css'))

        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for small font sizes
                small_fonts = re.findall(r'font-size:\s*[\d.]+px', content)
                small_fonts = [font for font in small_fonts if float(re.search(r'[\d.]+', font).group()) < 14]

                if small_fonts:
                    self.warnings.append(f"⚠️ {css_file.name}: Some font sizes may be too small for mobile")
                else:
                    self.passed.append(f"✅ {css_file.name}: Font sizes appear adequate")

            except Exception as e:
                self.issues.append(f"❌ Error reading {css_file}: {e}")

    def test_navigation(self):
        """Test navigation for mobile usability"""
        html_files = list(self.root_dir.rglob('*.html'))

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for hamburger menu or mobile navigation
                mobile_nav_indicators = [
                    'hamburger', 'mobile-menu', 'nav-toggle',
                    'md:hidden', 'lg:hidden', 'sm:flex'
                ]

                mobile_nav_found = any(indicator in content for indicator in mobile_nav_indicators)

                if mobile_nav_found:
                    self.passed.append(f"✅ {html_file.name}: Mobile navigation detected")
                else:
                    self.warnings.append(f"⚠️ {html_file.name}: Mobile navigation may need improvement")

            except Exception as e:
                self.issues.append(f"❌ Error reading {html_file}: {e}")

    def generate_report(self):
        """Generate comprehensive mobile testing report"""
        print("\n📱 MOBILE COMPATIBILITY TEST REPORT")
        print("=" * 50)

        print(f"\n🔴 ISSUES ({len(self.issues)}):")
        for issue in self.issues:
            print(f"  {issue}")

        print(f"\n🟡 WARNINGS ({len(self.warnings)}):")
        for warning in self.warnings:
            print(f"  {warning}")

        print(f"\n🟢 PASSED ({len(self.passed)}):")
        for passed in self.passed[:10]:  # Show first 10 passed items
            print(f"  {passed}")

        if len(self.passed) > 10:
            print(f"  ... and {len(self.passed) - 10} more passed tests")

        # Overall score
        total_tests = len(self.issues) + len(self.warnings) + len(self.passed)
        score = (len(self.passed) / total_tests) * 100 if total_tests > 0 else 0

        print("\n📊 OVERALL SCORE:")
        print(f"   {score:.1f}%")
        if score >= 90:
            print("🎉 Excellent mobile compatibility!")
        elif score >= 80:
            print("👍 Good mobile compatibility with minor improvements needed")
        elif score >= 70:
            print("⚠️ Fair mobile compatibility - improvements recommended")
        else:
            print("🔴 Poor mobile compatibility - significant improvements needed")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("1. Ensure all images have alt text for accessibility")
        print("2. Add lazy loading to images: loading='lazy'")
        print("3. Test touch targets are at least 44px")
        print("4. Verify font sizes are readable on mobile")
        print("5. Test forms work well on mobile devices")
        print("6. Ensure navigation is easy to use on small screens")

    def run_all_tests(self):
        """Run all mobile compatibility tests"""
        print("🚀 Starting Mobile Compatibility Tests...")

        self.test_viewport_meta()
        self.test_responsive_design()
        self.test_touch_targets()
        self.test_image_optimization()
        self.test_font_sizes()
        self.test_navigation()

        self.generate_report()

def main():
    print("📱 Our Books Mobile Compatibility Tester")
    print("=" * 45)

    tester = MobileTester("/home/yaseen/ourbooks")
    tester.run_all_tests()

if __name__ == "__main__":
    main()