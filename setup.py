#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages

# Refer to files relative to the directory containing setup.py
rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_version():
    return open(rel_file('VERSION')).read().strip()

def get_requirements():
    reqs = open(rel_file('REQUIREMENTS')).read().splitlines()
    return filter(lambda line: line[:1].isalnum(), reqs)

setup(
    name             = 'pistachio',
    version          = get_version(),
    author           = "Zachary Voase",
    author_email     = "z@zacharyvoase.com",
    url              = 'http://zacharyvoase.github.com/pistachio/',
    description      = "An experimental Mustache implementation in Python.",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = get_requirements(),
)
