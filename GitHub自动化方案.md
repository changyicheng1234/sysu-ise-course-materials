# GitHub 自动化维护方案

## 🎯 问题

上传到 GitHub 后，如何实现自动更新 README？如何维护这种课程作业项目？

## ✅ 解决方案

采用 **GitHub Actions** 实现完全自动化的维护流程。

## 🔄 工作流程

### 自动化流程

```
开发者提交文件
    ↓
GitHub 接收 Push
    ↓
触发 GitHub Actions
    ↓
运行更新脚本
    ↓
自动更新所有 README
    ↓
自动提交更改
    ↓
完成 ✅
```

### 详细步骤

1. **开发者操作**：
   - 添加文件到课程目录
   - `git add .`
   - `git commit -m "添加资料"`
   - `git push`

2. **GitHub Actions 自动执行**：
   - 检测到文件变化（排除 README 本身）
   - 运行 `更新README资料.py`
   - 扫描所有课程目录
   - 更新 README 的"资料介绍"部分
   - 自动提交更改

3. **结果**：
   - README 自动更新
   - 无需人工干预
   - 保持内容始终最新

## 📁 文件结构

```
项目根目录/
├── .github/
│   └── workflows/
│       └── update-readme.yml    # GitHub Actions 工作流
├── 更新README资料.py            # 自动更新脚本（已适配 GitHub）
├── 运行更新README.bat           # 本地批处理文件
├── CONTRIBUTING.md              # 贡献指南
├── 项目维护指南.md              # 维护说明
├── README.md                    # 项目主说明
└── [课程目录]/
    └── README.md                # 课程说明（自动更新）
```

## 🚀 部署步骤

### 1. 准备文件

确保以下文件已创建：

- ✅ `.github/workflows/update-readme.yml` - GitHub Actions 配置
- ✅ `更新README资料.py` - 已适配 GitHub 环境
- ✅ `CONTRIBUTING.md` - 贡献指南
- ✅ `.gitignore` - Git 忽略文件

### 2. 推送到 GitHub

```bash
git add .
git commit -m "feat: 添加 GitHub Actions 自动更新功能"
git push origin main
```

### 3. 启用 Actions

1. 进入仓库 Settings
2. 找到 **Actions** → **General**
3. 确保 **"Allow all actions and reusable workflows"** 已启用
4. 在 **"Workflow permissions"** 中选择 **"Read and write permissions"**

### 4. 测试

1. 添加一个测试文件到某个课程目录
2. 提交并推送：
   ```bash
   git add .
   git commit -m "test: 测试自动更新"
   git push
   ```
3. 查看 **Actions** 标签页
4. 应该能看到工作流运行
5. 检查 README 是否自动更新

## 🔧 技术细节

### GitHub Actions 配置

工作流文件：`.github/workflows/update-readme.yml`

**触发条件**：
- `push` 到 `main` 或 `master` 分支
- 文件变化（排除 README 本身）
- 可手动触发（`workflow_dispatch`）

**执行步骤**：
1. 检出代码
2. 设置 Python 环境
3. 运行更新脚本
4. 检查是否有更改
5. 如果有更改，自动提交

### 脚本适配

`更新README资料.py` 已适配 GitHub 环境：

```python
def get_base_path():
    """自动检测项目根目录"""
    # 1. 如果在 Git 仓库中，使用项目根目录
    if (current_file.parent / '.git').exists():
        return current_file.parent
    # 2. 如果在 GitHub Actions 中
    if os.environ.get('GITHUB_WORKSPACE'):
        return Path(os.environ['GITHUB_WORKSPACE'])
    # 3. 默认使用本地路径
    return Path(r"d:\学习\...")
```

### 权限配置

- 使用 `GITHUB_TOKEN`（GitHub 自动提供）
- 权限：`contents: write`
- 无需额外配置

## 📊 维护方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **GitHub Actions** | 完全自动化，无需人工 | 需要 GitHub 仓库 | 正式项目，多人协作 |
| **本地脚本** | 快速测试，可预览 | 需要手动运行 | 本地开发，批量处理 |
| **手动维护** | 完全控制 | 容易遗漏，工作量大 | 特殊需求，格式调整 |

## 🎯 推荐工作流

### 日常使用（推荐）

1. **添加资料** → 直接提交到 GitHub
2. **自动更新** → GitHub Actions 自动处理
3. **完成** → 无需其他操作

### 本地开发

1. **添加资料** → 放入课程目录
2. **运行脚本** → `python 更新README资料.py`
3. **检查效果** → 查看生成的 README
4. **提交更改** → 推送到 GitHub

## ⚠️ 注意事项

### 1. Actions 权限

确保 Actions 有写入权限：
- Settings → Actions → General
- Workflow permissions → Read and write permissions

### 2. 文件大小

- 大文件（>100MB）建议使用 Git LFS
- 避免提交不必要的文件

### 3. 提交频率

- Actions 每次运行都会提交
- 如果频繁提交，可能会产生很多 commit
- 可以考虑批量提交或使用 squash merge

### 4. 错误处理

- 如果 Actions 失败，查看日志
- 检查脚本是否有错误
- 确保文件路径正确

## 🔍 监控和调试

### 查看 Actions 运行

1. 进入仓库
2. 点击 **Actions** 标签页
3. 查看工作流运行历史
4. 点击具体运行查看日志

### 常见问题

**Q: Actions 没有运行？**
- 检查是否启用 Actions
- 检查工作流文件路径是否正确
- 检查触发条件是否满足

**Q: Actions 运行失败？**
- 查看日志找出错误
- 检查脚本是否有语法错误
- 检查文件权限

**Q: README 没有更新？**
- 检查脚本是否成功运行
- 检查是否有文件变化
- 检查提交是否成功

## 📈 未来改进

可以考虑的功能：

1. **增量更新**：只更新有变化的目录
2. **提交优化**：批量提交或使用 squash
3. **通知功能**：更新后发送通知
4. **预览功能**：在 PR 中预览更新效果
5. **验证功能**：检查文件格式和命名规范

## 📝 总结

通过 GitHub Actions，我们实现了：

✅ **完全自动化**：提交文件后自动更新 README  
✅ **无需人工干预**：GitHub 自动处理一切  
✅ **保持最新**：README 始终反映最新状态  
✅ **易于维护**：减少人工维护成本  

**核心优势**：
- 开发者只需添加文件，无需关心 README
- 自动化保证内容始终最新
- 降低维护成本，提高效率

---

**记住**：上传到 GitHub 后，一切都会自动运行！🚀
