import os

content_dir = 'content'
docs_dir = 'docs'

top = open('templates/top.html', 'r').read()
bottom = open('templates/bottom.html', 'r').read()

for filename in os.listdir(content_dir):
    if filename.endswith('.html'):
        content = open('%s/%s' % (content_dir, filename), 'r').read()
        page_content = top + content + bottom
        page_file = open('%s/%s' % (docs_dir, filename), 'w')
        page_file.write(page_content)
        page_file.close()

