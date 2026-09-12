from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    cpf: int
    birth_date: datetime

    risk_profile: str
    investment_goal: str
    balance: float

    model_config = ConfigDict(
        from_attributes=True
    )


class UserResponse(BaseModel):
    id: str
    username: str
    name: str
    email: EmailStr
    cpf: int
    birth_date: datetime

    risk_profile: str
    investment_goal: str
    balance: float

    is_active: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime
    last_login_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    cpf: int | None = None
    birth_date: datetime | None = None

    risk_profile: str | None = None
    investment_goal: str | None = None
    balance: float | None = None

    is_active: bool | None = None
    is_superuser: bool | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        from_attributes=True
    )


class RegisterResponse(BaseModel):
    message: str
    username: str
    
    model_config = ConfigDict(
        from_attributes=True
    )