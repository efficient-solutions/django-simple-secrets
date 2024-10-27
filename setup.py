#!/usr/bin/env python

"""setup.py: distutils/setuptools install script."""

from setuptools import setup

REQUIRES = [
    "Django>=4,<6"
]

try:
    with open("README.md", encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

setup(
    name="django-simple-secrets",
    version="0.1.0",
    author="Efficient Solutions LLC",
    author_email="contact@efficient.solutions",
    description="A Django integration for AWS Secrets Manager with caching and lazy loading support",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/efficient-solutions/django-simple-secrets",
    packages=["django_secrets"],
    license="MIT",
    install_requires=REQUIRES,
    python_requires=">= 3.10",
    keywords=[
        "Django", "AWS Secrets Manager"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
)
