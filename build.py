import os
import re

BLOG_DIR = 'blog'
CONTENT_DIR = 'content'
DOCS_DIR = 'docs'
TEMPLATES_DIR = 'templates'
TEMPLATE_BASE = '%s/base.html' % TEMPLATES_DIR


def main():
    """Build full html page for each html file in CONTENT_DIR"""
    base = open(TEMPLATE_BASE, 'r').read()
    base = _build_nav(base, _get_html_pages(CONTENT_DIR))
    for page_dict in _get_html_pages(CONTENT_DIR, base=base):
        _build_html_page(base, page_dict, DOCS_DIR)

def _get_html_pages(src_dir, base=None):
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
            'content': _build_blog_posts('%s/blog.html' % src_dir, base=base),
        },
        {
            'filename': 'projects.html',
            'title': 'Projects',
            'content': _get_content('%s/projects.html' % src_dir),
        },
    ]
    return pages

def _get_blog_posts(src_dir):
    blog_posts = [
        {
            'filename': 'blog_post_1.html',
            'date': 'May 29, 2018',
            'title': 'Discovering Delaware',
            'subtitle': 'Find out why Delaware is the place to be this summer!',
            'img': 'img/san-francisco.jpg',
        },
        {
            'filename': 'blog_post_2.html',
            'date': 'May 25, 2018',
            'title': 'Airflow Tutorial',
            'subtitle': 'A look at how to use Apache Airflow to build your data pipeline',
            'img': 'img/icons/about.svg',
        },
    ]
    return blog_posts

def _get_content(filepath):
    """Return contents of filepath"""
    return open(filepath, 'r').read()

def _build_blog_posts(filepath, base=None):
    blog = _get_content(filepath)
    blog_post_template = open('%s/blog_post.html' % TEMPLATES_DIR, 'r').read()
    blog_feed_item_template = open('%s/blog_feed_item.html' % TEMPLATES_DIR, 'r').read()

    # wrap blog_post_template with base
    base = base if base else _get_content(TEMPLATE_BASE)
    blog_post_template = _replace_braces(base, {'content': blog_post_template})

    # generate blog posts
    for blog_post_dict in _get_blog_posts(BLOG_DIR):
        _build_html_page(blog_post_template, blog_post_dict, DOCS_DIR)

    # generate feed items for main blog page
    # looping a second time because dict values are 'pop'ped after injected to prevent
    # infinite injection loops, so need to generate the list again
    blog_feed_items = ''
    for blog_post_dict in _get_blog_posts(BLOG_DIR):
        blog_feed_items += _replace_braces(blog_feed_item_template, blog_post_dict)
    blog = _replace_braces(blog, {'blog_feed_items': blog_feed_items})

    return blog



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
        # pop dict values to prevent infinite recursion loop
        replace_with = page_dict.pop(match.strip(), None)
        if replace_with:
            page = page.replace('{{%s}}' % match, replace_with)
            # support for nested templates
            page = _replace_braces(page, page_dict)
    return page


if __name__=='__main__':
    main()
