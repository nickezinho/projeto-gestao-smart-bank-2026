from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    app_name: str
    database_url: str
    secret_key: str

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )

get_settings = Settings()

