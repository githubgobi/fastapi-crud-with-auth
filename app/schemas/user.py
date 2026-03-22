from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, SecretStr

# --- Schemas --- 
class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

class UserCreate(UserBase):
    name: str = Field(alias="fullName")
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)

class UserLogin(UserBase):
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)
class UserResponse(UserBase):
    id: int
    name: str 
    email: str