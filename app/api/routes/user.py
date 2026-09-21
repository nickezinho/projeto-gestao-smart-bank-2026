from fastapi import APIRouter, Depends, HTTPException, Request
from schemas.users_schema import AccessTokenInput, RefreshTokenInput, UserCreate, UserLogin, TokenResponse, UserResponse
from services.user_service import UserService

from ..deps import get_db

from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("/register", response_model=UserResponse)
async def register_user(
    user_schema: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        new_user = await UserService.register_user(db, user_schema)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )

@user_router.post("/login", response_model=TokenResponse)
async def user_login(
    login_schema: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    try:
        user_login = await UserService.login(
            db,
            login_schema
        )
        return user_login
    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

@user_router.post("/me", response_model=UserResponse)
async def get_current_user(
    token_input: AccessTokenInput,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        current_user = await UserService.get_current_user(
            db,
            access_token=token_input.access_token
        )
        return current_user
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@user_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    token_input: RefreshTokenInput,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    try:
        new_tokens = await UserService.use_refresh_token(
            db,
            refresh_token=token_input.refresh_token
        )
        return new_tokens
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )