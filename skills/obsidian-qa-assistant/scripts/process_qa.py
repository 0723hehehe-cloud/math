import os
import sys
import json
import re
import argparse


SUBJECT_ORDER = {
    "高等数学": 0,
    "线性代数": 1,
}

HIGHER_CHAPTER_ORDER = [
    ("极限", 0),
    ("连续", 0),
    ("积分", 1),
    ("微分", 2),
    ("导数", 2),
    ("多元", 3),
    ("线性代数", 0),
]

LINEAR_CHAPTER_ORDER = [
    ("行列式", 0),
    ("矩阵", 1),
    ("向量", 2),
    ("线性方程组", 3),
    ("特征值", 4),
    ("特征向量", 4),
    ("二次型", 5),
]

MATH_ONE_ONLY_KEYWORDS = (
    "概率",
    "级数",
    "微分方程",
    "空间解析几何",
    "向量代数",
    "曲线积分",
    "曲面积分",
)


def strip_order_prefix(value):
    return re.sub(r'^\d+[-_、.\s]*', '', value or '').strip()


def typical_example_sort_key(item):
    subject = strip_order_prefix(item.get("subject", ""))
    chapter = strip_order_prefix(item.get("chapter", ""))
    chapter_rank = 99
    chapter_order = LINEAR_CHAPTER_ORDER if subject == "线性代数" else HIGHER_CHAPTER_ORDER
    for keyword, rank in chapter_order:
        if keyword in chapter:
            chapter_rank = rank
            break
    return (
        SUBJECT_ORDER.get(subject, 99),
        chapter_rank,
        chapter,
        item.get("keypoint", ""),
        item.get("title", ""),
    )


def parse_typical_note(content):
    """Parse visible heading hierarchy and the shared summary."""
    entries = []
    summary = []
    current = None
    in_summary = False

    def finish_current():
        if current is not None:
            entries.append(current.copy())

    for line in content.splitlines():
        if line.startswith("%% typical-example:") or line.startswith("<!-- typical-example:"):
            # Ignore legacy metadata lines; headings now carry the structure.
            continue
        if line.strip() == "## 总结":
            finish_current()
            current = None
            in_summary = True
            continue
        if in_summary:
            if line.strip() not in {
                "> [!tip] 典型例子总结",
                "> 后续在这里总结不同章节的典型模型、通用方法和易错规律。",
            }:
                summary.append(line)
        elif line.startswith("## "):
            finish_current()
            current = None
        elif line.startswith("### "):
            if current is not None:
                finish_current()
                current = None
        elif line.startswith("#### "):
            if current is not None:
                finish_current()
                current = None
        elif line.startswith("##### "):
            finish_current()
            current = {
                "subject": "",
                "chapter": "",
                "keypoint": "",
                "title": line[6:].strip(),
                "content": [],
            }
        elif current is not None:
            current["content"].append(line)
    finish_current()

    # Recover hierarchy labels for each entry from the headings preceding it.
    subject = chapter = keypoint = ""
    for line in content.splitlines():
        if line.startswith("## ") and line.strip() != "## 总结":
            subject = line[3:].strip()
            chapter = keypoint = ""
        elif line.startswith("### "):
            chapter = line[4:].strip()
            keypoint = ""
        elif line.startswith("#### "):
            keypoint = line[5:].strip()
        elif line.startswith("##### "):
            title = line[6:].strip()
            for entry in entries:
                if entry.get("title") == title and not entry.get("subject"):
                    entry.update({"subject": subject, "chapter": chapter, "keypoint": keypoint})
                    break
    return entries, summary


def render_typical_note(entries, summary):
    """Render the single, curriculum-ordered typical-example note."""
    lines = [
        "---",
        "type: 典型例子",
        "tags:",
        "  - 典型例子",
        "---",
        "",
        "# 典型例子",
        "",
        "> 本笔记按考研数学二范围整理：极限与连续 → 积分 → 微分 → 多元函数与线性代数。",
        "",
    ]
    last_subject = None
    last_chapter = None
    last_keypoint = None
    for index, item in enumerate(sorted(entries, key=typical_example_sort_key), 1):
        subject = strip_order_prefix(item.get("subject", "未分类"))
        chapter = strip_order_prefix(item.get("chapter", "未分类"))
        keypoint = item.get("keypoint", "未分类")
        title = item.get("title", f"典型例子 {index}")
        if subject != last_subject:
            lines.extend([f"## {subject}", ""])
            last_subject, last_chapter, last_keypoint = subject, None, None
        if chapter != last_chapter:
            lines.extend([f"### {chapter}", ""])
            last_chapter, last_keypoint = chapter, None
        if keypoint != last_keypoint:
            lines.extend([f"#### {keypoint}", ""])
            last_keypoint = keypoint
        lines.extend([
            f"##### {title}",
        ])
        content_lines = item.get("content", [])
        lines.extend(content_lines)
        lines.append("")

    lines.extend(["## 总结", "", "> [!tip] 典型例子总结"])
    if summary:
        lines.extend(line if line.startswith(">") else f"> {line}" for line in summary)
    else:
        lines.append("> 后续在这里总结不同章节的典型模型、通用方法和易错规律。")
    return "\n".join(lines).rstrip() + "\n"


def build_typical_example(data):
    """Add one example or summary to the single typical-example note."""
    subject = strip_order_prefix(data.get("subject", ""))
    if subject and subject not in SUBJECT_ORDER:
        raise ValueError("典型例子模块只接收数学二内容：高等数学或线性代数；不接收概率论等数学一内容。")
    topic_text = " ".join(str(data.get(field, "")) for field in ("chapter", "keypoint", "title"))
    if any(keyword in topic_text for keyword in MATH_ONE_ONLY_KEYWORDS):
        raise ValueError("该内容属于数学一或非数学二范围，不写入典型例子总笔记。")
    vault_root = data.get("vault_root", "D:/ob/考研数学")
    os.makedirs(vault_root, exist_ok=True)
    file_path = os.path.join(vault_root, "典型例子.md")
    existing = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing = f.read()
    entries, summary = parse_typical_note(existing)

    if data.get("title") and data.get("examples"):
        entry = {
            "subject": data.get("subject", "未分类"),
            "chapter": data.get("chapter", "未分类"),
            "keypoint": data.get("keypoint", "未分类"),
            "title": data["title"],
            "content": ["> [!example] 典型例子"],
        }
        entry["content"].extend(f"> {line}" for line in data["examples"].splitlines())
        entries = [e for e in entries if not (
            e.get("subject") == entry["subject"]
            and e.get("chapter") == entry["chapter"]
            and e.get("keypoint") == entry["keypoint"]
            and e.get("title") == entry["title"]
        )]
        entries.append(entry)

    if data.get("summary"):
        summary.extend(data["summary"].splitlines())

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(render_typical_note(entries, summary))
    print(json.dumps({"status": "success", "file_path": file_path.replace("\\", "/"), "is_merged": bool(existing)}))

def sanitize_filename(name):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def is_image_embed(line):
    """Return True for a standalone Markdown or Obsidian image embed."""
    value = line.strip()
    return bool(
        re.match(r'^!\[[^\]]*\]\([^)]*\)$', value)
        or re.match(r'^!\[\[[^\]]+\]\]$', value)
    )


def collect_and_remove_images(sections):
    """Remove all image embeds and return the first one for canonical placement."""
    first_image = None
    cleaned = {}
    for section_name, lines in sections.items():
        kept = []
        for line in lines:
            if is_image_embed(line):
                if first_image is None:
                    first_image = line.strip()
                continue
            kept.append(line)
        cleaned[section_name] = kept
    return cleaned, first_image

def parse_callout(lines, start_idx):
    """
    Parses a callout block starting at start_idx.
    Returns (callout_type, title, content_lines, end_idx)
    """
    first_line = lines[start_idx]
    # Match > [!type] Title or > [!type]- Title
    match = re.match(r'^>\s*\[!([^\]]+)\][-]?\s*(.*)$', first_line)
    if not match:
        return None, None, [], start_idx + 1
    
    callout_type = match.group(1).lower().strip()
    title = match.group(2).strip()
    
    content_lines = []
    idx = start_idx + 1
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('>'):
            # Check if this line is a new sibling callout
            if re.match(r'^>\s*\[![^\]]+\]', line):
                break
            # Strip the leading '>' and optional space
            content_line = re.sub(r'^>\s?', '', line)
            content_lines.append(content_line)
            idx += 1
        else:
            break
            
    return callout_type, title, content_lines, idx
            
    return callout_type, title, content_lines, idx

def parse_markdown(content):
    """
    Parses an existing Obsidian note into its structural components.
    Returns:
        yaml_lines: list of strings
        title: string
        sections: dict of callout_type -> list of content lines (without leading '>')
        other_blocks: list of lists of strings (for arbitrary content not in callouts)
    """
    lines = content.splitlines()
    yaml_lines = []
    title = ""
    sections = {}
    other_blocks = []
    
    in_yaml = False
    yaml_count = 0
    idx = 0
    
    # 1. Parse YAML Frontmatter
    if idx < len(lines) and lines[idx].strip() == "---":
        in_yaml = True
        yaml_lines.append(lines[idx])
        idx += 1
        while idx < len(lines):
            yaml_lines.append(lines[idx])
            if lines[idx].strip() == "---":
                idx += 1
                break
            idx += 1
            
    # 2. Parse Title and Callouts
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "":
            idx += 1
            continue
            
        if line.startswith("# "):
            title = line[2:].strip()
            idx += 1
            continue
            
        if line.startswith(">"):
            callout_type, c_title, c_lines, next_idx = parse_callout(lines, idx)
            if callout_type:
                sections[callout_type] = c_lines
                idx = next_idx
                continue
            else:
                block = [line]
                idx += 1
                while idx < len(lines) and not lines[idx].startswith("# ") and not lines[idx].startswith(">"):
                    block.append(lines[idx])
                    idx += 1
                other_blocks.append(block)
                continue
        
        # Arbitrary content block
        block = []
        while idx < len(lines) and not lines[idx].startswith("# ") and not lines[idx].startswith(">"):
            block.append(lines[idx])
            idx += 1
        if any(b.strip() for b in block):
            other_blocks.append(block)
            
    return yaml_lines, title, sections, other_blocks

def merge_section_lines(existing_lines, new_text):
    """
    Intelligently merges new_text (string) into existing_lines (list of strings).
    Avoids duplicate lines (like bullet points or formulas).
    """
    if not new_text:
        return existing_lines
    
    new_lines = new_text.splitlines()
    merged = list(existing_lines)
    
    # Strip empty lines from end of existing
    while merged and merged[-1].strip() == "":
        merged.pop()
        
    existing_stripped = {l.strip() for l in merged if l.strip()}
    
    # Determine if we should append directly or formatting is needed
    for line in new_lines:
        trimmed = line.strip()
        if not trimmed:
            continue
        # Avoid exact duplicate lines
        if trimmed in existing_stripped:
            continue
        
        # If merged is not empty and the last item doesn't have an empty line, and we are adding a formula block
        if trimmed.startswith("$$") and merged and merged[-1].strip() != "":
            merged.append("")
            
        merged.append(line)
        
    return merged

def get_subchapter_folder(note_type, subject, chapter, keypoint, title):
    if sanitize_filename(chapter) == "01-函数极限与连续":
        target = (keypoint or "") + (title or "")
        
        limit_keywords = ["极限", "无界", "无穷", "0乘"]
        for kw in limit_keywords:
            if kw in target:
                return "02-极限与未定式"
                
        func_keywords = ["函数", "对数", "三角", "双曲", "不等式", "绝对值", "有界性", "奇偶", "周期"]
        for kw in func_keywords:
            if kw in target:
                return "01-函数及其性质"
                
        return "02-极限与未定式"
        
    elif sanitize_filename(chapter) == "02-一元函数微分学":
        target = (keypoint or "") + (title or "")
        
        app_keywords = ["中值定理", "单调", "极值", "最值", "凹凸", "拐点", "渐近线", "曲率", "不等式证明", "零点"]
        for kw in app_keywords:
            if kw in target:
                return "02-中值定理与导数应用"
                
        return "01-导数与微分"
        
    return ""

def build_note(note_type, subject, chapter, title, keypoint, data):
    """
    Builds or merges an Obsidian note.
    """
    vault_root = data.get("vault_root", "D:/ob/考研数学")
    
    # Determine folder paths
    sub_folder = "错题本" if note_type == "错题" else "知识点"
    
    sub_ch = get_subchapter_folder(note_type, subject, chapter, keypoint, title)
    if note_type == "错题":
        if sub_ch:
            dir_path = os.path.join(vault_root, sub_folder, sanitize_filename(subject), sanitize_filename(chapter), sub_ch, sanitize_filename(keypoint))
        else:
            dir_path = os.path.join(vault_root, sub_folder, sanitize_filename(subject), sanitize_filename(chapter), sanitize_filename(keypoint))
    else:
        if sub_ch:
            dir_path = os.path.join(vault_root, sub_folder, sanitize_filename(subject), sanitize_filename(chapter), sub_ch)
        else:
            dir_path = os.path.join(vault_root, sub_folder, sanitize_filename(subject), sanitize_filename(chapter))
    
    # Determine filename
    filename = f"{sanitize_filename(title)}.md"
        
    file_path = os.path.join(dir_path, filename)
    os.makedirs(dir_path, exist_ok=True)
    
    # Read existing file if it exists
    existing_content = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
            
    yaml_lines, existing_title, sections, other_blocks = parse_markdown(existing_content)
    
    # Parse existing source if any
    existing_source = ""
    for line in yaml_lines:
        match = re.match(r'^source:\s*(.*)$', line.strip())
        if match:
            existing_source = match.group(1).strip()
            break
            
    source = data.get("source", existing_source)
    
    # Normalize image placement: one image, in the designated content callout only.
    sections, existing_image = collect_and_remove_images(sections)

    # Format Image Path
    img_embed = ""
    if data.get("image_path"):
        # Convert path to standard forward slashes for markdown URL
        img_url = data["image_path"].replace("\\", "/")
        if not img_url.startswith("file:///"):
            img_url = f"file:///{img_url}"
        img_embed = f"![]({img_url})"
    elif existing_image:
        img_embed = existing_image
        
    # Standard YAML
    tags = []
    if note_type == "错题":
        if sub_ch:
            tags = [f"错题本/{subject}/{chapter}/{sub_ch}/{keypoint}"]
        else:
            tags = [f"错题本/{subject}/{chapter}/{keypoint}"]
    else:
        if sub_ch:
            tags = [f"知识点/{subject}/{chapter}/{sub_ch}/{title}"]
        else:
            tags = [f"知识点/{subject}/{chapter}/{title}"]
        
    yaml_block = f"---\ntype: {note_type}\n"
    if note_type == "错题" and source:
        yaml_block += f"source: {source}\n"
    yaml_block += "tags:\n"
    for tag in tags:
        yaml_block += f"  - {tag}\n"
    yaml_block += "---"
    
    if note_type == "错题":
        # Check sections
        q_lines = sections.get("question", [])
        if not q_lines:
            q_lines = []
            input_text = data.get("input_text", "")
            if input_text:
                q_lines.extend(input_text.splitlines())
            if img_embed:
                q_lines.append(img_embed)
        else:
            # If question already exists, keep it, but make sure image path is not duplicated
            if img_embed and not any(img_embed.strip() in l for l in q_lines):
                q_lines.append(img_embed)
                
        s_lines = sections.get("success", [])
        if not s_lines:
            analysis_text = data.get("analysis", "")
            s_lines = [f"**相关知识点**: [[{keypoint}]]", ""]
            if analysis_text:
                s_lines.extend(analysis_text.splitlines())
        else:
            # Merge analysis
            analysis_text = data.get("analysis", "")
            if analysis_text:
                s_lines = merge_section_lines(s_lines, analysis_text)
                
        w_lines = sections.get("warning", [])
        if not w_lines:
            w_lines = []
            w_lines.append(f"- **核心考点**: {keypoint}")
            
            key_method = data.get('key_method', '')
            if key_method:
                km_lines = key_method.splitlines()
                w_lines.append(f"- **解题关键**: {km_lines[0]}")
                for kml in km_lines[1:]:
                    w_lines.append(f"  {kml}")
                    
            pitfalls = data.get('pitfalls', '')
            if pitfalls:
                pf_lines = pitfalls.splitlines()
                w_lines.append(f"- **易错点**: {pf_lines[0]}")
                for pfl in pf_lines[1:]:
                    w_lines.append(f"  {pfl}")
            
        d_lines = sections.get("danger", []) or sections.get("caution", [])
        if not d_lines:
            user_error = data.get("user_error", "") or data.get("my_error_reason", "")
            if user_error:
                d_lines = [f"- **核心错因**: {l}" if idx == 0 else f"  {l}" for idx, l in enumerate(user_error.splitlines())]

        # Format markdown output
        md_content = f"{yaml_block}\n\n# {title}\n\n"
        
        if d_lines:
            md_content += "> [!danger] ❌ 为什么错（个人错因与盲区）\n"
            for l in d_lines:
                md_content += f"> {l}\n"
            md_content += "\n"

        md_content += "> [!question] 题目\n"
        for l in q_lines:
            md_content += f"> {l}\n"
        md_content += "\n"
        
        md_content += "> [!success] 解析与答案\n"
        for l in s_lines:
            md_content += f"> {l}\n"
        md_content += "\n"
        
        md_content += "> [!warning] 易错点 & 核心考点\n"
        for l in w_lines:
            md_content += f"> {l}\n"
            
    else: # 知识点
        # Merge info section
        info_lines = sections.get("info", [])
        new_def = data.get("definition", "")
        if not info_lines:
            info_lines = []
            if new_def:
                info_lines.extend(new_def.splitlines())
            if img_embed:
                info_lines.append(img_embed)
        else:
            if new_def:
                info_lines = merge_section_lines(info_lines, new_def)
            if img_embed and not any(img_embed.strip() in l for l in info_lines):
                info_lines.append(img_embed)
                
        # Merge todo section (formulas)
        todo_lines = sections.get("todo", [])
        new_formulas = data.get("formulas", "")
        if not todo_lines:
            todo_lines = []
            if new_formulas:
                todo_lines.extend(new_formulas.splitlines())
        else:
            if new_formulas:
                todo_lines = merge_section_lines(todo_lines, new_formulas)
                
        # Merge tip section (conclusions)
        tip_lines = sections.get("tip", [])
        new_conclusions = data.get("conclusions", "")
        if not tip_lines:
            tip_lines = []
            if new_conclusions:
                tip_lines.extend(new_conclusions.splitlines())
        else:
            if new_conclusions:
                tip_lines = merge_section_lines(tip_lines, new_conclusions)
                
        # Merge example section
        example_lines = sections.get("example", [])
        new_examples = data.get("examples", "")
        if not example_lines:
            example_lines = []
            if new_examples:
                example_lines.extend(new_examples.splitlines())
        else:
            if new_examples:
                example_lines = merge_section_lines(example_lines, new_examples)
                
        # Format markdown output
        md_content = f"{yaml_block}\n\n# {title}\n\n"
        
        md_content += "> [!info] 概念定义\n"
        for l in info_lines:
            md_content += f"> {l}\n"
        md_content += "\n"
        
        md_content += "> [!todo] 核心公式与性质\n"
        for l in todo_lines:
            md_content += f"> {l}\n"
        md_content += "\n"
        
        md_content += "> [!tip] 考研核心结论 (必背)\n"
        for l in tip_lines:
            md_content += f"> {l}\n"
            
        if example_lines:
            md_content += "\n> [!example] 典型例子\n"
            for l in example_lines:
                md_content += f"> {l}\n"
            
    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")
        
    print(json.dumps({
        "status": "success",
        "file_path": file_path.replace("\\", "/"),
        "is_merged": len(existing_content) > 0
    }))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Obsidian QA and Concepts")
    parser.add_argument("--json-file", help="Path to input JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    
    args = parser.parse_args()
    
    if args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.stdin or not sys.stdin.isatty():
        data = json.loads(sys.stdin.read())
    else:
        print("Error: Must provide --json-file or input JSON via stdin")
        sys.exit(1)
        
    note_type = data.get("type")
    subject = data.get("subject")
    chapter = data.get("chapter")
    title = data.get("title")
    keypoint = data.get("keypoint")
    
    if note_type == "典型例子":
        typical_path = os.path.join(data.get("vault_root", "D:/ob/考研数学"), "典型例子.md")
        if not (data.get("examples") or data.get("summary") or os.path.exists(typical_path)):
            print("Error: 典型例子需要提供 examples 或 summary。")
            sys.exit(1)
        try:
            build_typical_example(data)
        except ValueError as exc:
            print(f"Error: {exc}")
            sys.exit(1)
        sys.exit(0)

    if not all([note_type, subject, chapter, title]):
        print("Error: Missing required fields ('type', 'subject', 'chapter', 'title') in JSON input.")
        sys.exit(1)
        
    build_note(note_type, subject, chapter, title, keypoint, data)
