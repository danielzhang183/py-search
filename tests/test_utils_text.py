#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本工具函数测试模块
"""

import os
import sys
import unittest

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_search.utils.text import (
    clean_text,
    extract_numbers,
    extract_emails,
    normalize_url,
    remove_html_tags,
    truncate_text
)


class TestCleanText(unittest.TestCase):
    """clean_text函数测试"""
    
    def test_normal_text(self):
        """测试正常文本"""
        self.assertEqual(clean_text("hello world"), "hello world")
    
    def test_text_with_spaces(self):
        """测试包含多余空白的文本"""
        self.assertEqual(clean_text("  hello   world  "), "hello world")
        self.assertEqual(clean_text("hello\n\nworld"), "hello world")
        self.assertEqual(clean_text("hello\t\tworld"), "hello world")
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text("   "), "")
    
    def test_none_input(self):
        """测试None输入"""
        self.assertEqual(clean_text(None), "")
    
    def test_chinese_text(self):
        """测试中文文本"""
        self.assertEqual(clean_text("  你好  世界  "), "你好 世界")


class TestExtractNumbers(unittest.TestCase):
    """extract_numbers函数测试"""
    
    def test_integers(self):
        """测试提取整数"""
        self.assertEqual(extract_numbers("价格：100元"), [100.0])
        self.assertEqual(extract_numbers("数量：10, 20, 30"), [10.0, 20.0, 30.0])
    
    def test_floats(self):
        """测试提取浮点数"""
        self.assertEqual(extract_numbers("价格：99.99"), [99.99])
        self.assertEqual(extract_numbers("温度：-5.5度"), [-5.5])
    
    def test_mixed(self):
        """测试混合数字"""
        result = extract_numbers("价格：$99.99，数量：10")
        self.assertEqual(len(result), 2)
        self.assertIn(99.99, result)
        self.assertIn(10.0, result)
    
    def test_no_numbers(self):
        """测试无数字文本"""
        self.assertEqual(extract_numbers("hello world"), [])
        self.assertEqual(extract_numbers(""), [])
    
    def test_negative_numbers(self):
        """测试负数"""
        self.assertEqual(extract_numbers("温度：-10度"), [-10.0])


class TestExtractEmails(unittest.TestCase):
    """extract_emails函数测试"""
    
    def test_single_email(self):
        """测试单个邮箱"""
        text = "联系邮箱：contact@example.com"
        result = extract_emails(text)
        self.assertEqual(result, ["contact@example.com"])
    
    def test_multiple_emails(self):
        """测试多个邮箱"""
        text = "邮箱1：user1@example.com，邮箱2：user2@test.org"
        result = extract_emails(text)
        self.assertEqual(len(result), 2)
        self.assertIn("user1@example.com", result)
        self.assertIn("user2@test.org", result)
    
    def test_no_emails(self):
        """测试无邮箱文本"""
        self.assertEqual(extract_emails("hello world"), [])
        self.assertEqual(extract_emails(""), [])
    
    def test_invalid_emails(self):
        """测试无效邮箱格式"""
        text = "这不是邮箱：notanemail"
        self.assertEqual(extract_emails(text), [])
    
    def test_complex_emails(self):
        """测试复杂邮箱格式"""
        text = "邮箱：user.name+tag@example.co.uk"
        result = extract_emails(text)
        self.assertEqual(len(result), 1)


class TestNormalizeUrl(unittest.TestCase):
    """normalize_url函数测试"""
    
    def test_absolute_url(self):
        """测试绝对URL"""
        url = "https://example.com/page?param=value#fragment"
        result = normalize_url(url)
        self.assertEqual(result, "https://example.com/page?param=value")
        self.assertNotIn("#", result)
    
    def test_relative_url(self):
        """测试相对URL"""
        base_url = "https://example.com"
        relative_url = "/page"
        result = normalize_url(relative_url, base_url)
        self.assertEqual(result, "https://example.com/page")
    
    def test_url_with_fragment(self):
        """测试包含fragment的URL"""
        url = "https://example.com#section"
        result = normalize_url(url)
        self.assertEqual(result, "https://example.com")
    
    def test_url_with_query(self):
        """测试包含查询参数的URL"""
        url = "https://example.com?key=value"
        result = normalize_url(url)
        self.assertEqual(result, "https://example.com?key=value")


class TestRemoveHtmlTags(unittest.TestCase):
    """remove_html_tags函数测试"""
    
    def test_simple_tags(self):
        """测试简单标签"""
        text = "<p>Hello World</p>"
        result = remove_html_tags(text)
        self.assertEqual(result, "Hello World")
    
    def test_multiple_tags(self):
        """测试多个标签"""
        text = "<h1>Title</h1><p>Content</p>"
        result = remove_html_tags(text)
        # clean_text会合并空白，所以结果可能是"Title Content"
        self.assertIn("Title", result)
        self.assertIn("Content", result)
        # 验证没有HTML标签
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
    
    def test_nested_tags(self):
        """测试嵌套标签"""
        text = "<div><p>Nested <strong>text</strong></p></div>"
        result = remove_html_tags(text)
        self.assertEqual(result, "Nested text")
    
    def test_no_tags(self):
        """测试无标签文本"""
        text = "Plain text"
        result = remove_html_tags(text)
        self.assertEqual(result, "Plain text")
    
    def test_self_closing_tags(self):
        """测试自闭合标签"""
        text = "Image: <img src='test.jpg' />"
        result = remove_html_tags(text)
        self.assertNotIn("<img", result)


class TestTruncateText(unittest.TestCase):
    """truncate_text函数测试"""
    
    def test_short_text(self):
        """测试短文本（不需要截断）"""
        text = "Hello"
        result = truncate_text(text, max_length=10)
        self.assertEqual(result, "Hello")
    
    def test_long_text(self):
        """测试长文本（需要截断）"""
        text = "This is a very long text that needs to be truncated"
        result = truncate_text(text, max_length=20)
        self.assertEqual(len(result), 20)
        self.assertTrue(result.endswith("..."))
    
    def test_custom_suffix(self):
        """测试自定义后缀"""
        text = "This is a very long text"
        result = truncate_text(text, max_length=10, suffix="[more]")
        # 结果应该是截断后的文本加上后缀
        self.assertTrue(result.endswith("[more]"))
        self.assertLessEqual(len(result), 10 + len("[more]"))
    
    def test_exact_length(self):
        """测试恰好等于最大长度"""
        text = "Exactly 10"
        result = truncate_text(text, max_length=10)
        self.assertEqual(result, "Exactly 10")
    
    def test_empty_text(self):
        """测试空文本"""
        result = truncate_text("", max_length=10)
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
