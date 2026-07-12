from fastapi import APIRouter
from fastapi import Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_confing import get_db
from crud.news import get_categories, get_news_list, get_news_count, get_news_detail, add_news_view, get_related_news

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
async def get_list(
        page:int = 1,
        page_size:int = Query(10, ge=1, le=100,alias="pageSize"),
        category_id:int = Query(None, ge=0, alias="categoryId"),
        db: AsyncSession = Depends(get_db)
):

    news = await get_news_list(db, page, page_size, category_id)
    num = await get_news_count(db, category_id)
    return {
        "code":200,
        "message": "获取新闻成功",
        "total": num,
        "data": news,
        "has_more": num > (page-1) * page_size + len(news)  # 是否有更多
    }

@router.get("/count")
async def get_count(
        category_id:int = Query(None, ge=0, alias="categoryId"),
        db: AsyncSession = Depends(get_db)
):

    num = await get_news_count(db, category_id)
    return {
        "code":200,
        "message": "获取新闻数量成功",
        "data": num
    }

@router.get("/getDetail")
async def get_detail(
        new_id:int = Query(..., ge=0, alias="newId"),
        db: AsyncSession = Depends(get_db)
):

    res = await get_news_detail(db, new_id)
    if res is None:
        raise Exception("新闻不存在")
    await add_news_view(res,db)
    related_news = await get_related_news(db,res.id,res.category_id,5)
    return {
        "code":200,
        "message": "获取新闻详情成功",
        "data": {
            "id": res.id,
            "title": res.title,
            "description": res.description,
            "content": res.content,
            "image": res.image,
            "author": res.author,
            "publish_time": res.publish_time,
            "category_id": res.category_id,
            "views": res.views,
            "relatedNews":related_news
        }

    }
