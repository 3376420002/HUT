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
    HOST: str = "0.0.0.0"
    PORT: int = 8800

    # QQsmpt config
    MAIL_HOST: str = "smtp.qq.com"
    MAIL_PORT: int = 465
    MAIL_USER: str = "3376420002@qq.com"
    MAIL_PASSWORD: str = "hycypovjkruqcihb"

    # ai large model config
    AI_MODEL_URL: str = "192.168.137.16:5000"

    # jwt config
    JWT_SECRET_KEY: str = "huoxiaya666"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 7

    # redis config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


settings = Settings()
