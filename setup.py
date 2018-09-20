try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python exercises for everyone',
    'author': 'muawiakh',
    'url': 'https://github.com/muawiakh/pyphercises.git',
    'author_email': 'amuawiakhan@gmail.com',
    'version': '1.0.0',
    'install_requires': ['flask'],
    'packages': [],
    'scripts': [],
    'name': 'pyphercises'
}

setup(**config)