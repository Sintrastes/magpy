#!/usr/bin/python3

from distutils.core import setup

setup(
    description = 'A python library for dealing with magmas.',
    author = 'Nathan BeDell',
    url = 'https://github.com/Sintrastes/magpy',
    download_url = 'https://github.com/Sintrastes/magpy.git',
    author_email = 'nabedell@liberty.edu',
    version = '0.1',
    install_requires = ['pymonad'],
    packages = ['magpy'],
    scripts = [],
    name = 'magpy',
    classifiers = ["Programming Language :: Python :: 3"])



