# Here's a comprehensive line-by-line explanation of your FastAPI UserService class for handling user database operations:
from src.db.models import User
from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_passwd_hash
# User: SQLModel database model for user table
# select, desc: SQLModel query builders for SELECT statements and descending order
# AsyncSession: Async database session for non-blocking operations
# UserCreateModel: Pydantic schema for user registration data validation
# generate_passwd_hash: Utility function to hash passwords securely
#================================================================================================================
class UserService:
    
# Service layer pattern: Separates business logic from route handlers
# Single responsibility: Handles all user-related database operations
# Reusable: Can be used across multiple routes and modules
#====================================================================================================================================
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement=select(User).where(User.email==email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
# Line-by-line breakdown:
# async def get_user_by_email(...): Async method that doesn't block the application
# email:str, session:AsyncSession: Takes email parameter and database session
# statement=select(User).where(User.email==email): Creates SQL SELECT query with WHERE clause
# Equivalent SQL: SELECT * FROM user_accounts WHERE email = ?
# result = await session.exec(statement): Executes query asynchronously without blocking
# user = result.first(): Gets first matching result or None if not found
# return user: Returns User object or None
#======================================================================================================================================
    async def user_exists(self,email:str,session:AsyncSession):
        user= await self.get_user_by_email(email,session)
        
        # if user is None:
        #     return False
        # else:
        #     return True
        
        return True if user is not None else False #Ternary operator
# Line-by-line breakdown:
# async def user_exists(...): Async method to check user existence
# user= await self.get_user_by_email(email,session): Reuses existing method for DRY principle
# Commented code: Shows the traditional if/else approach
# return True if user is not None else False: Ternary operator - concise conditional return
# Logic: If user exists → return True, if None → return False
# Ternary operator syntax: value_if_true if condition else value_if_false
#=========================================================================================================================
    
    async def create_user(self,user_data:UserCreateModel,session:AsyncSession):
        user_data_dict=user_data.model_dump()
        
        new_user =User(
            ** user_data_dict
        )
        
        new_user.password_hash=generate_passwd_hash(user_data_dict['password'])
        new_user.role ="user"
        session.add(new_user)
        
        await session.commit()
        return new_user
# Line-by-line breakdown:
# Data Preparation:
# user_data_dict=user_data.model_dump(): Converts Pydantic model to dictionary
# Purpose: SQLModel constructor requires dictionary, not Pydantic object
# User Object Creation:
# new_user =User(** user_data_dict): Creates User instance using dictionary unpacking
# **user_data_dict: Spreads dictionary keys as keyword arguments
# Example: {"username": "john", "email": "john@email.com"} becomes User(username="john", email="john@email.com")
# Security & Default Values:
# new_user.password_hash=generate_passwd_hash(user_data_dict['password']):
# Hashes plain password before database storage
# Overwrites any password field from model_dump
# new_user.role ="user": Sets default role for new users
# Database Operations:
# session.add(new_user): Adds user to session (pending transaction)
# await session.commit(): Commits transaction asynchronously to database
# return new_user: Returns created user with generated fields (uid, timestamps)