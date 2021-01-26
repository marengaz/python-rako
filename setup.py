import os
import re
import sys

from setuptools import find_packages, setup


def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.\-(?:alpha)(?:beta)]+?)\""
    path = ("python_rako", "__version__.py")
    return re.search(regex, read(*path)).group("version")


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="python-rako",
    version=get_version(),
    license="MIT",
    url="https://github.com/marengaz/python-rako",
    author="Ben Marengo",
    author_email="ben@marengo.co.uk",
    description="Asynchronous Python client for Rako Controls Lighting.",
    keywords=["rako", "controls", "api", "async", "client"],
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["python_rako"]),
    test_suite="tests",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=list(val.strip() for val in open("requirements.txt")),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
        "Development Status :: 4 - Beta",
    ],
)
