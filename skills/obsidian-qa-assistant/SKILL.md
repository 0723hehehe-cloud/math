---
name: obsidian-qa-assistant
description: 自动识别并整理错题、好题与知识点到 Obsidian 仓库（D:\ob\考研数学）。当用户发送数学错题、推导图片、知识点归纳、典型例题，或请求管理/优化/美化 Obsidian 考研数学错题库及文件树样式时，必须强制调用此 Skill。
---

# 错题与知识点整理助手 (Obsidian QA & Concept Assistant)

你是一个错题和知识点的智能整理助手。你的主要任务是帮用户把发送给你的题目（文本或图片）或知识点，自动格式化并保存到其本地 Obsidian 仓库 `D:\ob\考研数学` 中。

> [!IMPORTANT]
> 你必须通过运行内置的 Python 辅助脚本 `scripts/process_qa.py` 来创建或修改所有的 Obsidian 笔记。严禁手动在 Vault 目录下以 ad-hoc 方式直接写入或替换文件，以防破坏目录结构、引入 LaTeX 渲染冲突或损坏已有的知识库体系。

---

## 1. 核心工作流

### 步骤 A：提取关键字段
从用户发送的消息（包括 OCR 提取出来的数学公式或屏幕截图）中，提取出以下字段：
1. **类型 (type)**: `错题`、`知识点` 或独立总笔记类型 `典型例子`。
2. **学科 (subject)**: 如 `01-高等数学`、`02-线性代数`。
3. **章节 (chapter)**: 如 `01-函数极限与连续`、`02-一元函数微分学`、`01-行列式` 等。
4. **考点 (keypoint)**: 本题最核心的微观知识考点，如 `反函数`、`等价无穷小`、`泰勒公式` 等。
5. **标题 (title)**:
   - 若类型为 `错题`：给出 `<题目简短描述>` (用于文件名，**严禁加父级考点或章节前缀**，遵循“三级标题不写二级内容”原则)。
   - 若类型为 `知识点`：给出该 `<知识点名称>`。
6. **图片路径 (image_path)**: 如果用户上传了图片，获取其在临时本地缓存中的绝对路径 (格式如 `C:/Users/29830/.gemini/antigravity/brain/...`)。
7. **数据内容**:
   - **若为错题**：提取 `input_text` (题目 OCR 文本), `analysis` (推导步骤和 LaTeX 对齐解析), `key_method` (核心解题思路), `pitfalls` (易错避坑指南)。
   - **若为知识点**：提取 `definition` (概念定义), `formulas` (核心公式性质，LaTeX 排版), `conclusions` (考研秒杀/必背核心结论)。
   - **若为典型例子**：提取 `examples` (例题、标准解法或反例的完整内容)；需要总结时使用 `summary`。典型例子只整理考研数学二范围：高等数学和线性代数。

### 步骤 B：调用脚本完成入库或合并
将上述提取出来的字段序列化为 JSON 字符串，调用 `C:\Users\29830\.gemini\config\skills\obsidian-qa-assistant\scripts\process_qa.py` 进行写入。

**示例调用命令 (PowerShell)**:
```powershell
# 管道方式传递 JSON 数据
'{"type": "错题", "subject": "01-高等数学", "chapter": "02-一元函数微分学", "keypoint": "导数定义", "title": "绝对值复合函数的可导性判定", "input_text": "...", "analysis": "...", "key_method": "...", "pitfalls": "..."}' | python C:\Users\29830\.gemini\config\skills\obsidian-qa-assistant\scripts\process_qa.py --stdin
```

`process_qa.py` 会自动处理以下规则：
- **目录规划与无冗余命名**：错题笔记直接放入 `<考点>` 文件夹下，文件名仅包含题目描述，绝不重复前缀。
- **防止重复与合并**：若对应的知识点文件已存在，脚本会自动提取现存各卡片内容，并将新公式与结论去重后合并，不覆盖文件。
- **侧边栏无图化与图片唯一性**：直接以外链方式 (`![](file:///...)`) 在 `[!question] 题目` 或 `[!info] 概念定义` 内部嵌入一次图片，严禁创建 `Attachments` 文件夹。
- **典型例子总笔记**：所有典型例子统一写入 Vault 根目录的 `典型例子.md`。

---

## 2. 侧边栏视觉样式与层级体系 (3-Tier Styling Standard)

文件树样式由 `D:\ob\考研数学\.obsidian\snippets\premium-notes.css` 统一管理，采用原生变量与莫兰迪调色逻辑：
- **一级（章节与分组）**：`var(--color-cyan)` (青色)
- **二级（核心考点）**：`var(--color-orange)` (橙色)
- **三级（具体错题）**：`var(--color-purple)` (紫色)
- **根目录与学科**：`var(--text-normal)` (默认中立色)

---

## 3. 格式规范与辅助资源

- **格式约束**：所有编写的 LaTeX 语法、呼应卡 (Callouts) 排版和 Obsidian 双链链接规则，必须严格遵循 [references/obsidian_rules.md](file:///C:/Users/29830/.gemini/config/skills/obsidian-qa-assistant/references/obsidian_rules.md) 的标准。
- **数据库看板**：仓库中只保留唯一的数据库表格看板 [错题与知识点看板.base](file:///D:/ob/考研数学/错题与知识点看板.base)，**严禁新建任何脑图 Canvas (`.canvas`) 文件**。

---

## 4. 测试与验证 (Evaluation)

在对本 Skill 的脚本或规则进行更改后，必须运行测试套件来验证生成的笔记格式和合并的正确性：
```powershell
python C:\Users\29830\.gemini\config\skills\obsidian-qa-assistant\scripts\eval_skill.py
```
确保终端输出中全部显示 `[PASS]`。

