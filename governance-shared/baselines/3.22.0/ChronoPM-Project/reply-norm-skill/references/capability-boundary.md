# 问答规范能力触点清单（独立化迁出步骤）

## 规则

| 文件 | 触点 |
|---|---|
| `SKILL.md` | §7 底线 14–16；路由「问答规范」；规则索引本目录 |
| `references/05-query-rules.md` | 简单查询短条与底线 14–16 同文 |
| `references/00-pm-main-rules.md` | §5.0 指针：细则见本目录；何时准问执行 |
| `references/21-pm-profile-rules.md` | DF-005 / DF-006 指针到 reply-rules |
| `references/23-procedure-index.md` | P-REPLY |
| `governance-shared/scripts/audit_release.py` | 第 15 条必含本目录规则；禁嵌套 SKILL.md |

## 回归

`tests/regression-suite.md` RN-001～011

## 迁出步骤（未来）

1. 将上表规则段抽出为本包 references。
2. ChronoPM-Project 保留 SKILL 底线与 05 短条。
3. 本目录当前禁止 `SKILL.md`。将来抽独立包时再补 SKILL.md 作加载入口。
