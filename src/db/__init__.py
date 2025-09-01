from fastapi import FastAPI
from src.books.book_routes import book_router
from src.auth.routers import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tag.routes import tags_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("server is stopping")

version = 'v1'

# app = FastAPI(
#     title='Bookly',
#     description='A RESTful API for a book review web service',
#     version=version,
# )

app= FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version,
    
)

app.include_router(book_router,prefix="/books", tags=['books'])
app.include_router(auth_router, tags=['users'])
app.include_router(review_router, prefix=f"/reviews", tags=["reviews"]) #add this
app.include_router(tags_router, prefix="/tags", tags=["tags"])