"""
Auth token models
"""
from sqlmodel import SQLModel, Field


class AuthToken(SQLModel, table=True):
    """Auth token model"""
    __tablename__ = "tokens"
    id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    token: str = Field(nullable=False)
