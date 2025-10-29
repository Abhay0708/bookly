from fastapi import APIRouter, HTTPException, status, Depends
from src.db.models import User
from src.db.main import get_session
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.service import ReviewService
from src.auth.dependencies import RoleChecker, get_current_user
# APIRouter: Creates modular route groups for review endpoints
# HTTPException, status: For HTTP error responses and status codes
# User: SQLModel for user database model
# get_session: Dependency injection for database sessions
# ReviewCreateModel: Pydantic schema for review input validation
# ReviewService: Service layer containing review business logic
# RoleChecker, get_current_user: Custom authentication and authorization dependencies
#=======================================================================================================================
review_service = ReviewService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))
# Line-by-line breakdown:
# review_service = ReviewService(): Service class instance for review database operations
# review_router = APIRouter(): APIRouter instance for all review-related endpoints
# admin_role_checker = Depends(RoleChecker(["admin"])): Admin-only access dependency
# user_role_checker = Depends(RoleChecker(["user", "admin"])): User or admin access dependency
# Role hierarchy: Admin users can access both admin and user endpoints, regular users only access user endpoints.
#==============================================================================================================================
@review_router.get("/", dependencies=[user_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    books = await review_service.get_all_reviews(session)
    return books
# Line-by-line breakdown:
# @review_router.get("/"): GET endpoint at root path (becomes /reviews/ when included with prefix)
# dependencies=[user_role_checker]: Enforces user or admin role without injecting the result
# session: AsyncSession = Depends(get_session): Injects database session
# books = await review_service.get_all_reviews(session): Variable naming issue: Should be reviews, not books
# return books: Returns all reviews ordered by creation date (newest first)
# Purpose: List all reviews in the system (for admin dashboard or public listing).
@review_router.get("/{review_uid}", dependencies=[user_role_checker])
async def get_review(review_uid: str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_review(review_uid, session)
    
    if not review:
        raise HTTPException(
                detail="Cannot found this review",
                status_code=status.HTTP_403_FORBIDDEN,
            )
    return review
# Line-by-line breakdown:
# "/{review_uid}": Path parameter for review UUID
# dependencies=[user_role_checker]: Requires user or admin role
# review = await review_service.get_review(review_uid, session): Fetches review by ID
# if not review:: Checks if review exists
# raise HTTPException(...): Issues with this error:
# Grammar error: "Cannot found" should be "Cannot find"
# Wrong status code: Should be 404 NOT_FOUND instead of 403 FORBIDDEN
# return review: Returns review if found
#====================================================================================================================
@review_router.post('/book/{book_uid}')
async def add_review_to_book(book_uid: str,review_data: ReviewCreateModel,current_user: User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session,
    )
    return new_review
# Line-by-line breakdown:
# @review_router.post('/book/{book_uid}'): POST endpoint to add review to specific book
# Missing configurations: No status_code=201 or response_model specified
# book_uid: str: Book UUID from URL path
# review_data: ReviewCreateModel: Validates incoming review data automatically
# current_user: User = Depends(get_current_user): Gets authenticated user from JWT token
# session: AsyncSession = Depends(get_session): Database session injection
# Service Call:
# await review_service.add_review_to_book(...): Creates review with proper associations
# user_email=current_user.email: Identifies user from JWT token
# book_uid=book_uid: Associates review with specific book
# return new_review: Returns created review with all fields
# Security feature: Reviews are automatically associated with the authenticated user.
#===============================================================================================================================
@review_router.delete("/{review_uid}",dependencies=[user_role_checker],status_code=status.HTTP_204_NO_CONTENT,)
async def delete_review(review_uid: str,current_user: User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
    await review_service.delete_review_to_from_book(
        review_uid=review_uid, user_email=current_user.email, session=session
    )
    return None
# Line-by-line breakdown:
# @review_router.delete("/{review_uid}"): DELETE endpoint for specific review
# dependencies=[user_role_checker]: Requires user or admin role
# status_code=status.HTTP_204_NO_CONTENT: Correct status for successful deletion
# review_uid: str: Review UUID from path parameter
# current_user: User = Depends(get_current_user): Gets authenticated user for ownership check
# await review_service.delete_review_to_from_book(...): Calls service method (note: buggy method name and implementation)
# Authorization: Service checks if user owns the review before deletion
# return None: Returns None (could return {} for consistency)