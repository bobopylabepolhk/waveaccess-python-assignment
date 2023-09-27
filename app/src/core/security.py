import json
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from core.constants import UserRoles
from core.messages import AUTHORIZATION_ERROR, WRONG_ROLE
from core.settings import settings

crypt_ctx = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str):
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str):
    return crypt_ctx.verify(password, hashed_password)


def create_jwt(payload: dict, expires_in: int):
    exp = datetime.utcnow() + timedelta(minutes=expires_in)
    to_encode = {"exp": exp, "sub": str(payload)}

    return jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algo)


security = HTTPBearer()


def parse_jwt_payload(token: str):
    raw_payload = jwt.decode(
        token, key=settings.jwt_secret, algorithms=[settings.jwt_algo]
    )
    user = json.loads(raw_payload["sub"].replace("'", '"'))

    return user


async def has_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return parse_jwt_payload(credentials.credentials)
    except JWTError:
        raise HTTPException(401, AUTHORIZATION_ERROR)


def has_access_by_role(target_role: UserRoles):
    async def func(credentials: HTTPAuthorizationCredentials = Depends(security)):
        user = await has_access(credentials=credentials)
        role = user.get("role")

        if not role or UserRoles[role] != target_role:
            raise HTTPException(403, WRONG_ROLE.format(role, target_role.name))

    return func


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    user = await has_access(credentials)

    return user.get("id")
