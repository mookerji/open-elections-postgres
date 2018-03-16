#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sys
    reload(sys).setdefaultencoding("UTF-8")
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    print 'Please install or upgrade setuptools or pip to continue.'
    sys.exit(1)

INSTALL_REQUIRES = [
    'click',
    'numpy',
    'pandas',
    'recordclass',
]

setup(
    name='openelex_tools',
    version='0.1.0',
    description='Open Elections Tools',
    author='Bhaskar Mookerji',
    author_email='mookerji@gmail.com',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    platforms="Linux,Windows,Mac",
    use_2to3=False,
    zip_safe=False,
)
