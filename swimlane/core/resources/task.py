from swimlane.core.resources.base import APIResource


class Task(APIResource):
    _type = 'Core.Models.Integrations.Task, Core'

    def __init__(self, app, raw):
        super(Task, self).__init__(app._swimlane, raw)

        self.__app = app
        self.id = raw.get('id')
        self.name = raw.get('name')
        self.script = raw.get('action').get('script')
    
    @property
    def app(self):
        return self.__app
    
    def __str__(self):
        return '{self.name}'.format(self=self)