from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class UserCreate(UserBase):
    username: str = Field(min_length=8, max_length=128)
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)


class UserLogin(UserBase):
    username: str
    password: SecretStr = Field(min_length=8, max_length=128)


class UserResponse(UserBase):
    username: str
    first_name: str | None
    last_name: str | None
    email: str


class TokenData(UserBase):
    username: str = None


class Token(UserBase):
    access_token: str
    refresh_token: str
    token_type: str
