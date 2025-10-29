# This is a comprehensive SQLModel database schema for a book management system with users, books, reviews, and tags.
# Here's a detailed explanation of each component:
from sqlmodel import SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime,date
import uuid
from typing import Optional,List
# SQLModel: FastAPI's ORM that combines Pydantic and SQLAlchemy
# Field, Column: Define database fields and their properties
# Relationship: Define relationships between tables
# pg: PostgreSQL-specific data types
# datetime, date: For timestamp and date fields
# uuid: For unique identifiers
# Optional, List: Type hints for nullable fields and lists
# if TYPE_CHECKING:
# from src.books.models import BooK
#----------------------------------------------------------------------------------------------------------------------------
class User(SQLModel, table=True):
    __tablename__ = "user_accounts"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role:str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    ) 
    is_verified: bool = Field(default=False)
    email: str
    password_hash: str =Field(exclude= True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    # add this
    books: List["BooK"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    def __repr__(self) -> str:
        return f"<User {self.username}>"
# Key Fields:
# uid: Primary key using UUID (Universally Unique Identifier)
# username: User's login name
# first_name, last_name: Optional user details
# role: User role with default "user" value
# is_verified: Boolean for email verification status
# email: User's email address
# password_hash: Encrypted password (excluded from serialization)
# created_at, updated_at: Automatic timestamps
# Relationships:
# One-to-Many with Books: A user can own multiple books
# One-to-Many with Reviews: A user can write multiple reviews
#--------------------------------------------------------------------------------------------------------------------------
class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)
#=-===================================================================================================================================
class BooK(SQLModel, table=True):
    __tablename__ = "books"
    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
        
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language:str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="books") #add this
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tags: List["Tag"] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    
    def __repr__(self) -> str:
        return f"<Book {self.title}>"

# Key Fields:
# uid: Primary key (UUID)
# title, author, publisher: Book metadata
# published_date: Date type for publication date
# page_count: Integer for book length
# language: Book's language
# user_uid: Foreign key linking to user who added the book
# Relationships:
# Many-to-One with User: Each book belongs to one user
# One-to-Many with Reviews: A book can have multiple reviews
# Many-to-Many with Tags: A book can have multiple tags    
#===================================================================================================================================    
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(lt=5)
    review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[BooK] = Relationship(back_populates="reviews")
    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
# Key Fields:
# uid: Primary key (UUID)
# rating: Integer rating with constraint lt=5 (less than 5)
# review_text: Text content of the review
# user_uid, book_uid: Foreign keys to User and Book
# Relationships:
# Many-to-One with User: Each review belongs to one user
# Many-to-One with Book: Each review is for one book
#===================================================================================================================================  
class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["BooK"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
# Key Fields:
# uid: Primary key (UUID)
# name: Tag name (e.g., "Science Fiction", "Programming")
# Relationships:
# Many-to-Many with Books: Tags can be applied to multiple books
#=================================================================================================================================
