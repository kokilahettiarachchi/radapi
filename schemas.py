from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True



# User login schema
class UserLogin(BaseModel):
    username: str
    password: str

# Token schema for the access token
class Token(BaseModel):
    access_token: str
    token_type: str

# User schema with role and other attributes
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
