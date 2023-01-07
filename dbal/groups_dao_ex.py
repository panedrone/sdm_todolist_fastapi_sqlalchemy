"""

My hand-coded extension of generated class

"""
from dbal._groups_dao import _GroupsDao
from dbal.group import Group
from dbal.group_li import GroupLi


class GroupsDaoEx(_GroupsDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_all_groups(self):
        return self.ds.get_all_raw(GroupLi)

    def rename(self, g_id, g_name):
        self.ds.update_by_filter(Group, data={'g_name': g_name}, params={'g_id': g_id})
