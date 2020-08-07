#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
modules = find_packages(exclude=['examples'])
from os import path
import codecs
this_directory = path.abspath(path.dirname(__file__))
long_description = codecs.open(path.join(this_directory, 'README.md'), 'r', 'utf-8').read()

setup(
    name='epsapy',
    version='0.0.0',
    description='Electric Power System Analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/colives/epsapy',
    author='Carlos Olives, Francisco Casado',
    author_email='carlos.olives.camps@gmail.com, fcasadomachado@gmail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Electric Engineering Students',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_dir={'':'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
)
