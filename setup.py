from pyrave import __version__, __author__, __license__
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()


setup(name='pyrave',
      version=__version__,
      description="Python wrapper flutterwave's rave API",
      long_description=read_md('README.md'),
      url='https://github.com/Olamyy/pyrave',
      author=__author__,
      author_email='olamyy53@gmail.com',
      license=__license__,
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=['requests'],
      download_url='https://github.com/Olamyy/pyrave/archive/0.1.tar.gz',
      packages=['pyrave'],
      keywords=['rave', 'payment', 'pyrave'],
      zip_safe=False
      )

