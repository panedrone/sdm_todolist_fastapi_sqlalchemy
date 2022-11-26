"""

My hand-coded extension of generated class

"""
from dbal.group import Group
from dbal._groups_dao import _GroupsDao


class GroupsDaoEx(_GroupsDao):

    def __init__(self, ds):
        super().__init__(ds)

    def rename(self, g_id, g_name):
        self.ds.filter(Group, {'g_id': g_id}).update(values={'g_name': g_name})
