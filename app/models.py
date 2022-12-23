from pydantic import BaseModel
class RegistrationAccountInfo(BaseModel):
    user_id:str
    password:str
    name:str
    phone:str