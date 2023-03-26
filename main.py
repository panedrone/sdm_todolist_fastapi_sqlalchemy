import time
from typing import List

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from schemas import *
from db import get_ds
from dbal.data_store import DataStore
from dbal.project import Project
from dbal.projects_dao_ex import ProjectsDao
from dbal.task import Task
from dbal.tasks_dao_ex import TasksDao

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


@app.get('/projects/{p_id}/tasks', tags=["ProjectTaskLI"], response_model=List[SchemaProjectTaskLI])
def project_tasks(p_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDao(ds).get_project_tasks(p_id)


@app.post('/projects/{p_id}/tasks', tags=["ProjectTaskLI"], status_code=201)
async def task_create(p_id: int, item_request: SchemaTaskCreate, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    task = Task()
    task.p_id = p_id
    task.t_subject = j['t_subject']
    task.t_date = datetime.now().strftime("%Y-%m-%d")
    task.t_priority = 1
    task.t_comments = ''
    TasksDao(ds).create_task(task)
    ds.commit()


@app.get('/tasks/{t_id}', tags=["Task"], response_model=SchemaTaskEdit)
def task_read(t_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDao(ds).read_task(t_id)


@app.put('/tasks/{t_id}', tags=["Task"])
async def task_update(t_id: int, item_request: SchemaTaskEdit, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    TasksDao(ds).update_task(t_id, j)
    ds.commit()


@app.delete('/tasks/{t_id}', tags=["Task"], status_code=204)
async def task_delete(t_id: int, ds: DataStore = Depends(get_ds)):
    TasksDao(ds).delete_task(t_id)
    ds.commit()


if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)
