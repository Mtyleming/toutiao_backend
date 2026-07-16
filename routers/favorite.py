from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud.favorite import is_news_favorite, add_news_favorite, remove_news_favorite, get_favorite_list, \
    remove_all_favorites
from config.db_confing import get_db
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteNewsItemResponse, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    flag = await is_news_favorite(db, user.id, news_id)
    return success_response(meg="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=flag))


@router.post("/add")
async def add_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    flag = await add_news_favorite(db, user.id, news_id)
    return success_response(meg="添加收藏成功", data=FavoriteCheckResponse(isFavorite=flag))


@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    flag = await remove_news_favorite(db, user.id, news_id)
    return success_response(meg="取消收藏成功", data=FavoriteCheckResponse(isFavorite=flag))


@router.get("/list")
async def favorite_list(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize")
):
    res, total = await get_favorite_list(db, user.id, page, page_size)

    dto = FavoriteListResponse(total=total, hasMore=total > page * page_size, list=res)

    return success_response(meg="取消收藏成功", data=dto)

@router.delete("/clear")
async def remove_favorite(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    flag = await remove_all_favorites(db, user.id)
    return success_response(meg="清空收藏成功", data=FavoriteCheckResponse(isFavorite=flag))
