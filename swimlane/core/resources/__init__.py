from swimlane.core.resources.base import APIResource, APIResourceAdapter

from swimlane.core.resources.usergroup import User, Group, UserGroup
from swimlane.core.resources.app import App
from swimlane.core.resources.record import Record
from swimlane.core.resources.report import Report
#from .stats_report import StatsReport
#from .stats_result import StatsResult
#from .task import Task
from swimlane.utils import get_recursive_subclasses


RESOURCE_TYPE_MAP = {c._type: c for c in get_recursive_subclasses(APIResource) if getattr(c, '_type', None)}


def get_resource_class(raw_resource_data):
    """Returns appropriate APIResource class matching the provided raw $type value
    
    Returns None if no matching resource exists
    """
    return RESOURCE_TYPE_MAP.get(raw_resource_data['$type'])

