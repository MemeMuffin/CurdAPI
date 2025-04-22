from typing import Annotated
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from passlib.context import CryptContext


class Products(SQLModel, table=True):
    """Products table"""

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, index=True)
    price: int | None = Field(default=None, index=True)
    instock: bool | None = Field(default=None, index=True)


class PublicProducts(Products):
    id: int


class CreateProduct(BaseModel):
    """Create new product"""

    name: str
    price: int
    instock: bool


class UpdateProduct(BaseModel):
    """Update product"""

    name: str | None = None
    price: int | None = None
    instock: bool | None = None
