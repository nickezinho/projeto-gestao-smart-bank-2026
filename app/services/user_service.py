from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from schemas.users_schema import UserCreate, UserUpdate, UserLogin, TokenResponse
from models.user import User
from core.security import verify_password, hash_password, create_access_token, create_refresh_token, verify_token
from repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    async def register_user(session: AsyncSession, user_schema: UserCreate) -> User:
        existing_cpf = await UserRepository.get_user_by_cpf(
            session,
            user_schema.cpf
        )

        if existing_cpf:
            raise ValueError("CPF already registered")

        existing_email = await UserRepository.get_user_by_email(
            session,
            user_schema.email
        )

        if  existing_email:
            raise ValueError("Email already registered")

        existing_username = await UserRepository.get_user_by_username(
            session,
            user_schema.username
        )

        if existing_username:
            raise ValueError("Username already registered")

        new_user_schema = user_schema.model_copy()

        new_user_schema.password = hash_password(
            new_user_schema.password
        )

        new_user = await UserRepository.create_user(
            session,
            new_user_schema
        )

        return new_user

    @staticmethod
    async def authenticate_user(session: AsyncSession, user_schema: UserLogin) -> User:
        user = await UserRepository.get_user_by_username(
            session,
            user_schema.username
        )

        if not user:
            raise ValueError("User not found")

        if not verify_password(
                user_schema.password,
                user.hashed_password
        ):
            raise ValueError("Incorrect password")

        return user

    @staticmethod
    async def login(session: AsyncSession, login_schema: UserLogin) -> TokenResponse:
        user = await UserService.authenticate_user(
            session,
            login_schema
        )

        access_token = create_access_token(
            user.id
        )

        refresh_token = create_refresh_token(
            user.id
        )

        return TokenResponse(
            refresh_token=refresh_token,
            access_token=access_token,
            token_type='bearer'
        )

    @staticmethod
    async def get_current_user(session: AsyncSession, token: str) -> User:
        user_id = verify_token(token)

        if not user_id:
            raise ValueError("Invalid token")
        print(user_id)
        user = await UserRepository.get_user_by_id(
            session,
            user_id
        )

        if not user:
            raise ValueError("User not found")

        return user

    @staticmethod
    async def use_refresh_token(session: AsyncSession, refresh_token: str) -> TokenResponse:
        user_id = verify_token(refresh_token)

        if not user_id:
            raise ValueError("Invalid token")

        user = await UserRepository.get_user_by_id(
            session,
            user_id
        )

        if not user:
            raise ValueError("User not found")

        access_token = create_access_token(
            user.id
        )

        refresh_token = create_refresh_token(
            user.id
        )

        return TokenResponse(
            refresh_token=refresh_token,
            access_token=access_token,
            token_type='bearer'
        )

