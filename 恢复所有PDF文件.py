# -*- coding: utf-8 -*-
"""
恢复所有PDF文件：从Git历史中恢复被删除的PDF文件
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=False, show_output=True):
    """执行命令并显示结果"""
    if show_output:
        print(f"\n[步骤] {description}...")
        print(f"执行: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if show_output:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("错误:", result.stderr)
        
        if check and result.returncode != 0:
            if show_output:
                print(f"❌ 失败，退出码: {result.returncode}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        if show_output:
            print(f"❌ 执行出错: {e}")
        return False

def find_pdf_commits():
    """查找包含PDF文件的提交"""
    print("\n查找包含PDF文件的提交...")
    
    # 方法1: 尝试从最近的几个提交中查找
    commits = {}
    
    # 检查最近的10个提交
    for i in range(10):
        result = subprocess.run(
            f'git log --oneline -1 --skip={i}',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if not result.stdout.strip():
            break
            
        commit_hash = result.stdout.split()[0]
        
        # 检查这个提交中是否有PDF文件
        pdf_result = subprocess.run(
            f'git ls-tree -r --name-only {commit_hash} | findstr /i ".pdf"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if pdf_result.stdout.strip():
            pdf_files = [f.strip() for f in pdf_result.stdout.strip().split('\n') if f.strip()]
            if pdf_files:
                commits[commit_hash] = {
                    'msg': result.stdout.strip(),
                    'files': pdf_files
                }
                print(f"  找到提交 {commit_hash[:8]}: {len(pdf_files)} 个PDF文件")
    
    if not commits:
        # 方法2: 使用git log查找
        result = subprocess.run(
            'git log --all --full-history --name-only --pretty=format:"%H|%s" -- "*.pdf"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            current_commit = None
            
            for line in lines:
                if '|' in line:
                    commit_hash, commit_msg = line.split('|', 1)
                    current_commit = commit_hash
                    if current_commit not in commits:
                        commits[current_commit] = {'msg': commit_msg, 'files': []}
                elif current_commit and line.strip() and line.endswith('.pdf'):
                    if line not in commits[current_commit]['files']:
                        commits[current_commit]['files'].append(line)
    
    return commits

def main():
    print("=" * 70)
    print("恢复所有PDF文件")
    print("=" * 70)
    print("\n⚠️  这个脚本会：")
    print("1. 查找Git历史中包含PDF文件的提交")
    print("2. 从最近的提交中恢复所有PDF文件")
    print("3. 将PDF文件恢复到工作目录")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查当前分支
    print("\n" + "=" * 70)
    print("[步骤 1/5] 检查当前Git状态")
    print("=" * 70)
    
    result = subprocess.run(
        "git branch --show-current",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    current_branch = result.stdout.strip()
    print(f"当前分支: {current_branch}")
    
    # 步骤2: 查找包含PDF的提交
    print("\n" + "=" * 70)
    print("[步骤 2/5] 查找包含PDF文件的提交")
    print("=" * 70)
    
    commits = find_pdf_commits()
    
    if not commits:
        print("\n❌ 未找到包含PDF文件的提交")
        print("可能的原因：")
        print("1. PDF文件从未被提交到Git")
        print("2. Git历史已被清理")
        print("\n尝试从reflog中查找...")
        
        # 尝试从reflog中查找
        result = subprocess.run(
            'git reflog --all | head -20',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(result.stdout)
        
        # 尝试从HEAD@{1}恢复
        print("\n尝试从上一个HEAD恢复...")
        run_command("git checkout HEAD@{1} -- '*.pdf'", "从上一个HEAD恢复PDF文件", check=False)
        
        return
    
    # 显示找到的提交
    print(f"\n找到 {len(commits)} 个包含PDF文件的提交：")
    for i, (commit_hash, info) in enumerate(list(commits.items())[:5], 1):
        print(f"\n{i}. 提交: {commit_hash[:8]}...")
        print(f"   信息: {info['msg']}")
        print(f"   PDF文件数: {len(info['files'])}")
        if len(info['files']) <= 5:
            for pdf in info['files']:
                print(f"     - {pdf}")
        else:
            for pdf in info['files'][:3]:
                print(f"     - {pdf}")
            print(f"     ... 还有 {len(info['files']) - 3} 个PDF文件")
    
    # 步骤3: 选择要恢复的提交（使用最近的）
    print("\n" + "=" * 70)
    print("[步骤 3/5] 选择要恢复的提交")
    print("=" * 70)
    
    if len(commits) > 1:
        print("\n找到多个包含PDF的提交")
        print("将使用最近的提交来恢复所有PDF文件")
    
    # 获取最近的提交
    latest_commit = list(commits.keys())[0]
    latest_info = commits[latest_commit]
    
    print(f"\n将使用提交 {latest_commit[:8]}... 恢复PDF文件")
    print(f"该提交包含 {len(latest_info['files'])} 个PDF文件")
    
    # 步骤4: 从提交中恢复PDF文件
    print("\n" + "=" * 70)
    print("[步骤 4/5] 恢复PDF文件")
    print("=" * 70)
    
    restored_count = 0
    failed_files = []
    
    for pdf_file in latest_info['files']:
        print(f"\n恢复: {pdf_file}")
        
        # 检查文件是否存在
        full_path = os.path.join(project_path, pdf_file)
        if os.path.exists(full_path):
            print(f"  ⚠️  文件已存在，跳过")
            continue
        
        # 从提交中恢复文件
        success = run_command(
            f'git checkout {latest_commit} -- "{pdf_file}"',
            f"恢复 {pdf_file}",
            check=False,
            show_output=False
        )
        
        if success:
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path) / (1024 * 1024)  # MB
                print(f"  ✓ 恢复成功 ({file_size:.2f} MB)")
                restored_count += 1
            else:
                print(f"  ⚠️  命令成功但文件不存在")
                failed_files.append(pdf_file)
        else:
            print(f"  ❌ 恢复失败")
            failed_files.append(pdf_file)
    
    # 步骤5: 总结
    print("\n" + "=" * 70)
    print("[步骤 5/5] 恢复完成")
    print("=" * 70)
    
    print(f"\n恢复结果：")
    print(f"  ✓ 成功恢复: {restored_count} 个文件")
    print(f"  ❌ 失败: {len(failed_files)} 个文件")
    
    if failed_files:
        print("\n失败的文件：")
        for f in failed_files:
            print(f"  - {f}")
    
    # 检查当前目录中的PDF文件
    print("\n检查当前目录中的PDF文件...")
    result = subprocess.run(
        'powershell -Command "Get-ChildItem -Recurse -Filter *.pdf | Select-Object FullName | Measure-Object"',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if "Count" in result.stdout:
        count_line = [l for l in result.stdout.split('\n') if 'Count' in l]
        if count_line:
            print(f"当前目录中共有PDF文件: {count_line[0].strip()}")
    
    print("\n" + "=" * 70)
    print("✅ PDF文件恢复完成！")
    print("=" * 70)
    print("\n注意：")
    print("1. PDF文件已恢复到工作目录")
    print("2. 这些文件现在不会被Git跟踪（因为.gitignore配置）")
    print("3. 如果需要推送，请使用之前创建的脚本来处理大文件问题")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
