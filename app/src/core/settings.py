from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env')

	jwt_secret: str = Field(alias='SECRET_KEY')
	jwt_algo: str = "HS256"
	jwt_access_lifespan_minutes: int = 30
	jwt_refresh_lifespan_minutes: int = 24 * 60 * 60

	postgres_user: str = Field()
	postgres_password: str = Field()
	pghost: str = Field()
	pgport: str = Field()
	postgres_db: str = Field()

	def get_pg_conn_str(self, is_local: bool = False) -> str:
		host = 'localhost' if is_local else self.pghost

		return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{host}:{self.pgport}/{self.postgres_db}'


settings = Settings() # pyright: ignore