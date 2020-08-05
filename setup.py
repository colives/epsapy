#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:42:14 2020

@author: carlosolives
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='epsapy',
    version='0.0.1',
    description='Electric Power System Analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/colives/epsapy',
    author='Carlos Olives',
    author_email='carlos.olives.camps@gmail.com',
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
    packages=find_packages(),
    python_requires='>=3.5, <4',
)
