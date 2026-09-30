#!/usr/bin/env python3
"""只读：D-REQ-WP-01/02 + D-SOURCE-01。退出 0/1/2。"""
import argparse
import re
import sys
from pathlib import Path


def _ai(root: Path) -> Path:
    ai = root / "ai"
    return ai if ai.exists() else root


def _front(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def wp_reqs(text: str):
    ids = []
    in_s2 = False
    for line in text.splitlines():
        if line.startswith("## 2.") and "关联需求" in line:
            in_s2 = True
            continue
        if in_s2 and line.startswith("## "):
            break
        if in_s2 and line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0].startswith("REQ"):
                ids.append(cells[0].split()[0])
    return ids


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    args = p.parse_args()
    ai = _ai(Path(args.root))
    diffs = []
    reg = ai / "requirements" / "requirement-register.md"
    req_wps = {}
    if reg.exists():
        for line in reg.read_text(encoding="utf-8").splitlines():
            if line.startswith("|") and "REQ" in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0].startswith("REQ"):
                    wcol = cells[4] if len(cells) > 4 else ""
                    req_wps[cells[0]] = [x.strip() for x in re.split(r"[,，]", wcol) if x.strip().startswith("WP")]
    wpdir = ai / "wps"
    wp_files = set()
    wp_to_req = {}
    if wpdir.exists():
        for f in wpdir.glob("WP-*.md"):
            wp_files.add(f.stem)
            t = f.read_text(encoding="utf-8")
            fm = _front(t)
            wpid = fm.get("wp_id") or f.stem
            wp_to_req[wpid] = wp_reqs(t)
    for rid, wlist in req_wps.items():
        for w in wlist:
            if w not in wp_files and not any(x.startswith(w) for x in wp_files):
                diffs.append(f"D-REQ-WP-01 {rid} 工作包 {w} 无文件")
    for wpid, rlist in wp_to_req.items():
        for r in rlist:
            if r not in req_wps:
                diffs.append(f"D-REQ-WP-02 {wpid} 需求 {r} 不在登记册")
    src = ai / "requirements" / "sources"
    sidx = src / "_index.md" if src.exists() else None
    if src and src.exists():
        metas = {d.name for d in src.iterdir() if d.is_dir() and (d / "meta.md").exists()}
        idx_ids = set()
        if sidx and sidx.exists():
            for line in sidx.read_text(encoding="utf-8").splitlines():
                if line.startswith("|"):
                    cells = [c.strip() for c in line.strip("|").split("|")]
                    if cells and cells[0] not in ("编号", "SRC", ""):
                        idx_ids.add(cells[0])
        for m in metas - idx_ids:
            diffs.append(f"D-SOURCE-01 {m} 有 meta 无索引行")
        for i in idx_ids - metas:
            if i not in ("编号", "ID"):
                diffs.append(f"D-SOURCE-01 索引有 {i} 无 meta.md")
    for d in diffs:
        print("DIFF", d)
    if diffs:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
