from pydantic import BaseModel


class RegUser(BaseModel):
    username: str
    password: str

class PingCheck(BaseModel):
    ip: str
