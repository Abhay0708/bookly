from fastapi import APIRouter, HTTPException, status, Depends
from src.books.schemas import Book, BookUpdateModel, BookCreateModel,BookDetailModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker
# APIRouter: Creates modular route groups for book endpoints
# HTTPException, status: For HTTP error responses and status codes
# Pydantic schemas: Data validation models for requests and responses
# AsyncSession: Async database session for non-blocking operations
# get_session: Dependency injection for database sessions
# BookService: Service layer containing business logic
# AccessTokenBearer, RoleChecker: Custom authentication and authorization dependencies
#===============================================================================================================================
book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
# book_router: APIRouter instance for all book-related endpoints
# book_service: Service class instance for database operations
# access_token_bearer: Authentication dependency for JWT validation
#==============================================================================================================================================
@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
)-> dict:
    # print(user_details)
    books = await book_service.get_all_books(session)
    return books
# Line-by-line breakdown:
# @book_router.get("/"): GET endpoint at root path (becomes /books/ when included with prefix)
# response_model=List[Book]: Returns list of Book objects, auto-generates OpenAPI docs
# session: AsyncSession = Depends(get_session): Injects database session
# token_details: dict = Depends(access_token_bearer): Validates JWT access token and extracts payload
# _bool=Depends(RoleChecker(["admin", "user"])): Enforces role-based access - only admin or user roles allowed
# books = await book_service.get_all_books(session): Async call to service layer
# return books: Returns all books ordered by creation date (newest first)
#=============================================================================================================================================
@book_router.get("/user/{user_uid}", response_model=List[Book])
async def get_user_book_submissions(
    user_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
):
    books = await book_service.get_user_books(user_uid,session)
    return books
# Line-by-line breakdown:
# "/user/{user_uid}": Path parameter for specific user's books
# user_uid:str: UUID string parameter from URL path
# Same authentication pattern: JWT validation + role checking
# await book_service.get_user_books(user_uid,session): Gets books for specific user
# Use case: View all books submitted by a particular user
#===============================================================================================================================================
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
) -> dict:
    user_id = token_details.get("users")["user_uid"]
    new_book = await book_service.create_book(book_data,user_id, session)
    return new_book
# Line-by-line breakdown:
# status_code=status.HTTP_201_CREATED: Returns 201 Created on success
# book_data: BookCreateModel: Validates incoming book data automatically
# user_id = token_details.get("users")["user_uid"]: Extracts user ID from JWT token
# await book_service.create_book(book_data,user_id, session): Creates book with user ownership
# Security feature: Books are automatically associated with the authenticated user
#================================================================================================================================================
@book_router.get("/{book_uid}", response_model=BookDetailModel)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
# Line-by-line breakdown:
# "/{book_uid}": Path parameter for book UUID
# response_model=BookDetailModel: Returns book with reviews and tags (relationships included)
# book = await book_service.get_book(book_uid, session): Fetches book by ID
# if book: return book: Returns book if found
# raise HTTPException(...): Returns 404 Not Found if book doesn't exist
#===============================================================================================================================================
@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return updated_book
# Line-by-line breakdown:
# @book_router.patch(...): PATCH method for partial updates
# book_update_data: BookUpdateModel: Validates update data (excludes read-only fields)
# await book_service.update_book(...): Updates existing book
# if updated_book is None:: Service returns None if book not found
# Error handling: Clear 404 response for non-existent books
#===============================================================================================================================================
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _bool=Depends(RoleChecker(["admin", "user"]))
):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return {}
# Line-by-line breakdown:
# status_code=status.HTTP_204_NO_CONTENT: Returns 204 No Content on successful deletion
# await book_service.delete_book(book_uid, session): Deletes book from database
# return {}: Empty response body for successful deletion
# Consistent error handling: 404 if book doesn't exist