import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.user import UserParam
from utils import security


async def database_exists(user_param: UserParam, db: AsyncSession):
    query = select(User).where(User.username == user_param.username)
    res = await db.execute(query)
    return res.scalar_one_or_none()

async def create_user(user_param: UserParam, db: AsyncSession) -> User:
    password = security.get_hash(user_param.password)
    entity = User(username=user_param.username, password=password)
    db.add(entity)
    # flush 获取自增 id，由 get_db 在请求结束时统一 commit
    await db.flush()
    return entity

async def generate_token(user_id: int, db: AsyncSession) -> str:
    token = str(uuid.uuid4())
    expires = datetime.datetime.now() + datetime.timedelta(days=7)

    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    entity = result.scalar_one_or_none()
    if entity:
        entity.expires_at = expires
        entity.token = token
    else:
        db.add(UserToken(user_id=user_id, token=token, expires_at=expires))
    return token

