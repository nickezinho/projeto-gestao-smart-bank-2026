from fastapi import FastAPI 

app = FastAPI(
    tile="SmartInvest Bank API",
    description="API for a mock fintech"
    version="1.0.0"
)

app.include_router()