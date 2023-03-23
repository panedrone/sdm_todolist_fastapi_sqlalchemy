import time
from datetime import datetime
from typing import List

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import schemas
from db import get_ds
from dbal.data_store import DataStore
from dbal.project import Project
from dbal.projects_dao_ex import ProjectsDaoEx
from dbal.task import Task
from dbal.tasks_dao_ex import TasksDaoEx

app = FastAPI(title="SDM + FastAPI Application",
              description="SDM + FastAPI Application with Sqlalchemy",
              version="1.0.0", )

# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
app.mount("/static", StaticFiles(directory="static"), name="static")


# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
# Serving only index.html
@app.get("/")
async def read_index():
    return FileResponse('index.html')


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    # print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.get('/projects', tags=["GroupList"], response_model=List[schemas.SchemaProjectLi])
def get_all_projects(ds: DataStore = Depends(get_ds)):
    return ProjectsDaoEx(ds).get_all_projects()


@app.post('/projects', tags=["GroupList"], status_code=201)
async def project_create(item_request: schemas.SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    p_dao = ProjectsDaoEx(ds)
    project = Project(p_name=item_request.p_name)
    p_dao.create_project(project)
    ds.commit()


@app.get('/projects/{p_id}', tags=["Group"], response_model=schemas.SchemaProject)
def project_read(p_id: int, ds: DataStore = Depends(get_ds)):
    return ProjectsDaoEx(ds).read_project(p_id)


@app.put('/projects/{p_id}', tags=["Group"])
async def project_update(p_id: int, item_request: schemas.SchemaProjectCreateUpdate, ds: DataStore = Depends(get_ds)):
    ProjectsDaoEx(ds).rename(p_id, item_request.p_name)
    ds.commit()


@app.delete('/projects/{p_id}', tags=["Group"], status_code=204)
async def project_delete(p_id: int, ds: DataStore = Depends(get_ds)):
    ProjectsDaoEx(ds).delete_project(p_id)
    ds.commit()


@app.get('/projects/{p_id}/tasks', tags=["GroupTaskLI"], response_model=List[schemas.SchemaGroupTaskLI])
def project_tasks(p_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDaoEx(ds).get_tasks_by_project(p_id)


@app.post('/projects/{p_id}/tasks', tags=["GroupTaskLI"], status_code=201)
async def task_create(p_id: int, item_request: schemas.SchemaTaskCreate, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    task = Task()
    task.p_id = p_id
    task.t_subject = j['t_subject']
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    task.t_date = dt_string
    task.t_priority = 1
    task.t_comments = ''
    TasksDaoEx(ds).create_task(task)
    ds.commit()


@app.get('/tasks/{t_id}', tags=["Task"], response_model=schemas.SchemaTaskEdit)
def task_read(t_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDaoEx(ds).read_task(t_id)


@app.put('/tasks/{t_id}', tags=["Task"])
async def task_update(t_id: int, item_request: schemas.SchemaTaskEdit, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    TasksDaoEx(ds).update_task(t_id, j)
    ds.commit()


@app.delete('/tasks/{t_id}', tags=["Task"], status_code=204)
async def task_delete(t_id: int, ds: DataStore = Depends(get_ds)):
    TasksDaoEx(ds).delete_task(t_id)
    ds.commit()


if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)
