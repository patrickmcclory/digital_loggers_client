#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'beautifulsoup4>=4.4.1',
    'requests>=2.9.1',
    'configparser>=3.5.0'
    # TODO: put package requirements here
]

test_requirements = [
    'Click>=6.0'
    # TODO: put package test requirements here
]

setup(
    name='digital_loggers_client',
    version='0.1.0',
    description="Small client library for interacting with Digital Loggers Web Power Switches",
    long_description=readme + '\n\n' + history,
    author="Patrick McClory",
    author_email='patrick@mcclory.io',
    url='https://github.com/patrickmcclory/digital_loggers_client',
    packages=[
        'digital_loggers_client',
    ],
    package_dir={'digital_loggers_client':
                 'digital_loggers_client'},
    entry_points={
        'console_scripts': [
            'dl-client=digital_loggers_client.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='digital_loggers_client',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
