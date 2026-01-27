#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具函数测试模块
"""

import os
import sys
import unittest
import tempfile
import csv
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_search.utils.file import (
    save_to_csv,
    save_to_json,
    save_to_excel,
    ensure_directory,
    get_file_size,
    format_file_size
)


class TestSaveToCsv(unittest.TestCase):
    """save_to_csv函数测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.csv")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_save_simple_data(self):
        """测试保存简单数据"""
        data = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 30}
        ]
        result = save_to_csv(data, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        # 验证内容
        with open(self.test_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['name'], 'Alice')
    
    def test_save_empty_data(self):
        """测试保存空数据"""
        result = save_to_csv([], self.test_file)
        self.assertFalse(result)
    
    def test_append_mode(self):
        """测试追加模式"""
        data1 = [{'name': 'Alice', 'age': 25}]
        data2 = [{'name': 'Bob', 'age': 30}]
        
        save_to_csv(data1, self.test_file, mode='w')
        save_to_csv(data2, self.test_file, mode='a')
        
        # 验证追加
        with open(self.test_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
    
    def test_chinese_data(self):
        """测试中文数据"""
        data = [{'姓名': '张三', '年龄': '25'}]
        result = save_to_csv(data, self.test_file)
        self.assertTrue(result)
        
        # 验证中文内容
        with open(self.test_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            self.assertIn('张三', content)


class TestSaveToJson(unittest.TestCase):
    """save_to_json函数测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.json")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_save_dict(self):
        """测试保存字典"""
        data = {'name': 'Alice', 'age': 25}
        result = save_to_json(data, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        # 验证内容
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            self.assertEqual(loaded, data)
    
    def test_save_list(self):
        """测试保存列表"""
        data = [{'name': 'Alice'}, {'name': 'Bob'}]
        result = save_to_json(data, self.test_file)
        self.assertTrue(result)
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            self.assertEqual(loaded, data)
    
    def test_chinese_data(self):
        """测试中文数据"""
        data = {'姓名': '张三', '年龄': 25}
        result = save_to_json(data, self.test_file)
        self.assertTrue(result)
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            self.assertIn('姓名', loaded)
            self.assertEqual(loaded['姓名'], '张三')
    
    def test_custom_indent(self):
        """测试自定义缩进"""
        data = {'key': 'value'}
        result = save_to_json(data, self.test_file, indent=4)
        self.assertTrue(result)
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 4空格缩进应该有更多空格
            self.assertIn('    "key"', content)


class TestSaveToExcel(unittest.TestCase):
    """save_to_excel函数测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.xlsx")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_save_data(self):
        """测试保存数据到Excel"""
        try:
            import pandas as pd
            # 检查是否有openpyxl
            try:
                import openpyxl
            except ImportError:
                self.skipTest("openpyxl未安装，跳过Excel测试")
            
            data = [
                {'name': 'Alice', 'age': 25},
                {'name': 'Bob', 'age': 30}
            ]
            result = save_to_excel(data, self.test_file)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(self.test_file))
        except ImportError as e:
            self.skipTest(f"Excel依赖未安装: {e}")
    
    def test_save_empty_data(self):
        """测试保存空数据"""
        try:
            import pandas as pd
            try:
                import openpyxl
            except ImportError:
                self.skipTest("openpyxl未安装，跳过Excel测试")
            
            result = save_to_excel([], self.test_file)
            self.assertFalse(result)
        except ImportError as e:
            self.skipTest(f"Excel依赖未安装: {e}")
    
    def test_custom_sheet_name(self):
        """测试自定义工作表名称"""
        try:
            import pandas as pd
            try:
                import openpyxl
            except ImportError:
                self.skipTest("openpyxl未安装，跳过Excel测试")
            
            data = [{'name': 'Alice'}]
            result = save_to_excel(data, self.test_file, sheet_name='TestSheet')
            self.assertTrue(result)
        except ImportError as e:
            self.skipTest(f"Excel依赖未安装: {e}")


class TestEnsureDirectory(unittest.TestCase):
    """ensure_directory函数测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.new_dir = os.path.join(self.test_dir, "new_dir")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_create_new_directory(self):
        """测试创建新目录"""
        result = ensure_directory(self.new_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.new_dir))
        self.assertTrue(os.path.isdir(self.new_dir))
    
    def test_existing_directory(self):
        """测试已存在的目录"""
        os.makedirs(self.new_dir)
        result = ensure_directory(self.new_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.new_dir))
    
    def test_nested_directory(self):
        """测试嵌套目录"""
        nested_dir = os.path.join(self.test_dir, "level1", "level2", "level3")
        result = ensure_directory(nested_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(nested_dir))


class TestGetFileSize(unittest.TestCase):
    """get_file_size函数测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_existing_file(self):
        """测试存在的文件"""
        content = "Hello World"
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        size = get_file_size(self.test_file)
        self.assertIsNotNone(size)
        self.assertEqual(size, len(content.encode('utf-8')))
    
    def test_nonexistent_file(self):
        """测试不存在的文件"""
        size = get_file_size(os.path.join(self.test_dir, "nonexistent.txt"))
        self.assertIsNone(size)
    
    def test_empty_file(self):
        """测试空文件"""
        with open(self.test_file, 'w') as f:
            pass
        
        size = get_file_size(self.test_file)
        self.assertEqual(size, 0)


class TestFormatFileSize(unittest.TestCase):
    """format_file_size函数测试"""
    
    def test_bytes(self):
        """测试字节"""
        self.assertEqual(format_file_size(500), "500.00 B")
        self.assertEqual(format_file_size(1023), "1023.00 B")
    
    def test_kilobytes(self):
        """测试KB"""
        result = format_file_size(1024)
        self.assertIn("KB", result)
        self.assertEqual(result, "1.00 KB")
        
        result = format_file_size(2048)
        self.assertEqual(result, "2.00 KB")
    
    def test_megabytes(self):
        """测试MB"""
        result = format_file_size(1024 * 1024)
        self.assertIn("MB", result)
        self.assertEqual(result, "1.00 MB")
    
    def test_gigabytes(self):
        """测试GB"""
        result = format_file_size(1024 * 1024 * 1024)
        self.assertIn("GB", result)
        self.assertEqual(result, "1.00 GB")
    
    def test_terabytes(self):
        """测试TB"""
        result = format_file_size(1024 * 1024 * 1024 * 1024)
        self.assertIn("TB", result)
        self.assertEqual(result, "1.00 TB")
    
    def test_zero(self):
        """测试零字节"""
        self.assertEqual(format_file_size(0), "0.00 B")
    
    def test_decimal_values(self):
        """测试小数值"""
        result = format_file_size(1536)  # 1.5 KB
        self.assertIn("1.50", result)
        self.assertIn("KB", result)


if __name__ == '__main__':
    unittest.main()
