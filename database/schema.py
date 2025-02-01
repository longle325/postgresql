from sqlmodel import Field, Relationship, SQLModel, Session
from typing import Optional, List
from uuid import UUID, uuid4

class Company(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Id of the company"
    )

    name: str = Field(index=True, unique=True,default="",description="Name of the company",primary_key=False)

class User(SQLModel,table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Id of the user"
    )
    name: str = Field(default="",description="Name of the user")
    company_name: str = Field(default=None,foreign_key="company.name",description="Name of the company")
