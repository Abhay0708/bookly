import redis.asyncio as aioredis
from src.books.config import Config
# redis.asyncio as aioredis: Imports the asynchronous Redis client for non-blocking operations
# Config: Imports configuration settings (Redis host, port from environment variables)
#===========================================================================================================================
JTI_EXPIRY = 3600
# JTI_EXPIRY: Sets token blocklist expiration to 3600 seconds (1 hour)
# JTI: "JWT ID" - unique identifier for each JWT token
# After 1 hour, blocked tokens are automatically removed from Redis
#===============================================================================================================================
token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=0
)
# Line-by-line breakdown:
# token_blocklist: Global Redis client instance for managing blocked tokens
# aioredis.StrictRedis: Creates async Redis client with strict command parsing
# host=Config.REDIS_HOST: Redis server hostname (from .env: localhost)
# port=Config.REDIS_PORT: Redis server port (from .env: 6379)
# db=0: Uses Redis database 0 (Redis supports 16 databases by default)
#============================================================================================================================
async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
# Line-by-line breakdown:
# async def add_jti_to_blocklist(jti: str) -> None:: Async function that adds a JWT ID to the blocklist
# jti: str: Parameter containing the unique JWT token identifier
# await token_blocklist.set(...): Asynchronously sets a Redis key without blocking the application
# name=jti: Uses the JWT ID as the Redis key name
# value="": Stores empty string as value (we only care about key existence)
# ex=JTI_EXPIRY: Sets expiration time - key automatically deleted after 3600 seconds
# Purpose: When a user logs out, their JWT token ID gets added to this blocklist.
#============================================================================================================================================
async def token_in_blocklist(jti:str) -> bool:
    jti =  await token_blocklist.get(jti)
    return jti is not None
# Line-by-line breakdown:
# async def token_in_blocklist(jti:str) -> bool:: Async function that checks if a token is blocked
# jti = await token_blocklist.get(jti): Retrieves value from Redis using JWT ID as key
# await: Non-blocking Redis operation
# return jti is not None: Returns True if key exists (token is blocked), False if not found
# Logic: If the key exists in Redis, the token is blocklisted. If key doesn't exist, token is valid.