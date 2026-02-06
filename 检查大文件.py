# -*- coding: utf-8 -*-
"""
检查目录中超过100MB的文件
"""
import os
from pathlib import Path

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def check_large_files(directory, threshold_mb=100):
    """检查超过指定大小的文件"""
    threshold_bytes = threshold_mb * 1024 * 1024
    large_files = []
    total_size = 0
    file_count = 0
    
    print(f"正在扫描目录: {directory}")
    print(f"查找超过 {threshold_mb}MB 的文件...")
    print("-" * 80)
    
    for root, dirs, files in os.walk(directory):
        # 跳过.git目录
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_count += 1
                total_size += file_size
                
                if file_size > threshold_bytes:
                    relative_path = os.path.relpath(file_path, directory)
                    large_files.append((relative_path, file_size))
            except (OSError, PermissionError) as e:
                # 跳过无法访问的文件
                continue
    
    # 按文件大小排序
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n扫描完成！")
    print(f"总文件数: {file_count}")
    print(f"总大小: {format_size(total_size)}")
    print(f"超过 {threshold_mb}MB 的文件数: {len(large_files)}")
    print("=" * 80)
    
    if large_files:
        print(f"\n发现 {len(large_files)} 个超过 {threshold_mb}MB 的文件：\n")
        for i, (file_path, file_size) in enumerate(large_files, 1):
            print(f"{i}. {format_size(file_size):>12} - {file_path}")
        
        # 统计信息
        total_large_size = sum(size for _, size in large_files)
        print(f"\n这些大文件的总大小: {format_size(total_large_size)}")
        print(f"占全部文件的比例: {total_large_size/total_size*100:.2f}%")
    else:
        print(f"\n✓ 没有发现超过 {threshold_mb}MB 的文件！")
        print("所有文件都可以直接推送到GitHub（只要单个文件不超过100MB）")
    
    return large_files, total_size

if __name__ == "__main__":
    # 项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    
    print("=" * 80)
    print("检查大文件工具")
    print("=" * 80)
    
    large_files, total_size = check_large_files(project_path, threshold_mb=100)
    
    print("\n" + "=" * 80)
    print("检查完成")
    print("=" * 80)
    
    input("\n按 Enter 键退出...")
