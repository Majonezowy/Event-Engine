from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from backend.utils import db
from backend.utils.colorlog import logger
from backend.utils.jwt_util import create_jwt

load_dotenv(os.path.join(os.path.dirname(__file__), '../../secrets.env'))
jwt_secret = os.getenv('jwt_secret', 'tajemnica tasiemca')

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    klasa: str

@router.post("/login")
async def login(user: LoginRequest):
    if not user.email or not user.password:
        return {"error": "Email and password are required"}
    
    # Sprawdź, czy użytkownik istnieje
    existing_user = await db.fetch_one("SELECT * FROM users WHERE email = %s", user.email)
    if not existing_user:
        return {"error": "User not found"}
    if existing_user['password'] != user.password:
        return {"error": "Invalid password"}
    
    # JWT token
    token = create_jwt({"user_id": existing_user['id'], "email": existing_user['email']})

    return {"token": token, "user": {"id": existing_user['id'], "email": existing_user['email'], "class": existing_user.get('class')}}

@router.post("/register")
async def register(user: RegisterRequest):
    """
        Rejestruje nowego użytkownika.
        user: Obiekt zawierający email, hasło i klasę użytkownika.
    """

    logger.info(f"Attempting to register user: {user.email}")

    if not user.email or not user.password:
        return {"error": "Email and password are required"}
    
    # Sprawdź, czy użytkownik już istnieje
    existing_user = await db.fetch_one("SELECT * FROM users WHERE email = %s", user.email)
    if existing_user:
        logger.warning(f"User {user.email} already exists")
        return {"error": "User already exists"}

    db_query = "INSERT INTO users (email, password, class) VALUES (%s, %s, %s)"
    try:
        logger.info(f"Registering user {user.email} with class {user.klasa}")
        await db.execute(db_query, user.email, user.password, user.klasa)
    except Exception as e:
        logger.error(f"Failed to register user {user.email}: {str(e)}")
        return {"error": f"Failed to register user: {str(e)}"}
    logger.info(f"User {user.email} registered successfully")

    return {"message": f"User {user.email} registered successfully"}
