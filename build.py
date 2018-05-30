import os
import re

CONTENT_DIR = 'content'
TEMPLATES_DIR = 'templates'
DOCS_DIR = 'docs'
TEMPLATE_BASE = '%s/base.html' % TEMPLATES_DIR


def main():
    """Build full html page for each html file in CONTENT_DIR"""
    base = open(TEMPLATE_BASE, 'r').read()
    base = _build_nav(base, _get_html_pages(CONTENT_DIR))
    for page_dict in _get_html_pages(CONTENT_DIR):
        _build_html_page(base, page_dict, DOCS_DIR)

def _get_html_pages(src_dir):
    """Return list of page dicts"""
    pages = [
        {
            'filename': 'index.html',
            'title': 'Home',
            'content': _get_content('%s/index.html' % src_dir),
        },
        {
            'filename': 'about.html',
            'title': 'About',
            'content': _get_content('%s/about.html' % src_dir),
        },
        {
            'filename': 'blog.html',
            'title': 'Blog',
            'content': _get_content('%s/blog.html' % src_dir),
        },
        {
            'filename': 'projects.html',
            'title': 'Projects',
            'content': _get_content('%s/projects.html' % src_dir),
        },
    ]
    return pages

def _get_content(filepath):
    """Return contents of filepath"""
    return open(filepath, 'r').read()

def _build_nav(base, pages):
    nav = open('%s/nav.html' % TEMPLATES_DIR, 'r').read()
    nav_link_template = '''
        <li class="nav-item">
          <a class="nav-link" href="{{filename}}">{{title}}</a>
        </li>
        '''
    nav_links = ''
    for page_dict in pages:
        nav_links += _replace_braces(nav_link_template, page_dict)
    nav = _replace_braces(nav, {'nav_links': nav_links})
    print(nav)
    base = _replace_braces(base, {'nav': nav})
    return base

def _build_html_page(base, page_dict, dest_dir):
    """Inject page specified into base"""
    page_content = _replace_braces(base, page_dict)
    filename = page_dict['filename']
    dest_filename = '%s/%s' % (dest_dir, filename)
    page_file = open(dest_filename, 'w')
    page_file.write(page_content)
    page_file.close()
    print(dest_filename, 'built')


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
