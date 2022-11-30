"""

My hand-coded extension of generated class

"""
from dbal._tasks_dao import _TasksDao
from dbal.task import Task


class TasksDaoEx(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_tasks_by_group(self, g_id):
        tasks = self.ds.filter(Task, {'g_id': g_id}).order_by(Task.t_date, Task.t_id).all()
        return tasks

    def update_task(self, t_id, data: dict):
        self.ds.update_by_filter(Task, data, {'t_id': t_id})
