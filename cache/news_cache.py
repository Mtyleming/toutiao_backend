from typing import List, Any

from config.cache_config import get_list_or_dict, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"


##获取分类缓存
async def get_news_cache():
    return await get_list_or_dict(CATEGORIES_KEY)


## 写入新闻分类缓存
async def set_news_cache(data: List[dict[str, Any]], expire: int = 3600):
    await set_cache(CATEGORIES_KEY, data, expire)



# 写入缓存-新闻列表 key = news_list:分类id:页码:每页数量  + 列表数据 + 过期时间
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int = 1800):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


# 读取缓存-新闻列表 key = news_list:分类id:页码:每页数量
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_list_or_dict(key)


# 读取缓存-新闻详情 key = news:detail:新闻id
async def get_cached_news_detail(news_id: int) -> Optional[Dict[str, Any]]:
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_list_or_dict(key)


# 写入缓存-新闻详情 key = news:detail:新闻id + 新闻数据 + 过期时间
async def cache_news_detail(news_id: int, news_data: Dict[str, Any], expire: int = 300) -> bool:
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key, news_data, expire)

