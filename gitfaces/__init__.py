# -*- coding: utf-8 -*-
#
from __future__ import print_function

from gitfaces.__about__ import (
    __author__,
    __email__,
    __copyright__,
    __license__,
    __version__,
    __maintainer__,
    __status__
    )

from .main import fetch


try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end='')
