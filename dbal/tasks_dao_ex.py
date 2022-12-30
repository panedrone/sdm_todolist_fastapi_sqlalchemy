"""

My hand-coded extension of generated class

"""
from dbal._tasks_dao import _TasksDao
from dbal.task_li import TaskLI


class TasksDaoEx(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_tasks_by_group(self, g_id):
        fields = ['t_id', 't_date', 't_subject', 't_priority']
        params = {'g_id': g_id}
        tasks = self.ds.filter(TaskLI, params, fields).order_by(TaskLI.t_date, TaskLI.t_id).all()
        return tasks
