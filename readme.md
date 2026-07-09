# Toutiao Backend

基于 FastAPI 的今日头条后端项目。

## 项目简介

这是一个使用 Python + FastAPI 构建的后端 API 服务，提供基础的 HTTP 接口。

## 环境要求

- Python 3.10+
- pip

## 快速开始

### 1. 创建并激活虚拟环境

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

## API 接口说明

| 方法 | 路径 | 说明 | 返回值 |
|------|------|------|--------|
| GET | `/` | 健康检查 | `{"message": "Hello World"}` |
| GET | `/hello/{name}` | 问候接口 | `{"message": "Hello {name}"}` |

### 示例

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/hello/张三
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

- [ ] 添加数据库支持
- [ ] 添加用户认证
- [ ] 完善业务 API
