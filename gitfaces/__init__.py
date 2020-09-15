from gitfaces.__about__ import __version__

from . import cli
from .main import fetch

__all__ = ["__version__", "fetch", "cli"]
