import asyncio
import redis.asyncio as redis
from src.config import config

JTI_EXPIRY = 3600  # 1 hour

token_blocklist = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str):
    
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )
    
async def token_in_blocklist(jti: str) -> bool:
    
    exists = await token_blocklist.exists(jti)
    
    if exists:
        return True
    
    return False