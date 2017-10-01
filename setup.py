# Magic
'''
This "# Magic" comment is used to determine wether travis is being for actual
selenium_webextension development, or if it is being run by someone using this
as a package. If it changes, change the code in travis/setup.sh too.
'''
# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='selenium-webextensions',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1',

    description='Test WebExtension with Selenium in Chrome and Firefox',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/cowlicks/selenium-webextensions',

    # Author details
    author='Blake Griffith',
    author_email='blake.a.griffith@gmail.com',

    # Choose your license
    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3',
    ],

    keywords='testing pytest selenium development',

    packages=['selenium_webextensions'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    install_requires=['selenium', 'pytest'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'xvfb': ['xvfbwrapper'],
    },
)
