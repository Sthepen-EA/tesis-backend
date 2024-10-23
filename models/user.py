from pydantic import BaseModel


class User (BaseModel):
    name: str
    email: str
    phone: str
    state: str
    password: str
    role: str

class UserLogin (BaseModel):
    email: str
    password: str