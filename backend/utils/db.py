import os
import aiomysql
from dotenv import load_dotenv

from backend.utils.colorlog import logger

load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets.env'))

db_host = os.getenv('db_host', 'localhost')
db_user = os.getenv('db_user', 'root')
db_password = os.getenv('db_password', '')
db_name = os.getenv('db_name', 'EventEngine')

db_port = int(os.getenv('db_port', 3306))

async def get_pool():
    if not hasattr(get_pool, "pool"):
        get_pool.pool = await aiomysql.create_pool(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            autocommit=True
        )
        logger.info("Database connection pool created.")
    return get_pool.pool

async def fetch_one(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, args)
            return await cur.fetchone()

async def fetch_all(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, args)
            return await cur.fetchall()

async def execute(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, args)
            return cur.lastrowid
