from sqlalchemy import select
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schema.user_schema import UserCreate

class UserRepository:

    @staticmethod
    async def create_user(session: AsyncSession, user_schema: UserCreate) -> User:
        user = User(
            username=user_schema.username,
            name=user_schema.name,
            email=user_schema.email,
            password=user_schema.password,
            cpf=user_schema.cpf,
            birth_date=user_schema.birth_date,
            risk_profile=user_schema.risk_profile,
            investment_goal=user_schema.investment_goal,
            balance=user_schema.balance
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod