from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from cache import news_cache
from models.news import Category, News
from sqlalchemy import select, func


async def get_categories(db: AsyncSession, page: int = 0, limit: int = 100):
    cache_categories = await news_cache.get_news_cache()
    if cache_categories:
        return cache_categories


    result = await db.execute(select(Category).offset(page).limit(limit))
    cache_categories = result.scalars().all()

    if cache_categories:
        value = jsonable_encoder(cache_categories)
        await news_cache.set_news_cache(value)
    return cache_categories


async def get_news_list(db: AsyncSession, page: int = 1, page_size: int = 10, category_id: int = None):
    offset = (page - 1) * page_size
    query = select(News)

    # 动态添加条件（类似 Java 的 if 判断拼 SQL）
    if category_id is not None:
        query = query.where(News.category_id == category_id)
    # 分页
    query = query.offset(offset).limit(page_size)

    res = await db.execute(query)
    return res.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int = None):
    query = select(func.count(News.id))
    if category_id is not None:
        query = query.where(News.category_id == category_id)
    res = await db.execute(query)
    return res.scalar_one()


async def get_news_detail(db: AsyncSession, new_id: int):
    query = select(News).where(News.id == new_id)
    res = await db.execute(query)
    return res.scalars().one_or_none()


async def add_news_view(news: News, db: AsyncSession):
    news.views += 1
    await db.commit()


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int):
    query = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    res = await db.execute(query)
    # return res.scalars().all()
    resList = res.scalars().all()
    return [{
        "id": new.id,
        "title": new.title,
        "description": new.description,
        "content": new.content,
        "image": new.image,
        "author": new.author,
        "publish_time": new.publish_time,
        "category_id": new.category_id,
        "views": new.views
    } for new in resList]
