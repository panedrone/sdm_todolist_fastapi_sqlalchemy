from datetime import datetime
from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import time
import asyncio

from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import schemas
from db import get_ds
from dbal.data_store import DataStore
from dbal.group import Group
from dbal.groups_dao_ex import GroupsDaoEx
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


@app.get('/api/groups', tags=["GroupList"], response_model=List[schemas.SchemaGroupLi])
def get_all_groups(ds: DataStore = Depends(get_ds)):
    return GroupsDaoEx(ds).get_all_groups()


@app.post('/api/groups', tags=["GroupList"], response_model=schemas.SchemaGroup, status_code=201)
async def group_create(item_request: schemas.SchemaGroupCreate, ds: DataStore = Depends(get_ds)):
    async def do_create():
        g_dao = GroupsDaoEx(ds)
        group = Group(g_name=item_request.g_name)
        g_dao.create_group(group)
        ds.commit()
        return group

    return await do_create()


@app.get('/api/groups/{g_id}', tags=["Group"], response_model=schemas.SchemaGroup)
def group_read(g_id: int, ds: DataStore = Depends(get_ds)):
    return GroupsDaoEx(ds).read_group(g_id)


@app.put('/api/groups/{g_id}', tags=["Group"])
async def group_update(g_id: int, item_request: schemas.SchemaGroupBase, ds: DataStore = Depends(get_ds)):
    GroupsDaoEx(ds).rename(g_id, item_request.g_name)
    ds.commit()


@app.delete('/api/groups/{g_id}', tags=["Group"], status_code=204)
async def group_delete(g_id: int, ds: DataStore = Depends(get_ds)):
    GroupsDaoEx(ds).delete_group(g_id)
    ds.commit()


@app.get('/api/groups/{g_id}/tasks', tags=["GroupTaskLI"], response_model=List[schemas.SchemaGroupTaskLI])
def group_tasks(g_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDaoEx(ds).get_tasks_by_group(g_id)


@app.post('/api/groups/{g_id}/tasks', tags=["GroupTaskLI"], status_code=201)
async def task_create(g_id: int, item_request: schemas.SchemaCreateTask, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    task = Task()
    task.g_id = g_id
    task.t_subject = j['t_subject']
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    task.t_date = dt_string
    task.t_priority = 1
    task.t_comments = ''
    TasksDaoEx(ds).create_task(task)
    ds.commit()


@app.get('/api/tasks/{t_id}', tags=["Task"], response_model=schemas.SchemaEditTask)
def task_read(t_id: int, ds: DataStore = Depends(get_ds)):
    return TasksDaoEx(ds).read_task(t_id)


@app.put('/api/tasks/{t_id}', tags=["Task"])
async def task_update(t_id: int, item_request: schemas.SchemaEditTask, ds: DataStore = Depends(get_ds)):
    j = jsonable_encoder(item_request)
    TasksDaoEx(ds).update_task(t_id, j)
    ds.commit()


@app.delete('/api/tasks/{t_id}', tags=["Task"])
async def task_delete(t_id: int, ds: DataStore = Depends(get_ds)):
    TasksDaoEx(ds).delete_task(t_id)
    ds.commit()


if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)
