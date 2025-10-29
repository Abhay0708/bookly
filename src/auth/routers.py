# Here's a comprehensive line-by-line explanation of your FastAPI authentication router implementing a complete JWT-based authentication system:
from fastapi import APIRouter,Depends,status
from src.auth.schemas import UserCreateModel,UserModel,UserLoginModel,UserBooksModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.auth.utils import create_access_token,decode_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
from datetime import datetime
from src.auth.dependencies import RefreshTokenBearer,AccessTokenBearer,get_current_user,RoleChecker
from src.db.redis import add_jti_to_blocklist
# APIRouter: Creates modular route groups for authentication endpoints
# Pydantic schemas: Data validation models for requests and responses
# UserService: Database operations for user management
# get_session: Dependency injection for database sessions
# JWT utilities: Token creation, decoding, and password verification
# Custom dependencies: Token bearers for access/refresh token validation
# Redis integration: Token revocation via blocklist
#===================================================================================================================================
auth_router =APIRouter()
user_service= UserService()
role_checker=RoleChecker(["admin","user"])
REFRESH_TOKEN_EXPIRY =2
# auth_router: APIRouter instance for authentication routes
# user_service: Service class instance for user database operations
# role_checker: Role-based access control allowing "admin" and "user" roles
# REFRESH_TOKEN_EXPIRY = 2: Refresh token expires in 2 days
#========================================================================================================================================
@auth_router.post("/signup",response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession=Depends(get_session)):
    email =user_data.email
    user_exists =await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User with email already exist")
    
    new_user =await user_service.create_user(user_data,session)
    
    return new_user
# Line-by-line breakdown:
# @auth_router.post("/signup",...): POST endpoint for user registration
# response_model=UserModel: Automatic response serialization and documentation
# status_code=status.HTTP_201_CREATED: Returns 201 Created on success
# user_data:UserCreateModel: Validates incoming registration data
# email =user_data.email: Extracts email for duplicate checking
# user_exists =await user_service.user_exists(...): Async check for existing user
# raise HTTPException(...): Returns 403 Forbidden if user already exists
# new_user =await user_service.create_user(...): Creates new user with hashed password
# return new_user: Returns created user (password_hash excluded automatically)
#===============================================================================================================================================
@auth_router.post("/login")
async def login_user_account(login_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password
    
    user =await user_service.get_user_by_email(email,session)
    
    if user is not None:
        password_valid=verify_password(password,user.password_hash)
        
        if password_valid:
            access_token=create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid),
                    "role":user.role
                }
            )
            refresh_token=create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry= timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )
# Line-by-line breakdown:
# Credential Extraction:
# email=login_data.email, password=login_data.password: Extract credentials from validated request
# User Lookup:
# user =await user_service.get_user_by_email(email,session): Find user in database
# Password Verification:
# password_valid=verify_password(password,user.password_hash): Compare plain password with bcrypt hash
# Token Generation:
# Access token: Short-lived (1 hour default) with user data including role
# Refresh token: Long-lived (2 days) with refresh=True flag
# str(user.uid): Converts UUID to string for JSON serialization
# Successful Response:
# JSONResponse: Returns structured response with both tokens and user info
# Security: No sensitive data (password hash) in response
#================================================================================================================================================
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )
# Line-by-line breakdown:
# Depends(RefreshTokenBearer()): Validates that incoming token is a refresh token (not access token)
# expiry_timestamp = token_details["exp"]: Extracts expiration timestamp from token payload
# datetime.fromtimestamp(expiry_timestamp) > datetime.now(): Double-checks token hasn't expired
# create_access_token(user_data=token_details["user"]): Creates new access token from refresh token data
# Returns new access token: Client can continue API access without re-login
#==============================================================================================================================================
@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user),_: bool=Depends(role_checker)):
    return user
# Line-by-line breakdown:
# user=Depends(get_current_user): Injects authenticated user from valid access token
# _: bool=Depends(role_checker): Enforces role-based access control (admin or user roles)
# response_model=UserBooksModel: Returns user with books and reviews (relationships included)
# return user: Returns complete user profile with related data  
@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )
# Line-by-line breakdown:
# Depends(AccessTokenBearer()): Validates access token and extracts payload
# jti = token_details['jti']: Gets JWT ID (unique identifier for this specific token)
# await add_jti_to_blocklist(jti): Adds token to Redis blocklist for immediate revocation
# JSONResponse(...): Confirms successful logout
# Key security feature: Even if token hasn't expired, it's now blocked and cannot be used for API access.
# Authentication Flow Summary
#======================================================================================================================================
# Registration Flow:
# Validate input → Check for duplicate users → Create user → Return user profile
# Login Flow:
# Validate credentials → Generate tokens → Return access token + refresh token
# API Access Flow:
# Client sends access token → Token validated → User identified → Access granted
# Token Refresh Flow:
# Client sends refresh token → Validates it's refresh type → Generates new access token
# Logout Flow:
# Extract JWT ID from token → Add to Redis blocklist → Token immediately invalid
# Security Features
# Multiple Security Layers:
# Input validation: Pydantic schemas prevent malformed data
# Password hashing: bcrypt with automatic salting
# JWT signing: Cryptographic token integrity
# Token type separation: Access vs refresh token validation
# Role-based access: Fine-grained permission control
# Token revocation: Redis blocklist for immediate logout
# Best Practices Implemented:
# Short-lived access tokens (1 hour) limit exposure
# Long-lived refresh tokens (2 days) improve user experience
# Automatic token validation in dependencies
# Structured error responses for consistent API behavior
# UUID usage prevents sequential ID enumeration attacks
# This authentication router provides a comprehensive, secure, and production-ready JWT authentication system with all essential features: 
# registration, login, token refresh, profile access, role-based permissions, and secure logout with token revocation.