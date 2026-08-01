---
type: 典型例子
tags:
  - 典型例子/线性代数/00-线性代数综合/{keypoint}/RESTORED_FILE
---

import os
import sys
import json
import re
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

DEFAULT_VAULT = "D:/ob/考研数学"

def get_standard_chapter(raw_text, subject="高等数学"):
    if subject == "线性代数":
        if any(k in raw_text for k \in ["行列式"]): return "01-行列式"
        if any(k in raw_text for k \in ["矩阵"]): return "02-矩阵"
        if any(k in raw_text for k \in ["向量"]): return "03-向量"
        if any(k in raw_text for k \in ["方程组"]): return "04-线性方程组"
        if any(k in raw_text for k \in ["特征值", "特征向量", "相似"]): return "05-特征值与特征向量"
        if any(k in raw_text for k \in ["二次型"]): return "06-二次型"
        return "00-线性代数综合"
    
    # 高等数学 Chapters keyword mapping
    scores = {
        "01-函数极限与连续": 0,
        "02-一元函数微分学": 0,
        "03-一元函数积分学": 0,
        "04-多元函数微分学": 0,
        "05-二重积分": 0,
        "06-常微分方程": 0,
    }
    
    keywords = {
        "01-函数极限与连续": ["极限", "连续", "无穷小", "无穷大", "间断点", "渐近线", "数列", "反函数"],
        "02-一元函数微分学": ["一元函数微分", "导数", "可导", "极值", "拐点", "泰勒", "洛必达", "中值定理", "罗尔", "拉格朗日", "柯西", "切线", "法线", "单调性"],
        "03-一元函数积分学": ["一元函数积分", "定积分", "不定积分", "变限积分", "反常积分", "旋转体", "面积", "积分中值定理", "积分不等式", "积分等式", "分部积分", "换元积分"],
        "04-多元函数微分学": ["多元", "偏导", "全微分", "方向导数", "梯度", "条件极值", "隐函数求导", "混合偏导"],
        "05-二重积分": ["二重积分", "重积分", "极坐标", "雅可比", "交换次序", "对称性", "形心", "保号性"],
        "06-常微分方程": ["常微分方程", "微分方程", "算子法", "齐次方程", "伯努利", "特解", "通解", "一阶线性", "二阶常系数"]
    }
    
    for ch, kws in keywords.items():
        for kw in kws:
            if kw in raw_text:
                scores[ch] += 1
                
    # Specific strong weights
    if "二重积分" in raw_text: scores["05-二重积分"] += 10
    if "微分方程" in raw_text: scores["06-常微分方程"] += 10
    if "多元" in raw_text or "偏导" in raw_text: scores["04-多元函数微分学"] += 10
    if "极限" in raw_text: scores["01-函数极限与连续"] += 10
        
    max_ch = max(scores, key=scores.get)
    if scores[max_ch] == 0:
        return "00-高等数学综合"
    return max_ch

def clean_latex_blanks(text):
    if not text:
        return text
    text = re.sub(r'\\underline\{\\hspace\{[^}]+\}\}', '______', text)
    text = re.sub(r'\\underline\{[^}]*\}', '______', text)
    text = re.sub(r'(?<!\\)\b\int_', r'\int_', text)
    text = re.sub(r'(?<!\\)\bint\^', r'\int^', text)
    text = re.sub(r'(?<!\\)\bint\{', r'\int{', text)
    text = re.sub(r'f\(t\),dt', r'f(t) dt', text)
    text = re.sub(r',dt\b', r' dt', text)
    return text

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name or "").strip()

def build_note(data):
    vault_root = data.get("vault_root", DEFAULT_VAULT)
    note_type = data.get("type", "错题本")
    if note_type == "错题": note_type = "错题本"
    
    raw_subj = data.get("subject", "高等数学")
    subject = "线性代数" if "线性代数" in raw_subj else "高等数学"
    
    full_text_context = (data.get("chapter", "") + " " + data.get("keypoint", "") + " " + 
                         data.get("title", "") + " " + data.get("input_text", "") + " " +
                         data.get("key_method", "") + " " + data.get("analysis", ""))
                         
    chapter = get_standard_chapter(full_text_context, subject)
    
    keypoint = sanitize_filename(data.get("keypoint", "考点"))
    title = sanitize_filename(data.get("title", "笔记"))
    
    img_path = data.get("image_path", "")
    img_url = "file:///" + img_path.replace("\\", "/") if img_path else ""
    img_embed = f"" if img_url else ""

    if note_type == "错题本":
        top_dir = "错题本"
        q_text = clean_latex_blanks(data.get("input_text", ""))
        key_method = data.get("key_method", "")
        pitfalls = data.get("pitfalls", "")
        analysis = data.get("analysis", "")
        answer = data.get("answer", "")

        md = f"""---
type: 错题本
tags:
  - 典型例子/线性代数/00-线性代数综合/{keypoint}

# {title}

> [!question] 题目
> {q_text}
> 
> {img_embed}

> [!tip] ⚡ 秒杀法宝
> {key_method}

> [!failure] ❌ 真实错因剖析
> {pitfalls}

> [!success] 解析与答案
> {analysis}
"""
        if answer:
            md += f"\n> **【最终答案】**：{answer}\n"
            
    elif note_type == "典型例子":
        top_dir = "典型例子"
        q_text = clean_latex_blanks(data.get("input_text", ""))
        key_method = data.get("key_method", "")
        analysis = data.get("analysis", "")

        md = f"""---
type: 典型例子
tags:
  - 典型例子/{subject}/{chapter}/{keypoint}
---

# {title}

> [!example] 📖 经典范例原题
> {q_text}
> 
> {img_embed}

> [!tip] ⚡ 核心解题思路与范例总结
> {key_method}

> [!success] 详细推导步骤
> {analysis}
"""
    else:
        top_dir = "知识点"
        definition = data.get("definition", "")
        formulas = data.get("formulas", "")
        conclusions = data.get("conclusions", "")

        md = f"""---
type: 知识点
tags:
  - 知识点/{subject}/{chapter}/{title}
---

# {title}

> [!info] 概念定义
> {definition}
> 
> {img_embed}

> [!todo] 核心公式与定理
> {formulas}

> [!tip] 考点结论与秒杀小技巧
> {conclusions}
"""

    target_path = os.path.join(vault_root, top_dir, subject, chapter, keypoint, f"{title}.md")

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(md.strip() + "\n")
    print(f"Successfully written {note_type} note to clean path: {target_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()

    if args.stdin or not sys.stdin.isatty():
        data = json.loads(sys.stdin.read())
        build_note(data)
