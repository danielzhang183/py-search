# Coze API Python 集成指南

## 简介

Coze（扣子）是字节跳动的AI应用开发平台。本指南介绍如何在Python项目中集成Coze API。

## 安装

### 安装 cozepy SDK

```bash
pip3 install cozepy
```

或者使用：

```bash
python3 -m pip install cozepy
```

## 认证方式

Coze API 支持多种认证方式：

### 1. Personal Access Token (PAT) - 推荐

最简单的方式，适合快速开始。

```python
from cozepy import Coze
from cozepy.auth import PatAuth

# 创建PAT认证
auth = PatAuth(pat="your_pat_token")
client = Coze(auth=auth)
```

**获取PAT Token:**
1. 访问 https://www.coze.cn
2. 进入个人设置
3. 创建 Personal Access Token

### 2. JWT OAuth

适合生产环境，更安全。

```python
from cozepy import Coze
from cozepy.auth import JwtAuth

# 创建JWT认证
auth = JwtAuth(
    app_id="your_app_id",
    private_key_path="private_key.pem"
)
client = Coze(auth=auth)
```

**设置JWT认证:**
1. 在 coze.cn 创建 OAuth JWT 应用
2. 下载私钥文件（private_key.pem）
3. 配置API权限

### 3. Web OAuth

适合Web应用。

### 4. PKCE OAuth

适合移动应用。

## 基本使用

### 与Bot对话

```python
from cozepy import Coze
from cozepy.auth import PatAuth

# 初始化客户端
auth = PatAuth(pat="your_pat_token")
client = Coze(auth=auth)

# 发送消息
response = client.chat.create(
    bot_id="your_bot_id",
    user_id="user_123",
    query="你好，请介绍一下Python"
)

print(response.content)
```

### 流式对话（实时响应）

```python
# 流式对话
stream = client.chat.stream(
    bot_id="your_bot_id",
    user_id="user_123",
    query="请详细介绍Python的特性"
)

# 实时接收回复
for chunk in stream:
    print(chunk.content, end='', flush=True)
```

### 获取Bot列表

```python
# 获取所有bot
bots = client.bots.list()
for bot in bots:
    print(f"Bot ID: {bot.id}, Name: {bot.name}")
```

### 获取Bot信息

```python
# 获取特定bot信息
bot = client.bots.get(bot_id="your_bot_id")
print(f"Bot名称: {bot.name}")
print(f"Bot描述: {bot.description}")
```

## 完整示例

查看 `scripts/coze_integration_example.py` 获取完整示例代码。

## 在 py-search 项目中使用

项目已内置 Coze 集成模块 `py_search.coze_integration`，可以直接使用：

### 基本使用

```python
from py_search import CSVReader
from py_search.coze_integration import CozeClient, create_coze_client_from_env

# 方式1: 从环境变量创建（推荐）
client = create_coze_client_from_env()

# 方式2: 手动创建
client = CozeClient(access_token="your_pat_token")

# 读取CSV文件信息
reader = CSVReader(directory="./examples")
info = reader.get_file_info("example.csv")

# 使用Coze Bot分析
result = client.analyze_csv_data(
    bot_id="your_bot_id",
    user_id="user_123",
    csv_summary=f"文件: {info['filename']}, 行数: {info['rows']}, 列数: {info['columns']}",
    question="这个数据集有什么特点？"
)
print(result)
```

### 直接分析CSV文件

```python
# 直接上传CSV文件路径进行分析
result = client.upload_csv_for_analysis(
    bot_id="your_bot_id",
    user_id="user_123",
    csv_file_path="./examples/example.csv",
    question="请分析这个CSV文件的数据结构"
)
```

### 在CLI中使用

未来可以在 `cli.py` 中添加 `--coze` 参数，使用Coze Bot分析CSV数据。

## 环境变量配置

建议使用环境变量存储敏感信息：

```bash
# 在 ~/.zshrc 或 ~/.bash_profile 中添加
export COZE_PAT_TOKEN="your_pat_token"
export COZE_BOT_ID="your_bot_id"
```

在代码中使用：

```python
import os

pat_token = os.getenv("COZE_PAT_TOKEN")
bot_id = os.getenv("COZE_BOT_ID")
```

## 错误处理

```python
from cozepy.exceptions import CozeAPIError

try:
    response = client.chat.create(
        bot_id=bot_id,
        user_id="user_123",
        query="你好"
    )
except CozeAPIError as e:
    print(f"API错误: {e.status_code} - {e.message}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 最佳实践

1. **使用环境变量**: 不要在代码中硬编码token
2. **错误处理**: 始终包含适当的错误处理
3. **连接池**: 对于高并发场景，考虑使用连接池
4. **异步调用**: 对于大量请求，使用异步SDK
5. **速率限制**: 注意API速率限制，适当添加重试机制

## 异步使用

cozepy 也支持异步调用：

```python
import asyncio
from cozepy.async_client import AsyncCoze
from cozepy.auth import PatAuth

async def async_chat():
    auth = PatAuth(pat="your_pat_token")
    client = AsyncCoze(auth=auth)
    
    response = await client.chat.create(
        bot_id="your_bot_id",
        user_id="user_123",
        query="你好"
    )
    print(response.content)

# 运行
asyncio.run(async_chat())
```

## 资源链接

- **官方文档**: https://www.coze.cn/docs
- **GitHub仓库**: https://github.com/coze-dev/coze-py
- **PyPI包**: https://pypi.org/project/cozepy/
- **Gitee镜像**: https://gitee.com/coze-dev/coze-py

## 常见问题

### Q: 如何获取Bot ID？

A: 在coze.cn中创建或选择Bot后，Bot ID会显示在Bot详情页面。

### Q: PAT Token过期了怎么办？

A: 在coze.cn的个人设置中重新生成新的PAT Token。

### Q: 支持哪些Python版本？

A: cozepy 支持 Python 3.7+

### Q: 如何提高API调用速度？

A: 使用异步SDK (`AsyncCoze`) 可以显著提高并发性能。
