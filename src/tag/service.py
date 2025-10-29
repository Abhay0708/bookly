from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.db.models import Tag

from src.tag.schemas import TagAddModel, TagCreateModel
# status, HTTPException: FastAPI components for HTTP status codes and error responses

# desc, select: SQLModel query builders for SELECT statements and descending ORDER BY

# AsyncSession: Async database session for non-blocking operations

# BookService: Service layer for book-related operations (composition pattern)

# Tag: SQLModel database model for tag table

# TagAddModel, TagCreateModel: Pydantic schemas for input validation
#=======================================================================================================================
book_service = BookService()


server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)
# book_service = BookService(): Creates instance for dependency on book operations

# server_error: Pre-defined HTTP exception for internal server errors (though not used in the code)
#=======================================================================================================================

class TagService:

    async def get_tags(self, session: AsyncSession):
        """Get all tags"""

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()
# Line-by-line breakdown:

# async def get_tags(...): Async method for non-blocking database operations

# statement = select(Tag).order_by(desc(Tag.created_at)): Creates SQL query

# Equivalent SQL: SELECT * FROM tags ORDER BY created_at DESC

# result = await session.exec(statement): Executes query asynchronously

# return result.all(): Returns all tags as a list, ordered by newest first

# Purpose: Retrieves all tags for listing/admin purposes
#========================================================================================================================
    async def add_tags_to_book(
        self, book_uid: str, tag_data: TagAddModel, session: AsyncSession
    ):
        """Add tags to a book"""

        book = await book_service.get_book(book_uid=book_uid, session=session)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        for tag_item in tag_data.tags:
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item.name)
            )

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
# Line-by-line breakdown:

# Book Validation:
# book = await book_service.get_book(...): Reuses BookService to validate book existence

# if not book: raise HTTPException(...): Returns 404 if book doesn't exist

# Tag Processing Loop:
# for tag_item in tag_data.tags:: Iterates through list of tags from TagAddModel

# result = await session.exec(select(Tag).where(Tag.name == tag_item.name)): Checks if tag exists by name

# tag = result.one_or_none(): Gets existing tag or None if not found

# if not tag: tag = Tag(name=tag_item.name): Creates new tag if it doesn't exist

# Relationship Management:
# book.tags.append(tag): Adds tag to book's tags relationship (many-to-many)

# SQLModel handles junction table: Automatically manages BookTag junction table

# Database Operations:
# session.add(book): Adds book to session (includes new relationships)

# await session.commit(): Commits transaction asynchronously

# await session.refresh(book): Refreshes book object to get updated relationships

# return book: Returns book with associated tags

# Purpose: Associates multiple tags with a book, creating tags if they don't exist.
#=======================================================================================================================


    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        """Get tag by uid"""

        statement = select(Tag).where(Tag.uid == tag_uid)

        result = await session.exec(statement)

        return result.first()
# Line-by-line breakdown:

# statement = select(Tag).where(Tag.uid == tag_uid): Query for specific tag by UUID

# result = await session.exec(statement): Execute query asynchronously

# return result.first(): Returns first matching result or None if not found

# Purpose: Helper method for retrieving single tag by UUID
#========================================================================================================================
    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        """Create a tag"""

        statement = select(Tag).where(Tag.name == tag_data.name)

        result = await session.exec(statement)

        tag = result.first()

        if tag:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Tag exists"
            )

        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)

        await session.commit()

        return new_tag
# Line-by-line breakdown:

# Duplicate Check:
# statement = select(Tag).where(Tag.name == tag_data.name): Query for existing tag with same name

# tag = result.first(): Gets existing tag or None

# if tag: raise HTTPException(...): Enforces unique constraint on tag names

# Status code issue: Should be 409 CONFLICT instead of 403 FORBIDDEN

# Tag Creation:
# new_tag = Tag(name=tag_data.name): Creates new Tag instance

# session.add(new_tag): Adds to session (pending transaction)

# await session.commit(): Commits transaction asynchronously

# return new_tag: Returns created tag with generated UUID and timestamp

# Purpose: Creates new tag with uniqueness validation.
#======================================================================================================================
    async def update_tag(
        self, tag_uid, tag_update_data: TagCreateModel, session: AsyncSession
    ):
        """Update a tag"""

        tag = await self.get_tag_by_uid(tag_uid, session)

        update_data_dict = tag_update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

        await session.commit()

        await session.refresh(tag)

        return tag


    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        """Delete a tag"""

        tag = await self.get_tag_by_uid(tag_uid,session)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag does not exist"
            )

        await session.delete(tag)

        await session.commit()