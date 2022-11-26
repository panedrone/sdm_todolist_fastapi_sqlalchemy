from typing import List, Optional

from pydantic import BaseModel


class SchemaGroupBase(BaseModel):
    g_name: str


class SchemaGroupCreate(SchemaGroupBase):
    pass


class SchemaGroup(SchemaGroupBase):
    g_id: int

    class Config:
        orm_mode = True


class SchemaGroupLi(SchemaGroupBase):
    g_id: int
    g_tasks_count: int


# .................................

class SchemaTaskBase(BaseModel):
    class Config:
        orm_mode = True


class SchemaGroupTaskLI(SchemaTaskBase):
    t_id: int
    t_priority: int
    t_date: str
    t_subject: str


class SchemaCreateTask(SchemaTaskBase):
    t_subject: str


class SchemaEditTask(SchemaTaskBase):
    t_priority: int
    t_date: str
    t_subject: str
    t_comments: str
