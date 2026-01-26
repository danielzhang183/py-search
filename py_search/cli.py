#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行接口模块

提供命令行工具来使用CSV读取功能
"""

import argparse
import sys
from .csv_reader import read_csv_files, read_csv_simple


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='读取当前文件夹下的CSV文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 读取当前目录下所有CSV文件（使用pandas）
  %(prog)s --simple           # 使用标准库读取
  %(prog)s --file example.csv # 读取指定文件
  %(prog)s --dir /path/to/dir # 读取指定目录下的CSV文件
        """
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='使用标准库读取（不需要pandas）'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='读取指定的CSV文件'
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        help='指定要读取的目录路径'
    )
    
    args = parser.parse_args()
    
    try:
        if args.file:
            # 读取指定文件
            read_csv_simple(args.file, args.dir)
        else:
            # 读取目录下所有CSV文件
            read_csv_files(args.dir, use_pandas=not args.simple)
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
