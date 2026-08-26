#!/usr/bin/env python3
"""只读：C1–C8 计划投影 + D-TODO-WP + D-PLAN-REF + D-EFFECT + 可选 C9 §4。退出 0/1/2。"""
import argparse
import re
import sys
from pathlib import Path

STAGE13 = {
    "需求登记", "需求调研", "需求规划", "需求评审", "需求确认",
    "方案设计", "用例设计", "开发", "预演", "测试", "内部验收", "试运行", "上线",
}


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
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _section(text: str, title: str) -> str:
    pat = rf"^##\s*{re.escape(title)}\s*$"
    parts = re.split(r"^##\s+", text, flags=re.M)
    heads = re.findall(r"^##\s+(.+)$", text, re.M)
    for i, h in enumerate(heads):
        if h.strip() == title or h.strip().startswith(title):
            body = parts[i + 1] if i + 1 < len(parts) else ""
            return body
    return ""


def _table_rows(block: str):
    rows = []
    for line in block.splitlines():
        if line.startswith("|") and "---" not in line and not line.startswith("| WP 编号"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and not cells[0].startswith("WP 编号"):
                rows.append(cells)
    return rows


def _wp_sec1_dates(text: str):
    start = end = ""
    for line in text.splitlines():
        if "| 开始时间 |" in line:
            start = line.split("|")[2].strip()
        if "| 结束时间 |" in line:
            end = line.split("|")[2].strip()
    return start, end


def _wp_sec8(text: str):
    body = ""
    for m in re.finditer(r"^## 8\..+$", text, re.M):
        start = m.end()
        nxt = re.search(r"^##\s+", text[start:], re.M)
        body = text[start: start + nxt.start()] if nxt else text[start:]
        break
    rows = []
    for line in body.splitlines():
        if line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0] not in ("阶段", "字段"):
                rows.append(cells)
    return rows


def _chain_tail(text: str) -> str:
    body = ""
    m = re.search(r"^## 7\..+$", text, re.M)
    if m:
        start = m.end()
        nxt = re.search(r"^##\s+", text[start:], re.M)
        body = text[start: start + nxt.start()] if nxt else text[start:]
    lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.startswith("|")]
    return lines[-1] if lines else ""


def _split_refs(s: str):
    if not s or s in ("—", "-", ""):
        return []
    return [p.strip() for p in s.split(" / ") if p.strip()]


def _plan_sec4_stages(text):
    """PLAN §4 → {wp_id: set(stage names)}。小节标题 `### WP-xxx`，阶段行 `- 名 →`。"""
    m = re.search(r"^##\s*4[\.．、]?\s*", text, re.M)
    if not m:
        return {}
    start = m.end()
    nxt = re.search(r"^##\s+", text[start:], re.M)
    body = text[start: start + nxt.start()] if nxt else text[start:]
    out = {}
    current = None
    for line in body.splitlines():
        hm = re.match(r"^###\s+(WP-\S+)", line)
        if hm:
            current = hm.group(1)
            out.setdefault(current, set())
            continue
        sm = re.match(r"^-\s+(.+?)\s*→", line)
        if sm and current:
            out[current].add(sm.group(1).strip())
    return out


def _check_plan_section4(plans, wps):
    """比较对象=该 WP §8 实际行阶段名。STAGE13 只作缺标准名 HINT，不当失败条件。"""
    bucket_msgs = []
    for pf, pt, pfm in plans:
        sec4 = _plan_sec4_stages(pt)
        for cells in _table_rows(pt):
            if not cells:
                continue
            wpid = cells[0]
            if not str(wpid).startswith("WP-"):
                continue
            if wpid not in wps:
                continue
            _, wt, fm = wps[wpid]
            if (fm.get("effect") or "正常") == "废弃":
                continue
            stages8 = {r[0] for r in _wp_sec8(wt) if r}
            got = sec4.get(wpid)
            if got is None:
                bucket_msgs.append(f"C9 {wpid} @{pf.name} §4 无独立小节")
            elif got != stages8:
                bucket_msgs.append(
                    f"C9 {wpid} @{pf.name} §4阶段 {sorted(got)!r} ≠ §8 {sorted(stages8)!r}"
                )
            missing_std = STAGE13 - stages8
            if missing_std:
                print(f"HINT {wpid} §8 缺标准阶段名 {sorted(missing_std)}（可增删，非失败）")
    return bucket_msgs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument(
        "--check-plan-section4",
        action="store_true",
        help="写入/生成 PLAN 落盘前：§4 不全则 exit 1。默认巡检不加本开关，§4 问题 UNJUDGED exit 2。",
    )
    args = p.parse_args()
    ai = _ai(Path(args.root))
    diffs = []
    unjudged = []
    wps = {}
    wpdir = ai / "wps"
    if not wpdir.exists():
        print("无可校验 wps/，退出 0")
        return 0
    for f in wpdir.glob("WP-*.md"):
        t = f.read_text(encoding="utf-8")
        fm = _front(t)
        wps[fm.get("wp_id") or f.stem] = (f, t, fm)
    idx_text = (wpdir / "_index.md").read_text(encoding="utf-8") if (wpdir / "_index.md").exists() else ""
    idx_rows = {}
    for cells in _table_rows(idx_text):
        if cells:
            idx_rows[cells[0]] = cells
    plans = []
    pdir = ai / "plans"
    if pdir.exists():
        for f in pdir.glob("PLAN-*.md"):
            t = f.read_text(encoding="utf-8")
            fm = _front(t)
            if fm.get("status") == "废弃":
                continue
            plans.append((f, t, fm))
    for wpid, (fp, t, fm) in wps.items():
        effect = fm.get("effect") or "正常"
        if effect == "废弃":
            for pf, pt, _ in plans:
                if wpid in pt:
                    diffs.append(f"D-EFFECT-01 {wpid} 仍出现在 {pf.name}")
            ic = idx_rows.get(wpid)
            if ic and len(ic) > 2 and ic[2] != "废弃":
                diffs.append(f"D-EFFECT-01 {wpid} index 状态不是废弃")
            continue
        for pf, pt, pfm in plans:
            # C1
            if wpid in pt and not fp.exists():
                diffs.append(f"C1 {wpid} 计划引用但文件不存在")
        tail = _chain_tail(t)
        if tail == "已完成":
            rows8 = _wp_sec8(t)
            for r in reversed(rows8):
                if r and ("✅" in r[1] or "🔄" in r[1]):
                    tail = r[0]
                    break
        s1, s2 = _wp_sec1_dates(t)
        rows8 = _wp_sec8(t)
        cur_people = "⚠️待安排人"
        for r in rows8:
            if len(r) > 2 and "🔄" in r[1]:
                cur_people = r[2]
                break
        else:
            for r in reversed(rows8):
                if len(r) > 2 and "✅" in r[1]:
                    cur_people = r[2]
                    break
        keys = []
        for r in rows8:
            if len(r) > 4 and r[4] in ("是", "Y", "yes"):
                keys.append(r[0])
        for pf, pt, pfm in plans:
            for cells in _table_rows(pt):
                if cells and cells[0] == wpid:
                    if len(cells) > 2 and cells[2] != tail and tail:
                        diffs.append(f"C2 {wpid} @{pf.name} 状态 {cells[2]!r} ≠ 链尾 {tail!r}")
                    if len(cells) > 3 and cells[3] and cur_people and cells[3] != cur_people:
                        diffs.append(f"C3 {wpid} @{pf.name} 执行人 {cells[3]!r} ≠ {cur_people!r}")
                    if len(cells) > 4 and s1 and s2:
                        want = f"{s1}~{s2}"
                        if cells[4] != want:
                            diffs.append(f"C4 {wpid} @{pf.name} 排期 {cells[4]!r} ≠ {want!r}")
                    if len(cells) > 5 and keys:
                        got = set(re.split(r"[、,/]", cells[5]))
                        if set(keys) != {g for g in got if g}:
                            diffs.append(f"C5 {wpid} @{pf.name} 关键阶段不一致")
        # D-PLAN-REF
        yaml_refs = _split_refs(fm.get("plan_ref", ""))
        citing = []
        for pf, pt, pfm in plans:
            pid = pfm.get("plan_id") or pf.stem.split("-")[0] if False else pfm.get("plan_id") or pf.name.split(".")[0]
            if any(cells and cells[0] == wpid for cells in _table_rows(pt)):
                citing.append(pid)
        if set(yaml_refs) != set(citing) and (yaml_refs or citing):
            diffs.append(f"D-PLAN-REF-01 {wpid} yaml={yaml_refs} §3引用={citing}")
        ic = idx_rows.get(wpid)
        if ic and yaml_refs:
            col = ic[3] if len(ic) > 3 else ""
            if col and set(_split_refs(col)) != set(yaml_refs):
                diffs.append(f"D-PLAN-REF-01 {wpid} index plan_ref 不一致")
        # D-TODO-WP local files under todos
        tdir = ai / "todos"
        if tdir.exists() and s2:
            for md in tdir.glob("*/*.md"):
                if md.name.startswith("_") or "inbox" in str(md):
                    continue
                body = md.read_text(encoding="utf-8")
                for line in body.splitlines():
                    if wpid in line and line.startswith("|"):
                        cells = [c.strip() for c in line.strip("|").split("|")]
                        if len(cells) >= 8 and cells[7] not in ("—", "-", "") and cells[7] > s2:
                            diffs.append(f"D-TODO-WP-01 {md.name} 结束 {cells[7]} > WP 结束 {s2}")
    # C7 index status enum
    for wid, cells in idx_rows.items():
        if len(cells) > 2 and cells[2] not in ("待确认", "已规划", "进行中", "已完成", "废弃"):
            unjudged.append(f"C7 {wid} 状态列 {cells[2]!r} 非四枚举/废弃")
    c9 = _check_plan_section4(plans, wps)
    if args.check_plan_section4:
        diffs.extend(c9)
    else:
        unjudged.extend(c9)
    for d in diffs:
        print("DIFF", d)
    for u in unjudged:
        print("UNJUDGED", u)
    if diffs:
        return 1
    if unjudged:
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
