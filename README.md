# gitfaces

[![PyPi Version](https://img.shields.io/pypi/v/gitfaces.svg?style=flat-square)](https://pypi.org/project/gitfaces)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/gitfaces.svg?style=flat-square)](https://pypi.org/pypi/gitfaces/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/gitfaces.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/gitfaces)
[![PyPi downloads](https://img.shields.io/pypi/dm/gitfaces.svg?style=flat-square)](https://pypistats.org/packages/gitfaces)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/gitfaces/ci?style=flat-square)](https://github.com/nschloe/gitfaces/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/gitfaces.svg?style=flat-square)](https://codecov.io/gh/nschloe/gitfaces)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

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

### License
This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
