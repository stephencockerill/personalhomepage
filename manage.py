import sys

from utils import (
    build,
    new,
)

USAGE = '''usage:
    python manage.py <command>

commands:
    build       Build the site
    new         Create new blog post template
'''

def main():
    try:
        command = sys.argv[1]
    except:
        print(USAGE)
        return
    if command == 'build':
        build()
    elif command == 'new':
        new()
    else:
        print(USAGE)
        return

if __name__=='__main__':
    main()
