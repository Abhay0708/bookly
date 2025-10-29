from pydantic import BaseModel,Field
import uuid
from datetime import datetime
from src.books.schemas import Book
from typing import List
from src.reviews.schemas import ReviewModel
# BaseModel, Field: Core Pydantic classes for data validation and field configuration
# uuid: For unique identifier type hints
# datetime: For timestamp fields
# Book, ReviewModel: Related schemas for nested data
# List: Type hint for list fields
#============================================================================================================================
class UserCreateModel(BaseModel):
    first_name:str
    last_name:str
    username:str = Field(max_length=8)
    email:str = Field(max_length=40)
    password:str =Field(min_length=6)
    
# Purpose: Used for user registration endpoints
# Field-by-field breakdown:
# first_name: str: User's first name (required, no constraints)
# last_name: str: User's last name (required)
# username: str = Field(max_length=8): Username limited to 8 characters maximum
# email: str = Field(max_length=40): Email limited to 40 characters maximum
# password: str = Field(min_length=6): Password must be at least 6 character
# Key Features:
# No UUID field: Server generates this during registration
# Plain password: Gets hashed before database storage
# Input validation: Prevents invalid data from reaching the database
#==============================================================================================================   
class UserModel(BaseModel):
    uid: uuid.UUID = str
    username: str
    first_name: str 
    last_name: str
    is_verified: bool 
    email: str
    password_hash: str =Field(exclude= True)
    created_at: datetime
    updated_at:datetime 
# Purpose: Used for API responses and internal user representation
# Field-by-field breakdown:
# uid: uuid.UUID = str: Issue: Should be uid: uuid.UUID (remove = str)
# username: str: User's unique username
# first_name, last_name: str: User's name components
# is_verified: bool: Email verification status
# email: str: User's email address
# password_hash: str = Field(exclude=True): Excluded from JSON serialization for security
# created_at, updated_at: datetime: Automatic timestamps
# Key Features:
# exclude=True: Password hash never appears in API responses
# Complete user data: All database fields represented
# Read-only fields: Includes system-generated fields (uid, timestamps)
#==========================================================================================================================
class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]
    
# Purpose: Extended user model that includes related books and reviews
# Field explanation:
# books: List[Book]: List of books owned/added by the user
# reviews: List[ReviewModel]: List of reviews written by the user
# Inherits from UserModel: Gets all user fields plus relationships
# Usage scenarios:
# User profile pages showing their books and reviews
# Analytics endpoints showing user activity
# Admin dashboards displaying user engagement  
    
#================================================================================================================
class UserLoginModel(BaseModel):
    email:str = Field(max_length=40)
    password:str =Field(min_length=6)
# Purpose: Used for user authentication endpoints
# Field breakdown:
# email: str = Field(max_length=40): Email for login (matches registration constraint)
# password: str = Field(min_length=6): Plain text password (matches registration constraint)
# Key Features:
# Minimal fields: Only what's needed for authentication
# Consistent validation: Same constraints as registration
# Security: Password transmitted securely over HTTPS