from setuptools import setup
from pyrave import __version__, __author__, __license__


setup(name='pyrave',
      version=__version__,
      description="Python wrapper flutterwave's rave API",
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

