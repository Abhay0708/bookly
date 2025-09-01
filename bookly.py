from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Add CORS middleware
# this code is for only for restFox Ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins for development/testing
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],        # Allow all headers
)

class BookcreateModel(BaseModel):
    title:str
    author:str
    
@app.post("/create_book")
async def create_book(book_data:BookcreateModel):
    return {
        "title":book_data.title,
        "author":book_data.author
    }
    
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