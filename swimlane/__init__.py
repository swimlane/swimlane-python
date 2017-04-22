from __future__ import absolute_import
from pkg_resources import get_distribution, DistributionNotFound

from .core.client import Swimlane

__all__ = [
    'Swimlane',
]


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '0.0.0-dev'
