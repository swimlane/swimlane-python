"""Swimlane Python API driver"""

from __future__ import absolute_import

import logging

from .core.client import Swimlane
from .utils.version import get_package_version

__all__ = [
    'Swimlane',
]

__version__ = get_package_version()

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

