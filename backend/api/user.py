from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from backend.utils import db
from backend.utils.colorlog import logger
from backend.utils.jwt_util import create_jwt
from backend.utils.jwt_util import verify_jwt

load_dotenv(os.path.join(os.path.dirname(__file__), '../../secrets.env'))
jwt_secret = os.getenv('jwt_secret', 'tajemnica tasiemca')

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(LoginRequest):
    klasa: str

class AttendanceRequest(BaseModel):
    token: str
    node_id: int

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
    
    # JWT token with role
    token = create_jwt({
        "user_id": existing_user['id'],
        "email": existing_user['email'],
        "role": existing_user.get('role', 'user')
    })
    
    user_response = {
        "id": existing_user['id'],
        "email": existing_user['email'],
        "class": existing_user.get('class'),
        "role": existing_user.get('role', 'user')
    }
    return {"token": token, "user": user_response}

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

@router.post("/attend")
async def attend(request: AttendanceRequest):
    """
        Rejestruje obecność użytkownika.
        request: Obiekt zawierający token JWT i node_id.
    """
    verified_token = verify_jwt(request.token)
    user_id = verified_token.get('user_id') if verified_token else None
    if not (verified_token and user_id and request.node_id):
        return {"error": "Invalid or expired token, or missing node_id"}

    user = await db.fetch_one("SELECT 1 FROM users WHERE id = %s", user_id)
    node = await db.fetch_one("SELECT 1 FROM nodes WHERE id = %s", request.node_id)
    if not user:
        return {"error": "User not found"}
    if not node:
        return {"error": "Node not found"}

    existing_attendance = await db.fetch_one("SELECT 1 FROM attendance WHERE user_id = %s AND node_id = %s", user_id, request.node_id)
    if existing_attendance:
        return {"error": "Attendance already registered for this node"}

    try:
        await db.execute("INSERT INTO attendance (user_id, node_id, created_at) VALUES (%s, %s, NOW())", user_id, request.node_id)
        logger.info(f"Attendance for user {verified_token.get('email')} registered successfully")
    except Exception as e:
        logger.error(f"Failed to register attendance for user {verified_token.get('email')}: {str(e)}")
        return {"error": f"Failed to register attendance: {str(e)}"}
    return {"message": f"Attendance for user {verified_token.get('email')} registered successfully"}