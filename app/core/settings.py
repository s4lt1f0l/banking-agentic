from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "https://mhbjj-35-201-203-79.run.pinggy-free.link"
    LLM_MODEL: str = "gpt-oss:20b"
    INTENT_API_URL: str = "https://zhhck-136-116-203-18.run.pinggy-free.link/predict"

    class Config:
        env_file = ".env"

settings = Settings()