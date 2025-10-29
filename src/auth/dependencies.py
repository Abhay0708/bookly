# Here's a comprehensive line-by-line explanation of your FastAPI JWT authentication and role-based access control implementation:
from fastapi.security import HTTPBearer
from fastapi import Request,status,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List,Any
from src.db.models import User
# HTTPBearer: FastAPI's base class for Bearer token authentication
# HTTPAuthorizationCredentials: Type for authorization header credentials
# decode_token: Custom utility to decode JWT tokens
# token_in_blocklist: Redis function to check if token is revoked
# UserService: Service class for user database operations
#=======================================================================================
user_service= UserService()
class TokenBearer(HTTPBearer):
    
    def __init__(self,auto_error =True):
        super().__init__(auto_error=auto_error)
# TokenBearer(HTTPBearer): Custom class extending FastAPI's HTTPBearer
# auto_error=True: Automatically raises HTTP exceptions on authentication failures 
#=====================================================================================================================
    async def __call__(self, request:Request)-> HTTPAuthorizationCredentials | None:
        creds= await super().__call__(request)
        token=creds.credentials
        token_data=decode_token(token)
# Line-by-line breakdown:
# async def __call__(...): Makes the class callable as a FastAPI dependency
# creds= await super().__call__(request): Gets credentials from Authorization header
# token=creds.credentials: Extracts the actual token string
# token_data=decode_token(token): Decodes JWT to get payload data
#===========================================================================================================================
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"This token is invalid or has been revoked",
                    "resolution":"Please get new token"
                }
            )
            
# self.token_valid(token): Checks if token can be decoded successfully
# token_in_blocklist(token_data['jti']): Checks Redis for revoked tokens using JWT ID
# jti: "JWT ID" - unique identifier for each token
#=====================================================================================================
        self.verify_token_data(token_data)
            
        
        return token_data
    
    def token_valid(self,token:str)->bool:
        token_data=decode_token(token)
        return token_data is not None
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
# token_valid(): Simple validation check
# verify_token_data(): Abstract method - must be implemented by subclasses
#=============================================================================================================
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )
# Purpose: Ensures only access tokens (not refresh tokens) are accepted
# Logic: If token_data["refresh"] is True, it's a refresh token → reject it
#================================================================================================================
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
# Purpose: Ensures only refresh tokens are accepted
# Logic: If token_data["refresh"] is False, it's an access token → reject it       
#==============================================================================================================
async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["users"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user
# Line-by-line breakdown:
# token_details: dict = Depends(AccessTokenBearer()): Validates access token and returns payload
# session: AsyncSession = Depends(get_session): Injects database session
# user_email = token_details["users"]["email"]: Extracts email from token payload
# await user_service.get_user_by_email(...): Fetches user from database
# return user: Returns complete User object for use in routes
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action."
        )
# Line-by-line breakdown:
# __init__(self, allowed_roles: List[str]): Constructor accepts list of allowed roles
# self.allowed_roles = allowed_roles: Stores allowed roles for this checker instance
# current_user: User = Depends(get_current_user): Gets authenticated user
# if current_user.role in self.allowed_roles:: Checks if user's role is permitted
# return True: Grants access if role matches
# raise HTTPException(...): Denies access if role doesn't match
