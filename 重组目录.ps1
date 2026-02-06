# 重组目录脚本：将按学期组织的目录改为按课程名称组织

$basePath = "d:\学习\中山大学智能工程学院本科生课程作业"

# 定义课程映射：学期目录 -> 课程目录
$courseMappings = @{
    "大三上" = @(
        "分布式计算", "图像处理", "工程数学", "机器人实验", 
        "机械设计基础", "移动机器人规划", "自控matlab", "自控实验", 
        "计算机视觉", "运筹学", "通信原理"
    )
    "大三下" = @(
        "C++练习", "人因工程", "最优化", "形式与政策", 
        "扩散模型BMVC", "物联网", "现代控制理论", 
        "自然语言处理", "软工", "集群控制"
    )
    "大二下" = @(
        "微机原理", "心理健康", "数字逻辑", "数据库", 
        "视频技术", "自动控制原理", "计算机网络", "认识科学"
    )
    "大四上" = @(
        "VLAhand", "世界模型", "控制电机技术", 
        "模型与数据统一系统", "生产实习", "科技论文写作", "计算机控制技术"
    )
}

# 遍历每个学期目录
foreach ($semester in $courseMappings.Keys) {
    $semesterPath = Join-Path $basePath $semester
    
    if (-not (Test-Path $semesterPath)) {
        Write-Host "跳过不存在的目录: $semesterPath"
        continue
    }
    
    Write-Host "处理学期目录: $semester"
    
    foreach ($course in $courseMappings[$semester]) {
        $sourcePath = Join-Path $semesterPath $course
        $destPath = Join-Path $basePath $course
        
        if (Test-Path $sourcePath) {
            Write-Host "  移动课程: $course"
            
            # 如果目标目录不存在，创建它
            if (-not (Test-Path $destPath)) {
                New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            }
            
            # 移动目录内容
            Get-ChildItem -Path $sourcePath | ForEach-Object {
                $destItemPath = Join-Path $destPath $_.Name
                if (Test-Path $destItemPath) {
                    Write-Host "    警告: $($_.Name) 已存在，跳过"
                } else {
                    Move-Item -Path $_.FullName -Destination $destPath -Force
                }
            }
            
            # 删除空源目录
            if ((Get-ChildItem -Path $sourcePath -Force | Measure-Object).Count -eq 0) {
                Remove-Item -Path $sourcePath -Force
            }
        }
    }
}

Write-Host "`n目录重组完成！"
Write-Host "请检查结果，然后可以删除空的学期目录。"
