# Obsidian QA & Concept Formatting Guidelines

## 1. Vault Directory Structure
- **Vault Root**: `D:/ob/考研数学`
- **Questions Directory**: `D:/ob/考研数学/错题本/<二级学科>/<章节>/<考点>/`
- **Concepts Directory**: `D:/ob/考研数学/知识点/<二级学科>/<章节>/`

## 2. Naming Conventions
- **Questions**: `<题目简短描述>.md` (e.g. `绝对值复合函数的可导性判定.md`). 严禁在前缀冗余重复父级考点或章节名称（符合“三级标题不写二级内容”原则）。
- **Concepts**: `<知识点名称>.md` (e.g. `泰勒公式.md`)
- File names must only use alphanumeric characters, hyphens, and Chinese characters. Avoid slashes or special characters.

## 3. Formatting & LaTeX Guidelines
- **Double Bracket Linking**: Cross-reference concepts using standard Obsidian wikilinks: `[[知识点名称]]`.
- **Nesting callouts**: Ensure proper markdown spacing.
- **LaTeX Math Rules**:
  - Use `$$ ... $$` on their own lines for block-style equations.
  - Use `$ ... $` for inline math equations.
  - Do not put block `$$ ... $$` inside list items or blockquotes in a way that breaks the markdown renderer. Ensure they are on separate lines with correct indentation.
  - Highlight key math properties/equations using `==$公式$==` or `==**加粗内容**==`.
  - Align multi-step mathematical derivations using `\begin{aligned} ... \end{aligned}` blocks.

## 4. Image Reference Policies
- **Direct Cache Links**: All images must use the local AppData cache paths directly: `![](file:///C:/Users/...)`.
- **Single Embedding**: The image should be embedded exactly once in the designated Callout:
  - For questions: `[!question] 题目` card.
  - For concepts: `[!info] 概念定义` card.
- **Global Uniqueness**: The final note must contain exactly one image embed when an image is supplied. Remove duplicate, stale, or misplaced image embeds before writing the note.
- **No Vault Storage**: Do not save image files in the Obsidian Vault (`D:/ob/考研数学/`) or in any `Attachments/` folder. Keep Vault 100% pure markdown notes to keep the vault clean.

## 5. Sidebar Visual Hierarchy (3-Tier Styling Standard)
All file tree styles are maintained in `D:\ob\考研数学\.obsidian\snippets\premium-notes.css`:
- **Tier 1 (Chapters & Sub-chapters)**: `var(--color-cyan)` (内置青色)
- **Tier 2 (Keypoints)**: `var(--color-orange)` (内置橙色)
- **Tier 3 (Files)**: `var(--color-purple)` (内置紫色)
- **Root & Subjects**: `var(--text-normal)` (默认中立色)

