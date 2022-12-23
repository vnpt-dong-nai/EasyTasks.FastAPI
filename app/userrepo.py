import uuid, defs
from models import RegistrationAccountInfo

class UserRepository:
    def __init__(self):
        self.users = []

    def addUser(self, acc : RegistrationAccountInfo):
        for u in self.users:
            if u['user_id'] == acc.user_id:
                return defs.ERR_ALREADY_EXISTS, None
            
        self.users += [{'user_id':acc.user_id, 'password':acc.password, 'name': acc.name, 'phone':acc.phone, 'devices': {}}]
        return defs.ERR_NONE, acc.user_id
    
    def getUserByToken(self, device_id, token):
        for u in self.users:
            if device_id in u['devices']:
                if u['devices'][device_id] == token:
                    return u
        return None

    def updateUser(self, device_id, token, name, phone):
        u = self.getUserByToken(device_id, token)
        if u == None:
            return defs.ERR_NOT_FOUND
        
        if name != None and isinstance(name, str) and len(name.strip()) != '':
            u['name'] = name.strip()
        if phone != None and isinstance(phone, bool):
            u['phone'] = phone
        
        returnUser = { 'user_id':u['user_id'], 'name': u['name'], 'phone': u['phone'] }
        return defs.ERR_NONE, returnUser
        
    def login(self, user_id, password, device_id):
        for u in self.users:
            if u['user_id'] == user_id and u['password'] == password:
                if device_id in u['devices']:
                    return u['devices'][device_id]
                token = uuid.uuid4().hex
                u['devices'][device_id] = token
                return defs.ERR_NONE, token
            
        return defs.ERR_NOT_ALLOW, None

    def getAll(self):
        return self.users