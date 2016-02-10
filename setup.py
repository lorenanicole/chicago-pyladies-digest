#!/usr/bin/env python

import uuid
from setuptools import setup, find_packages
import os
from pip.req import parse_requirements

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
reqs_file = os.path.join(BASE_DIR, 'requirements.txt')
install_reqs = parse_requirements(reqs_file, session=uuid.uuid1())

setup(
    name="pyladies-digest",
    version="0.1",
    author="Lorena Mesa",
    author_email="me@lorenamesa.com",
    description=("Command line tool to create a MailChimp template for PyLadies chapters"),
    license="BSD",
    keywords="pyladies email digest mailchimp",
    install_requires=[str(ir.req) for ir in install_reqs],
    url="https://github.com/lorenanicole/chicago-pyladies-digest",
    packages=find_packages(),
    long_description=read('README.md'),
    scripts=[
        'bin/pyladies-digest',
    #     'bin/bambu-stem-test',
    #     'bin/bambu-crawl',
    #     'bin/bambu-curate'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: PyLadies Open Source Tool",
        "License :: OSI Approved :: BSD License",
    ],
)