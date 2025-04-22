import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from fastapi.security import SecurityScopes
from fastapi import Depends, status, Security
from dependencies.user_login_dependencies import (
    get_password_hash,
    get_user,
    verify_password,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    get_session,
)
from models.user_login import TokenData, User
from models.products import Products


def authenticate_user(session: Session, email: str, password: str):
    """Authenticates user with given user info"""
    user = get_user(session, email)
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates new token for user"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
):
    """Returns current user"""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user(session, email=token_data.username)
    if email is None:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Returns current active user"""
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_product(id: int, session: Annotated[Session, Depends(get_session)]):
    """Check if id entered is a valid product"""
    checked_product = select(Products).where(Products.id == id)
    result = session.exec(checked_product)
    return result.one()
