#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coze API 集成模块

提供与字节跳动Coze平台的集成功能，可以将CSV数据发送到Coze进行AI分析
"""

import os
from typing import Optional, Dict, Any, List
import json


class CozeClient:
    """Coze API 客户端"""
    
    def __init__(self, 
                 app_id: Optional[str] = None,
                 private_key_path: Optional[str] = None,
                 access_token: Optional[str] = None,
                 api_key: Optional[str] = None):
        """
        初始化Coze客户端
        
        Args:
            app_id: Coze应用ID（OAuth JWT方式）
            private_key_path: 私钥文件路径（OAuth JWT方式）
            access_token: 访问令牌（PAT方式）
            api_key: API密钥（API Key方式）
        """
        self.app_id = app_id or os.getenv('COZE_APP_ID')
        self.private_key_path = private_key_path or os.getenv('COZE_PRIVATE_KEY_PATH')
        self.access_token = access_token or os.getenv('COZE_ACCESS_TOKEN')
        self.api_key = api_key or os.getenv('COZE_API_KEY')
        
        # 尝试导入cozepy
        try:
            import cozepy
            self.cozepy = cozepy
            self._client = None
        except ImportError:
            raise ImportError(
                "cozepy未安装，请运行: pip3 install cozepy\n"
                "或访问: https://pypi.org/project/cozepy/"
            )
    
    def _get_client(self):
        """获取Coze客户端实例"""
        if self._client is not None:
            return self._client
        
        # 优先使用PAT方式（最简单）
        if self.access_token:
            self._client = self.cozepy.Coze(
                api_key=self.access_token,
                base_url="https://api.coze.cn"
            )
        # 使用API Key
        elif self.api_key:
            self._client = self.cozepy.Coze(
                api_key=self.api_key,
                base_url="https://api.coze.cn"
            )
        # 使用OAuth JWT（需要app_id和私钥）
        elif self.app_id and self.private_key_path:
            if not os.path.exists(self.private_key_path):
                raise FileNotFoundError(f"私钥文件不存在: {self.private_key_path}")
            
            # 使用JWT认证
            from cozepy.auth import JwtAuth
            auth = JwtAuth(
                app_id=self.app_id,
                private_key_path=self.private_key_path
            )
            self._client = self.cozepy.Coze(
                auth=auth,
                base_url="https://api.coze.cn"
            )
        else:
            raise ValueError(
                "需要提供认证信息：\n"
                "1. access_token (PAT方式，推荐)\n"
                "2. api_key (API Key方式)\n"
                "3. app_id + private_key_path (OAuth JWT方式)\n"
                "或设置环境变量：COZE_ACCESS_TOKEN, COZE_API_KEY, COZE_APP_ID, COZE_PRIVATE_KEY_PATH"
            )
        
        return self._client
    
    def chat(self, 
             bot_id: str,
             user_id: str,
             query: str,
             conversation_id: Optional[str] = None,
             stream: bool = False) -> Dict[str, Any]:
        """
        与Coze Bot对话
        
        Args:
            bot_id: Bot ID
            user_id: 用户ID
            query: 用户查询
            conversation_id: 会话ID（可选，用于多轮对话）
            stream: 是否使用流式响应
            
        Returns:
            对话响应
        """
        client = self._get_client()
        
        try:
            if stream:
                # 流式响应
                response = client.chat.stream(
                    bot_id=bot_id,
                    user_id=user_id,
                    query=query,
                    conversation_id=conversation_id
                )
                return {"stream": response}
            else:
                # 普通响应
                response = client.chat(
                    bot_id=bot_id,
                    user_id=user_id,
                    query=query,
                    conversation_id=conversation_id
                )
                return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            raise Exception(f"Coze API调用失败: {str(e)}")
    
    def analyze_csv_data(self,
                        bot_id: str,
                        user_id: str,
                        csv_summary: str,
                        question: Optional[str] = None) -> Dict[str, Any]:
        """
        使用Coze Bot分析CSV数据摘要
        
        Args:
            bot_id: Bot ID
            user_id: 用户ID
            csv_summary: CSV数据摘要（行数、列数、列名等信息）
            question: 要询问的问题（可选）
            
        Returns:
            AI分析结果
        """
        query = f"请分析以下CSV数据信息：\n{csv_summary}"
        if question:
            query += f"\n\n问题：{question}"
        
        return self.chat(bot_id=bot_id, user_id=user_id, query=query)
    
    def upload_csv_for_analysis(self,
                                bot_id: str,
                                user_id: str,
                                csv_file_path: str,
                                question: Optional[str] = None) -> Dict[str, Any]:
        """
        上传CSV文件路径给Coze Bot进行分析
        
        Args:
            bot_id: Bot ID
            user_id: 用户ID
            csv_file_path: CSV文件路径
            question: 要询问的问题（可选）
            
        Returns:
            AI分析结果
        """
        # 读取CSV文件基本信息
        from .csv_handler import CSVReader
        
        reader = CSVReader()
        try:
            info = reader.get_file_info(csv_file_path)
            summary = f"""
CSV文件: {info['filename']}
行数: {info['rows']}
列数: {info['columns']}
列名: {', '.join(info['column_names'])}
"""
            return self.analyze_csv_data(bot_id, user_id, summary, question)
        except Exception as e:
            raise Exception(f"读取CSV文件失败: {str(e)}")


def create_coze_client_from_env() -> CozeClient:
    """
    从环境变量创建Coze客户端（便捷函数）
    
    环境变量：
    - COZE_ACCESS_TOKEN: PAT访问令牌（推荐）
    - COZE_API_KEY: API密钥
    - COZE_APP_ID: 应用ID（OAuth JWT）
    - COZE_PRIVATE_KEY_PATH: 私钥路径（OAuth JWT）
    
    Returns:
        CozeClient实例
    """
    return CozeClient()
