from swimlane import Swimlane


app = Swimlane(
    host='https://swimlane-staging.swimlane.io/account',
    username='admin1',
    password='P00lParty!',
    max_retries=5,
    retry_interval=1
)

print(app.apps.list())