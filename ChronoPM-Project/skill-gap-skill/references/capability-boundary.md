# 技能缺口能力触点清单（独立化迁出步骤）

## 规则

| 文件 | 触点 |
|---|---|
| `references/00-pm-main-rules.md` | P-ALWAYS 第 4 步（只检测，不写文件） |
| `SKILL.md` | 「技能缺口」路由行 |
| `references/10-update-trigger-rules.md` | Level 1 一行 + Level 3 技能缺口信号 |
| `references/23-procedure-index.md` | P-SKILL-GAP |
| `references/11-output-artifact-rules.md` | Type=skill_gap；主文件 `需求-*.md`；禁归档事实源 |
| `governance-shared/scripts/audit_release.py` | 第 15 条必含本目录规则+模板；禁嵌套 SKILL.md |

## 模板

`skill-gap-skill/assets/templates/skill-gap-demand-template.md`

## 回归

`tests/regression-suite.md` 模块 68 SG-001~010

## 示例

`examples/20-技能缺口.md`

## 迁出步骤（未来）

1. 将上表规则段抽出为本包 references。
2. 模板随迁。
3. ChronoPM-Project 保留路由指针与 P-OUTPUT 交叉点。
4. 本目录当前禁止 `SKILL.md`。将来抽独立包时再补 SKILL.md 作加载入口。
