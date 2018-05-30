import os

CONTENT_DIR = 'content'
TEMPLATES_DIR = 'templates'
DOCS_DIR = 'docs'
TEMPLATE_BASE = '%s/base.html' % TEMPLATES_DIR

def _get_html_pages(src_dir):
    """Return list of html files in src_dir"""
    # I would rather build auto everything in CONTENT_DIR but for
    # the sake of the homework I'll manually populate the list.
    #return [f for f in os.listdir(src_dir) if f.endswith('.html')]
    pages = [
        {
            'filename': '%s/about.html' % src_dir,
            'title': 'About',
        },
        {
            'filename': '%s/blog.html' % src_dir,
            'title': 'Blog',
        },
        {
            'filename': '%s/index.html' % src_dir,
            'title': 'Home',
        },
        {
            'filename': '%s/projects.html' % src_dir,
            'title': 'Projects',
        },
    ]
    return pages

def _build_html_page(filename, dest_dir):
    """Wrap html file in top and bottom templates and save in dest_dir"""
    base = open(TEMPLATE_BASE, 'r').read()
    content = open(filename, 'r').read()
    page_content = base.replace('{{content}}', content)

    dest_filename = '%s/%s' % (dest_dir, filename.split('/')[-1])
    page_file = open(dest_filename, 'w')
    page_file.write(page_content)
    page_file.close()
    print(dest_filename, 'built')

def main():
    """Build full html page for each html file in CONTENT_DIR"""
    for page in _get_html_pages(CONTENT_DIR):
        _build_html_page(page['filename'], DOCS_DIR)


if __name__=='__main__':
    main()