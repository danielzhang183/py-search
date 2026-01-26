#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行接口模块

提供命令行工具来使用CSV读取功能
"""

import argparse
import os
import sys
from .csv_handler import read_csv_files, read_csv_simple, download_csv_from_url


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='读取当前文件夹下的CSV文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                              # 读取当前目录下所有CSV文件（使用pandas）
  %(prog)s --simple                     # 使用标准库读取
  %(prog)s --file example.csv           # 读取指定文件
  %(prog)s --dir /path/to/dir           # 读取指定目录下的CSV文件
  %(prog)s --download https://...       # 从URL下载CSV文件到examples文件夹
  %(prog)s --download https://... --filename data.csv  # 下载并指定文件名
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
    
    parser.add_argument(
        '--download',
        type=str,
        metavar='URL',
        help='从HTTPS URL下载CSV文件并保存到examples文件夹'
    )
    
    parser.add_argument(
        '--filename',
        type=str,
        help='下载文件时指定的文件名（与--download一起使用）'
    )
    
    args = parser.parse_args()
    
    try:
        if args.download:
            # 下载CSV文件
            save_path = download_csv_from_url(args.download, filename=args.filename)
            print(f"\n文件已保存到: {save_path}")
            # 下载后可以选择是否读取
            print("\n是否要读取下载的文件？(y/n): ", end='')
            try:
                choice = input().strip().lower()
                if choice == 'y':
                    filename = os.path.basename(save_path)
                    directory = os.path.dirname(save_path)
                    read_csv_files(directory, use_pandas=not args.simple)
            except (EOFError, KeyboardInterrupt):
                pass
        elif args.file:
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
