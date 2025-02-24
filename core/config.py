from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # mysql config
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "12345678"
    MYSQL_DB: str = "eye_diagnosis_system_db"
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    # fastapi config
    HOST: str = "127.0.0.1"
    PORT: int = 8000


settings = Settings()
