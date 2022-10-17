from pydantic import BaseModel


class Login(BaseModel):
    login_url: str


class Token(BaseModel):
    access_token: str