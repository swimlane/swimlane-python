#from .resource import Resource
from .app import App
from .record import Record
from .report import Report
#from .stats_report import StatsReport
#from .stats_result import StatsResult
from .user import User
#from .group import Group
#from .task import Task


TYPE_RESOURCE_MAP = {c._type: c for c in (App, Record, Report, User)}


def get_resource_class(raw_resource_data):
    """Returns appropriate APIResource class matching the provided raw $type value
    
    Returns None if no matching resource exists
    """
    return TYPE_RESOURCE_MAP.get(raw_resource_data['$type'])

