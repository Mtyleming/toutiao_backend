from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette import status

from config.db_confing import get_db
from crud.user import database_exists, create_user, generate_token, update_user, update_user_password_by_id
from models.users import User
from schemas.user import UserParam, UserAuthResponse, UserInfoResponse, UserUpdateParam, passwordParam
from utils import security
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(user_param: UserParam, db: AsyncSession = Depends(get_db)):
    # 判断用户是否存在
    if await database_exists(user_param, db):
        raise Exception("用户已存在")

    # 创建用户
    entity = await create_user(user_param, db)

    # 生成用户令牌
    token = await generate_token(entity.id, db)

    # 返回注册结果
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": entity.id,
    #             "username": entity.username,
    #             "bio": entity.bio,
    #             "avatar": entity.avatar
    #         }
    #     }
    # }
    res = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(entity))
    return success_response(data=res)


@router.post("/login")
async def login(user_param: UserParam, db: AsyncSession = Depends(get_db)):
    entity = await database_exists(user_param, db)
    if not entity:
        raise Exception("用户不存在")
    flag = security.verify_password(entity.password, user_param.password)
    if not flag:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await generate_token(entity.id, db)
    res = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(entity))
    return success_response(meg="登录成功", data=res)


@router.get("/info")
async def user_info(user: User = Depends(get_current_user)):
    return success_response(meg="获取用户信息成功", data=UserInfoResponse.model_validate(user))


@router.put("/update")
async def update_user_info(user_date: UserUpdateParam, user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    res = await update_user(user_date, user.username, db)
    return success_response(meg="更新用户信息成功", data=UserInfoResponse.model_validate(res))

@router.put("/password")
async def update_user_password(password_param: passwordParam, user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    user_param = UserParam(username=user.username, password=user.password)
    entity = await database_exists(user_param, db)
    if not entity:
        raise Exception("用户不存在")
    flag = security.verify_password(entity.password, password_param.oldPassword)
    if not flag:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="旧密码错误")

    update_flag = await update_user_password_by_id(entity.id, password_param.newPassword, db)

    return success_response(meg="更新用户密码成功" if update_flag else "更新用户密码失败")
