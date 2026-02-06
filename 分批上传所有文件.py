# -*- coding: utf-8 -*-
"""
分批上传所有文件到GitHub（包括PDF）
将7GB内容分成3批上传，避免单次推送过大
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=False, show_output=True):
    """执行命令并显示结果"""
    if show_output:
        print(f"\n[执行] {description}...")
        print(f"命令: {cmd}")
    
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
            if result.stderr and result.returncode != 0:
                print(f"错误: {result.stderr}")
        
        if check and result.returncode != 0:
            if show_output:
                print(f"❌ 失败，退出码: {result.returncode}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        if show_output:
            print(f"❌ 执行出错: {e}")
        return False

def get_directory_size(directory):
    """获取目录大小（MB）"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, PermissionError):
                    pass
    except Exception:
        pass
    return total_size / (1024 * 1024)  # 转换为MB

def main():
    print("=" * 80)
    print("分批上传所有文件到GitHub（包括PDF）")
    print("=" * 80)
    print("\n⚠️  这个脚本会：")
    print("1. 确保.gitignore允许PDF文件")
    print("2. 将文件分成3批上传")
    print("3. 每批独立提交和推送")
    print("\n⚠️  注意：")
    print("- 确保没有超过100MB的单个文件")
    print("- 确保网络连接稳定")
    print("- 每批推送可能需要较长时间，请耐心等待")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 确保.gitignore允许PDF
    print("\n" + "=" * 80)
    print("[步骤 1] 检查.gitignore配置")
    print("=" * 80)
    
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "*.pdf" in content and "# *.pdf" not in content:
                print("⚠️  .gitignore中PDF被忽略，需要修改...")
                # 注释掉PDF忽略规则
                content = content.replace("*.pdf", "# *.pdf  # 已注释，允许上传PDF文件")
                with open(gitignore_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✓ 已修改.gitignore，允许PDF文件")
            else:
                print("✓ .gitignore已配置允许PDF文件")
    
    # 定义分批上传的目录
    # 第一批：较小的课程目录 + 根目录文件
    batch1_dirs = [
        "人工智能导论",
        "最优化",
        "图像处理",
        "工程数学",
        "心理健康",
        "机械设计基础",
        "移动机器人规划",
        "现代控制理论",
        "自然语言处理",
        "视频技术",
        "科技论文写作",
        "计算机控制技术",
        "计算机视觉",
        "计算机网络",
        "认识科学",
        "通信原理",
        "控制电机技术",
        "数字逻辑",
        "数据库",
        "物联网",
        "集群控制",
        "运筹学",
        "毛概期末复习",
    ]
    
    # 第二批：中等大小的课程目录
    batch2_dirs = [
        "分布式计算",
        "自动控制原理",
        "自控实验",
        "微机原理",
    ]
    
    # 第三批：较大的课程目录
    batch3_dirs = [
        "机器人实验",
        "软件工程",
    ]
    
    # 根目录文件（第一批上传）
    root_files = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        ".gitignore",
    ]
    
    # 步骤2: 检查Git状态
    print("\n" + "=" * 80)
    print("[步骤 2] 检查Git状态")
    print("=" * 80)
    run_command("git status", "检查Git状态", check=False)
    
    # 检查当前分支
    result = subprocess.run(
        "git branch --show-current",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    current_branch = result.stdout.strip() or "main"
    print(f"当前分支: {current_branch}")
    
    # 步骤3: 第一批上传
    print("\n" + "=" * 80)
    print("[步骤 3] 第一批上传：较小的课程目录")
    print("=" * 80)
    print(f"包含目录: {', '.join(batch1_dirs)}")
    print("以及根目录文件")
    
    input("\n按 Enter 开始第一批上传...")
    
    # 添加根目录文件
    for file in root_files:
        file_path = os.path.join(project_path, file)
        if os.path.exists(file_path):
            run_command(f'git add "{file}"', f"添加 {file}", check=False, show_output=False)
    
    # 添加第一批目录
    for dir_name in batch1_dirs:
        dir_path = os.path.join(project_path, dir_name)
        if os.path.exists(dir_path):
            run_command(f'git add "{dir_name}/"', f"添加 {dir_name}", check=False, show_output=False)
    
    # 检查将要提交的文件
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        file_count = len([line for line in result.stdout.strip().split('\n') if line.strip()])
        print(f"\n第一批将要提交的文件数: {file_count}")
        run_command('git commit -m "第一批：较小的课程目录和根目录文件"', "创建第一批提交", check=False)
        
        print("\n正在推送第一批...")
        print("（这可能需要一些时间，请耐心等待）")
        
        # 配置推送参数
        run_command("git config http.postBuffer 524288000", "配置缓冲区", check=False, show_output=False)
        run_command("git config http.maxRequestBuffer 100M", "配置最大请求缓冲区", check=False, show_output=False)
        
        success = run_command("git push origin " + current_branch, "推送第一批", check=False)
        
        if success:
            print("\n✅ 第一批推送成功！")
        else:
            print("\n❌ 第一批推送失败，请检查错误信息")
            return
    else:
        print("⚠️  第一批没有新文件需要提交")
    
    # 步骤4: 第二批上传
    print("\n" + "=" * 80)
    print("[步骤 4] 第二批上传：中等大小的课程目录")
    print("=" * 80)
    print(f"包含目录: {', '.join(batch2_dirs)}")
    
    input("\n按 Enter 开始第二批上传...")
    
    # 添加第二批目录
    for dir_name in batch2_dirs:
        dir_path = os.path.join(project_path, dir_name)
        if os.path.exists(dir_path):
            run_command(f'git add "{dir_name}/"', f"添加 {dir_name}", check=False, show_output=False)
    
    # 检查将要提交的文件
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        file_count = len([line for line in result.stdout.strip().split('\n') if line.strip()])
        print(f"\n第二批将要提交的文件数: {file_count}")
        run_command('git commit -m "第二批：中等大小的课程目录"', "创建第二批提交", check=False)
        
        print("\n正在推送第二批...")
        print("（这可能需要一些时间，请耐心等待）")
        
        success = run_command("git push origin " + current_branch, "推送第二批", check=False)
        
        if success:
            print("\n✅ 第二批推送成功！")
        else:
            print("\n❌ 第二批推送失败，请检查错误信息")
            return
    else:
        print("⚠️  第二批没有新文件需要提交")
    
    # 步骤5: 第三批上传
    print("\n" + "=" * 80)
    print("[步骤 5] 第三批上传：较大的课程目录")
    print("=" * 80)
    print(f"包含目录: {', '.join(batch3_dirs)}")
    
    input("\n按 Enter 开始第三批上传...")
    
    # 添加第三批目录
    for dir_name in batch3_dirs:
        dir_path = os.path.join(project_path, dir_name)
        if os.path.exists(dir_path):
            run_command(f'git add "{dir_name}/"', f"添加 {dir_name}", check=False, show_output=False)
    
    # 添加其他可能遗漏的文件
    run_command("git add .", "添加其他文件", check=False, show_output=False)
    
    # 检查将要提交的文件
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        file_count = len([line for line in result.stdout.strip().split('\n') if line.strip()])
        print(f"\n第三批将要提交的文件数: {file_count}")
        run_command('git commit -m "第三批：较大的课程目录和其他文件"', "创建第三批提交", check=False)
        
        print("\n正在推送第三批...")
        print("（这可能需要一些时间，请耐心等待）")
        
        success = run_command("git push origin " + current_branch, "推送第三批", check=False)
        
        if success:
            print("\n✅ 第三批推送成功！")
        else:
            print("\n❌ 第三批推送失败，请检查错误信息")
            return
    else:
        print("⚠️  第三批没有新文件需要提交")
    
    # 最终检查
    print("\n" + "=" * 80)
    print("✅ 所有批次上传完成！")
    print("=" * 80)
    
    print("\n检查最终状态...")
    run_command("git status", "检查Git状态", check=False)
    
    print("\n" + "=" * 80)
    print("上传完成！")
    print("=" * 80)
    print("\n仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials")
    print("\n✓ 所有文件（包括PDF）已成功上传到GitHub")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
