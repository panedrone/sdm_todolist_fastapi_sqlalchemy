# sdm_demo_todolist_fastapi_sqlalchemy
Quick Demo of how to use [SQL DAL Maker](https://github.com/panedrone/sqldalmaker) + Python + FastAPI + SQLAlchemy.

Front-end is written in Vue.js, SQLite3 is used as a database.

![demo-go.png](demo-go.png)

dto.xml
```xml
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
```
ProjectsDao.xml
```xml
<crud dto="sa-Project"/>
```
TasksDao.xml
```xml
<crud dto="sa-Task"/>
```
Generated code in action:
```go
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