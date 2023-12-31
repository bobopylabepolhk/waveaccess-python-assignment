from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    testing: bool = Field(default=False)
    base_url: str = "BASE_URL"

    jwt_secret: str = "SECRET_KEY"
    jwt_algo: str = "HS256"
    jwt_access_lifespan_minutes: int = 30
    jwt_refresh_lifespan_minutes: int = 60 * 60 * 24

    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    pghost: str = Field(default="localhost")
    pgport: int = Field(default=5432)
    postgres_db: str = Field(default="postgres")

    model_config = SettingsConfigDict(extra="ignore")

    def get_pg_conn_str(self, is_local: bool = False) -> str:
        host = "localhost" if is_local or self.testing else self.pghost

        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            host,
            self.pgport,
            self.postgres_db,
        )


settings = Settings()
