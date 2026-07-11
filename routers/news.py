from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_confing import get_db
from crud.news import get_categories

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def categories(page:int = 0, limit:int = 100, db: AsyncSession = Depends(get_db)):

    categories = await get_categories(db, page, limit)
    return {
        "code":200,
        "message": "获取分类成功",
        "data":categories
    }

@router.get("/list")
async def get_news(page:int = 0, limit:int = 100,category_id:int = None, db: AsyncSession = Depends(get_db)):

    return {
        "code":200,
        "message": "获取新闻成功",
        "data": []
    }

