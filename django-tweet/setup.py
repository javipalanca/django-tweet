#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import tweet

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = tweet.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-tweet',
    version=version,
    description="""Tweet Model for Django""",
    long_description=readme + '\n\n' + history,
    author='Javi Palanca',
    author_email='jpalanca@gmail.com',
    url='https://github.com/javipalanca/django-tweet',
    packages=[
        'tweet',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-tweet',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
