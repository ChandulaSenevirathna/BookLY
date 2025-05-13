import aioredis
from src.config import config

JTI_EXPIRY = 3600  # 1 hour

token_blocklist = aioredis.StrictRedis(
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