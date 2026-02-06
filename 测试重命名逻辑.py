# -*- coding: utf-8 -*-
"""测试重命名逻辑"""
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

# 测试用例
test_cases = [
    "22354010常毅成",
    "22354010-常毅成",
    "22354010_常毅成",
    "常毅成22354010",
    "22354010常毅成作业一.pdf",
    "22354010-常毅成-期末报告.pdf",
    "22354010_常毅成_平时作业.pdf",
    "常毅成22354010作业2.pdf",
    "作业3-22354010-常毅成.pdf",
    "22354010.pdf",
    "01-研究论文-22354010-常毅成.pdf",
]

print("测试重命名逻辑:")
print("=" * 60)
for test in test_cases:
    result = clean_filename(test)
    print(f"{test:50} -> {result}")
