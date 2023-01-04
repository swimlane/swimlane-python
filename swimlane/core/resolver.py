import weakref


class SwimlaneResolver(object):
    """Provides automatic weakref resolution for Swimlane client to avoid circular references and 
    memory leaks """

    def __init__(self, swimlane):
        self.__ref_swimlane = weakref.ref(swimlane) if swimlane else swimlane

    @property
    def _swimlane(self):
        """Transparently resolve the swimlane weakref"""
        if not self.__ref_swimlane:
            referent = self.__ref_swimlane
        else:
            referent = self.__ref_swimlane()
        if referent is None:
            raise ReferenceError("The swimlane object has been garbage collected. The Swimlane "
                                 "object uses weak references to avoid memory leaks. The object "
                                 "gets garbage collected when there are no more references to it. "
                                 "See the weakref documentation for more information.")
        return referent


class AppResolver(SwimlaneResolver):
    """Provides automatic weakref resolution for Swimlane client and App instance"""

    def __init__(self, app):
        super(AppResolver, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app) if app else app

    @property
    def _app(self):
        if not self.__ref_app:
            referent = self.__ref_app
        else:
            referent = self.__ref_app()
        if referent is None:
            raise ReferenceError(
                "The App object of the Swimlane Object has been garbage collected. Both the App "
                "object and the Swimlane object use weak references to avoid memory leaks. The "
                "instance gets garbage collected when there are no more strong references to it. "
                "See the weakref documentation for more information.")
        return referent
