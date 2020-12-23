# Python: Rako Controls API Client

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]
[![Code Quality][code-quality-shield]][code-quality]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

Asynchronous Python client for Rako Controls.

## About

This package allows you to control and monitor Rako Controls devices
programmatically. It is mainly created to allow third-party programs to automate
their behavior.

## Installation

```bash
pip install python-rako
```

## Usage

```python
import asyncio


async def main():
    # TODO
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of ``MAJOR.MINOR.PATCH``. In a nutshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

In case you'd like to contribute, a `Makefile` has been included to ensure a
quick start.

```bash
make venv
source ./venv/bin/activate
make dev
```

Now you can start developing, run `make` without arguments to get an overview
of all make goals that are available (including description):

```bash
$ make
Asynchronous Python client for Rako Controls Lighting.

Usage:
  make help                            Shows this message.
  make dev                             Set up a development environment.
  make lint                            Run all linters.
  make lint-black                      Run linting using black & blacken-docs.
  make lint-flake8                     Run linting using flake8 (pycodestyle/pydocstyle).
  make lint-pylint                     Run linting using PyLint.
  make lint-mypy                       Run linting using MyPy.
  make test                            Run tests quickly with the default Python.
  make coverage                        Check code coverage quickly with the default Python.
  make install                         Install the package to the active Python's site-packages.
  make clean                           Removes build, test, coverage and Python artifacts.
  make clean-all                       Removes all venv, build, test, coverage and Python artifacts.
  make clean-build                     Removes build artifacts.
  make clean-pyc                       Removes Python file artifacts.
  make clean-test                      Removes test and coverage artifacts.
  make clean-venv                      Removes Python virtual environment artifacts.
  make dist                            Builds source and wheel package.
  make release                         Release build on PyP
  make venv                            Create Python venv environment.
```

## Authors & contributors

The original setup of this repository is by [Ben Marengo][marengaz].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

[License](LICENSE)

[build-shield]: https://github.com/marengaz/python-rako/workflows/Continuous%20Integration/badge.svg
[build]: https://github.com/marengaz/python-rako/actions
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/marengaz/python-rako.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/marengaz/python-rako/context:python
[codecov-shield]: https://codecov.io/gh/marengaz/python-rako/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/marengaz/python-rako
[contributors]: https://github.com/marengaz/python-rako/graphs/contributors
[marengaz]: https://github.com/marengaz
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/marengaz/python-rako.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2020.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[releases-shield]: https://img.shields.io/github/release/marengaz/python-rako.svg
[releases]: https://github.com/marengaz/python-rako/releases
[semver]: http://semver.org/spec/v2.0.0.html

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/marengaz
[github-actions-shield]: https://github.com/marengaz/rakomqtt/workflows/Test%20RakoMQTT/badge.svg?branch=master
[github-actions]: https://github.com/marengaz/rakomqtt/actions?query=workflow%3A%22Test+RakoMQTT%22+branch%3Amaster
