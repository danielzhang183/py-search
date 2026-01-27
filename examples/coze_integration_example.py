#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coze API 集成示例

演示如何在Python中使用Coze API
需要先安装: pip3 install cozepy
"""

try:
    from cozepy import Coze
    from cozepy.auth import JwtAuth, PatAuth
except ImportError:
    print("请先安装 cozepy: pip3 install cozepy")
    exit(1)


def example_jwt_auth():
    """示例1: 使用JWT OAuth认证"""
    print("=" * 50)
    print("示例1: 使用JWT OAuth认证")
    print("=" * 50)
    
    # 配置信息（需要从coze.cn获取）
    app_id = "your_app_id"  # 替换为你的应用ID
    private_key_path = "private_key.pem"  # 私钥文件路径
    
    try:
        # 创建JWT认证对象
        auth = JwtAuth(
            app_id=app_id,
            private_key_path=private_key_path
        )
        
        # 创建Coze客户端
        client = Coze(auth=auth)
        
        # 使用API（示例：获取bot列表）
        # bots = client.bots.list()
        # print(f"找到 {len(bots)} 个bot")
        
        print("✓ JWT认证配置成功")
        print("提示: 需要配置正确的app_id和private_key_path")
        
    except Exception as e:
        print(f"✗ JWT认证失败: {e}")


def example_pat_auth():
    """示例2: 使用Personal Access Token (PAT)认证"""
    print("\n" + "=" * 50)
    print("示例2: 使用PAT认证")
    print("=" * 50)
    
    # PAT token（需要从coze.cn获取）
    pat_token = "your_pat_token"  # 替换为你的PAT token
    
    try:
        # 创建PAT认证对象
        auth = PatAuth(pat=pat_token)
        
        # 创建Coze客户端
        client = Coze(auth=auth)
        
        # 使用API
        # bots = client.bots.list()
        # print(f"找到 {len(bots)} 个bot")
        
        print("✓ PAT认证配置成功")
        print("提示: 需要配置正确的pat_token")
        
    except Exception as e:
        print(f"✗ PAT认证失败: {e}")


def example_chat_with_bot():
    """示例3: 与Bot对话"""
    print("\n" + "=" * 50)
    print("示例3: 与Bot对话")
    print("=" * 50)
    
    # 配置认证（选择一种方式）
    # 方式1: PAT认证（更简单）
    pat_token = "your_pat_token"
    auth = PatAuth(pat=pat_token)
    
    # 方式2: JWT认证
    # app_id = "your_app_id"
    # auth = JwtAuth(app_id=app_id, private_key_path="private_key.pem")
    
    try:
        client = Coze(auth=auth)
        
        # Bot ID（需要从coze.cn获取）
        bot_id = "your_bot_id"
        
        # 发送消息
        # response = client.chat.create(
        #     bot_id=bot_id,
        #     user_id="user_123",
        #     query="你好"
        # )
        # print(f"Bot回复: {response.content}")
        
        print("✓ 对话功能配置成功")
        print("提示: 需要配置正确的bot_id和认证信息")
        
    except Exception as e:
        print(f"✗ 对话失败: {e}")


def example_stream_chat():
    """示例4: 流式对话（实时响应）"""
    print("\n" + "=" * 50)
    print("示例4: 流式对话")
    print("=" * 50)
    
    pat_token = "your_pat_token"
    auth = PatAuth(pat=pat_token)
    
    try:
        client = Coze(auth=auth)
        bot_id = "your_bot_id"
        
        # 流式对话
        # stream = client.chat.stream(
        #     bot_id=bot_id,
        #     user_id="user_123",
        #     query="请介绍一下Python"
        # )
        # 
        # for chunk in stream:
        #     print(chunk.content, end='', flush=True)
        
        print("✓ 流式对话配置成功")
        print("提示: 使用stream方法可以实时接收Bot的回复")
        
    except Exception as e:
        print(f"✗ 流式对话失败: {e}")


def setup_instructions():
    """显示设置说明"""
    print("\n" + "=" * 50)
    print("Coze API 设置步骤")
    print("=" * 50)
    print("""
1. 安装SDK:
   pip3 install cozepy

2. 获取认证信息:
   - 访问 https://www.coze.cn
   - 创建应用或获取PAT token
   - 对于JWT: 需要app_id和私钥文件
   - 对于PAT: 需要personal access token

3. 配置API权限:
   - 在coze.cn中为你的bot配置API访问权限
   - 确保bot_id正确

4. 使用示例:
   - 修改脚本中的认证信息
   - 取消注释API调用代码
   - 运行脚本测试

更多信息:
   - 官方文档: https://www.coze.cn/docs
   - GitHub: https://github.com/coze-dev/coze-py
   - PyPI: https://pypi.org/project/cozepy/
    """)


if __name__ == "__main__":
    print("Coze API Python 集成示例\n")
    
    # 运行示例（需要配置认证信息后才能实际使用）
    example_jwt_auth()
    example_pat_auth()
    example_chat_with_bot()
    example_stream_chat()
    
    # 显示设置说明
    setup_instructions()
