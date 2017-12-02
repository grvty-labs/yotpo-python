import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

requests = 'requests >= 2.1.0'
if sys.version_info < (2, 6):
    requests += ', < 2.1.0'
install_requires = [requests, "future==0.15.2"]


# Don't import openpay module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yotpo'))
from version import VERSION

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        import json
    except ImportError:
        install_requires.append('simplejson')

setup(
  name='YotpoPython',
  cmdclass={'build_py': build_py},
  version=VERSION,
  description='Yotpo python bindings',
  author='GRVTY',
  author_email='hola@grvtylabs.com',
  url='https://grvty.digital/',
  tests_require=['mock'],
  packages=['yotpo'],
  package_data={'yotpo': ['../VERSION']},
  install_requires=install_requires,
  # test_suite='openpay.test.all',
  use_2to3=True,
)
