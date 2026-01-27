#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行接口模块

提供K-means聚类分析命令行工具
"""

import argparse
import os
import sys


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='K-means聚类分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --analysis customer_data.csv  # 对CSV文件进行K-means聚类分析
  %(prog)s --analysis data.csv --clusters 4  # 指定聚类数为4
  %(prog)s --analysis data.csv --columns 消费金额 购买次数  # 指定使用的列
  %(prog)s --analysis data.csv --optimal  # 自动寻找最优聚类数
  %(prog)s --analysis data.csv --no-viz  # 不生成可视化图表
  %(prog)s --analysis data.csv --dir ./data  # 指定数据文件目录
        """
    )
    
    parser.add_argument(
        '--analysis',
        type=str,
        metavar='FILE',
        required=True,
        help='对指定的CSV文件进行K-means聚类分析'
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        help='指定CSV文件所在目录（默认为当前目录）'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        default=3,
        help='聚类数量（默认3）'
    )
    
    parser.add_argument(
        '--columns',
        type=str,
        nargs='+',
        help='指定用于聚类的数值列（多个列用空格分隔）'
    )
    
    parser.add_argument(
        '--optimal',
        action='store_true',
        help='自动寻找最优聚类数'
    )
    
    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='不生成可视化图表'
    )
    
    args = parser.parse_args()
    
    try:
        # K-means聚类分析
        _run_analysis(args.analysis, args.clusters, args.columns, args.dir, args.optimal, args.no_viz)
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def _run_analysis(csv_file: str, n_clusters: int, columns: list, directory: str, find_optimal: bool, no_viz: bool = False):
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
            
            # 生成最优聚类数分析图表
            try:
                from .visualizer import ClusterVisualizer
                visualizer = ClusterVisualizer()
                
                # 肘部法则图
                elbow_path = visualizer.plot_elbow_method(
                    optimal_result['k_range'],
                    optimal_result['inertias'],
                    optimal_k=n_clusters,
                    title=f"肘部法则 - {os.path.basename(csv_file)}"
                )
                
                # 轮廓系数图
                silhouette_path = visualizer.plot_silhouette_scores(
                    optimal_result['k_range'],
                    optimal_result['silhouette_scores'],
                    optimal_k=n_clusters,
                    title=f"轮廓系数分析 - {os.path.basename(csv_file)}"
                )
                
                print(f"\n✓ 肘部法则图已保存: {elbow_path}")
                print(f"✓ 轮廓系数图已保存: {silhouette_path}")
            except ImportError:
                pass  # matplotlib未安装，跳过可视化
            except Exception as e:
                print(f"⚠ 生成分析图表时出错: {e}", file=sys.stderr)
        
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
        
        # 保存结果到reports文件夹
        from .data_analyzer import save_analysis_results
        try:
            saved_files = save_analysis_results(result, csv_file, n_clusters)
            print(f"\n✓ 聚类结果已保存: {saved_files['csv']}")
            print(f"✓ 分析报告已保存: {saved_files['json']}")
            print(f"✓ 文本报告已保存: {saved_files['txt']}")
        except Exception as e:
            print(f"\n⚠ 保存结果时出错: {e}", file=sys.stderr)
        
        # 生成可视化图表
        if not no_viz:
            try:
                from .visualizer import visualize_cluster_result
                saved_images = visualize_cluster_result(result, csv_file)
                if saved_images:
                    print(f"\n✓ 可视化图表已生成:")
                    for chart_type, path in saved_images.items():
                        print(f"  - {chart_type.upper()}: {path}")
            except ImportError:
                print(f"\n提示: 安装matplotlib可生成可视化图表: pip install matplotlib")
            except Exception as e:
                print(f"\n⚠ 生成可视化图表时出错: {e}", file=sys.stderr)
        
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
