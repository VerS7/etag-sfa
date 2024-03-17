"""
User models
"""
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    role: str = Field(nullable=False, default="user")
