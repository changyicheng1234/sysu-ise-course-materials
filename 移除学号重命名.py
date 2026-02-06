# -*- coding: utf-8 -*-
"""
批量移除文件名中的学号信息，只保留姓名
"""
import os
from pathlib import Path

base_path = Path(r"d:\学习\中山大学智能工程学院本科生课程作业")
student_id = "22354010"
student_name = "常毅成"

def clean_filename(name):
    """清理文件名，移除学号"""
    cleaned = name
    
    # 模式1: 22354010常毅成 -> 常毅成
    cleaned = cleaned.replace(f"{student_id}{student_name}", student_name)
    
    # 模式2: 22354010-常毅成 -> 常毅成
    cleaned = cleaned.replace(f"{student_id}-{student_name}", student_name)
    cleaned = cleaned.replace(f"{student_id}-{student_name}-", f"{student_name}-")
    cleaned = cleaned.replace(f"-{student_id}-{student_name}", f"-{student_name}")
    
    # 模式3: 22354010_常毅成 -> 常毅成
    cleaned = cleaned.replace(f"{student_id}_{student_name}", student_name)
    cleaned = cleaned.replace(f"{student_id}_{student_name}_", f"{student_name}_")
    cleaned = cleaned.replace(f"_{student_id}_{student_name}", f"_{student_name}")
    
    # 模式4: 常毅成22354010 -> 常毅成
    cleaned = cleaned.replace(f"{student_name}{student_id}", student_name)
    
    # 模式5: 单独的学号（在文件名中）
    cleaned = cleaned.replace(f"-{student_id}-", "-")
    cleaned = cleaned.replace(f"_{student_id}_", "_")
    
    # 处理开头或结尾的学号
    if cleaned.startswith(f"{student_id}-"):
        cleaned = cleaned[len(f"{student_id}-"):]
    if cleaned.startswith(f"{student_id}_"):
        cleaned = cleaned[len(f"{student_id}_"):]
    if cleaned.startswith(student_id) and len(cleaned) > len(student_id) and cleaned[len(student_id)] in ['-', '_', ' ']:
        cleaned = cleaned[len(student_id)+1:]
    
    if cleaned.endswith(f"-{student_id}"):
        cleaned = cleaned[:-len(f"-{student_id}")]
    if cleaned.endswith(f"_{student_id}"):
        cleaned = cleaned[:-len(f"_{student_id}")]
    
    return cleaned

def rename_file_or_dir(old_path, new_path):
    """重命名文件或目录"""
    try:
        if old_path.exists():
            if new_path.exists():
                print(f"  跳过: {new_path.name} 已存在")
                return False
            old_path.rename(new_path)
            print(f"  ✓ 重命名: {old_path.name} -> {new_path.name}")
            return True
    except Exception as e:
        print(f"  ✗ 错误: 重命名 {old_path.name} 失败: {e}")
        return False

def main():
    print(f"开始处理目录: {base_path}")
    print(f"学号: {student_id}")
    print(f"姓名: {student_name}")
    print("=" * 60)
    
    if not base_path.exists():
        print(f"错误: 目录不存在 {base_path}")
        return
    
    # 使用os.walk从最深层的文件开始处理，避免重命名父目录后找不到子目录
    renamed_count = 0
    all_paths = []
    
    # 收集所有需要处理的路径（从深到浅）
    for root, dirs, files in os.walk(base_path, topdown=False):
        root_path = Path(root)
        
        # 处理文件
        for file in files:
            file_path = root_path / file
            all_paths.append(file_path)
        
        # 处理目录
        for dir_name in dirs:
            dir_path = root_path / dir_name
            all_paths.append(dir_path)
    
    # 处理所有路径
    for path in all_paths:
        old_name = path.name
        
        if student_id in old_name:
            new_name = clean_filename(old_name)
            
            if new_name != old_name:
                new_path = path.parent / new_name
                if rename_file_or_dir(path, new_path):
                    renamed_count += 1
    
    print("=" * 60)
    print(f"处理完成！共重命名 {renamed_count} 个文件/文件夹")

if __name__ == "__main__":
    main()
