# -*- coding: utf-8 -*-
"""
诊断为什么GitHub仓库是空的
"""
import subprocess
import os
import sys

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n{'='*70}")
    print(f"[诊断] {description}")
    print('='*70)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False, "", str(e)

def main():
    print("=" * 70)
    print("诊断：为什么GitHub仓库是空的？")
    print("=" * 70)
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 诊断1: 检查Git状态
    success, output, error = run_command("git status", "1. 检查Git状态")
    
    # 诊断2: 检查是否有提交
    success, output, error = run_command("git log --oneline -5", "2. 检查最近的提交")
    if not output.strip():
        print("⚠️  没有找到任何提交！这是问题所在。")
    
    # 诊断3: 检查有多少文件被跟踪
    success, output, error = run_command("git ls-files", "3. 检查被Git跟踪的文件")
    files = [f for f in output.strip().split('\n') if f.strip()]
    print(f"\n被Git跟踪的文件数量: {len(files)}")
    if len(files) == 0:
        print("⚠️  没有文件被Git跟踪！")
    else:
        print(f"前10个文件:")
        for f in files[:10]:
            print(f"  - {f}")
    
    # 诊断4: 检查工作目录中的文件
    print(f"\n{'='*70}")
    print("[诊断] 4. 检查工作目录中的文件（不包括.gitignore忽略的）")
    print('='*70)
    
    # 检查一些常见的文件类型
    common_files = []
    for root, dirs, files in os.walk('.'):
        # 跳过.git目录
        if '.git' in root:
            continue
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.bat', '.ps1')):
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                common_files.append(rel_path)
    
    print(f"\n找到 {len(common_files)} 个常见文件（.py, .md, .txt, .bat, .ps1）")
    if len(common_files) > 0:
        print("前10个文件:")
        for f in common_files[:10]:
            print(f"  - {f}")
    
    # 诊断5: 检查远程仓库
    success, output, error = run_command("git remote -v", "5. 检查远程仓库配置")
    
    # 诊断6: 检查远程分支
    success, output, error = run_command("git ls-remote origin", "6. 检查远程分支")
    
    # 诊断7: 检查.gitignore
    print(f"\n{'='*70}")
    print("[诊断] 7. 检查.gitignore配置")
    print('='*70)
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
            print(f".gitignore文件大小: {len(content)} 字符")
            # 先处理列表，避免在f-string中使用反斜杠
            lines = content.split('\n')
            rules = [l for l in lines if l.strip() and not l.strip().startswith('#')]
            print(f"规则数量: {len(rules)}")
            print("\n主要规则:")
            for line in lines[:20]:
                if line.strip() and not line.strip().startswith('#'):
                    print(f"  - {line.strip()}")
    else:
        print("⚠️  .gitignore文件不存在！")
    
    # 诊断8: 检查是否有未提交的更改
    success, output, error = run_command("git status --short", "8. 检查未提交的更改")
    if output.strip():
        print("⚠️  有未提交的更改！")
        print(output)
    else:
        print("✓ 没有未提交的更改")
    
    # 总结
    print("\n" + "=" * 70)
    print("诊断总结")
    print("=" * 70)
    
    # 检查提交
    success, log_output, _ = run_command("git log --oneline", "检查提交历史")
    has_commits = bool(log_output.strip())
    
    # 检查跟踪的文件
    success, ls_output, _ = run_command("git ls-files", "检查跟踪的文件")
    tracked_files = [f for f in ls_output.strip().split('\n') if f.strip()]
    
    print("\n可能的原因：")
    if not has_commits:
        print("❌ 1. 没有创建任何提交（最可能的原因）")
        print("   解决：运行 'git add .' 然后 'git commit -m \"初始提交\"'")
    elif len(tracked_files) == 0:
        print("❌ 2. 所有文件都被.gitignore忽略了")
        print("   解决：检查.gitignore，确保至少有一些文件被跟踪")
    else:
        print("❌ 3. 推送可能失败了")
        print("   解决：检查推送时的错误信息")
    
    print("\n建议的解决方案：")
    print("1. 运行：python 首次完整推送.py")
    print("2. 或者运行：python 彻底清理并推送.py（如果仍有大文件问题）")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
