import aioredis
from src.config import config

token_blocklist = aioredis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)