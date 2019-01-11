import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 6):
    sys.exit('Please use Python version 3.6 or higher.')

# get the version
version = {}
with open('pyphercises/version.py') as f:
    exec(f.read(), version)

config = {
    'description': 'Python exercises for everyone',
    'author': 'muawiakh',
    'url': 'https://github.com/muawiakh/pyphercises.git',
    'author_email': 'amuawiakhan@gmail.com',
    'version': version['_app_version_'],
    'install_requires': ['flask', 'flask-restful', 'requests', 'nose'],
    'packages': [],
    'scripts': [],
    'name': 'pyphercises'
}

setup(**config)
