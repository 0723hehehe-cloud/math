import os
import sys
import json
import re
import argparse

SUBJECT_ORDER = {
    "高等数学": 0,
    "线性代数": 1,
}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name or "").strip()

def get_subchapter_folder(subject, chapter, keypoint, title):
    subject_clean = sanitize_filename(subject)
    chapter_clean = sanitize_filename(chapter)
    target = f"{keypoint or ''} {title or ''}"
    
    if chapter_clean == "01-函数极限与连续":
        limit_keywords = ["极限", "无界", "无穷", "0乘", "未定式"]
        for kw in limit_keywords:
            if kw in target:
                return "02-极限与未定式"
                
        func_keywords = ["函数", "对数", "三角", "双曲", "不等式", "绝对值", "有界性", "奇偶", "周期"]
        for kw in func_keywords:
            if kw in target:
                return "01-函数及其性质"
                
        return "02-极限与未定式"
        
    elif chapter_clean == "02-一元函数微分学":
        app_keywords = ["中值定理", "单调", "极值", "最值", "凹凸", "拐点", "渐近线", "曲率", "不等式证明", "零点"]
        for kw in app_keywords:
            if kw in target:
                return "02-中值定理与导数应用"
                
        return "01-导数与微分"
        
    return ""

def parse_callout(lines, start_idx):
    """
    Parses a callout block starting at start_idx.
    Returns (callout_type, title, content_lines, end_idx)
    """
    first_line = lines[start_idx]
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
            if re.match(r'^>\s*\[![^\]]+\]', line):
                break
            content_line = re.sub(r'^>\s?', '', line)
            content_lines.append(content_line)
            idx += 1
        else:
            break
            
    return callout_type, title, content_lines, idx

def parse_markdown(content):
    """
    Parses an existing Obsidian note.
    Returns:
        yaml_lines: list of strings
        title: string
        sections: dict of callout_type -> list of content lines (without leading '>')
    """
    lines = content.splitlines()
    yaml_lines = []
    title = ""
    sections = {}
    
    idx = 0
    # Parse YAML Frontmatter
    if idx < len(lines) and lines[idx].strip() == "---":
        yaml_lines.append(lines[idx])
        idx += 1
        while idx < len(lines):
            yaml_lines.append(lines[idx])
            if lines[idx].strip() == "---":
                idx += 1
                break
            idx += 1
            
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
        idx += 1
            
    return yaml_lines, title, sections

def merge_info_lines(existing_lines, new_text):
    if not new_text:
        return existing_lines
    
    new_lines = new_text.splitlines()
    merged = list(existing_lines)
    
    # Strip empty trailing lines
    while merged and merged[-1].strip() == "":
        merged.pop()
        
    existing_stripped = {l.strip() for l in merged if l.strip()}
    
    for line in new_lines:
        trimmed = line.strip()
        if not trimmed:
            continue
        if trimmed in existing_stripped:
            continue
            
        if trimmed.startswith("$$") and merged and merged[-1].strip() != "":
            merged.append("")
        merged.append(line)
        
    return merged

def parse_todo_sections(todo_lines):
    """
    Parses the todo (core question types) callout lines into dict of:
    question_type_name (normalized) -> list of lines of that question type section.
    Also returns a list of question type titles in order.
    """
    sections = {}
    order = []
    current_title = None
    current_lines = []
    
    for line in todo_lines:
        # Match headings like ### 题型一：xxx or #### 题型二...
        match = re.match(r'^#{2,4}\s+(题型[^：\s:]+[:：]?\s*.*)$', line.strip())
        if match:
            if current_title:
                sections[current_title] = current_lines
            current_title = match.group(1).strip()
            # Normalize title for dict key (e.g. ignore full/half width colon differences)
            norm_title = re.sub(r'[:：\s]+', '', current_title)
            order.append((norm_title, current_title))
            current_lines = []
        else:
            if current_title:
                current_lines.append(line)
            else:
                # Content before any header
                if line.strip():
                    if "" not in sections:
                        sections[""] = []
                    sections[""].append(line)
                    
    if current_title:
        sections[current_title] = current_lines
        
    return sections, order

def merge_todo_sections(existing_lines, new_types):
    """
    Merges new question types into existing todo lines.
    new_types: list of dicts {"type_name": "...", "method": "...", "examples": "..."}
    """
    sections, order = parse_todo_sections(existing_lines)
    
    for qt in new_types:
        name = qt.get("type_name", "").strip()
        if not name:
            continue
            
        norm_name = re.sub(r'[:：\s]+', '', name)
        
        # Build new section lines
        new_sec_lines = []
        method = qt.get("method", "").strip()
        if method:
            method_lines = method.splitlines()
            new_sec_lines.append(f"- **核心方法**：{method_lines[0]}")
            for ml in method_lines[1:]:
                new_sec_lines.append(f"  {ml}")
        examples = qt.get("examples", "").strip()
        if examples:
            examples_lines = examples.splitlines()
            new_sec_lines.append(f"- **典型例示**：{examples_lines[0]}")
            for el in examples_lines[1:]:
                new_sec_lines.append(f"  {el}")
        source = qt.get("source", "").strip()
        if source:
            source_lines = source.splitlines()
            new_sec_lines.append(f"- **书目出处**：{source_lines[0]}")
            for sl in source_lines[1:]:
                new_sec_lines.append(f"  {sl}")
            
        # Find if it already exists
        matched_key = None
        for n_key, orig_key in order:
            if norm_name in n_key or n_key in norm_name:
                matched_key = orig_key
                break
                
        if matched_key:
            # Merge/replace lines smart-matching by prefix
            prefixes = ['- **核心方法**：', '- **典型例示**：', '- **书目出处**：']
            for l in new_sec_lines:
                matched_prefix = None
                for pref in prefixes:
                    if l.startswith(pref):
                        matched_prefix = pref
                        break
                
                if matched_prefix:
                    replaced = False
                    for idx, eline in enumerate(sections[matched_key]):
                        if eline.startswith(matched_prefix):
                            sections[matched_key][idx] = l
                            replaced = True
                            break
                    if not replaced:
                        sections[matched_key].append(l)
                else:
                    if l.strip() not in {line.strip() for line in sections[matched_key]}:
                        sections[matched_key].append(l)
        else:
            # Add new section
            sections[name] = new_sec_lines
            order.append((norm_name, name))
            
    # Reconstruct lines
    reconstructed = []
    if "" in sections:
        reconstructed.extend(sections[""])
        
    for _, orig_key in order:
        reconstructed.append(f"### {orig_key}")
        reconstructed.extend(sections[orig_key])
        reconstructed.append("")
        
    # Trim trailing empty lines
    while reconstructed and reconstructed[-1].strip() == "":
        reconstructed.pop()
        
    return reconstructed

def build_review_note(data):
    vault_root = data.get("vault_root", "D:/ob/考研数学").replace("\\", "/")
    raw_subject = data.get("subject", "01-高等数学").strip()
    if "高等数学" in raw_subject:
        subject = "01-高等数学"
    elif "线性代数" in raw_subject:
        subject = "02-线性代数"
    else:
        subject = raw_subject
    chapter = data.get("chapter", "01-函数极限与连续").strip()
    keypoint = data.get("keypoint", "周期性").strip()
    title = data.get("title", "周期性").strip()
    
    sub_ch = get_subchapter_folder(subject, chapter, keypoint, title)
    
    # Target directory structure
    if sub_ch:
        dir_path = os.path.join(vault_root, "总结复盘", sanitize_filename(subject), sanitize_filename(chapter), sub_ch)
    else:
        dir_path = os.path.join(vault_root, "总结复盘", sanitize_filename(subject), sanitize_filename(chapter))
        
    dir_path = dir_path.replace("\\", "/")
    os.makedirs(dir_path, exist_ok=True)
    
    filename = f"{sanitize_filename(title)}.md"
    file_path = os.path.join(dir_path, filename).replace("\\", "/")
    
    # Read existing file if it exists
    existing_content = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
            
    yaml_lines, existing_title, sections = parse_markdown(existing_content)
    
    # 1. Merge YAML Frontmatter
    tag_path = f"总结复盘/{subject}/{chapter}"
    if sub_ch:
        tag_path += f"/{sub_ch}"
    tag_path += f"/{title}"
    tag_path = tag_path.replace("\\", "/")
    
    yaml_block = f"---\ntype: 总结复盘\ntags:\n  - {tag_path}\n---"
    
    # 2. Merge Info Section (涉及知识点)
    info_lines = sections.get("info", [])
    new_def = data.get("definition", "")
    info_lines = merge_info_lines(info_lines, new_def)
    
    # 3. Merge Todo Section (核心题型与解法)
    todo_lines = sections.get("todo", [])
    new_types = data.get("question_types", [])
    todo_lines = merge_todo_sections(todo_lines, new_types)
    
    # Format note content
    md_content = f"{yaml_block}\n\n# {title} 总结复盘\n\n"
    
    md_content += "> [!info] 涉及知识点\n"
    for l in info_lines:
        for sub_l in l.splitlines():
            md_content += f"> {sub_l}\n"
    md_content += "\n"
    
    md_content += "> [!todo] 核心题型与解法\n"
    for l in todo_lines:
        for sub_l in l.splitlines():
            md_content += f"> {sub_l}\n"
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")
        
    print(json.dumps({
        "status": "success",
        "file_path": file_path,
        "is_merged": len(existing_content) > 0
    }))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Obsidian Concept Review and Question Types")
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
        
    build_review_note(data)
