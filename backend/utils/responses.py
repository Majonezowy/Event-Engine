from fastapi.responses import JSONResponse
from datetime import datetime

def error_response(message: str, status_code: int = 400):
    return JSONResponse(status_code=status_code, content={"error": message})

def serialize(obj):
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def success_response(message: str, data=None, status_code: int = 200):
    resp = {"message": message}
    if data is not None:
        resp["data"] = serialize(data)
    return JSONResponse(status_code=status_code, content=resp)
