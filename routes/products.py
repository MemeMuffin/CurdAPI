from typing import Annotated
from sqlmodel import Session, select
from fastapi.routing import APIRouter
from fastapi import Query, Depends, HTTPException, Response, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user_login import Token, User
from models.products import CreateProduct, PublicProducts, UpdateProduct, Products
from config.conn_db import get_session
from routes.utils import get_current_user, check_product


product = APIRouter()


@product.get("/all/", response_model=list[PublicProducts])
async def get_all_products(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user, scopes=["active"])],
):
    """Returns all products stored in the database"""
    statement = select(Products)
    products = session.exec(statement).all()
    return products


@product.post("/createproduct/", response_model=PublicProducts)
async def create_new_product(
    products: CreateProduct,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user, scopes=["active"])],
):
    """Updates the database with new info about product in the database"""
    new_product = Products(name=products.name, price=products.price, instock=products.instock)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@product.patch("/updateproduct/", response_model=PublicProducts)
async def update_product(
    id: int,
    products: UpdateProduct,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user, scopes=["active"])],
):
    """Updates given product with given product info"""
    if not await check_product(id, session):
        raise HTTPException(status_code=400, detail="Product ID is incorrect")
    stmt = select(Products).where(Products.id == id)
    updated_product = session.exec(stmt).first()
    for key, value in products.model_dump(exclude_unset=True).items():
        setattr(updated_product, key, value)
    session.add(updated_product)
    session.commit()
    session.refresh(updated_product)
    return updated_product


@product.delete("/deleteproduct/", response_model=PublicProducts)
async def delete_product(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user, scopes=["active"])],
):
    """Deletes the product with the given ID and returns its details"""
    if not await check_product(id, session):
        raise HTTPException(status_code=400, detail="Product ID is incorrect")
    stmt = select(Products).where(Products.id == id)
    deleted_product = session.exec(stmt).first()
    session.delete(deleted_product)
    session.commit()
    return deleted_product
