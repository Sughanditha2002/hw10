from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from enum import Enum
import uuid
import re
from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[\w\.-]+(?:\.[\w\.-]+)+(?:[\w\-\._~:/?#\[\]@!\$&\'()*\+,;=.]+)?$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    _validate_urls = validator(
        'profile_picture_url',
        'linkedin_profile_url',
        'github_profile_url',
        pre=True,
        allow_reuse=True
    )(validate_url)

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    @root_validator(pre=True)
    def at_least_one_non_null(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("At least one non-null field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID
    role: UserRole = Field(default=UserRole.AUTHENTICATED)
    is_professional: Optional[bool] = Field(default=False)

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="test@example.com")
    password: str = Field(..., example="MyPass123")

class UserListResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    size: int