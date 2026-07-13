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
