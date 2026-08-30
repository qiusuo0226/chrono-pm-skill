#!/usr/bin/env python3
"""只读：D-CONTRACT-01/02。退出 0/1/2。"""
import argparse
import re
import sys
from pathlib import Path


def _ai(root: Path) -> Path:
    ai = root / "ai"
    return ai if ai.exists() else root


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    args = p.parse_args()
    ai = _ai(Path(args.root))
    diffs = []
    creg = ai / "requirements" / "contract-register.md"
    cons = {}
    if creg.exists():
        for line in creg.read_text(encoding="utf-8").splitlines():
            if line.startswith("|") and "CON-" in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0].startswith("CON-"):
                    cons[cells[0]] = cells
    cited = set()
    rreg = ai / "requirements" / "requirement-register.md"
    blob = ""
    if rreg.exists():
        blob += rreg.read_text(encoding="utf-8")
    can = ai / "requirements" / "canonical"
    if can.exists():
        for f in can.rglob("*.md"):
            blob += "\n" + f.read_text(encoding="utf-8")
    for m in re.finditer(r"CON-[A-Za-z0-9\-]+", blob):
        cited.add(m.group(0))
    for cid in cited:
        if cid not in cons:
            diffs.append(f"D-CONTRACT-01 引用 {cid} 不在合同登记册")
    for cid, cells in cons.items():
        ptr = ""
        for c in cells:
            if "sources/" in c:
                ptr = c
                break
        if ptr and ptr not in ("-", "—"):
            # pointer like requirements/sources/CON-xxx/
            rel = ptr.split("sources/")[-1].strip("/").split()[0]
            meta = ai / "requirements" / "sources" / rel / "meta.md"
            if not meta.exists():
                diffs.append(f"D-CONTRACT-02 {cid} 拆解指针无 meta.md")
    for d in diffs:
        print("DIFF", d)
    if diffs:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
