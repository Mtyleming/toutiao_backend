from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserParam(BaseModel):
    username: str
    password: str

# 用户信息基础数据模型
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes = True
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes = True
    )


class UserUpdateParam(UserInfoBase):
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    model_config = ConfigDict(
        from_attributes=True
    )

class passwordParam(BaseModel):
    oldPassword: str = Field(None, max_length=50, description="旧密码")
    newPassword: str = Field(None, max_length=50, description="新密码")
