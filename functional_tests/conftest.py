import pytest
import json
import random
import string
import time
import sys
from swimlane import Swimlane
from faker import Faker
from io import BytesIO

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

pytest.fake = Faker()
file_path = str(Path(__file__).parent)

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://localhost",
                     help="By default: https://localhost")
    parser.addoption("--user", action="store",
                     default="admin", help="By default: admin")
    parser.addoption("--pass", action="store",
                     help="Password to log in as the supplied user")
    parser.addoption("--skipverify", action="store_false",
                     help="pass in to not verify the server version with the pydriver version")
    parser.addini("url", help="By default: https://localhost")
    parser.addini("user", help="By default: admin")
    parser.addini("pass", help="Password to log in as the supplied user")
    parser.addini("skipverify", help="pass in to not verify the server version with the pydriver version")


def api_url(pytestconfig):
    ini_option = pytestconfig.getini('url')
    if len(ini_option) > 0:
        return ini_option
    return pytestconfig.getoption("--url")


def api_user(pytestconfig):
    ini_option = pytestconfig.getini('user')
    if len(ini_option) > 0:
        return ini_option
    return pytestconfig.getoption("--user").lower()


def api_pass(pytestconfig):
    ini_option = pytestconfig.getini('pass')
    if len(ini_option) > 0:
        return ini_option  
    return pytestconfig.getoption("--pass")


def api_verifyVersion(pytestconfig):
    ini_option = pytestconfig.getini('skipverify')
    if len(ini_option) > 0:
        return ini_option
    return pytestconfig.getoption("--skipverify")


class Helpers:
    def __init__(self, pytestconfig, write_to_read_only=False):
        self.appIds = []
        self.userIds = []
        self.groupIds = []
        self.roleIds = []
        self.userDispNames = []
        self.groupNames = []
        self.appPairings = {'Email Collection': 'Other App', 'Helpers Source App': 'Helpers Target App',
                            'one of each type': 'target ref app', 'basic fields app': 'Helpers Target App'}
        self.url = api_url(pytestconfig)
        self.userName = api_user(pytestconfig)
        self.password = api_pass(pytestconfig)
        self.verifyVersion = api_verifyVersion(pytestconfig)
        self.swimlane_instance = self.open_swimlane_instance(
            self.url, self.userName, self.password, self.verifyVersion)

    def reconnect_swimlane(self, user=None, password=None, write_to_read_only=False):

        return self.open_swimlane_instance(self.url, user or self.userName, password or self.password, self.verifyVersion, write_to_read_only)

    def open_swimlane_instance(self, url, user, password, verifyVersion, write_to_read_only=False):
        print ('\nINITIALIZATION\n')
        print ('Version Verification check: %s\n' % verifyVersion)
        return Swimlane(url, user,  password, verify_ssl=False, verify_server_version=verifyVersion, write_to_read_only=write_to_read_only)

    def findCreateApp(self, defaultApp):
        appId = ""
        app = ""
        refFieldData = None
        try:
            app = self.swimlane_instance.apps.get(
                name="PYTHON-%s" % defaultApp)
            print ("App found without issues.")
            return app, appId
        except ValueError as E:
            if (str(E).startswith('No app with name')):
                self.createUserGroupsForApp(defaultApp)
                if (defaultApp in self.appPairings):
                    dependentApp = self.appPairings[defaultApp]
                    modifications = [{'field': "name", 'value': "PYTHON-%s" % dependentApp, 'type': "create"}, {'field': "acronym", 'value': generateUniqueAcronym(
                        self.swimlane_instance), 'type': 1}, {'field': "description", 'value': pytest.fake.sentence(), 'type': 1}]
                    with open('{file_path}/apps/{dependentApp}.json'.format(file_path=file_path, dependentApp=dependentApp)) as json_data:
                        manifest = json.load(json_data)
                    newapp = self.swimlane_instance.request(
                        'post', 'app/import', json={"manifest": manifest, "modifications": modifications}).json()
                    refFieldData = getAppIdsForRefField(newapp['application'])
                    self.appIds.append(newapp['application']['id'])
                modifications = [{'field': "name", 'value': "PYTHON-%s" % defaultApp, 'type': "create"}, {'field': "acronym", 'value': generateUniqueAcronym(
                    self.swimlane_instance), 'type': 1}, {'field': "description", 'value': pytest.fake.sentence(), 'type': 1}]
                with open('{file_path}/apps/{defaultApp}.json'.format(file_path=file_path, defaultApp=defaultApp)) as json_data:
                    manifest = json.load(json_data)
                if 'Application' in manifest:
                    manifest['Application']['Fields'] = updateRefField(
                        manifest['Application']['Fields'], refFieldData)
                else:
                    manifest['application']['fields'] = updateRefFieldNew(
                        manifest['application']['fields'], refFieldData)
                if ((pytest.groupsCreated != {}) or (pytest.usersCreated != {})):
                    print("Need to fix IDs")
                    manifest['application']['fields'] = updateUserGroupFields(
                        manifest['application']['fields'])
                newapp = self.swimlane_instance.request(
                    'post', 'app/import', json={"manifest": manifest, "modifications": modifications}).json()
                defaultApp = newapp['application']['name']
                self.appIds.append(newapp['application']['id'])
                appId = newapp['application']['id']
                app = self.swimlane_instance.apps.get(name=defaultApp)
                return app, appId
            else:
                print(str(E))
                return app, appId
    
    def import_content(self, file_name):
        with open('{file_path}/content/{file_name}'.format(file_name=file_name, file_path=file_path), 'rb') as file_handle:
            file_stream = file_handle.read()
        bytes_stream = BytesIO(file_stream)
        file = {
            'file': (file_name, bytes_stream, 'application/octet-stream')
        }
        data = {
            'runInBackground': False
        }
        tracking_id = self.swimlane_instance.request('post', 'content/import', files=file, data=data).text
        response = self.swimlane_instance.request('get', 'content/import/%s/status' % tracking_id).json()
        if response.get('state') == 'Success':
            for app in response.get('entities').get('application'):
                self.appIds.append(app.get('id'))
        else:
            print('Failed to import: {}'.format(response.get('errors')))
        

    def createUser(self, username='', groups=None, roles=None):
        password = pytest.fake.password()
        firstName = pytest.fake.first_name()
        lastName = pytest.fake.last_name()
        displayName = 'PYTHON-%s' % username if username != '' else (
            lastName + ', ' + firstName)

        user = {
            'userName': username if username != '' else 'python%s' % pytest.fake.user_name(),
            'notify': False,
            'email': pytest.fake.email(),
            'password': password,
            'confirmPassword': password,
            'groups': groups if groups != None else [],
            'roles': roles if roles != None else [],
            'firstName': firstName,
            'lastName': lastName,
            'middleInitial': random.choice(string.ascii_lowercase),
            'displayName': displayName
        }
        newUser = self.swimlane_instance.request(
            'post', 'user', json=user).json()
        newUser['password'] = password
        self.userIds.append(newUser['id'])
        self.userDispNames.append(newUser['displayName'])
        return newUser

    def createGroup(self, name=None, groups=None, roles=None, users=None):
        group = {
            'description': pytest.fake.sentence(),
            'disabled': False,
            'groups': groups if groups != None else [],
            'name': ("PYTHON-%s" % (name or pytest.fake.bs()))[:128],
            'roles': roles if roles != None else [],
            'users': users if users != None else []
        }
        newGroup = self.swimlane_instance.request(
            'post', 'groups', json=group).json()
        self.groupIds.append(newGroup['id'])
        self.groupNames.append(newGroup['name'])
        return newGroup

    def createRole(self, name=None, groups=None, users=None, sections=None):
        if sections is None:
            sections = ['Application', 'Report', 'Workspace',
                        'Dashboard', 'Applet', 'Settings']
        globalPerms = self.swimlane_instance.request('get', 'global').json()
        rolePermissions = {
            "$type": "Core.Models.Security.PermissionMatrix, Core"}
        for eachPerm in globalPerms:
            if eachPerm['name'] in sections:
                rolePermissions[eachPerm['id']] = {
                    "type": "Global",
                    "id": eachPerm['id'],
                    "name": eachPerm['name'],
                    "access": 15311 if eachPerm['name'] == 'Application' else 2063 if eachPerm['name'] == 'Applet' else 15,
                    "fields": {}

                }
        roleJSON = {
            "permissions": rolePermissions,
            "groups": groups if groups != None else [],
            "users": users if users != None else [],
            "name": 'PYTHON-%s' % (name or pytest.fake.color_name()),
            "disabled": False,
            "description": pytest.fake.sentence()
        }

        newRole = self.swimlane_instance.request(
            'post', 'roles', json=roleJSON).json()
        self.roleIds.append(newRole['id'])
        return newRole

    def waitOnJobByID(self, jobId):
        while True:
            loggingStuff = self.swimlane_instance.helpers.check_bulk_job_status(
                jobId)
            if (True in (ele['status'] == 'completed' for ele in loggingStuff)):
                break
            else:
                time.sleep(0.1)

    def updateApp(self, appID):
        newapp = self.swimlane_instance.request('get', 'app/%s' % appID).json()
        newapp['description'] = pytest.fake.sentence()
        self.swimlane_instance.request(
            'put', 'app/%s' % appID, json=newapp).json()
        return self.swimlane_instance.apps.get(id=appID)

    def cleanupData(self):
        dashboardsList = []
        workspacesList = []
        for eachApp in self.appIds:
            print ("Removing app with ID: %s" % eachApp)
            for eachWorkspace in self.swimlane_instance.request('get', 'workspaces/app/%s' % eachApp).json():
                workspacesList.append(eachWorkspace['id'])
                dashboardsList += eachWorkspace['dashboards']
            self.swimlane_instance.request('delete', 'app/%s' % eachApp)
        for eachUser in self.userIds:
            print ("Removing user with ID: %s" % eachUser)
            self.swimlane_instance.request('delete', 'user/%s' % eachUser)
        for eachGroup in self.groupIds:
            print ("Removing group with ID: %s" % eachGroup)
            self.swimlane_instance.request('delete', 'groups/%s' % eachGroup)
        for eachRole in self.roleIds:
            print ("Removing role with ID: %s" % eachRole)
            self.swimlane_instance.request('delete', 'roles/%s' % eachRole)
        dashboardsList = list(set(dashboardsList))
        for eachDashbaord in dashboardsList:
            print ("Removing dashboard with ID: %s" % eachDashbaord)
            self.swimlane_instance.request(
                'delete', 'dashboard/%s' % eachDashbaord)
        workspacesList = list(set(workspacesList))
        for eachWorkspace in workspacesList:
            print ("Removing workspace with ID: %s" % eachWorkspace)
            self.swimlane_instance.request(
                'delete', 'workspaces/%s' % eachWorkspace)
        self.appIds = []
        self.userIds = []
        self.groupIds = []
        self.roleIds = []

    def createUserGroupsForApp(self, appName):
        pytest.groupsCreated = {}
        pytest.usersCreated = {}
        try:
            with open('{file_path}/apps/{appName}.relations.json'.format(file_path=file_path, appName=appName)) as json_data:
                usersGroups = json.load(json_data)
                for eachGroup in usersGroups['groups']:
                    new_groups = [i for i in map(lambda arg: {"$type": "Core.Models.Base.Entity, Core", "id":  pytest.groupsCreated['PYTHON-%s' %
                                                                                                                                    arg[1]], "name": 'PYTHON-%s' % arg[1], "disabled": False}, enumerate(eachGroup['groups']))]
                    newGroup = self.createGroup(
                        name=eachGroup['name'], groups=new_groups, roles=eachGroup['roles'], users=eachGroup['users'])
                    pytest.groupsCreated[newGroup['name']] = newGroup['id']
                for eachUser in usersGroups['users']:
                    user_groups = [i for i in map(lambda arg: {"$type": "Core.Models.Base.Entity, Core", "id":  pytest.groupsCreated['PYTHON-%s' %
                                                                                                                                     arg[1]], "name": 'PYTHON-%s' % arg[1], "disabled": False}, enumerate(eachUser['groups']))]
                    newUser = self.createUser(
                        username=eachUser['name'], groups=user_groups, roles=eachUser['roles'])
                    pytest.usersCreated[newUser['displayName']] = newUser['id']
        except IOError:
            print('No users or groups to create')

    def loadFileStream(self, filename):
        with open('{file_path}/fixtures/{filename}'.format(file_path=file_path, filename=filename), 'rb') as file_handle:
            data = file_handle.read()
        return BytesIO(data)

    def py_ver_string_type(self):
        if self.py_ver() == 2:
            return "<type 'unicode'>"
        else:
            return "<class 'str'>"

    def py_ver_missing_param(self, expCount, actCount, missingName, comparison="at least"):
        if self.py_ver() == 2:
            return 'takes {} {} arguments ({} given)'.format(comparison, expCount, actCount)
        else:
            return "missing 1 required positional argument: '{}'".format(missingName)

    def py_ver_uni_str(self, value):
        return "{}'{}'".format(("", "u")[self.py_ver() == 2], value)

    def py_ver_no_json(self):
        if self.py_ver() == 2:
            return "No JSON object could be decoded"
        else:
            return "Expecting value: line 1 column 1 (char 0)"

    def py_ver(self):
        return sys.version_info[0]


@pytest.fixture(scope='session')
def helpers(pytestconfig):
    helpersInstance = Helpers(pytestconfig)
    yield helpersInstance


def updateRefField(fieldsJSON, targetIds):
    if targetIds != None:
        targetApp = list(targetIds.keys())[0]
        for eachField in fieldsJSON:
            if (eachField['FieldType'] == 8):
                eachField['TargetId'] = targetApp
                eachField['Columns'] = targetIds[targetApp]
    return fieldsJSON


def updateRefFieldNew(fieldsJSON, targetIds):
    if targetIds != None:
        targetApp = list(targetIds.keys())[0]
        for eachField in fieldsJSON:
            if ((eachField['fieldType'] == 8) or (eachField['fieldType'] == "reference")):
                eachField['targetId'] = targetApp
                eachField['columns'] = targetIds[targetApp]
    return fieldsJSON


def getAppIdsForRefField(appJSON):
    returnData = {}
    fieldIds = []
    for field in appJSON['fields']:
        fieldIds.append(field['id'])
    returnData[appJSON['id']] = fieldIds
    return returnData


def generateUniqueAcronym(swim_instance):
    acronymsList = [str(x.acronym) for x in swim_instance.apps.list()]
    acronym = ''
    while True:
        acronym = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        if acronym not in acronymsList:
            break
    return acronym


def updateUserGroupFields(fields):
    for eachField in fields:
        if "members" in eachField.keys():
            for eachMember in eachField["members"]:
                name = eachMember['name'][eachMember['name'].find("PYTHON-"):]
                if (eachMember['itemType'] == "group") or ((eachMember['itemType'] == "user") and (eachMember['selectionType'] == "members")):
                    eachMember['id'] = pytest.groupsCreated[name]
                elif (eachMember['itemType'] == "user"):
                    eachMember['id'] = pytest.usersCreated[name]
    return fields
