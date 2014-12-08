#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

"""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='ipponmanager',
    version='0.1.0',
    description='An application to manage Judo tournaments',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Lars Hutzelmann',
    author_email='lars_hutzelmann at gmx dot de',
    url='https://github.com/lhutzelmann/ipponmanager',
    packages=[
        'ipponmanager',
    ],
    package_dir={'ipponmanager': 'ipponmanager'},
    include_package_data=True,
    install_requires=[
    ],
    license='Simplified BSD License',
    zip_safe=False,
    keywords='ipponmanager',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 2-Clause License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
)
