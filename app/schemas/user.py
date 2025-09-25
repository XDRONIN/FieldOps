from pydantic import BaseModel, EmailStr, Field
from app.models.user import Role

# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    is_active: bool | None = True
    is_approved: bool | None = False
    role: Role | None = Role.USER

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Role

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None

from pydantic import ConfigDict

class UserInDBBase(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password_hash: str
