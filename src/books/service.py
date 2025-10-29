# Here's a comprehensive line-by-line explanation of your FastAPI BookService class implementing async CRUD operations for book management:
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel,BookUpdateModel
from sqlmodel import select,desc
from src.db.models import BooK
from datetime import datetime
# AsyncSession: Async database session for non-blocking operations
# BookCreateModel, BookUpdateModel: Pydantic schemas for input validation
# select, desc: SQLModel query builders for SELECT and descending ORDER BY
# BooK: SQLModel database model (note the capitalization quirk)
# datetime: For date/time operations (though commented out in this code)
#===============================================================================================================
class BookService:
# Service layer pattern: Encapsulates all book-related database operations
# Single responsibility: Handles only book CRUD operations
# Reusable: Can be used across multiple route handlers
#==============================================================================================================================
    async def get_all_books(self, session:AsyncSession):
        statement=select(BooK).order_by(desc(BooK.created_at))
        result=await session.exec(statement)
        return result.all()
# Line-by-line breakdown:
# async def get_all_books(...): Async method for non-blocking database operations
# statement=select(BooK).order_by(desc(BooK.created_at)): Creates SQL query
# Equivalent SQL: SELECT * FROM books ORDER BY created_at DESC
# result=await session.exec(statement): Executes query asynchronously
# return result.all(): Returns all matching records as a list
# Purpose: Retrieves all books ordered by newest first.
#========================================================================================================================
    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(BooK)
            .where(BooK.user_uid == user_uid)
            .order_by(desc(BooK.created_at))
        )
        result = await session.exec(statement)
        return result.all()
# Line-by-line breakdown:
# async def get_user_books(self, user_uid: str, session: AsyncSession): Gets books for specific user
# statement = (select(BooK).where(BooK.user_uid == user_uid).order_by(desc(BooK.created_at))):
# Multi-line query building for better readability
# WHERE clause: Filters by user ownership
# ORDER BY: Newest books first
# Equivalent SQL: SELECT * FROM books WHERE user_uid = ? ORDER BY created_at DESC
# Purpose: Retrieves all books owned by a specific user.
#==========================================================================================================================
    async def get_book(self, book_uid:str, session: AsyncSession):
        statement=select(BooK).where(BooK.uid==book_uid)
        result= await session.exec(statement)
        book = result.first()
        return book if book is not None else None
# Line-by-line breakdown:
# statement=select(BooK).where(BooK.uid==book_uid): Query for specific book by UUID
# result= await session.exec(statement): Execute query asynchronously
# book = result.first(): Gets first matching result or None if not found
# return book if book is not None else None: Ternary operator - explicit None return
# Purpose: Retrieves a single book by its unique identifier.    
#===================================================================================================================================
    async def create_book(self, book_data:BookCreateModel,user_uid: str, session:AsyncSession):
        book_data_dict=book_data.model_dump(exclude={'uid'})
        new_book =BooK(
            **book_data_dict
        )
        # new_book.published_date=datetime.strptime(book_data_dict['published_date'],"%Y-%m-%dT%H:%M:%S")
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book) 
        return new_book
# Line-by-line breakdown:
# Data Preparation:
# book_data_dict=book_data.model_dump(exclude={'uid'}): Convert Pydantic model to dict, excluding uid
# new_book =BooK(**book_data_dict): Dictionary unpacking to create Book instance
# Field Assignment:
# Commented date parsing: Shows alternative date handling approach
# new_book.user_uid = user_uid: Associates book with the creating user
# Database Operations:
# session.add(new_book): Adds book to session (pending transaction)
# await session.commit(): Commits transaction asynchronously
# await session.refresh(new_book): Refreshes object to get generated fields (uid, timestamps)
# return new_book: Returns created book with all fields populated
# Purpose: Creates new book with user ownership.   
#===============================================================================================================================
    async def update_book(self,book_uid:str, update_data:BookUpdateModel, session:AsyncSession):
        book_to_update=await self.get_book(book_uid,session)
        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(book_to_update,k ,v)
            await session.commit()
            return book_to_update
        else:
            return None
# Line-by-line breakdown:
# Book Retrieval:
# book_to_update=await self.get_book(book_uid,session): Reuses existing method for DRY principle
# if book_to_update is not None:: Checks if book exists
# Dynamic Field Updates:
# update_data_dict = update_data.model_dump(): Convert update model to dictionary
# for k, v in update_data_dict.items():: Iterate through update fields
# setattr(book_to_update,k ,v): Dynamic attribute setting - updates each field individually
# Transaction Handling:
# await session.commit(): Saves changes to database
# return book_to_update: Returns updated book object
# else: return None: Returns None if book not found
# Purpose: Updates existing book fields dynamically.       
#========================================================================================================================================    
    async def delete_book(self, book_uid:str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid,session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None
# Deletion Process:
# if book_to_delete is not None:: Confirms book exists
# await session.delete(book_to_delete): Marks object for deletion (async)
# await session.commit(): Executes the deletion transaction
# return {}: Returns empty dict indicating successful deletion
# else: return None: Returns None if book not found
# Purpose: Removes book from database permanently.
