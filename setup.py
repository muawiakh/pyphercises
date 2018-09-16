try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python exercises for everyone',
    'author': 'muawiakh',
    'url': 'https://github.com/muawiakh/pyphercises.git',
    'author_email': 'amuawiakhan@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': [],
    'scripts': [],
    'name': 'pyphercises'
}

setup(**config)
