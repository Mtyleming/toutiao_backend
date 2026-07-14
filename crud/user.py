import datetime
import uuid

from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.user import UserParam, UserUpdateParam
from utils import security


async def database_exists(user_param: UserParam, db: AsyncSession) -> User | None:
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


# 根据token查询用户
async def get_user_by_token(token: str, db: AsyncSession) -> User | None:
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    entity = result.scalar_one_or_none()
    if not entity or entity.expires_at < datetime.datetime.now():
        return None
    query = select(User).where(User.id == entity.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_user(user_date: UserUpdateParam, username: str, db: AsyncSession) -> User | None:
    user_param = UserParam(username=username,password="")
    # entity = await database_exists(user_param, db)
    # if not entity:
    #     raise Exception("用户不存在")
    # entity.nickname = user_date.nickname
    # entity.gender = user_date.gender
    # entity.bio = user_date.bio
    # entity.avatar = user_date.avatar
    # entity.phone = user_date.phone
    query = update(User).where(User.username == username).values(user_date.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    res = await db.execute(query)
    if res.rowcount == 0:
        raise Exception("用户不存在")
    return await database_exists(user_param, db)

async def update_user_password_by_id(user_id: int, password: str, db: AsyncSession) -> bool:
    password = security.get_hash(password)
    query = update(User).where(User.id == user_id).values(password=password)
    res = await db.execute(query)
    if res.rowcount == 0:
        raise Exception("修改失败")
    return True
