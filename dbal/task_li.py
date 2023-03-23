"""
Code generated by a tool. DO NOT EDIT.
https://sqldalmaker.sourceforge.net/
"""

from .data_store import *


class TaskLI(Base):
    """
    Task list item
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'tasks'

    t_id = Column('t_id', Integer, primary_key=True, autoincrement=True)
    p_id = Column('p_id', Integer, ForeignKey('projects.p_id'), nullable=True)
    t_priority = Column('t_priority', Integer)
    t_date = Column('t_date', String(65535))
    t_subject = Column('t_subject', String(65535))
