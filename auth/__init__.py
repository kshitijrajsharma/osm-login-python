from pydantic import BaseModel

class Login(BaseModel):
    url: str

class Token(BaseModel):
    access_token: str