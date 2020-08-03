#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:42:14 2020

@author: carlosolives
"""

import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EPSApy",
    version="0.0.1",
    author="Carlos Olives",
    author_email="carlos.olives.camps@gmail.com",
    description="Electric Power System Analysis",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/colives/epsapy",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires = '>= 3.6',
)