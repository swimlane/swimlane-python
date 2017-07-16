import weakref


class SwimlaneResolver(object):
    """Provides automatic weakref resolution for Swimlane client to avoid circular references and memory leaks"""

    def __init__(self, swimlane):
        self.__ref_swimlane = weakref.ref(swimlane)

    @property
    def _swimlane(self):
        """Transparently resolve the swimlane weakref"""
        return self.__ref_swimlane()


class AppResolver(SwimlaneResolver):
    """Provides automatic weakref resolution for Swimlane client and App instance"""

    def __init__(self, app):
        super(AppResolver, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        return self.__ref_app()
