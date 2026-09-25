# 升级到 3.30.1

> 从 3.30.0 升级到 3.30.1  
> 发布日期：2026-09-20  
> Schema：**0.17.0（不变）**  
> CR：CR-20260920-002  
> IA：IA-20260920-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> Patch。回归合计 **997**（996+1）。  
> 用户拍板：该纠正的就纠正。

## 变更摘要

过期检测补 ledger 原件指纹；digest-schemas 写死无 Python 属性串；19 号 missing_page 提示不阻断；skip 比较去掉 as_of。

## 施工禁区

- 禁止升 schema；禁止 migrate；禁止新目录/新 ProcID
- 禁止改栏目骨架；禁止脚本重编 `_digest.md`
- 禁止改写 `baselines/3.30.0/`
- README 用例数该行全部 996→997

## 工作区迁移

无。

## A. 施工

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR-002 / IA-002 / 本文件 | 治理 |
| A2 | `refresh_views.py` | ledger 列比对；reason=source；digest_status_cmp 去 as_of |
| A3 | digest-schemas.md | 属性串格式；原件层判定 |
| A4 | 05 | 无 Python 比对口径 |
| A5 | 19 §3.3b | missing_page 提示不阻断 |
| A6 | tests | SW-017；`test_source_digest_status.py` |
| A7 | 版本锁步 + README 997 | C9 |

## C9 顺序

1. `_version.py` → `3.30.1`
2. `python ChronoPM-Project/scripts/sync_version.py`
3. README×2 该行全部 996→997
4. `python governance-shared/scripts/audit_release.py` 全绿

施工只认 **997**。

## 验证

阻断加 SW-017。`python ChronoPM-Project/tests/test_source_digest_status.py` 打印 ok。

## 收尾（2026-09-20）

audit 17/17 通过。脚本用例 ok。Grok 不代更。schema 仍 0.17.0。AP 无残留。

## 收尾补记（2026-09-20）

用户指示收尾。升级可以投入使用。Grok 安装区不代更。业务仓未代迁。基线已同步本补记，无功能补丁。
