from fastapi import APIRouter
from pydantic import BaseModel

from backend.utils.colorlog import logger
from backend.utils.db import execute, fetch_all, fetch_one
from backend.utils.jwt_util import verify_jwt

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

@router.post("/")
async def list_nodes(node: NodeList):
    """
        Pobiera listę punktów (nodes) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    if token is None:
        return {"error": "Token is required"}
    verified_token = verify_jwt(token)
    if not verified_token:
        return {"error": "Invalid or expired token"}
    logger.info(f"Node list requested with token {token}")
    
    nodes = await fetch_all("SELECT * FROM nodes")
    print(nodes)
    if not nodes:
        return {"message": "No nodes found"}

    return {"message": "List of nodes retrieved successfully", "data": nodes}

@router.post("/details")
async def read_node(node: NodeRequest):
    """
        Wysła dane o danym punkcie (node) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id
    if node_id is None:
        return {"error": "Node ID is required"}
    if token is None:
        return {"error": "Token is required"}
    
    verified_token = verify_jwt(token)
    if not verified_token:
        return {"error": "Invalid or expired token"}
    
    node_data = await fetch_one("SELECT * FROM nodes WHERE id = %s", node_id)
    if not node_data:
        return {"error": "Node not found"}
    logger.info(f"Node {node_id} details requested with token {token}")

    return {"message": f"Details of node {node_id} retrieved successfully", "data": node_data}

@router.post("/add")
async def add_node(node: NodeAdd):
    """
        Dodaje nowy punkt (node) do systemu.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_name = node.node_name
    node_location = node.node_location
    description = node.description

    if token is None:
        return {"error": "Token is required"}
    
    if node_name is None:
        return {"error": "Node name is required"}
    
    if node_location is None:
        return {"error": "Node location is required"}
    
    verified_token = verify_jwt(token)
    if not verified_token:
        return {"error": "Invalid or expired token"}
    logger.info(f"Adding node with{node_name} at location {node_location} with token {token}")
    await execute("INSERT INTO nodes (name, location, description) VALUES (%s, %s, %s, %s)", node_name, node_location, description)
    logger.info(f"Node with name {node_name} added successfully")

    return {"message": f"Node with name {node_name} added successfully"}

@router.post("/delete")
async def delete_node(node: NodeDelete):
    """
        Usuwa punkt (node) z systemu.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id

    if node_id is None:
        return {"error": "Node ID is required"}
    
    if token is None:
        return {"error": "Token is required"}
    
    verified_token = verify_jwt(token)
    if not verified_token:
        return {"error": "Invalid or expired token"}
    logger.info(f"Deleting node with id {node_id} with token {token}")
    await execute("DELETE FROM nodes WHERE id = %s", node_id)
    
    return {"message": f"Node with id {node_id} deleted successfully"}

@router.post("/update")
async def update_node(node: NodeUpdate):
    """
        Aktualizuje dane punktu (node) w systemie.
        node: Obiekt zawierający token do autoryzacji oraz node_id.
    """
    token = node.token
    node_id = node.node_id
    node_name = node.node_name
    node_location = node.node_location

    if node_id is None:
        return {"error": "Node ID is required"}
    
    if token is None:
        return {"error": "Token is required"}
    
    verified_token = verify_jwt(token)
    if not verified_token:
        return {"error": "Invalid or expired token"}
    logger.info(f"Updating node with id {node_id} with token {token}")
    if node_name is not None:
        await execute("UPDATE nodes SET name = %s WHERE id = %s", node_name, node_id)
    if node_location is not None:
        await execute("UPDATE nodes SET location = %s WHERE id = %s", node_location, node_id)
    logger.info(f"Node with id {node_id} updated successfully")
    
    return {"message": f"Node with id {node_id} updated successfully"}

@router.post("/history")
async def node_history(node: NodeRequest):
    """
        <h1>Pobiera historię punktu (node) w systemie.</h1>\n
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