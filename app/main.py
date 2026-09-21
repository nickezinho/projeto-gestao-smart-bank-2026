from fastapi import FastAPI 
from api.routes.user import user_router

app = FastAPI(
    tile="SmartInvest Bank API",
    description="API for a mock fintech",
    version="1.0.0"
)

app.include_router(user_router)