#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

#with open('HISTORY.md') as history_file:
#    history = history_file.read()

requirements = [
    'django>=2.2.24',
    'selenium==3.141.0',
]

test_requirements = [
    'pytest>=3',
]

setup(
    author="Jack Linke",
    author_email='jack@watervize.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Repeatable documents for Django",
    install_requires=requirements,
    license="MIT license",
    #long_description=readme + '\n\n' + history,
    long_description=readme,
    include_package_data=True,
    keywords='replicat replicat-documents replicat_documents documents django pdf png jpg embed embedded',
    name='replicat_documents',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jacklinke/replicat-documents',
    version='0.1.0',
    zip_safe=False,
)
