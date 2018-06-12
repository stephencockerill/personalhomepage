import glob
import markdown
import os

from jinja2 import (
    Environment,
    FileSystemLoader,
)

CONTENT_DIR = 'content'
BLOG_DIR = '%s/blog_posts' % CONTENT_DIR
DOCS_DIR = 'docs'
TEMPLATES_DIR = 'templates'
TEMPLATE_NAV = '%s/nav.html' % TEMPLATES_DIR

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def build():
    """Build full html page for each html file in CONTENT_DIR"""
    nav = _build_nav()
    for page_dict in _get_html_pages(CONTENT_DIR, nav=nav):
        template = jinja_env.from_string(page_dict['content'])
        _write_content(
            '%s/%s'% (DOCS_DIR, page_dict['filename']),
            template.render(page_dict),
        )

def _get_html_pages(src_dir, nav=None):
    """Return list of page dicts"""
    pages = []
    for filepath in glob.glob("content/*.html"):
        page = {}
        filename = os.path.basename(filepath)
        title = filename.split('.')[0].title()
        page['filename'] = filename
        page['title'] = title
        page['content'] = _get_content(filepath)
        page['nav'] = nav
        if title == 'Blog':
            page['blog_feed_items'] = _build_blog_posts(nav=nav)
        elif title == 'Index':
            page['title'] = 'Home'
        pages.append(page)

    return pages

def _build_nav():
    nav_template = jinja_env.from_string(_get_content(TEMPLATE_NAV))
    return nav_template.render({
        'nav_links': _get_html_pages(CONTENT_DIR),
    })

def _get_blog_posts():
    """Build HTML pages from Markdown blog posts"""
    blog_posts = []
    md = markdown.Markdown(extensions=["markdown.extensions.meta"])
    for filepath in glob.glob('%s/*.md' % BLOG_DIR):
        blog_post = {}
        filename = os.path.basename(filepath)
        filename = '%s.html' % filename.split('.')[0]
        content = md.convert(_get_content(filepath))

        blog_post['content'] = content
        blog_post['filename'] = filename
        blog_post['title'] = md.Meta['title'][0]
        blog_post['author'] = md.Meta['author'][0]

        blog_post['date'] = md.Meta['date'][0]

        blog_posts.append(blog_post)
    return blog_posts

def _get_content(filepath):
    """Return contents of filepath"""
    return open(filepath, 'r').read()

def _write_content(dest_file, content):
    """Write content to dest_file"""
    dest_file = open(dest_file, 'w')
    dest_file.write(content)
    dest_file.close()
    print('built %s' % dest_file.name)

def _build_blog_posts(nav=None):
    """Build blog posts and return feed items html"""
    blog_feed_items = ''
    for blog_post_dict in _get_blog_posts():
        blog_post_dict['nav'] = nav
        # write blog post
        blog_post_template = jinja_env.from_string(
            _get_content('%s/blog_post.html' % TEMPLATES_DIR)
        )
        _write_content(
            '%s/%s' % (DOCS_DIR, blog_post_dict['filename']),
            blog_post_template.render(blog_post_dict),
        )

        # add to blog posts feed
        blog_feed_item_template = jinja_env.from_string(
            _get_content('%s/blog_feed_item.html' % TEMPLATES_DIR)
        )
        blog_feed_items += blog_feed_item_template.render(blog_post_dict)

    return blog_feed_items

def new(filename=None):
    content = _get_content('%s/blog_post.md' % TEMPLATES_DIR)
    if not filename:
        filename = 'new_blog_post_template'
    filename = '%s.md' % filename.split('.')[0]
    filepath = '%s/%s' % (BLOG_DIR, filename)
    _write_content(
        filepath,
        content,
    )
