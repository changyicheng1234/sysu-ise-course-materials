# -*- coding: utf-8 -*-
"""
批量移除所有README中的"资料扩展记录"部分
"""
import re
from pathlib import Path

BASE_PATH = Path(r"d:\学习\中山大学智能工程学院本科生课程作业")

def remove_extension_record(readme_path: Path):
    """移除README中的资料扩展记录部分"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除"资料扩展记录"部分
        content = re.sub(
            r'\n### 资料扩展记录.*?(?=\n## |$)',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 移除"本目录包含以下学习资料："这样的旧提示
        content = re.sub(
            r'\n本目录包含以下学习资料：\n\n',
            '\n',
            content
        )
        
        # 添加提示信息（如果还没有）
        if '💡' not in content and '## 资料介绍' in content:
            # 在"## 资料介绍"后添加提示
            content = re.sub(
                r'(## 资料介绍\n)',
                r'\1\n> 💡 **提示**：本目录的资料列表由脚本自动生成。添加新资料后，运行 `更新README资料.py` 或双击 `运行更新README.bat` 即可自动更新此部分。\n\n',
                content
            )
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"❌ {readme_path.parent.name}: {e}")
        return False

def main():
    """主函数"""
    print("开始移除所有README中的'资料扩展记录'部分...\n")
    
    readme_files = list(BASE_PATH.glob("*/README.md"))
    # 排除子目录中的README
    readme_files = [f for f in readme_files if f.parent.parent == BASE_PATH]
    
    print(f"找到 {len(readme_files)} 个README文件\n")
    
    success_count = 0
    for readme_path in sorted(readme_files):
        if remove_extension_record(readme_path):
            print(f"✅ {readme_path.parent.name}")
            success_count += 1
    
    print(f"\n完成！共处理 {success_count}/{len(readme_files)} 个文件")

if __name__ == "__main__":
    main()
