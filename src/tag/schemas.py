import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel
# uuid: For unique identifier type hints and UUID validation
# datetime: For timestamp field types with automatic validation
# List: Type hint for list fields containing multiple items
# BaseModel: Pydantic's base class for data validation and serialization
#=======================================================================================================================
class TagModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime
# Purpose: Complete tag representation for API responses and internal operations
# Field-by-field breakdown:
# uid: uuid.UUID: Unique identifier for the tag (primary key)
# Auto-validation: Ensures proper UUID format (e.g., 123e4567-e89b-12d3-a456-426614174000)
# Security: Non-sequential, prevents ID enumeration attacks
# Database mapping: Corresponds to primary key in tags table
# name: str: Tag name/label (required string)
# Examples: "Science Fiction", "Programming", "History", "Romance"
# Business logic: Used for categorizing books
# Required field: No default value, must be provided
# created_at: datetime: When tag was created (system-generated)
# Auto-validation: Accepts ISO 8601 format strings, datetime objects
# Example formats: "2025-09-02T11:30:00Z", "2025-09-02T11:30:00+05:30"
# System field: Set automatically by database
#=======================================================================================================================
class TagCreateModel(BaseModel):
    name: str
#Purpose: Input validation for creating new tags via POST endpoints
#========================================================================================================================
class TagAddModel(BaseModel):
    tags: List[TagCreateModel]
# Purpose: Bulk operations - adding multiple tags in a single API call
# # Field breakdown:
# # tags: List[TagCreateModel]: List of tag creation objects
# # Nested model validation: Each item in the list is validated as a TagCreateModel
# # Automatic validation: Pydantic validates each tag individually
# # Bulk insert support: Enables efficient batch operations