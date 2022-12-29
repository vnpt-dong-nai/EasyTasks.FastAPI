import uuid, defs
from models import AddTaskCommand, UpdateTaskCommand

class TaskRepository:
    def __init__(self):
        self.tasks = []

    def addTask(self, user_id, cmd: AddTaskCommand):
        task_id = uuid.uuid4().hex
        self.tasks += [{'task_id': task_id, 'user_id':user_id, 'text':cmd.text, 'done':False, 'archived':False, 'category_id': cmd.category_id}]
        return defs.ERR_NONE, task_id

    def updateTask(self, user_id, task_id, done, archived, text):
        for t in self.tasks:
            if t['task_id'] == task_id:
                if t['user'] != user_id:
                    return defs.ERR_NOT_FOUND
                
                if text != None and isinstance(text, str) and len(text.strip()) != '':
                    t['text'] = text.strip()
                if done != None and isinstance(done, bool):
                    t['done'] = done
                if archived != None and isinstance(archived, bool):
                    t['archived'] = archived
                
                return defs.ERR_NONE, t
        
    def getUserTasks(self, user_id:str):
        ls = []
        for t in self.tasks:
            if t['user_id'] == user_id:
                ls += [t]
        return ls
