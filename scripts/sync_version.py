#!/usr/bin/env python3
"""
版本同步脚本：读取 _version.py 的唯一版本源，同步到所有派生触点。
用法：python scripts/sync_version.py
前提：先手动修改 _version.py 中的 SKILL_VERSION，再运行本脚本。
"""
import re
import os
import json
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. 从唯一源头读取版本
version_mod_path = os.path.join(ROOT, 'scripts', '_version.py')
with open(version_mod_path, 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r"SKILL_VERSION\s*=\s*['\"]([\d.]+)['\"]", content)
if not m:
    raise RuntimeError(f"Cannot find SKILL_VERSION in {version_mod_path}")
version = m.group(1)

synced = []

# 2. 同步 VERSION 文件
version_file = os.path.join(ROOT, 'VERSION')
with open(version_file, 'w', encoding='utf-8') as f:
    f.write(version + '\n')
synced.append('VERSION')

# 3. 同步 SKILL.md frontmatter
skill_md_path = os.path.join(ROOT, 'SKILL.md')
with open(skill_md_path, 'r', encoding='utf-8') as f:
    skill_md = f.read()
today = date.today().isoformat()
updated = re.sub(r'^(version:\s*)[\d.]+', rf'\g<1>{version}', skill_md, count=1, flags=re.MULTILINE)
updated = re.sub(r'^(updated_at:\s*)[\d-]+', rf'\g<1>{today}', updated, count=1, flags=re.MULTILINE)
with open(skill_md_path, 'w', encoding='utf-8') as f:
    f.write(updated)
synced.append('SKILL.md frontmatter')

# 4. 同步 skill.json
skill_json_path = os.path.join(ROOT, 'skill.json')
if os.path.exists(skill_json_path):
    with open(skill_json_path, 'r', encoding='utf-8') as f:
        skill_json = json.load(f)
    skill_json['version'] = version
    # 维护 versionHistory（最新在前）
    if 'versionHistory' not in skill_json:
        skill_json['versionHistory'] = []
    entry = {
        'version': version,
        'date': today
    }
    # 若该版本已存在（如手动维护过 summary），则仅更新其字段，不重复追加
    if any(item.get('version') == version for item in skill_json['versionHistory']):
        for item in skill_json['versionHistory']:
            if item.get('version') == version:
                item.update(entry)
    else:
        # 插入头部，保持"最新在前"的顺序约定
        skill_json['versionHistory'].insert(0, entry)
    with open(skill_json_path, 'w', encoding='utf-8') as f:
        json.dump(skill_json, f, ensure_ascii=False, indent=2)
        f.write('\n')
    synced.append('skill.json')

print(f"Synced version {version} to: {', '.join(synced)}")
