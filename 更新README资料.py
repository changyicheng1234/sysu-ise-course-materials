# -*- coding: utf-8 -*-
"""
上传资料者使用
自动更新课程README中的"已有资料"部分
根据目录中的文件自动生成资料描述

注意：脚本只更新"已有资料"部分，其他所有部分（如"选课建议"、"考试攻略"等）完全保留，需要手动编辑
"""
import os
import re
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple

# 课程目录路径
# 自动检测：如果在Git仓库中，使用当前目录；否则使用本地路径
def get_base_path():
    """获取项目根目录路径"""
    current_file = Path(__file__).resolve()
    # 如果当前文件在项目根目录（有.git目录），使用当前目录
    if (current_file.parent / '.git').exists():
        return current_file.parent
    # 默认使用本地路径
    return Path(r"d:\学习\中山大学智能工程学院本科生课程作业")

BASE_PATH = get_base_path()

# 需要忽略的文件和目录
IGNORE_PATTERNS = [
    'README.md',
    '.git',
    '__pycache__',
    '.DS_Store',
    '~$',  # Word临时文件
]

# 文件类型分类关键词
FILE_CATEGORIES = {
    '作业': ['作业', 'homework', 'hw', 'assignment'],
    '实验': ['实验', 'exp', 'lab', '实验课'],
    '期末': ['期末', 'final', 'exam', '考试'],
    '期中': ['期中', 'midterm', 'mid'],
    '报告': ['报告', 'report', '论文', 'paper'],
    '课件': ['课件', 'ppt', 'pptx', 'slides', 'lecture'],
    '教材': ['教材', 'textbook', 'book', '书籍'],
    '代码': ['代码', 'code', 'src', 'script'],
    '复习': ['复习', 'review', '总结'],
    '习题': ['习题', 'exercise', 'problem'],
    '项目': ['项目', 'project', 'proj'],
}


def should_ignore(path: Path) -> bool:
    """判断文件或目录是否应该被忽略"""
    name = path.name
    for pattern in IGNORE_PATTERNS:
        if pattern in name:
            return True
    return False


def categorize_file(file_path: Path) -> str:
    """根据文件名和路径判断文件类别"""
    name_lower = file_path.name.lower()
    path_lower = str(file_path).lower()
    
    # 检查是否匹配某个类别
    for category, keywords in FILE_CATEGORIES.items():
        for keyword in keywords:
            if keyword in name_lower or keyword in path_lower:
                return category
    
    # 根据文件扩展名判断
    ext = file_path.suffix.lower()
    if ext in ['.docx', '.doc']:
        return '文档'
    elif ext in ['.pdf']:
        return 'PDF文档'
    elif ext in ['.pptx', '.ppt']:
        return '课件'
    elif ext in ['.py', '.m', '.cpp', '.go', '.js', '.java']:
        return '代码'
    elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
        return '图片'
    elif ext in ['.mp4', '.mov', '.avi']:
        return '视频'
    elif ext in ['.slx', '.mdl']:
        return 'Simulink模型'
    elif ext in ['.pdsprj']:
        return 'Proteus项目'
    else:
        return '其他文件'


def clean_filename(name: str) -> str:
    """清理文件名，移除学号等冗余信息"""
    # 移除常见的学号模式（如22354010）
    name = re.sub(r'\d{8,}', '', name)
    # 移除常见的姓名模式（如常毅成）
    # 移除多余的下划线和连字符
    name = re.sub(r'[-_]{2,}', '-', name)
    name = name.strip('-_ ')
    return name


def analyze_directory(dir_path: Path, course_name: str) -> Dict[str, List[str]]:
    """分析目录结构，返回分类的文件列表"""
    categories = defaultdict(list)
    files_seen = set()
    dir_items = defaultdict(list)  # 用于按目录分组
    
    def process_path(path: Path, depth: int = 0, parent_category: str = None):
        """递归处理路径"""
        if should_ignore(path):
            return
        
        # 限制递归深度，避免过深
        if depth > 3:
            return
        
        if path.is_file():
            # 跳过临时文件和系统文件
            if path.name.startswith('.') or path.name.startswith('~'):
                return
            
            # 生成文件描述
            category = categorize_file(path)
            relative_path = path.relative_to(dir_path)
            
            # 如果父目录有明确的类别，优先使用父目录的类别
            if parent_category and parent_category in FILE_CATEGORIES:
                category = parent_category
            
            # 简化路径描述
            if relative_path.parent.name and relative_path.parent.name != '.':
                # 如果文件在子目录中，只显示目录名和主要文件
                parent_name = clean_filename(relative_path.parent.name)
                # 对于子目录中的文件，只记录目录名
                desc = parent_name
            else:
                desc = clean_filename(relative_path.name)
                # 移除文件扩展名（对于某些类型）
                if category in ['作业', '实验', '报告', '课件', '教材']:
                    desc = re.sub(r'\.[^.]+$', '', desc)
            
            # 避免重复
            desc_key = f"{category}:{desc}"
            if desc_key not in files_seen:
                files_seen.add(desc_key)
                categories[category].append(desc)
        
        elif path.is_dir():
            # 检查目录名是否包含类别关键词
            dir_category = None
            dir_name_lower = path.name.lower()
            for category, keywords in FILE_CATEGORIES.items():
                for keyword in keywords:
                    if keyword in dir_name_lower:
                        dir_category = category
                        break
                if dir_category:
                    break
            
            # 处理子目录
            try:
                for item in path.iterdir():
                    process_path(item, depth + 1, dir_category or parent_category)
            except PermissionError:
                pass
    
    # 处理目录中的所有文件
    try:
        for item in dir_path.iterdir():
            process_path(item)
    except PermissionError:
        pass
    
    # 去重并排序
    for category in categories:
        categories[category] = sorted(list(set(categories[category])))
    
    return dict(categories)


def generate_materials_section(categories: Dict[str, List[str]], course_name: str) -> str:
    """生成资料介绍部分的Markdown内容"""
    if not categories:
        return """### 已有资料

*暂无资料*"""
    
    lines = ["### 已有资料", ""]
    
    # 按优先级排序类别
    priority_order = ['作业', '实验', '期中', '期末', '报告', '课件', '教材', '复习', '习题', '项目', '代码', '文档', 'PDF文档', '图片', '视频', 'Simulink模型', 'Proteus项目', '其他文件']
    
    for category in priority_order:
        if category in categories:
            items = categories[category]
            if items:
                # 去重并限制显示数量
                unique_items = list(dict.fromkeys(items))  # 保持顺序的去重
                display_items = unique_items[:15]  # 每个类别最多显示15项
                
                if len(display_items) == 1:
                    # 如果只有一项，直接显示
                    lines.append(f"- **{category}**：{display_items[0]}")
                else:
                    lines.append(f"- **{category}**：")
                    for item in display_items:
                        lines.append(f"  - {item}")
                    if len(unique_items) > 15:
                        lines.append(f"  - *（还有 {len(unique_items) - 15} 项，共 {len(unique_items)} 项）*")
                lines.append("")
    
    # 处理其他未分类的类别
    other_categories = [cat for cat in categories.keys() if cat not in priority_order]
    if other_categories:
        for category in sorted(other_categories):
            items = categories[category]
            if items:
                unique_items = list(dict.fromkeys(items))
                display_items = unique_items[:15]
                if len(display_items) == 1:
                    lines.append(f"- **{category}**：{display_items[0]}")
                else:
                    lines.append(f"- **{category}**：")
                    for item in display_items:
                        lines.append(f"  - {item}")
                    if len(unique_items) > 15:
                        lines.append(f"  - *（还有 {len(unique_items) - 15} 项）*")
                lines.append("")
    
    return "\n".join(lines)


def update_readme(course_dir: Path):
    """更新指定课程目录的README文件
    
    只更新"已有资料"部分，其他所有部分（如"选课建议"、"考试攻略"等）完全保留不变
    """
    readme_path = course_dir / "README.md"
    
    if not readme_path.exists():
        print(f"⚠️  {course_dir.name}: README.md 不存在，跳过")
        return
    
    # 读取现有README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ {course_dir.name}: 读取README失败 - {e}")
        return
    
    # 分析目录生成新的资料部分
    categories = analyze_directory(course_dir, course_dir.name)
    new_materials_section = generate_materials_section(categories, course_dir.name)
    
    # 只更新"已有资料"部分，其他所有部分完全保留不变
    # 查找"### 已有资料"到下一个###或##之间的内容（精确匹配，不包含其他部分）
    pattern = r'(### 已有资料.*?)(?=\n### |\n## |\Z)'
    
    new_materials_content = f"""### 已有资料

{new_materials_section.split('### 已有资料\n', 1)[-1].strip()}
"""
    
    if re.search(pattern, content, re.DOTALL):
        # 只替换"已有资料"部分，其他内容完全保留
        content = re.sub(pattern, new_materials_content, content, flags=re.DOTALL)
    else:
        # 如果没有找到"已有资料"部分，在文件末尾添加（不修改任何现有内容）
        # 确保在添加前有一个空行分隔
        if content and not content.endswith('\n'):
            content += '\n'
        content += '\n' + new_materials_content
    
    # 写入更新后的内容
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {course_dir.name}: README已更新（仅更新已有资料部分）")
    except Exception as e:
        print(f"❌ {course_dir.name}: 写入README失败 - {e}")


def main():
    """主函数：更新所有课程目录的README"""
    print("开始更新课程README文件...\n")
    
    # 获取所有课程目录
    course_dirs = []
    for item in BASE_PATH.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['大一上期末', '大一下期末', '毛概期末复习']:
            # 检查是否有README.md（确保是课程目录）
            if (item / "README.md").exists():
                course_dirs.append(item)
    
    print(f"找到 {len(course_dirs)} 个课程目录\n")
    
    # 更新每个目录的README
    for course_dir in sorted(course_dirs):
        update_readme(course_dir)
    
    print(f"\n完成！共处理 {len(course_dirs)} 个课程目录")


if __name__ == "__main__":
    main()
