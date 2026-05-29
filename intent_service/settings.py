from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INTENT_API_URL: str
    GRPC_PORT: int = 50051

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
