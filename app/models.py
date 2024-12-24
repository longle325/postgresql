from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

class CompanyBase(SQLModel):
    company_name: str = Field(index=True, unique=True)

class Company(CompanyBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="companies")

class UserBase(SQLModel):
    name: str = Field(index=True)
    company_name: str = Field(foreign_key="company.company_name")

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    companies: List[Company] = Relationship(back_populates="user")