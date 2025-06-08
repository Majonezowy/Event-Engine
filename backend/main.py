from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import importlib
from backend.utils.colorlog import logger
import asyncio
from backend.utils.db import execute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

routers_dir = os.path.join(os.path.dirname(__file__), "api")

if not os.path.exists(routers_dir):
    raise ValueError(f"The directory {routers_dir} does not exist.")

for file in os.listdir(routers_dir):
    if not file.endswith(".py") or file == "__init__.py":
        continue
    module_name = f"backend.api.{file[:-3]}"
    module = importlib.import_module(module_name)
    if hasattr(module, "router"):
        app.include_router(module.router)
        logger.info(f"Endpoint {file} has been imported.")
    else:
        logger.warning(f"Failed to import {file} endpoint.")

async def load_schema():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
    for stmt in statements:
        await execute(stmt)
    logger.info("Database schema loaded.")

load_schema_task = asyncio.create_task(load_schema())

if __name__ == "__main__":
    asyncio.run(load_schema())

