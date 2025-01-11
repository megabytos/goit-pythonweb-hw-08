import os
from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    DB_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"


config = Config
