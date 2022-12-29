from typing import Union
from taskrepo import TaskRepository
from userrepo import UserRepository
from fastapi import FastAPI, Body, Header, HTTPException
import defs
from models import RegistrationAccountInfo, UpdateAccountCommand, AddTaskCommand

app = FastAPI(openapi_tags=defs.api_tags)

repo = TaskRepository()
userRepo = UserRepository()

@app.get("/")
def welcome():
    return 'welcome to Easy Tasks API'

@app.get("/tasks/{user_id}", tags=['Tasks'])
def tasks_get_by_user(user_id:str):
    return repo.getUserTasks(user_id)

@app.put("/task/{user_id}", tags=['Tasks'])
def task_add_by_user(user_id:str, cmd:AddTaskCommand = Body()):
    return repo.addTask(user_id, cmd)

@app.post("/task/{user_id}/{task_id}", tags=['Tasks'])
def task_update_by_user(user_id:str, task_id:str, data:dict = Body()):
    done = None
    text = None
    if 'done' in data:
        done = data['done']
    
    if 'text' in data:
        text = data[text]

    archived = None
    if 'archived' in data:
        archived = data['archived']
    return repo.updateTask(user_id, task_id, done, archived, text)

@app.put("/user/register", tags=['Auth'])
def user_register(model:RegistrationAccountInfo = Body()):
    err, user_id = userRepo.addUser(model)
    if err == defs.ERR_ALREADY_EXISTS:
        return HTTPException(status_code=400, detail=f'Account already exists: {model.user_id}')
    return { 'user_id': user_id, 'activated':True, 'name': model.name, 'phone': model.phone, 'email': model.email }


@app.post("/user", tags=['Auth'])
def user_update(device_id:str=Header(), token:str=Header(), cmd:UpdateAccountCommand = Body()):
    return userRepo.updateUser(device_id, token, cmd)

@app.post("/user/login", tags=['Auth'])
def user_login(device_id:str = Header(default='test-device'), user_id:str=Body(default='tester_x'), password:str=Body(default='123456')):
    return userRepo.login(user_id, password, device_id)

@app.get("/users", tags=['Auth'])
def get_all_users(apikey:str = Header(default='dev.master')):
    if apikey == 'dev.master':
        return userRepo.getAll()
    return HTTPException(status_code=400, detail='You are not allowed')

