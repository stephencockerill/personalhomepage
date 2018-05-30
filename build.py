import os

CONTENT_DIR = 'content'
TEMPLATES_DIR = 'templates'
DOCS_DIR = 'docs'

def get_html_filenames(src_dir):
    """Return list of html files in src_dir"""
    return [f for f in os.listdir(src_dir) if f.endswith('.html')]

def build_html_page(src_dir, dest_dir, filename):
    """Wrap html file in top and bottom templates and save in dest_dir"""
    top = open('%s/top.html' % TEMPLATES_DIR, 'r').read()
    bottom = open('%s/bottom.html' % TEMPLATES_DIR, 'r').read()
    content = open('%s/%s' % (src_dir, filename), 'r').read()

    page_content = top + content + bottom
    page_file = open('%s/%s' % (dest_dir, filename), 'w')
    page_file.write(page_content)
    page_file.close()
    print('%s/%s' % (dest_dir, filename), 'built')

def main():
    """Build full html page for each html file in CONTENT_DIR"""
    for filename in get_html_filenames(CONTENT_DIR):
        build_html_page(CONTENT_DIR, DOCS_DIR, filename)


if __name__=='__main__':
    main()
