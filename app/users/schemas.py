from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    name:str
    email: EmailStr
    age:int

    @field_validator("age")
    def check_age(cls, age):
        if age <= 14:
            raise ValueError("You must be 14 years of age or older")
        return age

class UserShow(BaseModel):
    name:str
    email:EmailStr
    age:int

class UserUpdate(BaseModel):
    name:str|None = None
    email:EmailStr|None = None
    age:int|None = None

class UserSearch(BaseModel):
    name:str|None = None
    email:EmailStr|None = None
    age:int|None = None