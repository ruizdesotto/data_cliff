#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [] # TODO read prod requirements

test_requirements = [
    "pytest>=3",
]

setup(
    author="Miguel Ruiz",
    author_email="miguel.ruizdesotto@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="CLI tool to show differences on text data tracked by dvc.",
    entry_points={
        "console_scripts": [
            "cliff=data_cliff.cli:main",
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="data_cliff",
    name="data_cliff",
    packages=find_packages(include=["data_cliff", "data_cliff.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ruizdesotto/data_cliff",
    version="0.0.1",
    zip_safe=False,
)
