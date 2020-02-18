from gitfaces.__about__ import (
    __author__,
    __copyright__,
    __email__,
    __status__,
    __version__,
)

from . import cli
from .main import fetch

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__version__",
    "__status__",
    "fetch",
    "cli",
]
