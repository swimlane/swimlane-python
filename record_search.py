
from swimlane import Swimlane
import pandas as pd
import json, pendulum
swimlane = Swimlane('https://swimlane-main.swimlane.io', 'admin', 's!9^@14Sh8OHwI', verify_ssl=False)
app = swimlane.apps.get(name='TestADP')
record = app.records.get(id='TES-1')
print(record)
# record = app.records.get(name='TES-1')

json_report = [
    {
    'k1': 'v1',
    'k2': 'v2'
    },
    {
    'k1': 'v3',
    'k2': 'v4'
    },
    {
    'k1': 'v5',
    'k2': 'v6'
    }    
]
#for threatRecord in record['threat-intel']:
#  if threatRecord['greenplum-response'] is not None and threatRecord['greenplum-response'] != '':
#    jsonData = json.loads(threatRecord['greenplum-response'])
#    for row in jsonData:
#      row['intel_ticket'] = threatRecord['Tracking Id']
#      row['fraud_ticket'] = record['Tracking Id']
#      json_report.append(row)
#pdObj = pd.read_json(json.dumps(json_report, indent=4, sort_keys=True, default=str), orient='records')


pdObj = pd.read_json(json.dumps(json_report), orient='records')

#print(pdObj)