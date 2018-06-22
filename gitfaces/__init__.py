# -*- coding: utf-8 -*-
#
from __future__ import print_function

from gitfaces.__about__ import (
    __author__,
    __email__,
    __copyright__,
    __version__,
    __status__,
)

from .main import fetch
from . import cli

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__version__",
    "__status__",
    "fetch",
    "cli",
]

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end="")
