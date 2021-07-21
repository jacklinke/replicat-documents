#!/usr/bin/env python

import os
import re
import sys

import setuptools


def get_version(*file_paths):
    """Retrieves the version from replicat_documents/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("replicat_documents", "__init__.py")


if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")
requirements = open("requirements/requirements.txt").readlines()

setuptools.setup(
    author="Jack Linke",
    author_email="jack@watervize.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Repeatable documents for Django",
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    keywords="replicat replicat-documents replicat_documents documents django pdf png jpg embed embedded",
    name="replicat-documents",
    packages=[
        "replicat_documents",
    ],
    test_suite="tests",
    url="https://github.com/jacklinke/replicat-documents",
    version=version,
    zip_safe=False,
)
