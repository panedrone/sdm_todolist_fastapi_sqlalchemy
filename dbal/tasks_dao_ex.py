"""

My hand-coded extension of generated class

"""
from sqlalchemy import column

from dbal._tasks_dao import _TasksDao
from dbal.task_li import TaskLi


class TasksDaoEx(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_tasks_by_project(self, p_id):
        q = self.ds.get_query(TaskLi)
        q = q.filter_by(p_id=p_id)
        q = q.order_by(TaskLi.t_date, TaskLi.t_id)
        fields = ['t_id', 't_date', 't_subject', 't_priority']
        entities = [column(f) for f in fields]
        q = q.with_entities(*entities)  # not before filter_by!!!
        tasks = q.all()
        return tasks
