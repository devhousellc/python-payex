#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from payex import __version__


# Requirements
install_requires = [
    'six==1.11.0',
    'suds_py3==1.3.3.0',
]

setup(
    name='python3-payex',
    version=__version__,
    description='PayEx API wrapper',
    long_description=open('README.md').read(),
    author='Ivan K.',
    author_email='ivankunmail@gmail.com',
    url='https://github.com/devhousellc/python3-payex.git',
    packages=['payex'],
    license='BSD',
    install_requires=install_requires,
    test_suite='tests',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
