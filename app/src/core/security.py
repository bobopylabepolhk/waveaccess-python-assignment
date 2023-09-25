import json
from passlib.context import CryptContext
from datetime import datetime, timedelta
from core.messages import AUTHORIZATION_ERROR
from core.settings import settings

from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.messages import WRONG_ROLE
from core.constants import UserRoles

crypt_ctx = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str):
    return crypt_ctx.hash(password)

def verify_password(password: str, hashed_password: str):
    return crypt_ctx.verify(password, hashed_password)

def create_jwt(payload: dict, expires_in: int):
	exp = datetime.utcnow() + timedelta(minutes=expires_in)
	to_encode = { "exp": exp, "sub": str(payload) }
    
	return jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algo)

security = HTTPBearer()

async def has_access(credentials: HTTPAuthorizationCredentials=Depends(security)):
    token = credentials.credentials

    try:
        return jwt.decode(
        	token,
			key=settings.jwt_secret,
        	algorithms=[settings.jwt_algo]
        )
    except JWTError:
        raise HTTPException(401, AUTHORIZATION_ERROR)
    
def has_access_by_role(target_role: UserRoles):
    async def func(credentials: HTTPAuthorizationCredentials=Depends(security)):
        raw_jwt = await has_access(credentials=credentials)
        user = json.loads(raw_jwt['sub'].replace("'", '"'))
        role = user.get('role')

        if not role or UserRoles[role] != target_role:
            raise HTTPException(403, WRONG_ROLE.format(role, target_role.name))

    return func
