"""

My hand-coded extension of generated class

"""
from dbal._projects_dao import _ProjectsDao
from dbal.project import Project
from dbal.project_li import ProjectLi


class ProjectsDao(_ProjectsDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_all_projects(self):
        return self.ds.get_all_raw(ProjectLi)

    def rename_project(self, p_id, p_name):
        self.ds.update_by_filter(Project, data={'p_name': p_name}, params={'p_id': p_id})
