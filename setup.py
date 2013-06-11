#!/usr/bin/env python

import os
import sys

from setuptools import setup

import logging_assertions

os.chdir(os.path.dirname(sys.argv[0]) or ".")

setup(
    name="logging-assertions",
    version="%s.%s.%s" %logging_assertions.__version__,
    url="https://github.com/wolever/logging-assertions",
    author="David Wolever",
    author_email="david@wolever.net",
    description="Easily make assertions about logged messages in tests",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
    ],
    py_modules=["logging_assertions"],
)
