from datetime import datetime

from pydantic import BaseModel, validator


class _SchemaGroupBase(BaseModel):
    g_name: str

    @validator('g_name')
    def validator_g_name(cls, v):
        # https://github.com/pydantic/pydantic/issues/1223
        if not v:
            raise Exception('Group name may not be empty')
        return v

    class Config:
        orm_mode = True


class SchemaGroupCreate(_SchemaGroupBase):
    pass


class SchemaGroup(_SchemaGroupBase):
    g_id: int


class SchemaGroupLi(_SchemaGroupBase):
    g_id: int
    g_tasks_count: int


# .................................

class _SchemaTaskBase(BaseModel):
    t_subject: str

    @validator('t_subject')
    def validator_t_subject(cls, v):
        if not v:
            raise Exception('Task subject may not be empty')
        return v

    class Config:
        orm_mode = True


class SchemaGroupTaskLI(_SchemaTaskBase):
    t_id: int
    t_priority: int
    t_date: str


class SchemaTaskCreate(_SchemaTaskBase):
    pass


class SchemaTaskEdit(_SchemaTaskBase):
    t_priority: int
    t_date: str
    t_comments: str

    @validator('t_date')
    def validator_t_date(cls, v):
        if not v:
            raise Exception('Task date may not be empty')
        try:
            datetime.strptime(v, '%Y-%m-%d').date()
        except Exception:
            raise Exception("Task date format expected like '2022-12-31'")
        return v
