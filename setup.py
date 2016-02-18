#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
try:
    readme = open(os.path.join(here, 'README.rst')).read()
    changes = open(os.path.join(here, 'CHANGES.txt')).read()
    long_description = '\n\n'.join([readme, changes])
except:
    long_description = 'JSON-Schema converter for colander'


setup(
    name='colander_jsonschema',
    version='0.3dev',
    description='JSON-Schema converter for colander',
    long_description=long_description,
    author='OCHIAI, Gouji',
    author_email='gjo.ext@gmail.com',
    url='https://github.com/gjo/colander_jsonschema',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['colander>=1.0'],
    test_suite='colander_jsonschema.tests',
    classifiers=[
        'Environment :: Console',
        'Framework :: Pylons',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing',
    ],
)
