from datetime import datetime

import mock

from swimlane.core.fields.history import RevisionCursor, Revision
from swimlane.core.resources.usergroup import UserGroup

raw_revision_data = [
    {'$type': 'Core.Models.History.Revision, Core',
     'modifiedDate': '2017-04-10T16:26:17.065Z',
     'revisionNumber': 3.0,
     'status': 'historical',
     'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                'id': '58de1d1c07637a0264c0ca6a',
                'name': 'admin'},
     'version': {'$type': 'Core.Models.Record.Record, Core',
                 'actionsExecuted': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e557c8b81ce3e2c6515fd1': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.389Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6ac5c88412c4acda3d66c': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.396Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6aca5293267c35188ea37': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.401Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6acc099097a98678ccfcf': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.407Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6bee81f119baf40a659b9': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.984Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c62f257f2c4994b84140': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.412Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c6536afac95743437254': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.419Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c83415177d0ad68ea961': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.426Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e7bb9ad6e4d34e8f557b2b': True,
                     '58e7bbba9bc82babdd655653': True,
                     '58e7bd86ad9ba1f93ef4afae': True,
                     '58e7bddc6ed1ceda2950b621': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.437Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}}},
                 'allowed': [],
                 'applicationId': '58e4bb4407637a0e4c4f9873',
                 'applicationRevision': 72.0,
                 'comments': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'},
                 'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                   'id': '58de1d1c07637a0264c0ca6a',
                                   'name': 'admin'},
                 'createdDate': '2017-04-10T16:26:16.486Z',
                 'disabled': False,
                 'id': '58ebb22807637a02d4a14bd6',
                 'isNew': False,
                 'linkedData': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     'a99ut': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017},
                     'ac1oa': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 5,
                               'dow': 3,
                               'h': 23,
                               'm': 42,
                               'mm': 4,
                               'q': 2,
                               'w': 14,
                               'y': 2017},
                     'aiir8': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017}},
                 'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'},
                 'modifiedDate': '2017-04-10T16:26:16.999Z',
                 'referencedByIds': [],
                 'referencedRecordIds': [],
                 'sessionTimeSpent': 0,
                 'timeTrackingEnabled': True,
                 'totalTimeSpent': 0,
                 'trackingFull': 'RA-7',
                 'trackingId': 7.0,
                 'values': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e4bb4407637a0e4c4f9875': 'RA-7',
                     'a04rv': '10.0.1.184:56005:3172',
                     'a0g40': 'Alert Action',
                     'a0k7v': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bae8c61082e377cc4d82',
                               'value': 'Open'},
                     'a18qr': 'User.Activity.Failed Logins',
                     'a1r3v': 'Logon',
                     'a3rvw': '3172',
                     'a4l9p': 'logdec1',
                     'a5v09': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bafd83f418637cf91c3e',
                               'value': 'ESA Alert'},
                     'a5yg3': '3172',
                     'a6if8': '[{"lifetime": "60", "rid": "4531291", "payload": "7808", "size": "11956", "service": "0", "eth.src": "00:0C:29:5B:98:5E", "feed.name": "Swimlane_Feed", "medium": "1", "ip.dst": "178.238.235.143", "org.dst": "Contabo GmbH", "sessionid": "4534669", "latdec.dst": "51.2993", "eth.type": "2048", "ip.src": "10.0.1.183", "domain.dst": "contabo.host", "eth.dst": "00:50:56:A7:4D:79", "did": "packdec1", "longdec.dst": "9.491", "packets": "122", "streams": "2", "country.dst": "Germany", "time": 1491593904, "ip.proto": "1"}]',
                     'a7gm5': '<14>Apr  5 23:42:54 localhost CEF:0|RSA|Security Analytics ESA|10.4|Module_58e40ea9e4b070dfd2a59ad5_Alert|Alert Action|7|rt=2017-04-05T23:42Z id=890eb2b1-2d90-46a5-b1ed-6e58b408ed83 source=10.0.1.184:56005:3172  action=authentication failure;; client=sshd;; device_class=Unix;; device_ip=10.0.1.178;; device_type=crossbeamc;; did=logdec1;; ec_activity=Logon;; ec_outcome=Failure;; ec_subject=User;; ec_theme=Authentication;; esa_time=1491435774280;; event_cat_name=User.Activity.Failed Logins;; event_source_id=10.0.1.184:56005:3172;; header_id=0006;; host_src=178.238.235.143;; level=4;; medium=32;; msg_id=000103;; rid=3172;; sessionid=3172;; size=175;; time=1491435771;; user_dst=user;; username=0;;\x00',
                     'a7ira': 'User',
                     'a8vjm': 'Failure',
                     'a990o': '7',
                     'a99ut': '2017-04-10T16:26:17.457Z',
                     'aasnf': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bb144121bd73d8f53845',
                               'value': 'High'},
                     'ac1oa': '2017-04-05T23:42:54Z',
                     'acqdq': '1491435774280',
                     'af967': '890eb2b1-2d90-46a5-b1ed-6e58b408ed83',
                     'afbbv': '',
                     'afff3': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                               'id': '58de1d1c07637a0264c0ca6a',
                               'name': 'admin'},
                     'ahziu': '178.238.235.143',
                     'ai1zz': '4',
                     'aiir8': '2017-04-10T16:26:16.389Z',
                     'aio1w': 'sshd',
                     'aokp5': 'Unix',
                     'apf9i': '10.0.1.178',
                     'arnd6': 'authentication failure',
                     'arok4': 'crossbeamc',
                     'aw9gd': 'ip.src=10.0.1.178 || ip.dst=10.0.1.178',
                     'awmtq': 'Authentication',
                     'axdvr': '175'},
                 'visualizations': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], mscorlib]], mscorlib'}}},
    {'$type': 'Core.Models.History.Revision, Core',
     'modifiedDate': '2017-04-10T16:26:16.998Z',
     'revisionNumber': 2.0,
     'status': 'historical',
     'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                'id': '58de1d1c07637a0264c0ca6a',
                'name': 'admin'},
     'version': {'$type': 'Core.Models.Record.Record, Core',
                 'actionsExecuted': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e557c8b81ce3e2c6515fd1': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.389Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6ac5c88412c4acda3d66c': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.396Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6aca5293267c35188ea37': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.401Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6acc099097a98678ccfcf': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.407Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c62f257f2c4994b84140': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.412Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c6536afac95743437254': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.419Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c83415177d0ad68ea961': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.426Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e7bb9ad6e4d34e8f557b2b': True,
                     '58e7bbba9bc82babdd655653': True,
                     '58e7bd86ad9ba1f93ef4afae': True,
                     '58e7bddc6ed1ceda2950b621': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.437Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}}},
                 'allowed': [],
                 'applicationId': '58e4bb4407637a0e4c4f9873',
                 'applicationRevision': 72.0,
                 'comments': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'},
                 'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                   'id': '58de1d1c07637a0264c0ca6a',
                                   'name': 'admin'},
                 'createdDate': '2017-04-10T16:26:16.486Z',
                 'disabled': False,
                 'id': '58ebb22807637a02d4a14bd6',
                 'isNew': False,
                 'linkedData': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     'a99ut': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017},
                     'ac1oa': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 5,
                               'dow': 3,
                               'h': 23,
                               'm': 42,
                               'mm': 4,
                               'q': 2,
                               'w': 14,
                               'y': 2017},
                     'aiir8': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017}},
                 'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'},
                 'modifiedDate': '2017-04-10T16:26:16.954Z',
                 'referencedByIds': [],
                 'referencedRecordIds': [],
                 'sessionTimeSpent': 0,
                 'timeTrackingEnabled': True,
                 'totalTimeSpent': 0,
                 'trackingFull': 'RA-7',
                 'trackingId': 7.0,
                 'values': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e4bb4407637a0e4c4f9875': 'RA-7',
                     'a04rv': '10.0.1.184:56005:3172',
                     'a0g40': 'Alert Action',
                     'a0k7v': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bae8c61082e377cc4d82',
                               'value': 'Open'},
                     'a18qr': 'User.Activity.Failed Logins',
                     'a1r3v': 'Logon',
                     'a3rvw': '3172',
                     'a4l9p': 'logdec1',
                     'a5v09': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bafd83f418637cf91c3e',
                               'value': 'ESA Alert'},
                     'a5yg3': '3172',
                     'a7gm5': '<14>Apr  5 23:42:54 localhost CEF:0|RSA|Security Analytics ESA|10.4|Module_58e40ea9e4b070dfd2a59ad5_Alert|Alert Action|7|rt=2017-04-05T23:42Z id=890eb2b1-2d90-46a5-b1ed-6e58b408ed83 source=10.0.1.184:56005:3172  action=authentication failure;; client=sshd;; device_class=Unix;; device_ip=10.0.1.178;; device_type=crossbeamc;; did=logdec1;; ec_activity=Logon;; ec_outcome=Failure;; ec_subject=User;; ec_theme=Authentication;; esa_time=1491435774280;; event_cat_name=User.Activity.Failed Logins;; event_source_id=10.0.1.184:56005:3172;; header_id=0006;; host_src=178.238.235.143;; level=4;; medium=32;; msg_id=000103;; rid=3172;; sessionid=3172;; size=175;; time=1491435771;; user_dst=user;; username=0;;\x00',
                     'a7ira': 'User',
                     'a8vjm': 'Failure',
                     'a990o': '7',
                     'a99ut': '2017-04-10T16:26:17.457Z',
                     'aasnf': {'$type': 'Core.Models.Record.ValueSelection, Core',
                               'id': '58e7bb144121bd73d8f53845',
                               'value': 'High'},
                     'ac1oa': '2017-04-05T23:42:54Z',
                     'acqdq': '1491435774280',
                     'af967': '890eb2b1-2d90-46a5-b1ed-6e58b408ed83',
                     'afbbv': '',
                     'afff3': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                               'id': '58de1d1c07637a0264c0ca6a',
                               'name': 'admin'},
                     'ahziu': '178.238.235.143',
                     'ai1zz': '4',
                     'aiir8': '2017-04-10T16:26:16.389Z',
                     'aio1w': 'sshd',
                     'aokp5': 'Unix',
                     'apf9i': '10.0.1.178',
                     'arnd6': 'authentication failure',
                     'arok4': 'crossbeamc',
                     'aw9gd': 'ip.src=10.0.1.178 || ip.dst=10.0.1.178',
                     'awmtq': 'Authentication',
                     'axdvr': '175'},
                 'visualizations': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], mscorlib]], mscorlib'}}},
    {'$type': 'Core.Models.History.Revision, Core',
     'modifiedDate': '2017-04-10T16:26:16.953Z',
     'revisionNumber': 1.0,
     'status': 'historical',
     'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                'id': '58de1d1c07637a0264c0ca6a',
                'name': 'admin'},
     'version': {'$type': 'Core.Models.Record.Record, Core',
                 'actionsExecuted': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e557c8b81ce3e2c6515fd1': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.389Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6ac5c88412c4acda3d66c': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.396Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6aca5293267c35188ea37': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.401Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6acc099097a98678ccfcf': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.407Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c62f257f2c4994b84140': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.412Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c6536afac95743437254': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.419Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e6c83415177d0ad68ea961': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.426Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}},
                     '58e7bddc6ed1ceda2950b621': {
                         '$type': 'Core.Models.Workflow.History.ActionHistory, Core',
                         'dateExecuted': '2017-04-10T16:26:16.437Z',
                         'userId': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'}}},
                 'allowed': [],
                 'applicationId': '58e4bb4407637a0e4c4f9873',
                 'applicationRevision': 72.0,
                 'comments': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'},
                 'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                   'id': '58de1d1c07637a0264c0ca6a',
                                   'name': 'admin'},
                 'createdDate': '2017-04-10T16:26:16.486Z',
                 'disabled': False,
                 'id': '58ebb22807637a02d4a14bd6',
                 'isNew': False,
                 'linkedData': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     'a99ut': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017},
                     'aiir8': {'$type': 'Core.Models.Record.DateTimeParsed, Core',
                               'd': 10,
                               'dow': 1,
                               'h': 16,
                               'm': 26,
                               'mm': 4,
                               'q': 2,
                               'w': 15,
                               'y': 2017}},
                 'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                    'id': '58de1d1c07637a0264c0ca6a',
                                    'name': 'admin'},
                 'modifiedDate': '2017-04-10T16:26:16.486Z',
                 'referencedByIds': [],
                 'referencedRecordIds': [],
                 'sessionTimeSpent': 0,
                 'timeTrackingEnabled': True,
                 'totalTimeSpent': 0,
                 'trackingFull': 'RA-7',
                 'trackingId': 7.0,
                 'values': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib',
                     '58e4bb4407637a0e4c4f9875': 'RA-7',
                     'a04rv': '10.0.1.184:56005:3172',
                     'a0g40': 'Alert Action',
                     'a18qr': 'User.Activity.Failed Logins',
                     'a1r3v': 'Logon',
                     'a3rvw': '3172',
                     'a4l9p': 'logdec1',
                     'a5yg3': '3172',
                     'a7gm5': '<14>Apr  5 23:42:54 localhost CEF:0|RSA|Security Analytics ESA|10.4|Module_58e40ea9e4b070dfd2a59ad5_Alert|Alert Action|7|rt=2017-04-05T23:42Z id=890eb2b1-2d90-46a5-b1ed-6e58b408ed83 source=10.0.1.184:56005:3172  action=authentication failure;; client=sshd;; device_class=Unix;; device_ip=10.0.1.178;; device_type=crossbeamc;; did=logdec1;; ec_activity=Logon;; ec_outcome=Failure;; ec_subject=User;; ec_theme=Authentication;; esa_time=1491435774280;; event_cat_name=User.Activity.Failed Logins;; event_source_id=10.0.1.184:56005:3172;; header_id=0006;; host_src=178.238.235.143;; level=4;; medium=32;; msg_id=000103;; rid=3172;; sessionid=3172;; size=175;; time=1491435771;; user_dst=user;; username=0;;\x00',
                     'a7ira': 'User',
                     'a8vjm': 'Failure',
                     'a990o': '7',
                     'a99ut': '2017-04-10T16:26:17.457Z',
                     'acqdq': '1491435774280',
                     'af967': '890eb2b1-2d90-46a5-b1ed-6e58b408ed83',
                     'afbbv': '',
                     'afff3': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                               'id': '58de1d1c07637a0264c0ca6a',
                               'name': 'admin'},
                     'ahziu': '178.238.235.143',
                     'ai1zz': '4',
                     'aiir8': '2017-04-10T16:26:16.389Z',
                     'aio1w': 'sshd',
                     'aokp5': 'Unix',
                     'apf9i': '10.0.1.178',
                     'arnd6': 'authentication failure',
                     'arok4': 'crossbeamc',
                     'aw9gd': 'ip.src=10.0.1.178 || ip.dst=10.0.1.178',
                     'awmtq': 'Authentication',
                     'axdvr': '175'},
                 'visualizations': {
                     '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], mscorlib]], mscorlib'}}}]


def test_history_field(mock_record, mock_swimlane):
    history = mock_record['History']
    assert isinstance(history, RevisionCursor)

    mock_response = mock.MagicMock()
    mock_response.json.return_value = raw_revision_data

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):

        # Get number of revisions
        num_revisions = len(history)
        assert num_revisions == 3

        # Iterate backwards over revisions
        for idx, revision in enumerate(history):
            assert isinstance(revision, Revision)
            assert str(revision) == 'RA-7 ({})'.format(revision.revision_number)
            assert isinstance(revision.modified_date, datetime)
            assert isinstance(revision.user, UserGroup)
            assert revision.version.id == mock_record.id
            assert num_revisions - revision.revision_number == idx

