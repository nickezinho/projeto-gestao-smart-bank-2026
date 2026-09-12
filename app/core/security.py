from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import get_settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(
        user_id: int,
        token_type: str,
        duration: timedelta
) -> str:
    expiration = datetime.now(timezone.utc) + duration

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        get_settings.secret_key,
        get_settings.algorithm
    )


def create_access_token(user_id: int) -> str:
    return create_token(
        user_id,
        "access",
        timedelta(
            minutes=get_settings.access_token_expire_minutes
        )
    )


def create_refresh_token(user_id: int) -> str:
    return create_token(
        user_id,
        "refresh",
        timedelta(
            days=get_settings.refresh_token_expire_minutes
        )
    )


def verify_token(
    token: str,
    expected_type: str
):
    try:
        payload = jwt.decode(
            token,
            get_settings.secret_key,
            algorithms=[get_settings.algorithm]
        )

        if payload.get("type") != expected_type:
            raise JWTError("Invalid token type")

        return payload

    except JWTError:
        raise JWTError("Invalid token")