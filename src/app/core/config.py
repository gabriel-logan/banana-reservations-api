from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./banana_reservations.db"
    jwt_secret: str = "super-secret"
    jwt_algorithm: str = "HS256"

    model_config = {"env_file": ".env"}


settings = Settings()
