# from passlib.context import CryptContext
#
# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )
#
#
# def get_hash(param: str):
#     return pwd_context.hash(param)

from argon2 import PasswordHasher

ph = PasswordHasher()

# 加密
def get_hash(param: str) -> str:
    return ph.hash(param)

# 验证
def verify_password(hash: str, password: str) -> bool:
    try:
        return ph.verify(hash, password)
    except Exception:
        return False

