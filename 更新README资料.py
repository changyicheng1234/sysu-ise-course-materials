# -*- coding: utf-8 -*-
"""
上传资料者使用
自动更新课程README中的"已有资料"部分
根据目录中的文件自动生成资料描述
同时同步更新"收录内容.md"文件

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

# 课程分类规则（用于更新收录内容.md）
COURSE_CATEGORIES = {
    '特殊目录': ['大一上期末', '大一下期末'],
    '全校通用课程': ['马克思主义基本原理', '毛概期末复习'],
    '专业基础课程': [
        'C++程序设计', '数据结构与算法', '微机原理', '数字逻辑', 
        '工程数学', '信号与系统', '离散数学'
    ],
    '专业核心课程': [
        '人工智能导论', '人工智能基础与进阶实训', '机器学习', 
        '计算机视觉', '自然语言处理', '分布式计算', '数据库', 
        '计算机网络', '软件工程', '智能机器人技术'
    ],
    '控制与机器人相关课程': [
        '自动控制原理', '自控实验', '现代控制理论', '机器人实验', 
        '移动机器人规划', '集群控制', '控制电机技术', '计算机控制技术'
    ],
    '其他专业课程': [
        '图像处理', '视频技术', '物联网', '运筹学', '最优化', 
        '机械设计基础', '科技论文写作', '认识科学', '通信原理'
    ],
    '通识课程': ['心理健康']
}

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
    
    materials_body = new_materials_section.split('### 已有资料\n', 1)[-1].strip()
    new_materials_content = f"""### 已有资料

{materials_body}
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


def get_course_category(course_name: str) -> Tuple[str, str]:
    """根据课程名称获取其分类
    返回: (分类名称, 子分类名称) 或 (None, None) 如果未找到
    """
    # 检查特殊目录
    if course_name in COURSE_CATEGORIES['特殊目录']:
        return ('特殊目录', None)
    
    # 检查全校通用课程
    if course_name in COURSE_CATEGORIES['全校通用课程']:
        return ('全校通用课程', None)
    
    # 检查智能工程学院专用课程的子分类
    subcategories = ['专业基础课程', '专业核心课程', '控制与机器人相关课程', '其他专业课程', '通识课程']
    for subcategory in subcategories:
        if course_name in COURSE_CATEGORIES.get(subcategory, []):
            return ('智能工程学院专用课程', subcategory)
    
    return (None, None)


def update_collection_file(course_dirs: List[Path]):
    """更新收录内容.md文件"""
    collection_path = BASE_PATH / "收录内容.md"
    
    # 收集所有课程，按分类组织
    courses_by_category = defaultdict(lambda: defaultdict(list))
    
    # 处理特殊目录（即使没有README.md也要包含）
    for special_dir in ['大一上期末', '大一下期末']:
        special_path = BASE_PATH / special_dir
        if special_path.exists() and special_path.is_dir():
            courses_by_category['特殊目录'][None].append(special_dir)
    
    # 处理其他课程目录
    for course_dir in course_dirs:
        course_name = course_dir.name
        category, subcategory = get_course_category(course_name)
        
        if category:
            courses_by_category[category][subcategory].append(course_name)
        else:
            # 未分类的课程，添加到"其他专业课程"
            courses_by_category['智能工程学院专用课程']['其他专业课程'].append(course_name)
    
    # 生成新的收录内容
    lines = ["# 收录内容", ""]
    lines.append("本项目收录了以下课程的学习资料：")
    lines.append("")
    
    # 特殊目录
    if '特殊目录' in courses_by_category:
        special_courses = sorted(courses_by_category['特殊目录'][None])
        for course in special_courses:
            lines.append(f"- [{course}]({course}/)")
        lines.append("")
    
    # 全校通用课程
    if '全校通用课程' in courses_by_category:
        lines.append("## 全校通用课程")
        lines.append("")
        general_courses = sorted(courses_by_category['全校通用课程'][None])
        for course in general_courses:
            lines.append(f"- [{course}]({course}/)")
        lines.append("")
    
    # 智能工程学院专用课程
    if '智能工程学院专用课程' in courses_by_category:
        lines.append("## 智能工程学院专用课程")
        lines.append("")
        
        # 按子分类顺序处理
        subcategory_order = [
            '专业基础课程', '专业核心课程', '控制与机器人相关课程', 
            '其他专业课程', '通识课程'
        ]
        
        for subcategory in subcategory_order:
            if subcategory in courses_by_category['智能工程学院专用课程']:
                courses = sorted(courses_by_category['智能工程学院专用课程'][subcategory])
                if courses:
                    lines.append(f"### {subcategory}")
                    for course in courses:
                        lines.append(f"- [{course}]({course}/)")
                    lines.append("")
        
        # 处理其他未在预定义列表中的子分类
        for subcategory in courses_by_category['智能工程学院专用课程']:
            if subcategory not in subcategory_order:
                courses = sorted(courses_by_category['智能工程学院专用课程'][subcategory])
                if courses:
                    lines.append(f"### {subcategory}")
                    for course in courses:
                        lines.append(f"- [{course}]({course}/)")
                    lines.append("")
    
    # 写入文件
    try:
        with open(collection_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"\n✅ 收录内容.md 已更新")
    except Exception as e:
        print(f"\n❌ 更新收录内容.md失败 - {e}")


def main():
    """主函数：更新所有课程目录的README和收录内容.md"""
    print("开始更新课程README文件...\n")
    
    # 获取所有课程目录（排除特殊目录，因为它们不需要README.md）
    course_dirs = []
    special_dirs = ['大一上期末', '大一下期末']  # 这些目录不需要README.md，会在收录内容中单独处理
    for item in BASE_PATH.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in special_dirs:
            # 检查是否有README.md（确保是课程目录）
            if (item / "README.md").exists():
                course_dirs.append(item)
    
    print(f"找到 {len(course_dirs)} 个课程目录\n")
    
    # 更新每个目录的README
    for course_dir in sorted(course_dirs):
        update_readme(course_dir)
    
    # 同步更新收录内容.md（会自动包含特殊目录）
    update_collection_file(course_dirs)
    
    print(f"\n完成！共处理 {len(course_dirs)} 个课程目录")


if __name__ == "__main__":
    main()
