from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    LLM_MODEL: str = "gpt-oss:20b"
    INTENT_SERVICE_HOST: str = "intent-service"
    INTENT_SERVICE_PORT: int = 50051
    INTENT_SERVICE_TIMEOUT: float = 30.0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
