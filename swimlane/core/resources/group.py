from swimlane.core.resources.base import APIResourceAdapter, APIResource


class GroupAdapter(APIResourceAdapter):

    def list(self):
        response = self._swimlane.request('get', 'groups')
        return [Group(self._swimlane, raw_group_data) for raw_group_data in response.json().get('groups', [])]

    def get(self, group_id=None, name=None):
        """Retrieve single group record"""
        if group_id is None and name is None:
            raise ValueError('Must provide either group_id or name')

        if group_id:
            response = self._swimlane.request('get', 'groups/{}'.format(group_id))
            return Group(self._swimlane, response.json())

        else:
            response = self._swimlane.request('get', 'groups/lookup?name={}'.format(name))
            matched_groups = response.json()

            for group_data in matched_groups:
                if group_data.get('name') == name:
                    return Group(self._swimlane, group_data)
            else:
                raise ValueError('Unable to find group with name "{}"'.format(name))


class Group(APIResource):
    """A class for working with Swimlane groups"""

    _type = 'Core.Models.Groups.Group, Core'
