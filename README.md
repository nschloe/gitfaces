# gitfaces

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/gitfaces/master.svg)](https://circleci.com/gh/nschloe/gitfaces)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/gitfaces.svg)](https://codecov.io/gh/nschloe/gitfaces)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/gitfaces.svg)](https://pypi.org/project/gitfaces)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/gitfaces.svg?logo=github&label=Stars)](https://github.com/nschloe/gitfaces)

gitfaces collects avatars for all contributors of a given Git repository. (This
can be used for [Gource's](https://github.com/acaudwell/Gource)
`--user-image-dir`, for example.)

Simply type
```
gitfaces /path/to/git/repo out/
```
and gitfaces will start fetching from [Gravatar](https://en.gravatar.com/) and
[GitHub](https://github.com/). Once done, the `out/` directory will contain
all the avatars.

### Installation

gitfaces is [available from the Python Package
Index](https://pypi.org/project/gitfaces/), so simply type
```
pip install -U gitfaces
```
to install or upgrade.

### Testing

To run the gitfaces unit tests, check out this repository, set the environment
variable `GITFACES_TEST` to the local path of a Git repository on which you
would like the tests to be performed, and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

gitfaces is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
