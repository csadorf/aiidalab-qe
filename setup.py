#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'aiida-core~=1.0',
    'aiidalab-widgets-base==1.0.0a7',
    'aiida-quantumespresso~=2.0',
    'appmode-aiidalab~=0.5.0',
    'ase~=3.18',
    'fileupload~=0.1',
    'future~=0.16',
    'Markdown~=2.6',
    'nglview~=2.7',
    ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Carl Simon Adorf",
    author_email='simon.adorf@epfl.ch',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An AiiDA lab app for Quantum ESPRESSO calculations.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='quantum_espresso',
    name='aiidalab-qe-app',
    packages=find_packages(include=['qe_app']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aiidalab/aiidalab-qe',
    version='0.1.0',
    zip_safe=False,
)
