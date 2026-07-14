#根据token查询用户 返回用户
from fastapi import Header
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_confing import get_db
from crud.user import get_user_by_token


async def get_current_user(authorization: str = Header(..., alias="Authorization"), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_token(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="无效的token")
    return user
