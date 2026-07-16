from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


# 检查收藏状态：当前用户 是否 收藏了这一条新闻
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None


# 添加收藏（已收藏则直接返回 True，避免唯一约束报错）
async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    if await is_news_favorite(db, user_id, news_id):
        return True

    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite is not None


# 取消收藏
async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    sql = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(sql)
    await db.commit()
    return result.rowcount > 0


# 获取收藏列表：获取的是某个用户的收藏列表 + 分页功能
async def get_favorite_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    # offset 必须在 Python 里算好，MySQL 的 LIMIT 不支持 :page_size*(:page-1) 这种表达式
    offset = (page - 1) * page_size
    query = text(
        "SELECT news.*, favorite.id AS favorite_id, favorite.created_at AS favorite_time "
        "FROM news "
        "INNER JOIN favorite ON news.id = favorite.news_id "
        "WHERE favorite.user_id = :user_id "
        "ORDER BY favorite.created_at DESC "
        "LIMIT :offset, :page_size"
    )
    count = await db.execute(text("SELECT COUNT(*) FROM favorite WHERE user_id = :user_id"), {"user_id": user_id})
    res = await db.execute(query, {
        "user_id": user_id,
        "offset": offset,
        "page_size": page_size,
    })
    return res.mappings().all(), count.scalar_one()


# 清空收藏列表：当前用户的收藏列表
async def remove_all_favorites(
        db: AsyncSession,
        user_id: int
):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)

    # 返回一个删除的数量
    return result.rowcount > 0
