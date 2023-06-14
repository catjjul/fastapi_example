from pydantic import BaseModel, Field
import datetime


class TokenSchema(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    login: str = Field(..., description="login")
    password: str = Field(..., min_length=8, max_length=24, description="password")
    salary: int = Field(0)
    change_date: datetime.date = Field(datetime.date.fromisoformat('1970-01-01'))


class UserOut(BaseModel):
    salary: int
    change_date: datetime.date


class SystemUser(UserOut):
    password: str
