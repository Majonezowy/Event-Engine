import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from backend.utils.db import execute

load_dotenv(os.path.join(os.path.dirname(__file__), '../../secrets.env'))
jwt_secret = os.getenv('jwt_secret', 'tajemnica tasiemca')

JWT_ALGORITHM = 'HS256'
JWT_EXP_MINUTES = 60

def create_jwt(payload: dict, exp_minutes: int = JWT_EXP_MINUTES) -> str:
    payload = payload.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    return jwt.encode(payload, jwt_secret, algorithm=JWT_ALGORITHM)

def verify_jwt(token: str) -> dict | None:
    try:
        decoded = jwt.decode(token, jwt_secret, algorithms=[JWT_ALGORITHM])
        user_id = decoded.get('user_id')
        if user_id:
            user = execute("SELECT * FROM users WHERE id = %s", user_id)
            if not user:
                return None
        else:
            return None
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
