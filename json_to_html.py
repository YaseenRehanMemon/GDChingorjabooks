import json
import sys

def convert_json_to_html(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Escape single quotes in content
    for section in data['sections']:
        section['content'] = section['content'].replace("'", "'\'")

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/styles.css">
    <!-- MathJax configuration and script loading -->
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\(', '\)']]
            }},
            svg: {{
                fontCache: 'global'
            }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
    <input type="checkbox" id="theme-toggle" class="theme-toggle-checkbox">
    
    <div class="page-container">
        <header>
            <h1>{data['title']}</h1>
            <label for="theme-toggle" class="theme-toggle-label">
                <span class="sun">Light</span>
                <span class="moon">Dark</span>
            </label>
        </header>

        <nav class="sidebar">
            <h2>Navigation</h2>
            <ul>
'''
    for section in data['sections']:
        html_content += f'''                <li><a href="#{section['id']}">{section['title']}</a></li>
'''
    html_content += f'''            </ul>
        </nav>

        <main class="content">
'''
    for section in data['sections']:
        html_content += f'''            <section id="{section['id']}">
                <h2>{section['title']}</h2>
                {section['content']}
            </section>
'''
    html_content += f'''        </main>
    </div>
</body>
</html>
'''
    print(html_content)

if __name__ == '__main__':
    json_file_path = sys.argv[1]
    convert_json_to_html(json_file_path)
