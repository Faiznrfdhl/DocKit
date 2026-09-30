from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "demo_full"
    ENVIRONMENT: str = "development"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "dockit"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "demo_full"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
