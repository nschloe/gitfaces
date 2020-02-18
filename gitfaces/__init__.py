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
