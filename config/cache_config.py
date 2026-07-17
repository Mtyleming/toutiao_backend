import json

import redis.asyncio as redis

# protocol=2：兼容旧版 Redis（不支持 RESP3 / HELLO 命令）
# 当前环境 Redis 版本约为 2.6.8，新版 redis-py 默认会发 HELLO，会报 unknown command 'HELLO'
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
    protocol=2,
)


# 获取缓存字符串
async def get_cache(key: str):
    try:
        res = await redis_client.get(key)
        return res
    except Exception as e:
        print(e)
        return None


# 获取列表或者字典
async def get_list_or_dict(key: str):
    try:
        res = await redis_client.get(key)
        if res is not None:
            return json.loads(res)
        return None
    except Exception as e:
        print(e)
        return None


# 设置缓存
async def set_cache(key: str, value, expire: int = 3600):
    try:
        data = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        # Redis < 2.6.12 不支持 SET key value EX seconds，需用 SETEX
        if expire and expire > 0:
            await redis_client.setex(key, expire, data)
        else:
            await redis_client.set(key, data)
        return True
    except Exception as e:
        print(e)
        return False
