# 拆解能力触点清单（独立化迁出步骤）

## 规则

| 文件 | 触点 |
|---|---|
| `references/07-requirement-rules.md` | §8.6 / §8.9.5 / §8.11–§8.14（WF-SD-1/2、分片、自动编号） |
| `references/05-query-rules.md` | 源文档路由；对账/重拆 |
| `references/02-meeting-rules.md` / 00 WF-3 | 会议转写/纪要不走本目录（v3.22.0） |
| `references/06-file-rules.md` | atoms/facts 分片例外；parse-log 归档；软阈值 |
| `references/14-self-check-rules.md` | D24 |
| `references/17-domain-glossary-rules.md` | 拆解术语节流 |
| `references/18-init-wizard-rules.md` | sources/ 已预建，不新增预灌 |
| `references/19-info-completeness-rules.md` | 台账/分片/parse-log 存在性 |
| `references/20-workspace-version-rules.md` | schema 0.12.0 零清门禁 |

## 模板

四份拆解模板在 `source-split-skill/assets/templates/`：`source-doc-meta-template.md`、`source-index-template.md`、`source-parse-log-template.md`、`source-atoms-index-template.md`。`source-type-registry-template.md` **仍在** Project `assets/templates/`。

## 回归

`tests/regression-suite.md` Module 53（SD-001~006）+ Module 54（SD-101~113）+ Module 76 MTG（会议≠拆解）

## 迁出步骤（未来）

1. 将上表规则段抽出为本包 references。
2. 模板随迁。
3. ChronoPM-Project 保留 REQ/WP 交叉点指针。
4. 本目录当前禁止 `SKILL.md`。将来抽独立包时再补 SKILL.md 作加载入口。
