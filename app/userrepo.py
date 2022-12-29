import uuid, defs
from models import RegistrationAccountInfo, UpdateAccountCommand

class UserRepository:
    def __init__(self):
        self.users = []

    def addUser(self, acc : RegistrationAccountInfo):
        for u in self.users:
            if u['user_id'] == acc.user_id:
                return defs.ERR_ALREADY_EXISTS, None
            
        self.users += [{'user_id':acc.user_id, 'password':acc.password, 'email':acc.email, 'name': acc.name, 'phone':acc.phone, 'devices': {}}]
        return defs.ERR_NONE, acc.user_id
    
    def getUserByToken(self, device_id, token):
        for u in self.users:
            if device_id in u['devices']:
                if u['devices'][device_id] == token:
                    return u
        return None

    def updateUser(self, device_id, token, cmd:UpdateAccountCommand):
        u = self.getUserByToken(device_id, token)
        if u == None:
            return defs.ERR_NOT_FOUND
        
        if cmd.name != None and len(cmd.name.strip()) != '':
            u['name'] = cmd.name.strip()
        if cmd.email != None and len(cmd.email.strip()) != '':
            u['email'] = cmd.email.strip()
        if cmd.phone != None:
            u['phone'] = cmd.phone
        
        returnUser = { 'user_id':u['user_id'], 'name': u['name'], 'phone': u['phone'], 'email': u['email'] }
        return defs.ERR_NONE, returnUser
        
    def login(self, user_id, password, device_id):
        for u in self.users:
            if u['user_id'] == user_id and u['password'] == password:
                token = uuid.uuid4().hex
                if device_id in u['devices']:
                    token = u['devices'][device_id]
                else:
                    u['devices'][device_id] = token
                return { 'errCode': defs.ERR_NONE, 'token': token, 'userInfo': self.getPublicUserInfo(u) }
        return { 'errCode': defs.ERR_NOT_FOUND, 'errMsg': 'Invalid user_id or password' }

    def getAll(self):
        return self.users
    
    def getPublicUserInfo(self, userEntity:dict):
        return { 'user_id': userEntity['user_id'], 'name': userEntity['name'], 'email': userEntity['email'], 'phone': userEntity['phone'] }