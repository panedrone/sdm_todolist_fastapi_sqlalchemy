from db import SessionLocal
from dbal.data_store import create_ds

from dbal.tasks_dao_ex import TasksDao

session = SessionLocal()
try:
    ds = create_ds(session)

    t = TasksDao(ds).read_task(117)

    print(f"{t.t_subject}")

    t = TasksDao(ds).read_task(1)

    print(f"{t.t_subject}")

finally:
    session.close()
