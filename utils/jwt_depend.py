from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from models.entity import User_password
from core.config import settings


# 验证密码
def verify_password(plain_password: str, hashed_password: str):
    return plain_password == hashed_password


# 验证用户
def authenticate_user(username: str, password: str):
    user = seek_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


# 创建 Token
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# 验证 Token
def verify_token(token: str) -> User_password:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None:
            raise credentials_exception
        return User_password(username=username, token_type=token_type)
    except JWTError:
        raise credentials_exception
