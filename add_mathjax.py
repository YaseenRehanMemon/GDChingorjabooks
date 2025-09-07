import os
import re

# Define the MathJax configuration with correct escaping
mathjax_config = '''    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            },
            svg: {
                fontCache: 'global'
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>'''

# Get all HTML files in the chemistrybooks directory
html_files = [f for f in os.listdir('chemistrybooks') if f.endswith('.html')]

# Process each HTML file
for filename in html_files:
    filepath = os.path.join('chemistrybooks', filename)
    
    # Read the file content
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if MathJax is already properly configured
    if 'MathJax' in content and 'tex:' in content and 'inlineMath' in content:
        print(f'{filename} already has proper MathJax configuration')
        continue
    
    # If MathJax config exists but is incorrect, remove it first
    if 'MathJax' in content:
        # Remove existing MathJax config
        content = re.sub(r'\s*<script>[^<]*window\.MathJax[^<]*</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'\s*<script[^<]*MathJax-script[^<]*</script>\s*', '', content, flags=re.DOTALL)
    
    # Insert MathJax configuration before </head> tag
    content = content.replace('</head>', f'{mathjax_config}\n</head>')
    
    # Write the updated content back to the file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f'Updated {filename}')