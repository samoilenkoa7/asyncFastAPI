from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600 # seconds
    jwt_secret: str


settings = Settings(
    _env_file='~/Documents/asyncFastAPI/.env',
    _env_file_encoding='utf-8',
)
