from pydantic import BaseModel
import uuid
from datetime import datetime,date
from typing import List
from src.reviews.schemas import ReviewModel
from src.tag.schemas import TagModel
# BaseModel: Pydantic's base class for data validation and serialization
# uuid: For unique identifier type hints
# datetime, date: For timestamp and date field types
# List: Type hint for list fields containing multiple items
# ReviewModel, TagModel: Related schemas for nested model relationships
#====================================================================================================================
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at:datetime
    updated_at:datetime
# Purpose: Complete book representation for API responses and internal operations
# Field-by-field breakdown:
# uid: uuid.UUID: Unique identifier (primary key from database)
# title: str: Book title (required string)
# author: str: Book author name
# publisher: str: Publishing company name
# published_date: date: Publication date (date type, not datetime)
# page_count: int: Number of pages in the book
# language: str: Language the book is written in
# created_at: datetime: When record was created (system-generated)
# updated_at: datetime: When record was last modified (system-generated)
# Key Features:
# Complete field set: Includes all database columns
# System fields included: Contains auto-generated timestamps and UUID
# Read-only usage: Typically used for GET endpoint responses
#=================================================================================================================================
"""
class BookDetailModel(Book):
    reviews: List[ReviewModel]
    tags:List[TagModel]
"""
# Purpose: Extended book model that includes related reviews and tags data
# Line-by-line breakdown:
# class BookDetailModel(Book):: Inherits all fields from the base Book model
# reviews: List[ReviewModel]: List of review objects associated with this book
# tags: List[TagModel]: List of tag objects categorizing this book
# Inheritance Benefits:
# Code reuse: Gets all Book fields automatically
# Consistency: Maintains same field definitions as base model
# Extension: Adds relationship data without duplication
# Usage scenarios:
# Book detail pages: Show book info with reviews and tags
# Admin dashboards: Complete book overview with all relationships
# Search results: Rich book data with categorization
#================================================================================================================
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
# Purpose: Input validation for creating new books via POST endpoints
#================================================================================================================================
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
# Purpose: Input validation for updating existing books via PATCH endpoints
