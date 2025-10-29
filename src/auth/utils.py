# Here's a comprehensive line-by-line explanation of your FastAPI authentication utilities for password hashing and JWT token management:
from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt
from src.books.config import Config
import uuid
import logging
# CryptContext: Passlib's main class for password hashing with bcrypt
# datetime, timedelta: For token expiration timestamps
# jwt: PyJWT library for creating and decoding JWT tokens
# Config: Application settings (JWT_SECRET, JWT_ALGORITHM)
# uuid: For generating unique token identifiers (JTI)
# logging: For error logging in token decoding
#===================================================================================================================
passwd_context= CryptContext(
    schemes=['bcrypt']
)
ACCESS_TOKEN_EXPIRY = 3600 
# Line-by-line breakdown:
# CryptContext(schemes=['bcrypt']): Creates password hasher using bcrypt algorithm
# bcrypt: Secure, slow hashing algorithm that includes automatic salt generation
# ACCESS_TOKEN_EXPIRY = 3600: Default token expiry set to 3600 seconds (1 hour)
#=========================================================================================================================
def generate_passwd_hash(password:str) -> str:
    hash =passwd_context.hash(password)
    return hash
# Purpose: Converts plain text password to secure bcrypt hash
# passwd_context.hash(password): Creates unique bcrypt hash with automatic salt
# Each call generates different hash: Even same password produces different results due to random salt
# Example output: $2b$12$EixZaYVK1fsbw1ZfbX3OXe...
#==================================================================================================================================
def verify_password(password:str,hash:str) ->bool:
    return passwd_context.verify(password,hash)
# Purpose: Verifies if plain password matches stored hash
# passwd_context.verify(password,hash): Compares plain password against bcrypt hash
# Returns boolean: True if password matches, False if not
# Secure comparison: Uses constant-time comparison to prevent timing attacks
#=================================================================================================================================
def create_access_token(user_data:dict,expiry:timedelta=None, refresh:bool=False):
    payload = {}
    payload["users"]=user_data
    payload["exp"]=datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4())
    payload['refresh']=refresh 
    
    token=jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token
# Line-by-line breakdown:
# Payload Construction:
# payload = {}: Creates empty dictionary for JWT claims
# payload["users"]=user_data: Stores user information (email, id, etc.)
# payload["exp"]=datetime.now() + (...): Sets expiration timestamp
# expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY): Uses custom expiry or default 1 hour
# payload['jti']=str(uuid.uuid4()): Generates unique JWT ID for token revocation
# payload['refresh']=refresh: Boolean flag indicating token type (access vs refresh)
# Token Encoding:
# jwt.encode(...): Creates signed JWT token string
# payload=payload: The data to encode
# key=Config.JWT_SECRET: Secret key for signing (from environment variables)
# algorithm=Config.JWT_ALGORITHM: Signing algorithm (typically HS256)
#=================================================================================================================================
def decode_token(token:str)-> str:
    try:
        token_data=jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
# Line-by-line breakdown:
# Token Decoding:
# jwt.decode(...): Decodes and verifies JWT token
# jwt=token: The token string to decode
# key=Config.JWT_SECRET: Same secret used for encoding
# algorithms=[Config.JWT_ALGORITHM]: Allowed algorithms (security measure)
# Error Handling:
# try/except jwt.PyJWTError: Catches JWT-related errors (expired, invalid signature, etc.)
# logging.exception(e): Logs the specific error for debugging
# return None: Returns None for invalid tokens
#=================================================================================================================================
