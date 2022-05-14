from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    developer_key: str = Field(default_factory=str, env='DEVELOPER_KEY')

    class Config:
        env_file = 'config/.env.example'
        env_file_encoding = 'utf-8'
