"""

My hand-coded extension of generated class

"""

from dbal._tasks_dao import _TasksDao
from dbal.task_li import TaskLi


class TasksDaoEx(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_project_tasks(self, p_id):
        q = self.ds.get_query(TaskLi)
        q = q.filter_by(p_id=p_id)
        q = q.order_by(TaskLi.t_date, TaskLi.t_id)
        q = q.with_entities(TaskLi.t_id, TaskLi.t_date, TaskLi.t_subject, TaskLi.t_priority)  # not before filter_by!!!
        tasks = q.all()
        return tasks
