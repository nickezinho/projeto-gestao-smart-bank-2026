from sqlalchemy import Boolean, Float, DateTime, Column, Integer, String, func
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    cpf = Column(Integer, unique=True, index=True, nullable=False)

    risk_profile = Column(String, nullable=False)
    investment_goal = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)

    balance = Column(Float, nullable=False)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(), 
        default=func.now()
    )

    last_login_at = Column(
            DateTime(timezone=True),
            onupdate=func.now(), 
            default=func.now()
        )
