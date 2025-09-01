from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# FastAPI, Header: Main FastAPI framework and Header function for extracting HTTP headers
# CORSMiddleware: Middleware to handle Cross-Origin Resource Sharing (CORS) for browser requests
# BaseModel: Pydantic class for data validation and serialization
# Optional: Type hint indicating a parameter can be None

app = FastAPI()
# Creates the main FastAPI application instance



# Add CORS middleware
# this code is for only for restFox Ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins for development/testing
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],        # Allow all headers
)
#--------------------------------------------------------------------------------------------------------------
class BookcreateModel(BaseModel):
    title:str
    author:str
# Defines a data validation model for book creation
# title: Required string field for book title
# author: Required string field for book author
#------------------------------------------------------------------------------------------------------------------
@app.post("/create_book")
async def create_book(book_data:BookcreateModel):
    return {
        "title":book_data.title,
        "author":book_data.author
    }
# @app.post: Creates a POST endpoint at /create_book
# book_data: BookcreateModel: Automatically validates incoming JSON against the model
# return: Returns the validated book data as JSON response
#------------------------------------------------------------------------------------------------------------------------------
# Header(None): Extracts specific HTTP headers from the request, returns None if not present
# Optional[str]: Each header parameter can be None or string
# Parameters extract common headers:
# user_agent: Browser/client information
# accept_encoding: Compression formats client accepts
# referer: Previous page URL that linked to this request
# connection: Connection management (keep-alive, close)
# accept_language: Client's preferred languages
# host: Target server hostname
# @app.get: Creates a GET endpoint at /get_headers

@app.get('/get_headers')
async def get_all_request_headers(
    user_agent: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    connection: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
):
    request_headers = {}
    request_headers["User-Agent"] = user_agent
    request_headers["Accept-Encoding"] = accept_encoding
    request_headers["Referer"] = referer
    request_headers["Accept-Language"] = accept_language
    request_headers["Connection"] = connection
    request_headers["Host"] = host

    return request_headers

# Creates an empty dictionary to store header values
# Populates the dictionary with extracted header values
# Returns the headers as a JSON response

#-------------------------------------------------------------------------------------------------------------------------------------------------------------