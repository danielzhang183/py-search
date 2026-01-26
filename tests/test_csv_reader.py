#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV读取器测试模块
"""

import os
import sys
import unittest
import tempfile
import csv

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_search.csv_reader import CSVReader, read_csv_simple


class TestCSVReader(unittest.TestCase):
    """CSVReader测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录和测试CSV文件
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "test.csv")
        
        # 创建测试CSV文件
        with open(self.test_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['姓名', '年龄', '城市'])
            writer.writerow(['张三', '25', '北京'])
            writer.writerow(['李四', '30', '上海'])
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_find_csv_files(self):
        """测试查找CSV文件"""
        reader = CSVReader(self.test_dir)
        csv_files = reader.find_csv_files()
        self.assertEqual(len(csv_files), 1)
        self.assertIn("test.csv", csv_files[0])
    
    def test_read_with_standard_lib(self):
        """测试使用标准库读取CSV"""
        reader = CSVReader(self.test_dir)
        rows = reader.read_with_standard_lib("test.csv")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ['姓名', '年龄', '城市'])
        self.assertEqual(rows[1], ['张三', '25', '北京'])
    
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        reader = CSVReader(self.test_dir)
        with self.assertRaises(FileNotFoundError):
            reader.read_with_standard_lib("nonexistent.csv")
    
    def test_get_file_info(self):
        """测试获取文件信息"""
        reader = CSVReader(self.test_dir)
        try:
            info = reader.get_file_info("test.csv")
            self.assertEqual(info['rows'], 2)  # 不包括表头
            self.assertEqual(info['columns'], 3)
            self.assertEqual(info['column_names'], ['姓名', '年龄', '城市'])
        except ImportError:
            # 如果没有pandas，跳过此测试
            self.skipTest("pandas未安装，跳过此测试")


if __name__ == '__main__':
    unittest.main()
