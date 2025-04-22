from typing import Annotated
from fastapi import FastAPI, Security, dependencies
from config.conn_db import create_db_and_tables
from contextlib import asynccontextmanager
from routes.user_login import userlogin as login
from routes.products import product as products
from models.user_login import User
from routes.utils import get_current_active_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Generates and intializes new db with table"""
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)


app.include_router(login, prefix="/login", tags=["Authentication"])
app.include_router(products, prefix="/user/products", tags=["Products"])
