from datetime import datetime

from pydantic import BaseModel, validator


class _SchemaProjectBase(BaseModel):
    class Config:
        orm_mode = True


class SchemaProjectCreateUpdate(_SchemaProjectBase):
    p_name: str

    # @classmethod  # -------- don't use with @validator!!!
    @validator('p_name')
    def validate_p_name(cls, v):
        # https://github.com/pydantic/pydantic/issues/1223
        # https://levelup.gitconnected.com/how-to-validate-your-data-with-custom-validators-of-pydantic-models-743561a4ab53
        if not v:
            raise ValueError('Project name may not be empty')
        return v


class SchemaProject(_SchemaProjectBase):
    p_id: int
    p_name: str


class SchemaProjectLi(_SchemaProjectBase):
    p_id: int
    p_name: str
    p_tasks_count: int


# .................................

class _SchemaTaskBase(BaseModel):
    t_subject: str

    # @classmethod  # -------- don't use with @validator!!!
    @validator('t_subject')
    def validate_t_subject(cls, v):
        if not v:
            raise ValueError('Task subject may not be empty')
        return v

    class Config:
        orm_mode = True


class SchemaProjectTaskLI(_SchemaTaskBase):
    t_id: int
    t_priority: int
    t_date: str


class SchemaTaskCreate(_SchemaTaskBase):
    pass


class SchemaTaskEdit(_SchemaTaskBase):
    t_id: int
    t_priority: int
    t_date: str
    t_comments: str

    # @classmethod  # -------- don't use with @validator!!!
    @validator('t_date')
    def validate_t_date(cls, v):
        if not v:
            raise Exception('Task date may not be empty')
        try:
            dt = datetime.strptime(v, '%Y-%m-%d').date()
            return str(dt)  # 2020-4-8 becomes 2020-04-08
        except Exception:
            raise ValueError("Task date format expected like '2022-12-31'")

    # @classmethod  # -------- don't use with @validator!!!
    @validator('t_priority')
    def validate_t_priority(cls, v):
        if v < 1 or v > 10:
            raise Exception('Task priority should be an integer in the range 1..10')
        return v
