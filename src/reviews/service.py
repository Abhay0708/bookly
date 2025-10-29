from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateModel
from fastapi import status,HTTPException
from sqlmodel import desc, select
# from fastapi.exceptions import HTTPException
import logging
# Review: SQLModel database model for review table
# UserService, BookService: Service layers for related entities
# AsyncSession: Async database session for non-blocking operations
# ReviewCreateModel: Pydantic schema for input validation
# status, HTTPException: FastAPI components for HTTP responses and errors
# desc, select: SQLModel query builders for SELECT and descending ORDER BY
# logging: For error logging and debugging
#=====================================================================================================================================
book_service = BookService()
user_service = UserService()
# Service instances: Creates instances of related services for dependency resolution
# Composition pattern: ReviewService depends on UserService and BookService
# Reusability: Leverages existing service logic instead of duplicating database queries
#=======================================================================================================================================
class ReviewService:
    async def add_review_to_book(self,user_email:str, book_uid:str ,review_data:ReviewCreateModel ,session:AsyncSession):
        try:
            book =await book_service.get_book(book_uid=book_uid,session=session)
            user=await user_service.get_user_by_email(email=user_email,session=session)
            review_data_dict = review_data.model_dump()
            new_review=Review(
                **review_data_dict
            )
            if not book:
                raise HTTPException(
                    detail="Book not found", status_code=status.HTTP_404_NOT_FOUND
                )
            if not user:
                raise HTTPException(
                    detail="Book not found", status_code=status.HTTP_404_NOT_FOUND
                )
            new_review.user=user
            new_review.book=book
            session.add(new_review)
            await session.commit()
            return new_review
        
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops ... Something"
            )
# Line-by-line breakdown:
# Method Signature:
# async def add_review_to_book(...): Async method for creating reviews
# Parameters: user_email (from JWT), book_uid (from URL), review_data (validated input), session (database)
# Entity Validation:
# book =await book_service.get_book(...): Fetches book to ensure it exists
# user=await user_service.get_user_by_email(...): Fetches user to ensure they exist
# Dependency on other services: Reuses existing business logic
# Review Creation:
# review_data_dict = review_data.model_dump(): Converts Pydantic model to dictionary
# new_review=Review(**review_data_dict): Dictionary unpacking to create Review instance
# Existence Validation:
# if not book: raise HTTPException(...): Returns 404 if book doesn't exist
# if not user: raise HTTPException(...): Error: Message says "Book not found" but should be "User not found"
# Relationship Assignment:
# new_review.user=user: Sets SQLModel relationship (foreign key gets set automatically)
# new_review.book=book: Sets SQLModel relationship (foreign key gets set automatically)
# Database Operations:
# session.add(new_review): Adds review to session (pending transaction)
# await session.commit(): Commits transaction asynchronously
# return new_review: Returns created review with all fields populated
# Error Handling:
# except Exception as e:: Catches any unexpected errors
# logging.exception(e): Logs full exception details for debugging
# Generic error response: Returns 500 Internal Server Error 
#==================================================================================================================================   
    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        result = await session.exec(statement)
        return result.first()
# Line-by-line breakdown:
# statement = select(Review).where(Review.uid == review_uid): Creates SQL query for specific review
# Equivalent SQL: SELECT * FROM reviews WHERE uid = ?
# result = await session.exec(statement): Executes query asynchronously
# return result.first(): Returns first matching result or None if not found
# Purpose: Retrieves single review by UUID for other operations.
#=======================================================================================================================================
    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        return result.all()
# Line-by-line breakdown:
# select(Review).order_by(desc(Review.created_at)): Query all reviews ordered by newest first
# Equivalent SQL: SELECT * FROM reviews ORDER BY created_at DESC
# await session.exec(statement): Execute query asynchronously
# return result.all(): Returns all matching records as a list
# Purpose: Retrieves all reviews for admin/listing purposes.
#========================================================================================================================================
    async def delete_review_to_from_book(self, review_uid: str, user_email: str, session: AsyncSession):
        user = await user_service.get_user_by_email(user_email, session)
        review = await self.get_review(review_uid, session)
        if not review or (review.user is not user):
            raise HTTPException(
                detail="Cannot delete this review",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        await session.delete(review)
        await session.commit()
        return {}
# Line-by-line breakdown:
# Authorization Check:
# user = await user_service.get_user_by_email(user_email, session): Gets current user
# review = await self.get_review(review_uid, session): Gets review to delete
# if not review or (review.user is not user):: Authorization logic
# Ensures review exists AND belongs to current user
# raise HTTPException(..., status.HTTP_403_FORBIDDEN): Proper authorization error
# Delete Logic (BUGGY):
# session.add(review): ERROR: This adds the review back instead of deleting it!
# await session.commit(): Commits the incorrect operation
# What this should be: