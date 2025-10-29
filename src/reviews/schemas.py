import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
# uuid: For unique identifier type hints and UUID validation
# datetime: For timestamp field types
# Optional: Type hint indicating a field can be None (shorthand for Union[X, None])
# BaseModel: Pydantic's base class for data validation and serialization
# Field: Function to add constraints, metadata, and validation rules to fields
#====================================================================================================================
class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    update_at: datetime
# Purpose: Complete review representation for API responses and internal operations
# Field-by-field breakdown:
# Primary Key:
# uid: uuid.UUID: Unique identifier for the review (primary key)
# Auto-validation: Ensures proper UUID format
# Security: Non-sequential, prevents ID enumeration
# Review Content:
# rating: int = Field(lt=5): Numeric rating with constraint validation
# Field(lt=5): "Less than 5" - rating must be 0, 1, 2, 3, or 4
# Common pattern: 5-star rating system (0-4 scale)
# Auto-validation: Rejects ratings of 5 or higher
# review_text: str: The actual review content (required string)
# Relationship Fields:
# user_uid: Optional[uuid.UUID]: Foreign key to user who wrote the review
# Optional: Can be None (nullable in database)
# UUID validation: Ensures proper format when provided
# book_uid: Optional[uuid.UUID]: Foreign key to book being reviewed
# Optional: Can be None (nullable in database)
# Relationship: Links review to specific book
# System Timestamps:
# created_at: datetime: When review was created (system-generated)
# update_at: datetime: When review was last modified (Note: likely typo, should be updated_at)
class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str
# Purpose: Input validation for creating new reviews via POST endpoints
# Field breakdown:
# rating: int = Field(lt=5): Same rating constraint as ReviewModel
# review_text: str: Review content (required)