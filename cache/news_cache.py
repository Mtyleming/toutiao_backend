from typing import List, Any

from config.cache_config import get_list_or_dict, set_cache

CATEGORIES_KEY = "news:categories"


##获取分类缓存
async def get_news_cache():
    return await get_list_or_dict(CATEGORIES_KEY)


## 写入新闻分类缓存
async def set_news_cache(data: List[dict[str, Any]], expire: int = 3600):
    await set_cache(CATEGORIES_KEY, data, expire)
