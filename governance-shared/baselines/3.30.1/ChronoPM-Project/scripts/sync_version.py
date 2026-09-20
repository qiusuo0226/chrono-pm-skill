#!/usr/bin/env python3
"""
版本同步脚本：读取 _version.py 的唯一版本源，同步到所有派生触点。
用法（在 ChronoPM-Project/ 包根或仓库根均可）：
    python ChronoPM-Project/scripts/sync_version.py
前提：先手动修改 scripts/_version.py 中的 SKILL_VERSION，再运行本脚本。

CR-G：包内触点在 ChronoPM-Project/；README×2 在仓库根；Portfolio 版本锁步。
"""
import json
import os
import re
from datetime import date

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(PKG_ROOT)
if os.path.isfile(os.path.join(PKG_ROOT, "README.md")):
    # 旧布局兜底（仓库根即包根）
    REPO_ROOT = PKG_ROOT
PORTFOLIO_ROOT = os.path.join(REPO_ROOT, "ChronoPM-Portfolio")

# 1. 从唯一源头读取版本
version_mod_path = os.path.join(PKG_ROOT, "scripts", "_version.py")
with open(version_mod_path, "r", encoding="utf-8") as f:
    content = f.read()
m = re.search(r"SKILL_VERSION\s*=\s*['\"]([\d.]+)['\"]", content)
if not m:
    raise RuntimeError(f"Cannot find SKILL_VERSION in {version_mod_path}")
version = m.group(1)
today = date.today().isoformat()
synced = []


def sync_version_file(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(version + "\n")


def sync_skill_md(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    updated = re.sub(r"^(version:\s*)[\d.]+", rf"\g<1>{version}", text, count=1, flags=re.MULTILINE)
    updated = re.sub(r"^(updated_at:\s*)[\d-]+", rf"\g<1>{today}", updated, count=1, flags=re.MULTILINE)
    updated = re.sub(r"(Skill 包版本号（当前 )[\d.]+", rf"\g<1>{version}", updated, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)


def sync_skill_json(path):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        skill_json = json.load(f)
    skill_json["version"] = version
    if "versionHistory" not in skill_json:
        skill_json["versionHistory"] = []
    entry = {"version": version, "date": today}
    if any(item.get("version") == version for item in skill_json["versionHistory"]):
        for item in skill_json["versionHistory"]:
            if item.get("version") == version:
                item.update(entry)
    else:
        skill_json["versionHistory"].insert(0, entry)
    if isinstance(skill_json.get("blueprint"), dict):
        skill_json["blueprint"]["lastVersion"] = version
        skill_json["blueprint"]["lastUpdated"] = today
    with open(path, "w", encoding="utf-8") as f:
        json.dump(skill_json, f, ensure_ascii=False, indent=2)
        f.write("\n")


# Project 包内
sync_version_file(os.path.join(PKG_ROOT, "VERSION"))
synced.append("ChronoPM-Project/VERSION")
sync_skill_md(os.path.join(PKG_ROOT, "SKILL.md"))
synced.append("ChronoPM-Project/SKILL.md")
sync_skill_json(os.path.join(PKG_ROOT, "skill.json"))
synced.append("ChronoPM-Project/skill.json")

blueprint_path = os.path.join(PKG_ROOT, "SKILL_BLUEPRINT.md")
if os.path.exists(blueprint_path):
    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint = f.read()
    updated = re.sub(r"(\|\s*当前版本\s*\|\s*)[\d.]+", rf"\g<1>{version}", blueprint, count=1)
    if updated != blueprint:
        with open(blueprint_path, "w", encoding="utf-8") as f:
            f.write(updated)
        synced.append("SKILL_BLUEPRINT.md §1")

# 仓根 README
for name, pat_title, pat_table in (
    ("README.md", r"^(# ChronoPM v)[\d.]+", r"(\|\s*Skill 版本\s*\|\s*)[\d.]+"),
    ("README.en.md", r"^(# ChronoPM v)[\d.]+", r"(\|\s*Skill version\s*\|\s*)[\d.]+"),
):
    path = os.path.join(REPO_ROOT, name)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    updated = re.sub(pat_title, rf"\g<1>{version}", text, count=1, flags=re.MULTILINE)
    updated = re.sub(pat_table, rf"\g<1>{version}", updated, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)
    synced.append(name)

# Portfolio 锁步
if os.path.isdir(PORTFOLIO_ROOT):
    pv = os.path.join(PORTFOLIO_ROOT, "VERSION")
    if os.path.exists(pv):
        sync_version_file(pv)
        synced.append("ChronoPM-Portfolio/VERSION")
    ps = os.path.join(PORTFOLIO_ROOT, "SKILL.md")
    if os.path.exists(ps):
        sync_skill_md(ps)
        synced.append("ChronoPM-Portfolio/SKILL.md")
    pj = os.path.join(PORTFOLIO_ROOT, "skill.json")
    if os.path.exists(pj):
        sync_skill_json(pj)
        synced.append("ChronoPM-Portfolio/skill.json")

print(f"Synced version {version} to: {', '.join(synced)}")
