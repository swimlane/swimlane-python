from swimlane import Swimlane
application_name = 'SPT-6612'
record_id = 'a1UwwX8dx9lE0vNq8'

swimlane = Swimlane('https://localhost', 'admin', 'P00lParty!', verify_ssl=False)
app = swimlane.apps.get(name=application_name)
record = app.records.get(id=record_id)
groupB = swimlane.groups.get(name='Group B')
record.add_restriction(groupB)