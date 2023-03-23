# sdm_demo_todolist_fastapi_sqlalchemy
Quick Demo of how to use [SQL DAL Maker](https://github.com/panedrone/sqldalmaker) + Python + FastAPI + SQLAlchemy.

Front-end is written in Vue.js, SQLite3 is used as database.

![demo-go.png](demo-go.png)

![erd.png](erd.png)

dto.xml
```xml
<dto-class name="sa-Group" ref="groups"/>

<dto-class name="sa-GroupLi" ref="get_groups.sql">

    <header><![CDATA[    """
        Group list item
        """]]></header>

</dto-class>

<dto-class name="sa-Task" ref="tasks"/>

<dto-class name="sa-TaskLI" ref="tasks">

    <header><![CDATA[    """
        Task list item
        """
        __table_args__ = {'extend_existing': True}]]></header>

    <field column="t_comments" type="-"/>

</dto-class>
```
GroupsDao.xml
```xml
<crud dto="sa-Group" table="groups"/>
```
TasksDao.xml
```xml
<crud dto="sa-Task" table="tasks"/>
```
Generated code in action:
```go
@app.get('/groups', tags=["GroupList"], response_model=List[schemas.SchemaProjectLi])
def get_all_groups(ds: DataStore = Depends(get_ds)):
    return GroupsDaoEx(ds).get_all_groups()


@app.post('/groups', tags=["GroupList"], status_code=201)
async def group_create(item_request: schemas.SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    g_dao = GroupsDaoEx(ds)
    group = Group(g_name=item_request.g_name)
    g_dao.create_group(group)
    ds.commit()


@app.get('/groups/{g_id}', tags=["Group"], response_model=schemas.SchemaProject)
def group_read(g_id: int, ds: DataStore = Depends(get_ds)):
    return GroupsDaoEx(ds).read_group(g_id)


@app.put('/groups/{g_id}', tags=["Group"])
async def group_update(g_id: int, item_request: schemas.SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    GroupsDaoEx(ds).rename(g_id, item_request.g_name)
    ds.commit()


@app.delete('/groups/{g_id}', tags=["Group"], status_code=204)
async def group_delete(g_id: int, ds: DataStore = Depends(get_ds)):
    GroupsDaoEx(ds).delete_group(g_id)
    ds.commit()
```