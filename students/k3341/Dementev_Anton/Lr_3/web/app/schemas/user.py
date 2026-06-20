from typing import Optional

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    is_active: bool


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None


class PasswordChange(SQLModel):
    old_password: str
    new_password: str
