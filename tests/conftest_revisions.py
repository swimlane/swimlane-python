import pytest

from swimlane.core.resources.app import App
from swimlane.core.resources.app_revision import AppRevision
from swimlane.core.resources.record import Record
from swimlane.core.resources.record_revision import RecordRevision


@pytest.fixture
def mock_revision_app(mock_swimlane):
    """An app with two fields: value selection and history."""
    return App(mock_swimlane, {
        "$type":"Core.Models.Application.Application, Core",
        "acronym":"PHT",
        "trackingFieldId":"5cd46fce433cf20015dd46f7",
        "layout":[
            {
                "$type":"Core.Models.Layouts.FieldLayout, Core",
                "fieldId":"agy01",
                "helpTextType":"none",
                "helpText":" ",
                "layoutType":"field",
                "id":"5cd46fdac741d5d54a2b5c32",
                "row":1,
                "col":1,
                "sizex":2.0,
                "sizey":0.0
            },
            {
                "$type":"Core.Models.Layouts.FieldLayout, Core",
                "fieldId":"axtys",
                "helpTextType":"none",
                "helpText":" ",
                "layoutType":"field",
                "id":"5cd46fddb36d66d467d4abe6",
                "row":1,
                "col":3,
                "sizex":2.0,
                "sizey":0.0
            }
        ],
        "fields":[
            {
                "$type":"Core.Models.Fields.History.HistoryField, Core",
                "id":"axtys",
                "name":"History",
                "key":"history",
                "fieldType":"history",
                "required":False,
                "readOnly":False,
                "supportsMultipleOutputMappings":False
            },
            {
                "$type":"Core.Models.Fields.ValuesListField, Core",
                "values":[
                    {
                        "$type":"Core.Models.Fields.ValuesList.ValuesListValues, Core",
                        "id":"5cd46fe3ca4746cda7e41a33",
                        "name":"value1",
                        "selected":False,
                        "description":"",
                        "otherText":False,
                        "otherTextDescription":"",
                        "otherTextDefaultValue":"",
                        "otherTextRequired":"False"
                    }
                ],
                "controlType":"select",
                "selectionType":"single",
                "id":"agy01",
                "name":"Selection",
                "key":"selection",
                "fieldType":"valuesList",
                "required":False,
                "readOnly":False,
                "supportsMultipleOutputMappings":False
            },
            {
                "$type":"Core.Models.Fields.TrackingField, Core",
                "prefix":"PHT-",
                "id":"5cd46fce433cf20015dd46f7",
                "name":"Tracking Id",
                "key":"tracking-id",
                "fieldType":"tracking",
                "readOnly":True,
                "supportsMultipleOutputMappings":False
            }
        ],
        "maxTrackingId":1.0,
        "workspaces":[
            "5cd46fce433cf20015dd4727"
        ],
        "createWorkspace":False,
        "createdDate":"2019-05-09T18:22:06.181Z",
        "createdByUser":{
            "$type":"Core.Models.Utilities.UserGroupSelection, Core",
            "id":"aBZ3vZmPSsd6l4GLj",
            "name":"admin"
        },
        "modifiedDate":"2019-05-09T18:24:02.642Z",
        "modifiedByUser":{
            "$type":"Core.Models.Utilities.UserGroupSelection, Core",
            "id":"aBZ3vZmPSsd6l4GLj",
            "name":"admin"
        },
        "timeTrackingEnabled":False,
        "permissions":{
            "$type":"Core.Models.Security.PermissionMatrix, Core"
        },
        "id":"a34xbNOoo2P3ivyjY",
        "name":"Pydriver History Test",
        "disabled":False
    })


@pytest.fixture
def mock_revision_record(mock_revision_app):
    """A record from the mock_revision_app."""
    return Record(mock_revision_app, {
        "$type":"Core.Models.Record.Record, Core",
        "name":"PHT-1",
        "allowed":[

        ],
        "trackingId":1.0,
        "trackingFull":"PHT-1",
        "applicationId":"a34xbNOoo2P3ivyjY",
        "isNew":False,
        "values":{
            "$type":"System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
            "agy01":{
                "$type":"Core.Models.Record.ValueSelection, Core",
                "id":"5cd46fe3ca4746cda7e41a33",
                "value":"value1"
            },
            "5cd46fce433cf20015dd46f7":"PHT-1"
        },
        "repeatFieldCurrentValues":{
            "$type":"System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
        },
        "actionsExecuted":{
            "$type":"System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
        },
        "visualizations":{
            "$type":"System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], System.Private.CoreLib]], System.Private.CoreLib"
        },
        "applicationRevision":3.0,
        "locked":False,
        "comments":{
            "$type":"System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], System.Private.CoreLib]], System.Private.CoreLib"
        },
        "createdDate":"2019-05-09T18:23:39.881Z",
        "modifiedDate":"2019-05-09T18:24:20.027Z",
        "createdByUser":{
            "$type":"Core.Models.Utilities.UserGroupSelection, Core",
            "id":"aBZ3vZmPSsd6l4GLj",
            "name":"admin"
        },
        "modifiedByUser":{
            "$type":"Core.Models.Utilities.UserGroupSelection, Core",
            "id":"aBZ3vZmPSsd6l4GLj",
            "name":"admin"
        },
        "sessionTimeSpent":0,
        "totalTimeSpent":0,
        "timeTrackingEnabled":True,
        "isHangfireCreatedAndUnpersisted":False,
        "infiniteLoopFlag":False,
        "id":"aPkMtjrzV54YxyS59",
        "disabled":False
    })


@pytest.fixture
def raw_record_revision_data():
    """Raw record revision data for mock_revision_record."""
    return [
        {
            "$type": "Core.Models.History.Revision, Core",
            "revisionNumber": 3.0,
            "status": "current",
            "userId": {
                "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                "id": "aBZ3vZmPSsd6l4GLj",
                "name": "admin"
            },
            "modifiedDate": "2019-05-09T18:24:20.027Z",
            "version": {
                "$type": "Core.Models.Record.Record, Core",
                "name": "PHT-1",
                "allowed": [

                ],
                "trackingId": 1.0,
                "trackingFull": "PHT-1",
                "applicationId": "a34xbNOoo2P3ivyjY",
                "referencedRecordIds": [

                ],
                "referencedByIds": [

                ],
                "isNew": False,
                "values": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
                    "agy01": {
                        "$type": "Core.Models.Record.ValueSelection, Core",
                        "id": "5cd46fe3ca4746cda7e41a33",
                        "value": "value1"
                    },
                    "5cd46fce433cf20015dd46f7": "PHT-1"
                },
                "repeatFieldCurrentValues": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "valuesDocument": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
                    "agy01": {
                        "$type": "Core.Models.Record.ValueSelection, Core",
                        "id": "5cd46fe3ca4746cda7e41a33",
                        "value": "value1"
                    },
                    "5cd46fce433cf20015dd46f7": "PHT-1"
                },
                "actionsExecuted": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "visualizations": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "applicationRevision": 3.0,
                "locked": False,
                "comments": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "createdDate": "2019-05-09T18:23:39.881Z",
                "modifiedDate": "2019-05-09T18:24:20.027Z",
                "createdByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "modifiedByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "sessionTimeSpent": 0,
                "totalTimeSpent": 0,
                "timeTrackingEnabled": True,
                "isHangfireCreatedAndUnpersisted": False,
                "infiniteLoopFlag": False,
                "id": "aPkMtjrzV54YxyS59",
                "disabled": False
            }
        },
        {
            "$type": "Core.Models.History.Revision, Core",
            "revisionNumber": 2.0,
            "status": "historical",
            "userId": {
                "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                "id": "aBZ3vZmPSsd6l4GLj",
                "name": "admin"
            },
            "modifiedDate": "2019-05-09T18:23:48.539Z",
            "version": {
                "$type": "Core.Models.Record.Record, Core",
                "name": "PHT-1",
                "allowed": [

                ],
                "trackingId": 1.0,
                "trackingFull": "PHT-1",
                "applicationId": "a34xbNOoo2P3ivyjY",
                "referencedRecordIds": [

                ],
                "referencedByIds": [

                ],
                "isNew": False,
                "values": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
                    "agy01": {
                        "$type": "Core.Models.Record.ValueSelection, Core",
                        "id": "5cd46fe379be68acd2039061",
                        "value": "value2"
                    },
                    "5cd46fce433cf20015dd46f7": "PHT-1"
                },
                "repeatFieldCurrentValues": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "actionsExecuted": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "visualizations": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "applicationRevision": 2.0,
                "locked": False,
                "comments": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "createdDate": "2019-05-09T18:23:39.881Z",
                "modifiedDate": "2019-05-09T18:23:48.539Z",
                "createdByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "modifiedByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "sessionTimeSpent": 0,
                "totalTimeSpent": 0,
                "timeTrackingEnabled": True,
                "isHangfireCreatedAndUnpersisted": False,
                "infiniteLoopFlag": False,
                "id": "aPkMtjrzV54YxyS59",
                "disabled": False
            }
        },
        {
            "$type": "Core.Models.History.Revision, Core",
            "revisionNumber": 1.0,
            "status": "historical",
            "userId": {
                "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                "id": "aBZ3vZmPSsd6l4GLj",
                "name": "admin"
            },
            "modifiedDate": "2019-05-09T18:23:39.881Z",
            "version": {
                "$type": "Core.Models.Record.Record, Core",
                "name": "PHT-1",
                "allowed": [

                ],
                "trackingId": 1.0,
                "trackingFull": "PHT-1",
                "applicationId": "a34xbNOoo2P3ivyjY",
                "referencedRecordIds": [

                ],
                "referencedByIds": [

                ],
                "isNew": False,
                "values": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
                    "agy01": {
                        "$type": "Core.Models.Record.ValueSelection, Core",
                        "id": "5cd46fe302c8ff905e042cc0",
                        "value": "value3"
                    },
                    "5cd46fce433cf20015dd46f7": "PHT-1"
                },
                "repeatFieldCurrentValues": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "actionsExecuted": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib"
                },
                "visualizations": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "applicationRevision": 2.0,
                "locked": False,
                "comments": {
                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], System.Private.CoreLib]], System.Private.CoreLib"
                },
                "createdDate": "2019-05-09T18:23:39.881Z",
                "modifiedDate": "2019-05-09T18:23:39.881Z",
                "createdByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "modifiedByUser": {
                    "$type": "Core.Models.Utilities.UserGroupSelection, Core",
                    "id": "aBZ3vZmPSsd6l4GLj",
                    "name": "admin"
                },
                "sessionTimeSpent": 0,
                "totalTimeSpent": 0,
                "timeTrackingEnabled": True,
                "isHangfireCreatedAndUnpersisted": False,
                "infiniteLoopFlag": False,
                "id": "aPkMtjrzV54YxyS59",
                "disabled": False
            }
        }
    ]


@pytest.fixture
def mock_record_revisions(mock_revision_app, raw_record_revision_data):
    """All record revisions for mock_revision_record."""
    return [RecordRevision(mock_revision_app, raw) for raw in raw_record_revision_data]


@pytest.fixture
def raw_app_revision_data():
    """Raw app revision data for mock_revision_app"""
    return [
        {
            "$type":"Core.Models.History.Revision, Core",
            "revisionNumber":3.0,
            "status":"current",
            "userId":{
                "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                "id":"aBZ3vZmPSsd6l4GLj",
                "name":"admin"
            },
            "modifiedDate":"2019-05-09T18:24:02.642Z",
            "version":{
                "$type":"Core.Models.Application.Application, Core",
                "acronym":"PHT",
                "trackingFieldId":"5cd46fce433cf20015dd46f7",
                "layout":[
                    {
                        "$type":"Core.Models.Layouts.FieldLayout, Core",
                        "fieldId":"agy01",
                        "helpTextType":"none",
                        "helpText":" ",
                        "layoutType":"field",
                        "id":"5cd46fdac741d5d54a2b5c32",
                        "row":1,
                        "col":1,
                        "sizex":2.0,
                        "sizey":0.0
                    },
                    {
                        "$type":"Core.Models.Layouts.FieldLayout, Core",
                        "fieldId":"axtys",
                        "helpTextType":"none",
                        "helpText":" ",
                        "layoutType":"field",
                        "id":"5cd46fddb36d66d467d4abe6",
                        "row":1,
                        "col":3,
                        "sizex":2.0,
                        "sizey":0.0
                    }
                ],
                "fields":[
                    {
                        "$type":"Core.Models.Fields.History.HistoryField, Core",
                        "id":"axtys",
                        "name":"History",
                        "key":"history",
                        "fieldType":"history",
                        "required":False,
                        "readOnly":False,
                        "supportsMultipleOutputMappings":False
                    },
                    {
                        "$type":"Core.Models.Fields.ValuesListField, Core",
                        "values":[
                            {
                                "$type":"Core.Models.Fields.ValuesList.ValuesListValues, Core",
                                "id":"5cd46fe3ca4746cda7e41a33",
                                "name":"value1",
                                "selected":False,
                                "description":"",
                                "otherText":False,
                                "otherTextDescription":"",
                                "otherTextDefaultValue":"",
                                "otherTextRequired":"False"
                            }
                        ],
                        "controlType":"select",
                        "selectionType":"single",
                        "id":"agy01",
                        "name":"Selection",
                        "key":"selection",
                        "fieldType":"valuesList",
                        "required":False,
                        "readOnly":False,
                        "supportsMultipleOutputMappings":False
                    },
                    {
                        "$type":"Core.Models.Fields.TrackingField, Core",
                        "prefix":"PHT-",
                        "id":"5cd46fce433cf20015dd46f7",
                        "name":"Tracking Id",
                        "key":"tracking-id",
                        "fieldType":"tracking",
                        "readOnly":True,
                        "supportsMultipleOutputMappings":False
                    }
                ],
                "maxTrackingId":1.0,
                "workspaces":[

                ],
                "createWorkspace":False,
                "createdDate":"2019-05-09T18:22:06.181Z",
                "createdByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "modifiedDate":"2019-05-09T18:24:02.642Z",
                "modifiedByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "timeTrackingEnabled":False,
                "id":"a34xbNOoo2P3ivyjY",
                "name":"Pydriver History Test",
                "disabled":False
            }
        },
        {
            "$type":"Core.Models.History.Revision, Core",
            "revisionNumber":2.0,
            "status":"historical",
            "userId":{
                "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                "id":"aBZ3vZmPSsd6l4GLj",
                "name":"admin"
            },
            "modifiedDate":"2019-05-09T18:23:08.766Z",
            "version":{
                "$type":"Core.Models.Application.Application, Core",
                "acronym":"PHT",
                "trackingFieldId":"5cd46fce433cf20015dd46f7",
                "layout":[
                    {
                        "$type":"Core.Models.Layouts.FieldLayout, Core",
                        "fieldId":"agy01",
                        "helpTextType":"none",
                        "helpText":" ",
                        "layoutType":"field",
                        "id":"5cd46fdac741d5d54a2b5c32",
                        "row":1,
                        "col":1,
                        "sizex":2.0,
                        "sizey":0.0
                    },
                    {
                        "$type":"Core.Models.Layouts.FieldLayout, Core",
                        "fieldId":"axtys",
                        "helpTextType":"none",
                        "helpText":" ",
                        "layoutType":"field",
                        "id":"5cd46fddb36d66d467d4abe6",
                        "row":1,
                        "col":3,
                        "sizex":2.0,
                        "sizey":0.0
                    }
                ],
                "fields":[
                    {
                        "$type":"Core.Models.Fields.ValuesListField, Core",
                        "values":[
                            {
                                "$type":"Core.Models.Fields.ValuesList.ValuesListValues, Core",
                                "id":"5cd46fe3ca4746cda7e41a33",
                                "name":"value1",
                                "selected":False,
                                "description":"",
                                "otherText":False,
                                "otherTextDescription":"",
                                "otherTextDefaultValue":"",
                                "otherTextRequired":"False"
                            },
                            {
                                "$type":"Core.Models.Fields.ValuesList.ValuesListValues, Core",
                                "id":"5cd46fe379be68acd2039061",
                                "name":"value2",
                                "selected":False,
                                "description":"",
                                "otherText":False,
                                "otherTextDescription":"",
                                "otherTextDefaultValue":"",
                                "otherTextRequired":"False"
                            },
                            {
                                "$type":"Core.Models.Fields.ValuesList.ValuesListValues, Core",
                                "id":"5cd46fe302c8ff905e042cc0",
                                "name":"value3",
                                "selected":False,
                                "description":"",
                                "otherText":False,
                                "otherTextDescription":"",
                                "otherTextDefaultValue":"",
                                "otherTextRequired":"False"
                            }
                        ],
                        "controlType":"select",
                        "selectionType":"single",
                        "id":"agy01",
                        "name":"Selection",
                        "key":"selection",
                        "fieldType":"valuesList",
                        "required":False,
                        "readOnly":False,
                        "supportsMultipleOutputMappings":False
                    },
                    {
                        "$type":"Core.Models.Fields.History.HistoryField, Core",
                        "id":"axtys",
                        "name":"History",
                        "key":"history",
                        "fieldType":"history",
                        "required":False,
                        "readOnly":False,
                        "supportsMultipleOutputMappings":False
                    },
                    {
                        "$type":"Core.Models.Fields.TrackingField, Core",
                        "prefix":"PHT-",
                        "id":"5cd46fce433cf20015dd46f7",
                        "name":"Tracking Id",
                        "key":"tracking-id",
                        "fieldType":"tracking",
                        "readOnly":True,
                        "supportsMultipleOutputMappings":False
                    }
                ],
                "maxTrackingId":1.0,
                "workspaces":[

                ],
                "createWorkspace":False,
                "createdDate":"2019-05-09T18:22:06.181Z",
                "createdByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "modifiedDate":"2019-05-09T18:23:08.766Z",
                "modifiedByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "timeTrackingEnabled":False,
                "id":"a34xbNOoo2P3ivyjY",
                "name":"Pydriver History Test",
                "disabled":False
            }
        },
        {
            "$type":"Core.Models.History.Revision, Core",
            "revisionNumber":1.0,
            "status":"historical",
            "userId":{
                "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                "id":"aBZ3vZmPSsd6l4GLj",
                "name":"admin"
            },
            "modifiedDate":"2019-05-09T18:22:06.181Z",
            "version":{
                "$type":"Core.Models.Application.Application, Core",
                "acronym":"PHT",
                "trackingFieldId":"5cd46fce433cf20015dd46f7",
                "layout":[

                ],
                "fields":[
                    {
                        "$type":"Core.Models.Fields.TrackingField, Core",
                        "prefix":"PHT-",
                        "id":"5cd46fce433cf20015dd46f7",
                        "name":"Tracking Id",
                        "key":"tracking-id",
                        "fieldType":"tracking",
                        "readOnly":True,
                        "supportsMultipleOutputMappings":False
                    }
                ],
                "maxTrackingId":0.0,
                "workspaces":[

                ],
                "createWorkspace":False,
                "createdDate":"2019-05-09T18:22:06.181Z",
                "createdByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "modifiedDate":"2019-05-09T18:22:06.181Z",
                "modifiedByUser":{
                    "$type":"Core.Models.Utilities.UserGroupSelection, Core",
                    "id":"aBZ3vZmPSsd6l4GLj",
                    "name":"admin"
                },
                "timeTrackingEnabled":False,
                "id":"a34xbNOoo2P3ivyjY",
                "name":"Pydriver History Test",
                "disabled":False
            }
        }
    ]

@pytest.fixture
def mock_app_revisions(mock_swimlane, raw_app_revision_data):
    """All record revisions for mock_revision_record."""
    return [AppRevision(mock_swimlane, raw) for raw in raw_app_revision_data]
