# sdm_demo_todolist_fastapi_sqlalchemy

Quick Demo of how to use [SQL DAL Maker](https://github.com/panedrone/sqldalmaker) + Python + FastAPI + SQLAlchemy.

Front-end is written in Vue.js, SQLite3 is used as a database.

![demo-go.png](demo-go.png)

dto.xml

```xml

<dto-classes>

    <dto-class name="sa-Project" ref="projects"/>

    <dto-class name="sa-ProjectLi" ref="get_projects.sql"/>

    <dto-class name="sa-Task" ref="tasks"/>

    <dto-class name="sa-TaskLi" ref="tasks">

        <header><![CDATA[    """
    Task list item
    """
    __table_args__ = {'extend_existing': True}]]></header>

        <field column="t_comments" type="-"/>

    </dto-class>

</dto-classes>
```

ProjectsDao.xml

```xml

<dao-class>

    <crud dto="sa-Project"/>

</dao-class>
```

TasksDao.xml

```xml

<dao-class>

    <crud dto="sa-Task"/>

</dao-class>
```

Generated code in action:

```python
from typing import List
from fastapi import Depends, FastAPI
from db import get_ds
from dbal.data_store import DataStore
from dbal.project import Project
from dbal.projects_dao_ex import ProjectsDao
from schemas import *

app = FastAPI(title="SDM + FastAPI + SQLAlchemy",
              description="Quick Demo of how to use SQL DAL Maker + Python + FastAPI + SQLAlchemy",
              version="1.0.0", )


@app.get('/projects', tags=["ProjectList"], response_model=List[SchemaProjectLi])
def get_all_projects(ds: DataStore = Depends(get_ds)):
    return ProjectsDao(ds).get_all_projects()


@app.post('/projects', tags=["ProjectList"], status_code=201)
async def project_create(item_request: SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    project = Project(p_name=item_request.p_name)
    ProjectsDao(ds).create_project(project)
    ds.commit()


@app.get('/projects/{p_id}', tags=["Project"], response_model=SchemaProject)
def project_read(p_id: int, ds: DataStore = Depends(get_ds)):
    return ProjectsDao(ds).read_project(p_id)


@app.put('/projects/{p_id}', tags=["Project"])
async def project_update(p_id: int, item_request: SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    ProjectsDao(ds).rename_project(p_id, item_request.p_name)
    ds.commit()


@app.delete('/projects/{p_id}', tags=["Project"], status_code=204)
async def project_delete(p_id: int, ds: DataStore = Depends(get_ds)):
    ProjectsDao(ds).delete_project(p_id)
    ds.commit()
```