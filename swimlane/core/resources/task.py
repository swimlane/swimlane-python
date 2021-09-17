from swimlane.core.resources.base import APIResource


class Task(APIResource):
    _type = 'Core.Models.Integrations.Task, Core'

    def __init__(self, swimlane, raw):
        super(Task, self).__init__(swimlane, raw)
        self.app_id = raw.get('applicationId')
        self.id = raw.get('id')
        self.name = raw.get('name')
        self.script = raw.get('action').get('script')
    
    def __str__(self):
        return '{self.name}'.format(self=self)

