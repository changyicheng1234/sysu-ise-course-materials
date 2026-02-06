# GitHub 大文件上传问题解决方案

## GitHub 的文件大小限制

### 硬性限制
- **单个文件超过 50MB**：GitHub 会**拒绝推送**
- **单个文件超过 100MB**：即使推送成功，GitHub 也会警告，且文件可能无法正常显示
- **单次推送总大小**：建议不超过 **2GB**，超过可能导致 HTTP 500 错误
- **仓库总大小**：建议不超过 **1GB**，硬限制是 **100GB**

### 常见错误信息
- `remote: error: File xxx is 150.00 MB; this exceeds GitHub's file size limit of 100.00 MB`
- `error: RPC failed; HTTP 500`
- `error: failed to push some refs`

## 解决方案（按推荐顺序）

### 方案一：使用 .gitignore 忽略大文件（最简单）✅

**适用场景**：大文件还没有被提交到 Git 历史中

**步骤**：
1. 确保 `.gitignore` 文件已正确配置（你的已经配置好了）
2. 如果文件已经被跟踪，需要先从 Git 索引中移除：
```bash
git rm --cached 大文件路径
git commit -m "移除大文件"
```

**优点**：简单快速，不影响历史记录  
**缺点**：如果文件已经在历史中，此方法无效

---

### 方案二：清理 Git 历史记录（推荐）✅

**适用场景**：大文件已经被提交到 Git 历史中

你已经有了两个脚本可以使用：

#### 方法 A：使用 `彻底清理并推送.py`（推荐）
```bash
python 彻底清理并推送.py
```

这个脚本会：
- 创建新的孤立分支（丢弃所有历史）
- 只添加当前未被忽略的文件
- 强制推送到远程

**优点**：彻底解决问题，仓库大小最小  
**缺点**：会丢失 Git 历史记录（对课程作业通常不是问题）

#### 方法 B：使用 `清理Git历史中的大文件.py`
```bash
python 清理Git历史中的大文件.py
```

这个脚本会：
- 使用 `git filter-branch` 从历史中移除大文件
- 保留其他历史记录
- 强制推送到远程

**优点**：保留部分历史记录  
**缺点**：操作复杂，可能需要很长时间

---

### 方案三：使用 Git LFS（Large File Storage）📦

**适用场景**：需要保留大文件，但不想让它们占用普通 Git 存储

**步骤**：
1. 安装 Git LFS：
```bash
# Windows (使用 Chocolatey)
choco install git-lfs

# 或下载安装：https://git-lfs.github.com/
```

2. 初始化 Git LFS：
```bash
git lfs install
```

3. 跟踪大文件类型：
```bash
git lfs track "*.jpg"
git lfs track "*.png"
git lfs track "*.pth"
# 或跟踪整个目录
git lfs track "计算机视觉/Plant-Pathology-sysu-2023-main/**"
```

4. 提交 `.gitattributes` 文件：
```bash
git add .gitattributes
git commit -m "配置 Git LFS"
```

5. 正常提交和推送：
```bash
git add .
git commit -m "使用 LFS 管理大文件"
git push origin main
```

**优点**：可以保留大文件，不影响仓库大小  
**缺点**：需要 GitHub 账户有 LFS 配额（免费账户 1GB 存储 + 1GB 带宽/月）

---

### 方案四：分批推送（临时方案）⚠️

**适用场景**：文件太大，但不想清理历史

**步骤**：
1. 配置更大的缓冲区：
```bash
git config http.postBuffer 524288000  # 500MB
git config http.maxRequestBuffer 100M
```

2. 尝试推送（可能仍然失败）：
```bash
git push origin main
```

**优点**：不需要修改历史  
**缺点**：通常无效，因为 GitHub 服务器端有限制

---

### 方案五：使用外部存储（最佳实践）🌟

**适用场景**：有大量大文件需要管理

**推荐服务**：
- **Google Drive / OneDrive**：存储数据集、模型文件
- **百度网盘 / 阿里云盘**：国内访问方便
- **GitHub Releases**：适合发布版本文件
- **云存储服务**：AWS S3、Azure Blob Storage 等

**在 README 中说明**：
```markdown
## 数据文件下载

由于文件较大，数据集和模型文件存储在外部：
- 数据集：[下载链接]
- 模型文件：[下载链接]
```

**优点**：不占用 GitHub 空间，下载方便  
**缺点**：需要手动管理链接

---

## 快速诊断工具

### 检查仓库中的大文件

**PowerShell**：
```powershell
# 检查工作目录中的大文件
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 50MB} | Select-Object FullName, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB,2)}}

# 检查 Git 历史中的大文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | Where-Object {$_ -match '^blob'} | ForEach-Object {$_ -replace '^blob ', ''} | Sort-Object {[int]($_ -split ' ')[1]} -Descending | Select-Object -First 10
```

**Git Bash**：
```bash
# 检查 Git 历史中的大文件
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 --reverse | \
  head -10
```

---

## 推荐流程（针对你的情况）

基于你已经创建的脚本，推荐流程：

1. **首先运行** `彻底清理并推送.py`
   - 这会创建全新的分支，彻底解决问题
   - 对于课程作业，丢失历史记录通常不是问题

2. **如果仍然失败**，检查：
   - `.gitignore` 是否正确配置
   - 工作目录中是否还有大文件
   - 网络连接是否正常

3. **长期方案**：
   - 确保 `.gitignore` 包含所有大文件类型
   - 提交前检查文件大小
   - 考虑使用 Git LFS 或外部存储

---

## 预防措施

### 提交前检查清单

- [ ] 检查 `.gitignore` 是否包含所有大文件类型
- [ ] 运行 `git status` 确认没有大文件被跟踪
- [ ] 检查单个文件大小（不应超过 50MB）
- [ ] 检查仓库总大小（建议不超过 1GB）

### 自动检查脚本

可以创建一个提交前钩子（pre-commit hook）自动检查：

```bash
# .git/hooks/pre-commit
#!/bin/bash
# 检查是否有大于 50MB 的文件
large_files=$(git diff --cached --name-only | xargs ls -lh 2>/dev/null | awk '$5 ~ /[0-9]+M/ && $5+0 > 50 {print $9}')
if [ -n "$large_files" ]; then
    echo "错误：发现大于 50MB 的文件："
    echo "$large_files"
    echo "请使用 .gitignore 忽略这些文件或使用 Git LFS"
    exit 1
fi
```

---

## 常见问题

### Q: 为什么删除了文件，推送还是失败？
**A**: 因为文件还在 Git 历史记录中。需要使用 `git filter-branch` 或创建新分支来清理历史。

### Q: 可以使用 `git push --force` 吗？
**A**: 可以，但会覆盖远程历史。如果是个人仓库或团队同意，可以使用。**注意**：会丢失远程的历史记录。

### Q: Git LFS 收费吗？
**A**: GitHub 免费账户提供 1GB 存储空间和 1GB 带宽/月。超出后需要付费。

### Q: 如何恢复被清理的历史？
**A**: 如果使用了 `--force` 推送，历史记录无法恢复。建议在清理前备份仓库。

---

## 总结

对于你的情况（课程作业仓库），**最简单有效的方法是运行 `彻底清理并推送.py`**，它会：
- ✅ 创建全新的分支（丢弃历史）
- ✅ 只添加未被忽略的文件
- ✅ 强制推送到远程

这样可以快速解决问题，虽然会丢失历史记录，但对课程作业来说通常不是问题。
