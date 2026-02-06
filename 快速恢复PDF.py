# -*- coding: utf-8 -*-
"""
快速恢复所有PDF文件：从Git历史中恢复
"""
import subprocess
import os

def run_cmd(cmd):
    """执行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("=" * 70)
    print("快速恢复所有PDF文件")
    print("=" * 70)
    
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    
    print("\n正在从Git历史中恢复PDF文件...")
    
    # 尝试从最近的几个提交中恢复
    restored = False
    
    for i in range(1, 6):  # 检查HEAD~1到HEAD~5
        print(f"\n尝试从 HEAD~{i} 恢复...")
        success, stdout, stderr = run_cmd(f'git checkout HEAD~{i} -- "*.pdf"')
        
        if success:
            # 检查是否有文件被恢复
            success2, stdout2, _ = run_cmd('git status --short | findstr ".pdf"')
            if stdout2.strip():
                print(f"✓ 从 HEAD~{i} 恢复了PDF文件")
                restored = True
                break
        else:
            print(f"  HEAD~{i} 中没有PDF文件或无法访问")
    
    if not restored:
        # 尝试从所有分支中查找
        print("\n尝试从所有分支中查找PDF文件...")
        success, stdout, _ = run_cmd('git branch -a')
        branches = [b.strip().replace('*', '').strip() for b in stdout.split('\n') if b.strip()]
        
        for branch in branches[:5]:  # 只检查前5个分支
            branch = branch.replace('remotes/origin/', '')
            print(f"\n尝试从分支 {branch} 恢复...")
            success, _, _ = run_cmd(f'git checkout {branch} -- "*.pdf" 2>nul')
            if success:
                success2, stdout2, _ = run_cmd('git status --short | findstr ".pdf"')
                if stdout2.strip():
                    print(f"✓ 从分支 {branch} 恢复了PDF文件")
                    restored = True
                    break
    
    # 重置暂存区（只保留工作目录的文件）
    print("\n重置Git索引（保留工作目录的文件）...")
    run_cmd('git reset HEAD')
    
    # 检查恢复的文件
    print("\n检查恢复的PDF文件...")
    success, stdout, _ = run_cmd('dir /s /b *.pdf 2>nul')
    if stdout.strip():
        pdf_files = [f.strip() for f in stdout.split('\n') if f.strip()]
        print(f"\n✓ 找到 {len(pdf_files)} 个PDF文件：")
        for pdf in pdf_files[:10]:
            print(f"  - {pdf}")
        if len(pdf_files) > 10:
            print(f"  ... 还有 {len(pdf_files) - 10} 个PDF文件")
    else:
        print("\n⚠️  未找到PDF文件")
        print("可能的原因：")
        print("1. PDF文件从未被提交到Git")
        print("2. Git历史已被清理")
        print("3. 需要从远程仓库拉取")
    
    print("\n" + "=" * 70)
    print("恢复完成！")
    print("=" * 70)
    print("\n注意：")
    print("1. PDF文件已恢复到工作目录")
    print("2. 这些文件现在不会被Git跟踪（因为.gitignore）")
    print("3. 文件只存在于本地，不会被推送到GitHub")
    
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    main()
