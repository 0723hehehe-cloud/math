import argparse
import os
import re
import sys

from process_qa import build_typical_example


def extract_example_block(lines):
    """Return (start, end, content) for the first example callout."""
    for start, line in enumerate(lines):
        if re.match(r'^>\s*\[!example\]', line):
            end = start + 1
            while end < len(lines) and lines[end].startswith('>'):
                end += 1
            content = []
            for block_line in lines[start + 1:end]:
                content.append(re.sub(r'^>\s?', '', block_line))
            return start, end, content
    return None


def migrate(vault_root):
    migrated = 0
    for root, _, files in os.walk(vault_root):
        if os.path.normpath(root) == os.path.normpath(vault_root):
            continue
        for filename in files:
            if not filename.endswith('.md') or filename == '典型例子.md':
                continue
            path = os.path.join(root, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.splitlines()
            block = extract_example_block(lines)
            if not block:
                continue

            start, end, example_lines = block
            relative = os.path.relpath(path, os.path.join(vault_root, '知识点'))
            parts = relative.split(os.sep)
            if len(parts) < 2:
                continue
            subject = parts[0]
            chapter = parts[1] if len(parts) > 1 else '未分类'
            keypoint = os.path.splitext(filename)[0]
            title = f'{keypoint}中的典型例子'
            build_typical_example({
                'vault_root': vault_root,
                'type': '典型例子',
                'subject': subject,
                'chapter': chapter,
                'keypoint': keypoint,
                'title': title,
                'examples': '\n'.join(example_lines),
            })

            new_lines = lines[:start] + lines[end:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines).rstrip() + '\n')
            migrated += 1
            print(f'Migrated: {path}')
    print(f'Migrated example blocks: {migrated}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move knowledge-note example callouts into 典型例子.md')
    parser.add_argument('vault_root')
    args = parser.parse_args()
    migrate(args.vault_root)
