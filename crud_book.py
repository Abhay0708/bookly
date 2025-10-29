# This is a complete CRUD (Create, Read, Update, Delete) API for managing books using FastAPI. 
# Here's a brief explanation of each section:
from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
# FastAPI, status: Main framework and HTTP status codes
# CORSMiddleware: Handles cross-origin requests for frontend integration
# BaseModel: Pydantic for data validation
# List: Type hint for returning lists
# HTTPException: For raising HTTP errors
#------------------------------------------------------------------------------------------------------------------------------------------
app=FastAPI()
# Add CORS middleware
# this code is for only for restFox Ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins for development/testing
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],        # Allow all headers
)
books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Algorithms and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2021-01-01",
        "page_count": 9282,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Head First HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English",
    },
]
# In-memory list of book dictionaries serving as a mock database
# Contains 6 sample books with fields: id, title, author, publisher, published_date, page_count, language
class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str
class BookUpdate(BaseModel):
    title:str
    author:str
    publisher:str
    page_count:int
    language:str
# Book: Complete model for responses and creation
# BookUpdate: Partial model for updates (excludes id and published_date)
@app.get("/books",response_model=List[Book])
async def get_all_books():
    return books
# Returns all books as a list
# Response model ensures proper JSON serialization
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book) -> dict:
    new_book=book_data.model_dump()
    books.append(new_book)
    return new_book
# Accepts book data, validates it against Book model
# model_dump() converts Pydantic model to dictionary
# Appends to books list and returns created book
# Returns 201 Created status
@app.get("/books/{book_id}")
async def get_book(book_id:int) ->dict:
    for book in books:
        if book['id']==book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )
# Searches for book by ID in the list
# Returns book if found, otherwise raises 404 Not Found
@app.patch("/books/{book_id}")
async def update_book(book_id: int,book_update:BookUpdate)->dict:
    for book in books:
        if book['id']==book_id:
            book['title']=book_update.title
            book['author']=book_update.author
            book['publisher']=book_update.publisher
            book['page_count']=book_update.page_count
            book['language']=book_update.language
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Not Found"
    )
# PATCH method for partial updates
# Finds book by ID and updates specified fields
# Uses BookUpdate model (excludes id and published_date)
    
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
# Removes book from list if found
# Returns 204 No Content status
# Returns empty dict on successful deletion
