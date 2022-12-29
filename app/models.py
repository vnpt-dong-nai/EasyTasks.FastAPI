from pydantic import BaseModel

class RegistrationAccountInfo(BaseModel):
    user_id:str
    email:str
    password:str
    name:str
    phone:str

    class Config:
        schema_extra = {
            "example": {
                "name": "Texter X",
                "user_id": "tester_x",
                "email": "tester_x@test.vn",
                "password": "123456",
                "phone": "0919112233"
            }
        }

class UpdateAccountCommand(BaseModel):
    user_id:str
    email:str | None = None
    name:str | None = None
    phone:str | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Texter X2",
                "user_id": "tester_x",
                "email": "tester_x2@test.vn",
                "phone": "0919112244"
            }
        }

class AddTaskCommand(BaseModel):
    text:str
    category_id:str

    class Config:
        schema_extra = {
            "example": {
                "text": "Buy a bottle of Milk",
                "category_id": "shopping"
            }
        }

class UpdateTaskCommand(BaseModel):
    task_id:str
    text:str | None = None
    category_id:str | None = None
    done:bool | None = None
    archive: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "text": "Buy 2x bottle of Milk",
            }
        }