from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category
from sqlalchemy import select

async def get_categories(db: AsyncSession,page:int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(page).limit(limit))
    return result.scalars().all()
