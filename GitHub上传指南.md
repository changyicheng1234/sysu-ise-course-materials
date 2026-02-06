# GitHub 上传指南

## 快速上传步骤

### 方法一：使用批处理脚本（推荐）

1. 双击运行 `上传到GitHub.bat` 文件
2. 按照提示操作即可

### 方法二：手动执行 Git 命令

在项目根目录打开命令行（PowerShell 或 CMD），依次执行以下命令：

#### 1. 初始化 Git 仓库（如果还没有初始化）

```bash
git init
```

#### 2. 添加远程仓库

```bash
git remote add origin https://github.com/changyicheng1234/-.git
```

如果已经添加过远程仓库，可以使用以下命令更新：

```bash
git remote set-url origin https://github.com/changyicheng1234/-.git
```

#### 3. 配置 Git 用户信息（如果还没有配置）

```bash
git config user.name "changyicheng1234"
git config user.email "changyicheng1234@users.noreply.github.com"
```

#### 4. 添加所有文件

```bash
git add .
```

#### 5. 提交更改

```bash
git commit -m "更新：上传课程资料到 GitHub"
```

#### 6. 设置主分支并推送

```bash
git branch -M main
git push -u origin main
```

## 常见问题

### 1. 推送时要求输入用户名和密码

GitHub 已经不再支持使用密码进行 HTTPS 认证。你需要：

**选项 A：使用 Personal Access Token (PAT)**

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (classic)"
3. 设置权限：至少勾选 `repo` 权限
4. 生成 token 后，在推送时：
   - 用户名：输入你的 GitHub 用户名 `changyicheng1234`
   - 密码：输入刚才生成的 Personal Access Token

**选项 B：使用 SSH 密钥（推荐）**

1. 生成 SSH 密钥：
```bash
ssh-keygen -t ed25519 -C "changyicheng1234@users.noreply.github.com"
```

2. 将公钥添加到 GitHub：
   - 复制 `~/.ssh/id_ed25519.pub` 的内容
   - 访问 https://github.com/settings/keys
   - 点击 "New SSH key"，粘贴公钥

3. 将远程仓库地址改为 SSH：
```bash
git remote set-url origin git@github.com:changyicheng1234/-.git
```

### 2. 文件太大无法推送

如果某些文件（如视频、大图片）超过 GitHub 的 100MB 限制，可以：

1. 检查 `.gitignore` 文件，确保大文件被忽略
2. 如果文件已经在 Git 历史中，需要从历史中移除：
```bash
git rm --cached 文件名
git commit -m "移除大文件"
```

### 3. 推送被拒绝（rejected）

如果远程仓库已经有内容，需要先拉取：

```bash
git pull origin main --allow-unrelated-histories
```

然后解决冲突后再推送。

### 4. 只推送部分文件

如果只想推送特定文件：

```bash
git add 文件名或目录
git commit -m "更新特定文件"
git push origin main
```

## 后续更新

以后如果有新的更改，只需要执行：

```bash
git add .
git commit -m "更新说明"
git push origin main
```

或者使用 `上传到GitHub.bat` 脚本自动完成这些步骤。

## 注意事项

- ⚠️ 确保 `.gitignore` 文件正确配置，避免上传敏感信息
- ⚠️ 大文件（>100MB）无法直接推送到 GitHub
- ⚠️ 首次推送可能需要较长时间，请耐心等待
- ✅ 建议定期提交和推送，避免一次性推送过多文件
