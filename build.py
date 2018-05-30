import os
import re

CONTENT_DIR = 'content'
TEMPLATES_DIR = 'templates'
DOCS_DIR = 'docs'
TEMPLATE_BASE = '%s/base.html' % TEMPLATES_DIR


def main():
    """Build full html page for each html file in CONTENT_DIR"""
    for page_dict in _get_html_pages(CONTENT_DIR):
        _build_html_page(page_dict, DOCS_DIR)

def _build_html_page(page_dict, dest_dir):
    """Wrap html file in top and bottom templates and save in dest_dir"""
    base = open(TEMPLATE_BASE, 'r').read()
    page_content = _replace_braces(base, page_dict)

    filename = page_dict['filename']
    dest_filename = '%s/%s' % (dest_dir, filename.split('/')[-1])
    page_file = open(dest_filename, 'w')
    page_file.write(page_content)
    page_file.close()
    print(dest_filename, 'built')

def _get_html_pages(src_dir):
    """Return list of page dicts"""
    pages = [
        {
            'filename': '%s/about.html' % src_dir,
            'title': 'About',
            'content': _get_content('%s/about.html' % src_dir),
        },
        {
            'filename': '%s/blog.html' % src_dir,
            'title': 'Blog',
            'content': _get_content('%s/blog.html' % src_dir),
        },
        {
            'filename': '%s/index.html' % src_dir,
            'title': 'Home',
            'content': _get_content('%s/index.html' % src_dir),
        },
        {
            'filename': '%s/projects.html' % src_dir,
            'title': 'Projects',
            'content': _get_content('%s/projects.html' % src_dir),
        },
    ]
    return pages

def _get_content(filename):
    """Return contents of filename"""
    return open(filename, 'r').read()

def _replace_braces(page, page_dict):
    """Return page with {{key}} replaced with page_dict value"""
    pattern = r'(?<={{).+?(?=}})'
    matches = set(re.findall(pattern, page))
    for match in matches:
        print('{{%s}}' % match)
        replace_with = page_dict.pop(match.strip(), None)
        if replace_with:
            page = page.replace('{{%s}}' % match, replace_with)
            # support for nested templates
            page = _replace_braces(page, page_dict)
    return page

if __name__=='__main__':
    main()
