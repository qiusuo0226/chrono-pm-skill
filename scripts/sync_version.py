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

# 4. 同步 skill.json（含 blueprint.lastVersion，D-19 扩展）
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
        # 插入头部，保持“最新在前”的顺序约定
        skill_json['versionHistory'].insert(0, entry)
    # blueprint.lastVersion / lastUpdated（D-19 扩展触点）
    if isinstance(skill_json.get('blueprint'), dict):
        skill_json['blueprint']['lastVersion'] = version
        skill_json['blueprint']['lastUpdated'] = today
    with open(skill_json_path, 'w', encoding='utf-8') as f:
        json.dump(skill_json, f, ensure_ascii=False, indent=2)
        f.write('\n')
    synced.append('skill.json')

# 5. 同步 README.md（标题 + 版本表，D-19 扩展）
readme_path = os.path.join(ROOT, 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    updated = re.sub(r'^(# ChronoPM v)[\d.]+', rf'\g<1>{version}', readme, count=1, flags=re.MULTILINE)
    updated = re.sub(r'(\|\s*Skill 版本\s*\|\s*)[\d.]+', rf'\g<1>{version}', updated, count=1)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated)
    synced.append('README.md（标题+版本表）')

# 6. 同步 README.en.md（标题 + 版本表，D-19 扩展）
readme_en_path = os.path.join(ROOT, 'README.en.md')
if os.path.exists(readme_en_path):
    with open(readme_en_path, 'r', encoding='utf-8') as f:
        readme_en = f.read()
    updated = re.sub(r'^(# ChronoPM v)[\d.]+', rf'\g<1>{version}', readme_en, count=1, flags=re.MULTILINE)
    updated = re.sub(r'(\|\s*Skill version\s*\|\s*)[\d.]+', rf'\g<1>{version}', updated, count=1)
    with open(readme_en_path, 'w', encoding='utf-8') as f:
        f.write(updated)
    synced.append('README.en.md（标题+版本表）')

# 7. 同步 SKILL.md 版本控制表（“当前 X.X.X”，D-19 扩展；重读避免覆盖步骤 3 的 frontmatter 更新）
with open(skill_md_path, 'r', encoding='utf-8') as f:
    skill_md_now = f.read()
updated = re.sub(r'(Skill 包版本号（当前 )[\d.]+', rf'\g<1>{version}', skill_md_now, count=1)
if updated != skill_md_now:
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(updated)
    synced.append('SKILL.md 版本控制表')

# 8. 同步 SKILL_BLUEPRINT.md §1 当前版本（D-19 扩展）
blueprint_path = os.path.join(ROOT, 'SKILL_BLUEPRINT.md')
if os.path.exists(blueprint_path):
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        blueprint = f.read()
    updated = re.sub(r'(\|\s*当前版本\s*\|\s*)[\d.]+', rf'\g<1>{version}', blueprint, count=1)
    if updated != blueprint:
        with open(blueprint_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        synced.append('SKILL_BLUEPRINT.md §1')

print(f"Synced version {version} to: {', '.join(synced)}")
