"""
Code generated by a tool. DO NOT EDIT.
https://sqldalmaker.sourceforge.net/
"""

from .data_store import *


class Project(Base):
    __tablename__ = 'projects'

    p_id = Column('p_id', Integer, primary_key=True, autoincrement=True)
    p_name = Column('p_name', String(256))