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
  %(prog)s --analysis customer_data.csv  # 对CSV文件进行K-means聚类分析
  %(prog)s --analysis data.csv --clusters 4  # 指定聚类数为4
  %(prog)s --analysis data.csv --columns 消费金额 购买次数  # 指定使用的列
  %(prog)s --analysis data.csv --optimal  # 自动寻找最优聚类数
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
    
    parser.add_argument(
        '--analysis',
        type=str,
        metavar='FILE',
        help='对指定的CSV文件进行K-means聚类分析'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        default=3,
        help='聚类数量（与--analysis一起使用，默认3）'
    )
    
    parser.add_argument(
        '--columns',
        type=str,
        nargs='+',
        help='指定用于聚类的数值列（与--analysis一起使用，多个列用空格分隔）'
    )
    
    parser.add_argument(
        '--optimal',
        action='store_true',
        help='自动寻找最优聚类数（与--analysis一起使用）'
    )
    
    args = parser.parse_args()
    
    try:
        if args.analysis:
            # K-means聚类分析
            _run_analysis(args.analysis, args.clusters, args.columns, args.dir, args.optimal)
        elif args.download:
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


def _run_analysis(csv_file: str, n_clusters: int, columns: list, directory: str, find_optimal: bool):
    """
    执行K-means聚类分析并输出结果
    
    Args:
        csv_file: CSV文件名
        n_clusters: 聚类数量
        columns: 要使用的列
        directory: 文件所在目录
        find_optimal: 是否寻找最优聚类数
    """
    try:
        from .data_analyzer import DataAnalyzer, kmeans_analyze_csv
        
        print("=" * 60)
        print("K-means聚类分析")
        print("=" * 60)
        print(f"\n正在分析文件: {csv_file}")
        if directory:
            print(f"目录: {directory}")
        
        # 如果指定了寻找最优聚类数
        if find_optimal:
            print("\n正在寻找最优聚类数...")
            from .csv_handler import CSVReader
            reader = CSVReader(directory=directory)
            df = reader.read_with_pandas(csv_file)
            
            analyzer = DataAnalyzer()
            data, used_columns = analyzer.preprocess_data(df, numeric_columns=columns)
            
            optimal_result = analyzer.find_optimal_clusters(data, max_clusters=10)
            n_clusters = optimal_result['optimal_k']
            
            print(f"\n✓ 最优聚类数: {n_clusters}")
            print(f"\n各聚类数的轮廓系数:")
            for k, score in zip(optimal_result['k_range'], optimal_result['silhouette_scores']):
                marker = " ← 最优" if k == n_clusters else ""
                print(f"  k={k}: {score:.4f}{marker}")
        
        # 执行聚类分析
        print(f"\n正在执行K-means聚类（k={n_clusters}）...")
        result = kmeans_analyze_csv(
            csv_file=csv_file,
            n_clusters=n_clusters,
            numeric_columns=columns,
            directory=directory
        )
        
        # 输出结果
        print("\n" + "=" * 60)
        print("分析结果")
        print("=" * 60)
        print(f"\n文件: {result['file']}")
        print(f"总样本数: {result['total_samples']}")
        print(f"聚类数: {result['n_clusters']}")
        print(f"使用的特征: {', '.join(result['used_columns'])}")
        
        print(f"\n各客户群体统计:")
        for cluster_id in sorted(result['cluster_info'].keys()):
            info = result['cluster_info'][cluster_id]
            print(f"\n聚类 {cluster_id}:")
            print(f"  样本数: {info['count']}")
            if info['mean']:
                print(f"  平均值:")
                for col, val in info['mean'].items():
                    print(f"    {col}: {val:.2f}")
        
        # 聚类质量指标
        cr = result['cluster_result']
        print(f"\n聚类质量指标:")
        if cr['silhouette_score']:
            print(f"  轮廓系数: {cr['silhouette_score']:.4f} (范围: -1到1，越大越好)")
        print(f"  簇内平方和: {cr['inertia']:.2f} (越小越好)")
        
        # 显示部分样本的聚类标签
        print(f"\n前10个样本的聚类标签:")
        df_with_cluster = result['dataframe']
        display_cols = ['cluster'] + result['used_columns'][:3]  # 显示聚类标签和前3个特征
        if '客户ID' in df_with_cluster.columns:
            display_cols.insert(0, '客户ID')
        print(df_with_cluster[display_cols].head(10).to_string(index=False))
        
        print("\n✓ 分析完成！")
        
    except ImportError as e:
        print(f"\n✗ 错误: {e}", file=sys.stderr)
        print("\n提示: 请安装必要的依赖:", file=sys.stderr)
        print("  pip install pandas scikit-learn numpy", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 分析失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
