# Toutiao Backend

基于 FastAPI 的今日头条后端项目。

## 项目简介

这是一个使用 Python + FastAPI 构建的后端 API 服务，提供基础的 HTTP 接口。

## 环境要求

- Python 3.10+
- pip

## 快速开始

### 1. 创建并激活虚拟环境

> **注意**：项目路径变更后，旧的 `.venv` 会失效（`uvicorn`、`pip` 等命令无法启动）。需要删除旧环境后重新创建。

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
uvicorn main:app --reload
```

启动后访问：

- API 根地址：http://127.0.0.1:8000/
- 自动文档：http://127.0.0.1:8000/docs

## 常见问题

### 虚拟环境启动不了 / uvicorn 或 pip 无反应

**原因**：虚拟环境是在旧目录（如 `D:\toutiao_backend`）创建的，项目移动到新目录后，`.venv` 内部路径仍指向旧位置，导致启动器失效。

**解决方法**：

```bash
# 1. 删除旧虚拟环境
Remove-Item -Recurse -Force .venv   # Windows PowerShell
# rm -rf .venv                        # macOS / Linux

# 2. 重新创建并安装依赖
python -m venv .venv
.venv\Scripts\activate                # Windows
pip install -r requirements.txt

# 3. 启动服务
uvicorn main:app --reload
```

**临时替代方案**（不重建环境时）：用 `python -m` 方式调用

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### 缓存设置失败：`unknown command 'HELLO'`

**原因**：本机 Redis 版本过旧（例如 2.6.8），而新版 `redis-py` 默认使用 RESP3 协议，连接时会发送 `HELLO` 命令；旧 Redis 不认识该命令。另外旧版也不支持 `SET key value EX 秒数`，会导致设置带过期时间的缓存失败。

**已做兼容处理**（`config/cache_config.py`）：

- 连接时使用 `protocol=2`，避免发送 `HELLO`
- 带过期时间时使用 `SETEX`，兼容 Redis 2.6.x

**建议**：有条件时升级 Redis 到 6.x / 7.x，功能更全、更稳定。

## 缓存相关说明

| 函数 | 用途 | 参数 | 返回值 |
|------|------|------|--------|
| `get_cache(key)` | 读取字符串缓存 | `key`：缓存键 | 字符串或 `None` |
| `get_list_or_dict(key)` | 读取 JSON 列表/字典缓存 | `key`：缓存键 | 解析后的对象或 `None` |
| `set_cache(key, value, expire=3600)` | 写入缓存 | `value` 可为字符串/字典/列表；`expire` 为过期秒数 | 成功 `True`，失败 `False` |

新闻分类接口会先读缓存，没有再查数据库并写入缓存。

## API 接口说明

| 方法 | 路径 | 说明 | 返回值 |
|------|------|------|--------|
| GET | `/` | 健康检查 | `{"message": "Hello World"}` |
| GET | `/hello/{name}` | 问候接口 | `{"message": "Hello {name}"}` |
| POST | `/api/user/register` | 用户注册 | 见下方说明 |
| POST | `/api/user/login` | 用户登录 | 待实现 |

### 用户注册

**请求地址**：`POST /api/user/register`

**请求体**（JSON）：

```json
{
  "username": "你的用户名",
  "password": "你的密码"
}
```

**成功响应**：

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "登录令牌",
    "userInfo": {
      "id": 1,
      "username": "你的用户名",
      "bio": "个人简介",
      "avatar": "头像地址"
    }
  }
}
```

**用户名已存在**：

```json
{
  "code": 400,
  "message": "用户已存在"
}
```

### 示例

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/hello/张三
curl -X POST http://127.0.0.1:8000/api/user/register -H "Content-Type: application/json" -d "{\"username\":\"test\",\"password\":\"123456\"}"
```

## 项目结构

```
toutiao_backend/
├── main.py           # FastAPI 主入口
├── test_main.http    # 接口测试文件
├── requirements.txt  # Python 依赖
├── readme.md         # 项目说明
└── .gitignore        # Git 忽略规则
```

## GitHub 仓库

项目地址：https://github.com/Mtyleming/toutiao_backend

## Git 与 GitHub 使用

### 提交代码

```bash
git add .
git commit -m "你的提交说明"
git push
```

### 拉取最新代码

```bash
git pull
```

## 后续规划

- [x] 添加数据库支持
- [x] 添加用户注册
- [ ] 完善用户登录
