from fastapi import FastAPI
from src.books.book_routes import book_router
from src.auth.routers import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tag.routes import tags_router
# FastAPI: Main application class
# Router imports: Modular route handlers for different features (books, auth, reviews, tags)
# asynccontextmanager: Decorator for creating async context managers
# init_db: Database initialization function from previous code
#----------------------------------------------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("server is stopping")
# Line-by-line breakdown:
# @asynccontextmanager: Decorator that creates an async context manager
# async def lifespan(app:FastAPI):: Function that handles application startup/shutdown events
# print("Server is starting..."): Startup code - runs BEFORE the app accepts requests
# await init_db(): Creates database tables during startup
# yield: Separation point - everything after runs during shutdown
# print("server is stopping"): Shutdown code - runs AFTER the app stops accepting requests
# Key concept: Code before yield = startup, code after yield = shutdown
version = 'v1'
# Defines API version for documentation and organization
#======================================================================================================================
app= FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version,
    
)
# Parameters explained:
# title: API name shown in OpenAPI docs (Swagger UI)
# description: API description for documentation
# version: API version (appears in docs and OpenAPI schema)
# Missing lifespan=lifespan: Should be added to enable startup/shutdown events
#=========================================================================================================================
app.include_router(book_router,prefix="/books", tags=['books'])
app.include_router(auth_router, tags=['users'])
app.include_router(review_router, prefix=f"/reviews", tags=["reviews"]) #add this
app.include_router(tags_router, prefix="/tags", tags=["tags"])
# Line-by-line breakdown:
# Book Router:
# app.include_router(book_router, prefix="/books", tags=['books'])
# book_router: Router containing book-related endpoints
# prefix="/books": All routes get /books prefix (e.g., /books/create)
# tags=['books']: Groups endpoints under "books" in Swagger UI
# Auth Router:
# app.include_router(auth_router, tags=['users'])
# No prefix: Routes use their original paths (e.g., /login, /register)
# tags=['users']: Groups under "users" section in docs
# Review Router:
# prefix=f"/reviews": Uses f-string (unnecessary here, could be "/reviews")
# Groups review-related endpoints under /reviews prefix
# Tags Router:
# prefix="/tags": All tag endpoints prefixed with /tags
# tags=["tags"]: Documentation grouping
#+===============================================================================================================================