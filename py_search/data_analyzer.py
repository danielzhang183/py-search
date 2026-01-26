#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析模块

提供CSV数据的分析和处理功能，包括：
1. K-means聚类分析
2. 数据预处理
3. 可视化（可选）
"""

import os
import json
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import numpy as np


class DataAnalyzer:
    """数据分析器类"""
    
    def __init__(self):
        """初始化数据分析器"""
        pass
    
    def preprocess_data(self, df, numeric_columns: Optional[List[str]] = None):
        """
        数据预处理：选择数值列并标准化
        
        Args:
            df: pandas DataFrame
            numeric_columns: 要使用的数值列，如果为None则自动选择所有数值列
            
        Returns:
            处理后的数据（numpy数组）和列名列表
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas未安装，请运行: pip install pandas")
        
        # 如果没有指定列，自动选择所有数值列
        if numeric_columns is None:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            raise ValueError("没有找到数值列，无法进行聚类分析")
        
        # 提取数值数据
        data = df[numeric_columns].values
        
        # 处理缺失值
        data = np.nan_to_num(data, nan=0.0)
        
        return data, numeric_columns
    
    def kmeans_cluster(self, 
                      data: np.ndarray,
                      n_clusters: int = 3,
                      random_state: int = 42,
                      max_iter: int = 300) -> Dict[str, Any]:
        """
        K-means聚类分析
        
        Args:
            data: 输入数据（numpy数组）
            n_clusters: 聚类数量，默认为3
            random_state: 随机种子，默认为42
            max_iter: 最大迭代次数，默认为300
            
        Returns:
            包含聚类结果的字典
        """
        try:
            from sklearn.cluster import KMeans
        except ImportError:
            raise ImportError(
                "scikit-learn未安装，请运行: pip install scikit-learn\n"
                "K-means聚类需要scikit-learn库"
            )
        
        # 执行K-means聚类
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            max_iter=max_iter,
            n_init=10
        )
        labels = kmeans.fit_predict(data)
        
        # 计算聚类中心
        centers = kmeans.cluster_centers_
        
        # 计算每个聚类的样本数
        unique, counts = np.unique(labels, return_counts=True)
        cluster_counts = dict(zip(unique, counts))
        
        # 计算轮廓系数（评估聚类质量）
        try:
            from sklearn.metrics import silhouette_score
            silhouette_avg = silhouette_score(data, labels)
        except:
            silhouette_avg = None
        
        return {
            'labels': labels,
            'centers': centers,
            'cluster_counts': cluster_counts,
            'n_clusters': n_clusters,
            'silhouette_score': silhouette_avg,
            'inertia': kmeans.inertia_  # 簇内平方和
        }
    
    def find_optimal_clusters(self,
                              data: np.ndarray,
                              max_clusters: int = 10,
                              random_state: int = 42) -> Dict[str, Any]:
        """
        使用肘部法则和轮廓系数找到最优聚类数
        
        Args:
            data: 输入数据
            max_clusters: 最大聚类数，默认为10
            random_state: 随机种子
            
        Returns:
            包含最优聚类数和评估指标的字典
        """
        try:
            from sklearn.cluster import KMeans
            from sklearn.metrics import silhouette_score
        except ImportError:
            raise ImportError("scikit-learn未安装，请运行: pip install scikit-learn")
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, min(max_clusters + 1, len(data)))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
            labels = kmeans.fit_predict(data)
            inertias.append(kmeans.inertia_)
            
            if len(set(labels)) > 1:  # 至少需要2个不同的聚类
                silhouette_scores.append(silhouette_score(data, labels))
            else:
                silhouette_scores.append(0)
        
        # 找到轮廓系数最高的k值
        optimal_k = k_range[np.argmax(silhouette_scores)]
        
        return {
            'optimal_k': optimal_k,
            'k_range': list(k_range),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores
        }
    
    def analyze_csv_with_clustering(self,
                                    csv_file: str,
                                    n_clusters: int = 3,
                                    numeric_columns: Optional[List[str]] = None,
                                    directory: Optional[str] = None) -> Dict[str, Any]:
        """
        分析CSV文件并进行K-means聚类
        
        Args:
            csv_file: CSV文件路径
            n_clusters: 聚类数量
            numeric_columns: 要使用的数值列
            directory: 文件所在目录
            
        Returns:
            包含分析结果的字典
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas未安装，请运行: pip install pandas")
        
        from .csv_handler import CSVReader
        
        # 读取CSV文件
        reader = CSVReader(directory=directory)
        df = reader.read_with_pandas(csv_file)
        
        # 数据预处理
        data, used_columns = self.preprocess_data(df, numeric_columns)
        
        # 执行聚类
        cluster_result = self.kmeans_cluster(data, n_clusters=n_clusters)
        
        # 将聚类标签添加到原始数据
        df['cluster'] = cluster_result['labels']
        
        # 统计每个聚类的信息
        cluster_info = {}
        for cluster_id in range(n_clusters):
            cluster_data = df[df['cluster'] == cluster_id]
            cluster_info[cluster_id] = {
                'count': len(cluster_data),
                'mean': cluster_data[used_columns].mean().to_dict() if len(cluster_data) > 0 else {}
            }
        
        return {
            'file': csv_file,
            'n_clusters': n_clusters,
            'used_columns': used_columns,
            'cluster_result': cluster_result,
            'cluster_info': cluster_info,
            'dataframe': df,
            'total_samples': len(df)
        }


def kmeans_analyze_csv(csv_file: str,
                       n_clusters: int = 3,
                       numeric_columns: Optional[List[str]] = None,
                       directory: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷函数：对CSV文件进行K-means聚类分析
    
    Args:
        csv_file: CSV文件路径
        n_clusters: 聚类数量，默认为3
        numeric_columns: 要使用的数值列，如果为None则自动选择
        directory: 文件所在目录
        
    Returns:
        分析结果字典
    """
    analyzer = DataAnalyzer()
    return analyzer.analyze_csv_with_clustering(
        csv_file=csv_file,
        n_clusters=n_clusters,
        numeric_columns=numeric_columns,
        directory=directory
    )


def save_analysis_results(result: Dict[str, Any], 
                          original_file: str, 
                          n_clusters: int,
                          reports_dir: Optional[str] = None) -> Dict[str, str]:
    """
    保存分析结果到reports文件夹
    
    Args:
        result: 分析结果字典
        original_file: 原始CSV文件名
        n_clusters: 聚类数量
        reports_dir: 报告保存目录，如果为None则使用项目根目录下的reports文件夹
        
    Returns:
        包含保存文件路径的字典
    """
    try:
        # 确定reports目录
        if reports_dir is None:
            # 获取项目根目录（假设reports在项目根目录下）
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(current_dir, "reports")
        
        # 创建reports文件夹
        os.makedirs(reports_dir, exist_ok=True)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成文件名（去除扩展名）
        base_name = os.path.splitext(os.path.basename(original_file))[0]
        
        saved_files = {}
        
        # 保存带聚类标签的CSV文件
        df_with_cluster = result['dataframe']
        csv_output_file = os.path.join(reports_dir, f"{base_name}_clustered_{timestamp}.csv")
        df_with_cluster.to_csv(csv_output_file, index=False, encoding='utf-8-sig')
        saved_files['csv'] = csv_output_file
        
        # 保存分析报告（JSON格式）
        report = {
            'analysis_time': datetime.now().isoformat(),
            'source_file': original_file,
            'n_clusters': n_clusters,
            'total_samples': result['total_samples'],
            'used_columns': result['used_columns'],
            'cluster_info': {
                str(k): {
                    'count': v['count'],
                    'mean': {str(k2): float(v2) for k2, v2 in v['mean'].items()} if v['mean'] else {}
                }
                for k, v in result['cluster_info'].items()
            },
            'quality_metrics': {
                'silhouette_score': float(result['cluster_result']['silhouette_score']) if result['cluster_result']['silhouette_score'] else None,
                'inertia': float(result['cluster_result']['inertia'])
            }
        }
        
        json_output_file = os.path.join(reports_dir, f"{base_name}_report_{timestamp}.json")
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        saved_files['json'] = json_output_file
        
        # 保存文本格式的报告（更易读）
        txt_output_file = os.path.join(reports_dir, f"{base_name}_report_{timestamp}.txt")
        with open(txt_output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("K-means聚类分析报告\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"分析时间: {report['analysis_time']}\n")
            f.write(f"源文件: {report['source_file']}\n")
            f.write(f"总样本数: {report['total_samples']}\n")
            f.write(f"聚类数: {report['n_clusters']}\n")
            f.write(f"使用的特征: {', '.join(report['used_columns'])}\n\n")
            
            f.write("各聚类统计:\n")
            f.write("-" * 60 + "\n")
            for cluster_id in sorted(report['cluster_info'].keys(), key=int):
                info = report['cluster_info'][cluster_id]
                f.write(f"\n聚类 {cluster_id}:\n")
                f.write(f"  样本数: {info['count']}\n")
                if info['mean']:
                    f.write(f"  平均值:\n")
                    for col, val in info['mean'].items():
                        f.write(f"    {col}: {val:.2f}\n")
            
            f.write(f"\n聚类质量指标:\n")
            f.write("-" * 60 + "\n")
            if report['quality_metrics']['silhouette_score']:
                f.write(f"  轮廓系数: {report['quality_metrics']['silhouette_score']:.4f} (范围: -1到1，越大越好)\n")
            f.write(f"  簇内平方和: {report['quality_metrics']['inertia']:.2f} (越小越好)\n")
        
        saved_files['txt'] = txt_output_file
        
        return saved_files
        
    except Exception as e:
        raise Exception(f"保存结果时出错: {str(e)}")
