import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'Quiz API'
    db_user: str = os.getenv('DB_USER', 'postgres')
    db_pass: str = os.getenv('DB_PASSWORD', 'postgres')
    db_hostname: str = os.getenv('DB_HOST', 'localhost')
    db_port: str = os.getenv('DB_PORT', '5432')
    db_name: str = os.getenv('DB_NAME', 'postgres')
    quiz_api_url: str = 'https://jservice.io/api/random?count={}'

    @property
    def database_url(self) -> str:
        return (f'postgresql+asyncpg://{self.db_user}:{self.db_pass}'
                f'@{self.db_hostname}:{self.db_port}/{self.db_name}')


settings = Settings()
