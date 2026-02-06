# GitHub 仓库设置指南

本指南将帮助你完成 GitHub 仓库的初始设置，确保项目可以正常使用 GitHub Actions 自动更新功能。

## 📋 前置准备

在开始之前，请确保：
- ✅ 已安装 Git
- ✅ 已注册 GitHub 账号
- ✅ 已配置 Git 用户信息（用户名和邮箱）

## 🚀 步骤一：创建 GitHub 仓库

### 1.1 在 GitHub 上创建新仓库

1. 登录 GitHub，点击右上角的 **+** 号，选择 **New repository**
2. 填写仓库信息：
   - **Repository name**: 建议使用 `中山大学智能工程学院课程资料` 或 `SYSU-ISE-Course-Materials`
   - **Description**: `中山大学智能工程学院本科生课程资料共享项目`
   - **Visibility**: 选择 **Public**（公开，便于开源）
   - **不要**勾选 "Initialize this repository with a README"（因为本地已有文件）
3. 点击 **Create repository**

### 1.2 记录仓库地址

创建完成后，GitHub 会显示仓库地址，格式类似：
```
https://github.com/your-username/your-repo-name.git
```
请记录这个地址，后续会用到。

## 🔧 步骤二：初始化本地 Git 仓库

### 2.1 检查 Git 状态

在项目根目录打开终端（PowerShell 或 CMD），运行：

```bash
git status
```

如果显示 "not a git repository"，需要初始化：

```bash
git init
```

### 2.2 配置 Git 用户信息（如果未配置）

```bash
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"
```

### 2.3 添加所有文件

```bash
git add .
```

### 2.4 创建初始提交

```bash
git commit -m "初始提交：中山大学智能工程学院课程资料共享项目"
```

### 2.5 设置主分支名称

```bash
git branch -M main
```

### 2.6 添加远程仓库

将 `your-username` 和 `your-repo-name` 替换为你的实际信息：

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
```

### 2.7 推送到 GitHub

```bash
git push -u origin main
```

如果提示输入用户名和密码，请使用：
- **用户名**: 你的 GitHub 用户名
- **密码**: 使用 Personal Access Token（不是 GitHub 密码）

> 💡 **提示**: 如果还没有 Personal Access Token，请参考 [GitHub 文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) 创建。

## ⚙️ 步骤三：配置 GitHub Actions

这是**最关键**的步骤，确保自动更新功能正常工作。

### 3.1 启用 GitHub Actions

1. 进入你的 GitHub 仓库页面
2. 点击 **Settings**（设置）标签页
3. 在左侧菜单中找到 **Actions** → **General**
4. 在 **Actions permissions** 部分：
   - 选择 **Allow all actions and reusable workflows**
5. 在 **Workflow permissions** 部分：
   - 选择 **Read and write permissions**（重要！）
   - 勾选 **Allow GitHub Actions to create and approve pull requests**（可选）
6. 滚动到底部，点击 **Save**（保存）

### 3.2 验证工作流文件

确保以下文件存在且正确：
- ✅ `.github/workflows/update-readme.yml` 已存在
- ✅ 文件内容包含 `permissions: contents: write`

### 3.3 测试 GitHub Actions

1. 在仓库中创建一个测试文件（或修改现有文件）
2. 提交并推送更改：
   ```bash
   git add .
   git commit -m "test: 测试 GitHub Actions"
   git push
   ```
3. 在 GitHub 仓库页面，点击 **Actions** 标签页
4. 你应该能看到一个名为 "自动更新README" 的工作流正在运行
5. 等待工作流完成（通常需要 1-2 分钟）
6. 如果成功，README 文件应该会自动更新

## ✅ 步骤四：验证配置

### 检查清单

- [ ] GitHub 仓库已创建并设置为 Public
- [ ] 本地代码已推送到 GitHub
- [ ] GitHub Actions 已启用
- [ ] Workflow permissions 设置为 "Read and write permissions"
- [ ] `.github/workflows/update-readme.yml` 文件存在
- [ ] 测试工作流已成功运行
- [ ] README 文件已自动更新

### 常见问题排查

#### ❌ 问题 1: GitHub Actions 没有运行

**解决方案**:
1. 检查 Settings → Actions → General 中 Actions 是否已启用
2. 检查 `.github/workflows/update-readme.yml` 文件路径是否正确
3. 查看 Actions 标签页是否有错误信息

#### ❌ 问题 2: 工作流运行失败，提示权限不足

**解决方案**:
1. 进入 Settings → Actions → General
2. 确保 **Workflow permissions** 设置为 **Read and write permissions**
3. 保存后重新运行工作流

#### ❌ 问题 3: 推送代码时提示认证失败

**解决方案**:
1. 使用 Personal Access Token 代替密码
2. 或者配置 SSH 密钥进行认证

#### ❌ 问题 4: 工作流运行成功但 README 没有更新

**解决方案**:
1. 检查工作流日志，查看是否有错误
2. 确认 `更新README资料.py` 脚本是否正常运行
3. 检查是否有文件变化触发了工作流

## 📝 后续操作

### 添加仓库描述和主题

1. 进入仓库 Settings → General
2. 在 **Topics** 中添加标签，例如：
   - `education`
   - `course-materials`
   - `chinese-university`
   - `shenzhen-university`
   - `courseware`

### 添加仓库徽章（可选）

在 README.md 顶部添加徽章，例如：

```markdown
![GitHub Actions](https://github.com/your-username/your-repo/workflows/自动更新README/badge.svg)
![License](https://img.shields.io/badge/license-CC--BY--NC--SA--4.0-blue.svg)
```

### 设置仓库主页

1. 进入 Settings → Pages
2. 如果使用 GitHub Pages，可以配置源分支

## 🎉 完成！

现在你的项目已经：
- ✅ 托管在 GitHub 上
- ✅ 配置了 GitHub Actions 自动更新
- ✅ 可以接受贡献和 Pull Request

## 📚 相关文档

- [项目维护指南](项目维护指南.md) - 详细的维护说明
- [贡献指南](CONTRIBUTING.md) - 如何贡献内容
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

**提示**: 如果遇到任何问题，请查看 [项目维护指南](项目维护指南.md) 中的"常见问题"部分，或提交 Issue。
