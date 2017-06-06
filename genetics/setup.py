"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tpe3',
    version='0.1.0',
    description='TPE3 - Algoritmos geneticos',
    long_description=long_description,
    url='https://bitbucket.org/itba/sia-2017-5',
    author='ITBA - Grupo 5 2017',
    author_email='pypa-dev@googlegroups.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ai neuralnetworks',
    packages=find_packages(exclude=[
        'contrib',
        'docs',
        'tests'
    ]),

    install_requires=[
        'numpy',
        'matplotlib',
        'jsonschema'
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['pip-tools'],
        'test': ['coverage'],
    },

    package_data={
        'tpe3': [
            'data/configs/*.json',
            'data/fulldata/*.tsv',
            'data/testdata/*.tsv'
        ],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'tp3 = tp3.__main__:main',
        ],
    },
)
