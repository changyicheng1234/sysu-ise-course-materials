# -*- coding: utf-8 -*-
"""
重组目录脚本：将按学期组织的目录改为按课程名称组织
"""
import os
import shutil
from pathlib import Path

base_path = Path(r"d:\学习\中山大学智能工程学院本科生课程作业")

# 定义课程映射：学期目录 -> 课程列表
course_mappings = {
    "大三上": [
        "分布式计算", "图像处理", "工程数学", "机器人实验", 
        "机械设计基础", "移动机器人规划", "自控matlab", "自控实验", 
        "计算机视觉", "运筹学", "通信原理"
    ],
    "大三下": [
        "C++练习", "人因工程", "最优化", "形式与政策", 
        "扩散模型BMVC", "物联网", "现代控制理论", 
        "自然语言处理", "软工", "集群控制"
    ],
    "大二下": [
        "微机原理", "心理健康", "数字逻辑", "数据库", 
        "视频技术", "自动控制原理", "计算机网络", "认识科学"
    ],
    "大四上": [
        "VLAhand", "世界模型", "控制电机技术", 
        "模型与数据统一系统", "生产实习", "科技论文写作", "计算机控制技术"
    ]
}

# 遍历每个学期目录
for semester, courses in course_mappings.items():
    semester_path = base_path / semester
    
    if not semester_path.exists():
        print(f"跳过不存在的目录: {semester_path}")
        continue
    
    print(f"\n处理学期目录: {semester}")
    
    for course in courses:
        source_path = semester_path / course
        dest_path = base_path / course
        
        if source_path.exists():
            print(f"  移动课程: {course}")
            
            # 如果目标目录不存在，创建它
            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)
            
            # 移动目录内容
            for item in source_path.iterdir():
                dest_item_path = dest_path / item.name
                if dest_item_path.exists():
                    print(f"    警告: {item.name} 已存在，跳过")
                else:
                    try:
                        if item.is_dir():
                            shutil.move(str(item), str(dest_path))
                        else:
                            shutil.move(str(item), str(dest_path))
                    except Exception as e:
                        print(f"    错误: 移动 {item.name} 时出错: {e}")
            
            # 删除空源目录
            try:
                if source_path.exists() and not any(source_path.iterdir()):
                    source_path.rmdir()
                    print(f"    已删除空目录: {source_path}")
            except Exception as e:
                print(f"    无法删除目录 {source_path}: {e}")

print("\n目录重组完成！")
print("请检查结果，然后可以删除空的学期目录。")
