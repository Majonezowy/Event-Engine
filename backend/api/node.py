from fastapi import APIRouter
from pydantic import BaseModel

from backend.utils.colorlog import logger
from backend.utils.db import execute, fetch_all, fetch_one
from backend.utils.jwt_util import verify_jwt
from backend.utils.responses import error_response, success_response

router = APIRouter(
    prefix="/node",
    tags=["node"]
)

class TokenBase(BaseModel):
    token: str

class NodeRequest(TokenBase):
    node_id: int

class NodeList(TokenBase):
    pass

class NodeAdd(TokenBase):
    node_name: str
    node_location: str
    description: str | None = None

class NodeDelete(TokenBase):
    node_id: int

class NodeUpdate(TokenBase):
    node_id: int
    node_name: str | None = None
    node_location: str | None = None
    description: str | None = None

def is_admin(token: str) -> bool:
    verified = verify_jwt(token)
    if not isinstance(verified, dict):
        return False
    return verified.get('role') == 'admin'

@router.post("/")
async def list_nodes(node: NodeList):
    """
        Pobiera listę punktów (nodes) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    if token is None:
        return error_response("Token is required", 401)
    verified_token = verify_jwt(token)
    if not verified_token:
        return error_response("Invalid or expired token", 401)
    if not is_admin(token):
        return error_response("Admin privileges required", 403)
    logger.info(f"Node list requested with token {token}")
    nodes = await fetch_all("SELECT * FROM `nodes`")
    logger.info(f"Fetched nodes with fetch_all: {nodes}")
    if not nodes:
        return success_response("No nodes found", data=[], status_code=200)
    return success_response("List of nodes retrieved successfully", data=nodes, status_code=200)

@router.post("/details")
async def read_node(node: NodeRequest):
    """
        Wysła dane o danym punkcie (node) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id
    if node_id is None:
        return error_response("Node ID is required", 400)
    if token is None:
        return error_response("Token is required", 401)
    verified_token = verify_jwt(token)
    if not verified_token:
        return error_response("Invalid or expired token", 401)
    node_data = await fetch_one("SELECT * FROM nodes WHERE id = %s", node_id)
    if not node_data:
        return error_response("Node not found", 404)
    logger.info(f"Node {node_id} details requested with token {token}")
    return success_response(f"Details of node {node_id} retrieved successfully", data=node_data, status_code=200)

@router.post("/add")
async def add_node(node: NodeAdd):
    """
        Dodaje nowy punkt (node) do systemu.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_name = getattr(node, 'node_name', None)
    node_location = getattr(node, 'node_location', None)
    if token is None:
        return error_response("Token is required", 401)
    if node_name is None:
        return error_response("Node name is required", 400)
    if node_location is None:
        return error_response("Node location is required", 400)
    if not is_admin(token):
        return error_response("Admin privileges required", 403)
    verified_token = verify_jwt(token)
    if not verified_token:
        return error_response("Invalid or expired token", 401)
    logger.info(f"Adding node with name {node_name} at location {node_location} with token {token}")
    await execute("INSERT INTO nodes (name, location) VALUES (%s, %s)", node_name, node_location)
    logger.info(f"Node with name {node_name} added successfully")
    return success_response(f"Node with name {node_name} added successfully", status_code=201)

@router.post("/delete")
async def delete_node(node: NodeDelete):
    """
        Usuwa punkt (node) z systemu.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = getattr(node, 'node_id', None)
    if node_id is None:
        return error_response("Node ID is required", 400)
    if token is None:
        return error_response("Token is required", 401)
    if not is_admin(token):
        return error_response("Admin privileges required", 403)
    verified_token = verify_jwt(token)
    if not verified_token:
        return error_response("Invalid or expired token", 401)
    logger.info(f"Deleting node with id {node_id} with token {token}")
    await execute("DELETE FROM nodes WHERE id = %s", node_id)
    return success_response(f"Node with id {node_id} deleted successfully", status_code=200)

@router.post("/update")
async def update_node(node: NodeUpdate):
    """
        Aktualizuje dane punktu (node) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = getattr(node, 'node_id', None)
    node_name = getattr(node, 'node_name', None)
    node_location = getattr(node, 'node_location', None)
    if node_id is None:
        return error_response("Node ID is required", 400)
    if token is None:
        return error_response("Token is required", 401)
    if not is_admin(token):
        return error_response("Admin privileges required", 403)
    verified_token = verify_jwt(token)
    if not verified_token:
        return error_response("Invalid or expired token", 401)
    logger.info(f"Updating node with id {node_id} with token {token}")
    if node_name is not None:
        await execute("UPDATE nodes SET name = %s WHERE id = %s", node_name, node_id)
    if node_location is not None:
        await execute("UPDATE nodes SET location = %s WHERE id = %s", node_location, node_id)
    logger.info(f"Node with id {node_id} updated successfully")
    return success_response(f"Node with id {node_id} updated successfully", status_code=200)

@router.post("/history")
async def node_history(node: NodeRequest):
    """
        <h1 style="color: red;">Nie zaimplementowano</h1>\n
        Pobiera historię punktu (node) w systemie.\n
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id

    if node_id is None:
        return {"error": "Node ID is required"}
    
    if token is None:
        return {"error": "Token is required"}
    
    return {"message": f"History of node {node_id} with token {token} retrieved successfully"}

@router.post("/export")
async def export_node(node: NodeRequest):
    """
        <h1 style="color: red;">Nie zaimplementowano</h1>\n
        Eksportuje dane punktu (node) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id

    if node_id is None:
        return {"error": "Node ID is required"}
    
    if token is None:
        return {"error": "Token is required"}
    
    return {"message": f"Data for node {node_id} with token {token} exported successfully"}

@router.post("/import")
async def import_node(node: NodeRequest):
    """
        <h1 style="color: red;">Nie zaimplementowano</h1>\n
        Importuje dane punktu (node) do systemu.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id

    if node_id is None:
        return {"error": "Node ID is required"}
    
    if token is None:
        return {"error": "Token is required"}
    
    return {"message": f"Data for node {node_id} with token {token} imported successfully"}