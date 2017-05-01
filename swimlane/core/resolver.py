import weakref


class SwimlaneResolver(object):
    """Provides automatic weakref resolution for Swimlane client to avoid circular references and memory leaks"""

    def __init__(self, swimlane):
        self.__ref_swimlane = weakref.ref(swimlane)

    @property
    def _swimlane(self):
        """Transparently resolve the swimlane weakref"""
        return self.__ref_swimlane()
