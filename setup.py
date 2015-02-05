# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
cssutils setup

use EasyInstall or install with
    >python setup.py install
"""
__docformat__ = 'restructuredtext'
__author__ = 'Christof Hoeke with contributions by Walter Doerwald and lots of other people'
__date__ = '$LastChangedDate::                            $:'

import codecs
import os

# For Python 2.5
try:
    next
except NameError:
    next = lambda iter: iter.next()

# extract the version without importing the module
lines = open('src/cssutils/__init__.py')
is_ver_line = lambda line: line.startswith('VERSION = ')
line = next(line for line in lines if is_ver_line(line))

exec(line, locals(), globals())

# use the build_py_2to3 if we're building on Python 3
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

def read(*rnames):
    return codecs.open(os.path.join(*rnames), encoding='utf-8').read()

long_description = '\n' + read('README.txt') + '\n'# + read('CHANGELOG.txt')


try:
    from Cython.Distutils import build_ext
    CYTHON = True
except ImportError:
    print('\nWARNING: Cython not installed. '
          'Falcon will still work fine, but may run '
          'a bit slower.\n')
    CYTHON = False

if CYTHON:
    from os import path
    MYDIR = path.abspath(os.path.dirname(__file__)) + '/src'
    def list_modules(dirname):
        filenames = glob.glob(path.join(dirname, '*.py'))

        module_names = []
        for name in filenames:
            module, ext = path.splitext(path.basename(name))
            if module != '__init__':
                module_names.append(module)

        print module_names
        return module_names

    """
    ext_modules = [
        Extension('cssutils.css.' + ext, [path.join('src','cssutils','css' , ext + '.py')])
        for ext in list_modules(path.join(MYDIR, 'cssutils', 'css'))]

    ext_modules += [
        Extension('cssutils.stylesheets.' + ext,
                  [path.join('src','cssutils', 'stylesheets', ext + '.py')])

        for ext in list_modules(path.join(MYDIR, 'cssutils', 'stylesheets'))]
    """
    ext_modules = [
        Extension('cssutils.css.value', [path.join('src','cssutils','css' ,  'value.py')])]

    cmdclass = {'build_ext': build_ext}
else:
    cmdclass = {'build_py': build_py}
    ext_modules = []

setup(
    name='cssutils',
    version=VERSION,
    package_dir={'':'src'},
    packages=find_packages('src'),
    test_suite='cssutils.tests', #'nose.collector'
    tests_require='mock',
    entry_points={
        'console_scripts': [
            'csscapture = cssutils.scripts.csscapture:main',
            'csscombine = cssutils.scripts.csscombine:main',
            'cssparse = cssutils.scripts.cssparse:main'
        ]
    },
    description='A CSS Cascading Style Sheets library for Python',
    long_description=long_description,
    author='Christof Hoeke',
    author_email='c@cthedot.de',
    url='http://cthedot.de/cssutils/',
    download_url='https://bitbucket.org/cthedot/cssutils/downloads',
    license='LGPL 2.1 or later, see also http://cthedot.de/cssutils/',
    keywords='CSS, Cascading Style Sheets, CSSParser, DOM Level 2 Stylesheets, DOM Level 2 CSS',
    platforms='Python 2.5 and later. Python 3.2 and later. Jython 2.5.1 and later.',
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
        ]
    )
