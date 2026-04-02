import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取古诗词和作者
pattern = r'<a[^>]*>([^<]+)</a>\s*(?:<span[^>]*>——&nbsp;</span><a[^>]*>([^<]+)</a>)?'
matches = re.findall(pattern, content)

# 过滤出古诗词（长度大于5且包含中文）
poems = []
for match in matches:
    poem = match[0].strip()
    author = match[1].strip() if len(match) > 1 and match[1] else ''
    if len(poem) > 5 and any('\u4e00' <= c <= '\u9fff' for c in poem):
        poems.append((poem, author))

# 生成清理后的HTML
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>古诗词名句</title>
    <style>
        body {
            font-family: "SimSun", "宋体", serif;
            background-color: #f5f5dc;
            padding: 20px;
            line-height: 2;
        }
        .poem-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .poem-item {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px dashed #ccc;
        }
        .poem-text {
            font-size: 18px;
            color: #333;
        }
        .poem-author {
            font-size: 14px;
            color: #666;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="poem-container">
'''

for poem, author in poems:
    if author:
        html_content += f'''        <div class="poem-item">
            <span class="poem-text">{poem}</span>
            <span class="poem-author">—— {author}</span>
        </div>
'''
    else:
        html_content += f'''        <div class="poem-item">
            <span class="poem-text">{poem}</span>
        </div>
'''

html_content += '''    </div>
</body>
</html>
'''

with open('index_clean.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'已生成清理后的文件 index_clean.html，共 {len(poems)} 条古诗词')
