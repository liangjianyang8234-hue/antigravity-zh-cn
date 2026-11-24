<div align="center">

# Antigravity 中文界面补丁

**让常用菜单与设置，用熟悉的中文呈现。**

Windows · Antigravity 2.34.0 指定构建 · 可恢复 · 非官方

如果这个项目帮到了你，欢迎点击仓库右上角的 **Star ⭐**。

点亮一颗星，让更多需要中文界面的朋友找到它。

</div>

---

## 这是什么？

一个为 Antigravity 桌面应用制作的本地中文界面补丁。它在原有界面预加载脚本中加入翻译逻辑，翻译已收录的菜单、按钮和设置说明。

- **常用界面中文化**：首页导航、常规、应用、外观、快捷键、通知、模型用量和浏览器设置中的已收录文案。
- **自动备份与恢复**：安装前备份原始归档，恢复时核对 SHA-256。
- **严格版本检查**：仅接受实际验证过的原版构建，遇到不匹配版本会停止。
- **本地运行**：补丁代码不添加联网请求、遥测或账号登录。
- **免费使用**：无需点 Star 才能下载或安装；喜欢再点 ⭐ 就好。

> 这是社区制作的非官方补丁，与 Google 无隶属或背书关系。不是完整中文发行版，部分动态文字或未适配页面仍可能显示英文。无法承诺所有功能绝对零影响。

## 支持范围

| 项目 | 当前支持 |
| --- | --- |
| 系统 | Windows x64 |
| Antigravity 版本 | 2.34.0，且原始归档 SHA-256 必须匹配下方数值 |
| 安装位置 | 默认用户目录、常见 Program Files 目录，或使用 `--app-dir` 指定 |
| macOS / Linux | 暂不支持 |
| 其他版本 / 同版本不同构建 | 不强行安装，请提交适配请求 |

已验证原始 `resources/app.asar` 的 SHA-256：

```text
8934adef0622c9271c92eea950a71848764a66f7b10023ccbd82e54b959adb0e
```

版本号相同也可能有不同构建。请勿删除校验或用旧归档覆盖新版。

## 普通用户：下载与安装

1. 从本仓库的 **Releases** 页面下载 `Antigravity-ZH-CN-v0.1.0-windows-x64.zip`。
2. 解压整个文件夹，完全退出 Antigravity。
3. 双击 `Antigravity-ZH-CN.exe`，输入 **1**，按 Enter 安装。
4. 看到安装成功提示后，从你原来的快捷方式打开 Antigravity。

Windows 发布包自带运行环境，**不需要另装 Python**，也不需要登录 GitHub。安装器不会自动结束你的进程，不会修改桌面快捷方式。

如果你下载的是 **Source code** 源码压缩包，里面没有 EXE，请使用下方源码运行方式。

安装在其他位置时，可在命令行手动指定：

```powershell
.\Antigravity-ZH-CN.exe install --app-dir "D:\Apps\Antigravity"
```

`--app-dir` 应指向 `Antigravity.exe` 所在文件夹，而不是 `resources` 文件夹。

## 恢复英文原版

完全退出 Antigravity，重新打开补丁工具，输入 **2** 并按 Enter。

也可以执行：

```powershell
.\Antigravity-ZH-CN.exe restore
```

原始备份保存在当前 Windows 用户的：

```text
%LOCALAPPDATA%\AntigravityZhPatch\backups\<安装位置标识>\
```

请保留该目录。恢复操作会检查当前程序和备份是否匹配；程序更新或被其他工具改动后，会拒绝覆盖。删除下载包不等于卸载补丁，应先运行恢复操作。

## 检查状态与预检查

```powershell
.\Antigravity-ZH-CN.exe status
.\Antigravity-ZH-CN.exe install --dry-run
```

`--dry-run` 只检查并在内存中构建补丁，不写入程序或备份文件。

## 源码运行

需要 Windows 和 Python 3.10 或更高版本，仅使用 Python 标准库，无需安装运行依赖。

```powershell
python src/patcher.py
python src/patcher.py install --dry-run
python src/patcher.py install
python src/patcher.py restore
```

## 它改了什么？

只向 `app.asar` 里的 `dist/preload.js` 追加本地翻译逻辑。归档索引及对应完整性字段会随文件长度重新计算；其他内部文件的内容逐项验证一致。本次已验证构建中，其余 **788 个文件内容不变**。

翻译脚本只处理已收录的界面文字和部分显示用属性，跳过输入框、可编辑区、代码、Markdown 消息等区域，并限制项目与对话链接的处理。不更换原有按钮或事件处理函数，不主动修改模型调用、账号数据、配置值、项目文件、权限开关或系统设置。

界面采用运行时文字替换，新打开的页面可能短暂出现英文。由于应用 DOM 结构可能变化，仍可能有漏译或个别误译，欢迎提供具体页面反馈。

## 常见问题

**提示“版本或构建校验值不在支持列表中”？**

当前安装包与已验证构建不同。工具会停止，不会强行修改。请提交版本适配请求，不要改校验值后直接使用。

**已经安装其他汉化补丁？**

先使用原补丁的恢复工具还原。此工具不会接管或覆盖没有对应恢复记录的旧补丁。

**提示先退出 Antigravity？**

关闭所有 Antigravity 窗口；如应用仍在后台运行，请从应用菜单正常退出，再重试。

**软件更新后中文消失？**

更新可能替换原程序归档。等补丁适配新版本后再安装，不要用旧备份覆盖更新后的软件。

**需要管理员权限吗？**

默认用户安装目录通常不需要；如果系统拒绝写入受保护的安装目录，本工具会报错，不会自动提权或修改目录权限。

## 验证情况

- 已有本机 Antigravity 2.34.0 首页和多个设置页的基础界面验证。
- 公开安装器有 12 项自动检查，覆盖归档重建、非目标文件一致性、安装恢复往返、预检查无写入、重复安装、版本拒绝、损坏备份、更新后拒绝恢复、写入失败及运行进程检查。
- 使用原始归档在临时目录中完成公开版的安装与恢复往返，未改动开发者正在使用的安装。
- Windows EXE 已在 PATH 不含 Python 的环境中通过启动和原始归档安装预检查；这项检查没有写入实际安装。
- 未覆盖所有页面、付费请求、真实模型生成或全部工作流的端到端验证。

## 自行构建发布包

在 Windows x64 上运行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe tools/build_release.py
```

产物位于 `release/`。构建过程只打包本项目源码和 Python 运行环境，不复制 Antigravity 程序或用户备份。可执行文件是未签名的本地构建。

运行检查：

```powershell
python -m unittest discover -s tests -v
```

有本机原始归档时，设置 `AGY_TEST_ORIGINAL` 为它的路径，可额外启用真实归档往返检查。原始归档始终留在本机，不提交到仓库。

## 一起完善中文界面

- 发现漏译或误译：提交 Issue，说明版本、页面与原文。
- 想贡献翻译：编辑 `src/ui-zh-cn.js`，提交 Pull Request。
- 觉得实用：给项目点 **Star ⭐**，或把仓库链接分享给需要的朋友。

## 许可

本项目新增的补丁代码和文档采用 [MIT License](LICENSE)。Antigravity 本身的名称、商标和原程序归各自权利人所有，不包含在本项目的 MIT 授权中。发布包不附带原程序、修改后的完整原程序归档或私人备份。
