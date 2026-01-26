#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚类结果可视化模块

提供多种可视化方式展示K-means聚类结果：
1. 2D/3D散点图
2. 聚类中心可视化
3. 轮廓系数分析图
4. 肘部法则图
5. 聚类分布统计图
"""

import os
import sys
from typing import List, Optional, Dict, Any, Tuple
import numpy as np


class ClusterVisualizer:
    """聚类结果可视化器"""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        初始化可视化器
        
        Args:
            output_dir: 图片保存目录，如果为None则使用项目根目录下的reports文件夹
        """
        if output_dir is None:
            # 获取项目根目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(current_dir, "reports")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_2d_clusters(self,
                        data: np.ndarray,
                        labels: np.ndarray,
                        centers: Optional[np.ndarray] = None,
                        feature_names: Optional[List[str]] = None,
                        title: str = "K-means聚类结果 (2D)",
                        save_path: Optional[str] = None) -> str:
        """
        绘制2D散点图展示聚类结果
        
        Args:
            data: 原始数据（numpy数组）
            labels: 聚类标签
            centers: 聚类中心（可选）
            feature_names: 特征名称列表
            title: 图表标题
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')  # 使用非交互式后端
        except ImportError:
            raise ImportError("matplotlib未安装，请运行: pip install matplotlib")
        
        if data.shape[1] < 2:
            raise ValueError("数据至少需要2个特征才能绘制2D图")
        
        # 使用前两个特征
        x = data[:, 0]
        y = data[:, 1]
        
        # 创建图形
        plt.figure(figsize=(10, 8))
        
        # 获取唯一的聚类标签
        unique_labels = np.unique(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        
        # 绘制每个聚类的点
        for i, label in enumerate(unique_labels):
            mask = labels == label
            plt.scatter(x[mask], y[mask], 
                       c=[colors[i]], 
                       label=f'聚类 {label}',
                       s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # 绘制聚类中心
        if centers is not None and len(centers) > 0:
            plt.scatter(centers[:, 0], centers[:, 1],
                       c='red', marker='x', s=200, linewidths=3,
                       label='聚类中心', zorder=10)
        
        # 设置标签和标题
        x_label = feature_names[0] if feature_names and len(feature_names) > 0 else '特征1'
        y_label = feature_names[1] if feature_names and len(feature_names) > 1 else '特征2'
        
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        
        # 保存图片
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"cluster_2d_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_3d_clusters(self,
                        data: np.ndarray,
                        labels: np.ndarray,
                        centers: Optional[np.ndarray] = None,
                        feature_names: Optional[List[str]] = None,
                        title: str = "K-means聚类结果 (3D)",
                        save_path: Optional[str] = None) -> str:
        """
        绘制3D散点图展示聚类结果
        
        Args:
            data: 原始数据（numpy数组）
            labels: 聚类标签
            centers: 聚类中心（可选）
            feature_names: 特征名称列表
            title: 图表标题
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        try:
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
        except ImportError:
            raise ImportError("matplotlib未安装，请运行: pip install matplotlib")
        
        if data.shape[1] < 3:
            raise ValueError("数据至少需要3个特征才能绘制3D图")
        
        # 使用前三个特征
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        
        # 创建3D图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 获取唯一的聚类标签
        unique_labels = np.unique(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        
        # 绘制每个聚类的点
        for i, label in enumerate(unique_labels):
            mask = labels == label
            ax.scatter(x[mask], y[mask], z[mask],
                      c=[colors[i]], 
                      label=f'聚类 {label}',
                      s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # 绘制聚类中心
        if centers is not None and len(centers) > 0:
            ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2],
                      c='red', marker='x', s=200, linewidths=3,
                      label='聚类中心')
        
        # 设置标签和标题
        x_label = feature_names[0] if feature_names and len(feature_names) > 0 else '特征1'
        y_label = feature_names[1] if feature_names and len(feature_names) > 1 else '特征2'
        z_label = feature_names[2] if feature_names and len(feature_names) > 2 else '特征3'
        
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.set_zlabel(z_label, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        
        # 保存图片
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"cluster_3d_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_elbow_method(self,
                         k_range: List[int],
                         inertias: List[float],
                         optimal_k: Optional[int] = None,
                         title: str = "肘部法则 - 寻找最优聚类数",
                         save_path: Optional[str] = None) -> str:
        """
        绘制肘部法则图
        
        Args:
            k_range: 聚类数范围
            inertias: 对应的簇内平方和
            optimal_k: 最优聚类数（可选，用于标记）
            title: 图表标题
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
        except ImportError:
            raise ImportError("matplotlib未安装，请运行: pip install matplotlib")
        
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
        
        if optimal_k:
            # 标记最优聚类数
            idx = k_range.index(optimal_k)
            plt.plot(optimal_k, inertias[idx], 'ro', markersize=12, label=f'最优 k={optimal_k}')
            plt.axvline(x=optimal_k, color='r', linestyle='--', alpha=0.5)
        
        plt.xlabel('聚类数 (k)', fontsize=12)
        plt.ylabel('簇内平方和 (Inertia)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        if optimal_k:
            plt.legend()
        
        # 保存图片
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"elbow_method_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_silhouette_scores(self,
                              k_range: List[int],
                              scores: List[float],
                              optimal_k: Optional[int] = None,
                              title: str = "轮廓系数分析",
                              save_path: Optional[str] = None) -> str:
        """
        绘制轮廓系数图
        
        Args:
            k_range: 聚类数范围
            scores: 对应的轮廓系数
            optimal_k: 最优聚类数（可选，用于标记）
            title: 图表标题
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
        except ImportError:
            raise ImportError("matplotlib未安装，请运行: pip install matplotlib")
        
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, scores, 'go-', linewidth=2, markersize=8)
        
        if optimal_k:
            # 标记最优聚类数
            idx = k_range.index(optimal_k)
            plt.plot(optimal_k, scores[idx], 'ro', markersize=12, label=f'最优 k={optimal_k}')
            plt.axvline(x=optimal_k, color='r', linestyle='--', alpha=0.5)
        
        plt.xlabel('聚类数 (k)', fontsize=12)
        plt.ylabel('轮廓系数 (Silhouette Score)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        if optimal_k:
            plt.legend()
        
        # 保存图片
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"silhouette_scores_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_cluster_distribution(self,
                                 cluster_counts: Dict[int, int],
                                 title: str = "聚类分布统计",
                                 save_path: Optional[str] = None) -> str:
        """
        绘制聚类分布统计图（柱状图）
        
        Args:
            cluster_counts: 每个聚类的样本数字典
            title: 图表标题
            save_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
        except ImportError:
            raise ImportError("matplotlib未安装，请运行: pip install matplotlib")
        
        clusters = sorted(cluster_counts.keys())
        counts = [cluster_counts[k] for k in clusters]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(clusters, counts, color=plt.cm.Spectral(np.linspace(0, 1, len(clusters))))
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=11)
        
        plt.xlabel('聚类编号', fontsize=12)
        plt.ylabel('样本数量', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.xticks(clusters)
        
        # 保存图片
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"cluster_distribution_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def visualize_analysis_result(self,
                                 result: Dict[str, Any],
                                 original_file: str,
                                 save_all: bool = True) -> Dict[str, str]:
        """
        可视化完整的分析结果，生成所有图表
        
        Args:
            result: 分析结果字典
            original_file: 原始文件名
            save_all: 是否保存所有图表
            
        Returns:
            包含所有保存图片路径的字典
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(original_file))[0]
        
        saved_images = {}
        
        # 获取数据
        df = result['dataframe']
        labels = result['cluster_result']['labels']
        centers = result['cluster_result']['centers']
        used_columns = result['used_columns']
        
        # 提取数值数据
        data = df[used_columns].values
        
        try:
            # 1. 2D散点图（使用前两个特征）
            if data.shape[1] >= 2:
                path_2d = self.plot_2d_clusters(
                    data, labels, centers, used_columns,
                    title=f"K-means聚类结果 - {base_name} (2D)",
                    save_path=os.path.join(self.output_dir, f"{base_name}_2d_{timestamp}.png")
                )
                saved_images['2d'] = path_2d
            
            # 2. 3D散点图（使用前三个特征）
            if data.shape[1] >= 3:
                path_3d = self.plot_3d_clusters(
                    data, labels, centers, used_columns,
                    title=f"K-means聚类结果 - {base_name} (3D)",
                    save_path=os.path.join(self.output_dir, f"{base_name}_3d_{timestamp}.png")
                )
                saved_images['3d'] = path_3d
            
            # 3. 聚类分布统计图
            path_dist = self.plot_cluster_distribution(
                result['cluster_result']['cluster_counts'],
                title=f"聚类分布统计 - {base_name}",
                save_path=os.path.join(self.output_dir, f"{base_name}_distribution_{timestamp}.png")
            )
            saved_images['distribution'] = path_dist
            
        except Exception as e:
            print(f"⚠ 生成可视化图表时出错: {e}", file=sys.stderr)
        
        return saved_images


def visualize_cluster_result(result: Dict[str, Any],
                            original_file: str,
                            output_dir: Optional[str] = None,
                            save_all: bool = True) -> Dict[str, str]:
    """
    便捷函数：可视化聚类结果
    
    Args:
        result: 分析结果字典
        original_file: 原始文件名
        output_dir: 输出目录
        save_all: 是否保存所有图表
        
    Returns:
        包含所有保存图片路径的字典
    """
    visualizer = ClusterVisualizer(output_dir=output_dir)
    return visualizer.visualize_analysis_result(result, original_file, save_all)
