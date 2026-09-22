# 升级到 3.27.0

> 从 3.26.0 升级到 3.27.0  
> 发布日期：2026-09-10  
> Schema：**0.16.0 → 0.17.0**  
> CR：CR-20260910-003（投影）、CR-20260910-004（表/边/协议）、CR-20260910-005（迁移/联邦）  
> IA：IA-20260910-003 / 004 / 005  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（SKILL / 00 / skill-contract）。  
> 回归合计 **961**。  
> 用户拍板：执行升级；过程中 tag 并推远程；完全执行完再交用户审核。

## 变更摘要

1. **CR-003**：`parse_todos` 只读 §1.1、去重、WP 正则。
2. **CR-004**：范围登记表 + relations + 05 失败门 + D44。
3. **CR-005**：migrate 0.17.0 抽取回填；清零才算该工作区升完；V-15。

三 CR **分补丁提交**，同发 3.27.0。顺序 003→004→005。

## 施工禁区

- 禁止新规则文件 / 新 ProcID / 新 verify 引擎 / 向量库
- 禁止领域枚举进包；禁止业务仓绝对路径
- 禁止查询全量扫描建表（14 §2.1）
- 禁止改写 `baselines/3.26.0/`
- 正式文档不得引用 upgrade-plan 路径（发布删 AP）
- 禁止写入业务库；Grok 安装区不代更

## 工作区迁移

```
python scripts/migrate_workspace.py --project-root <单项目根>
```

建 `ai/registers/`；抽取显式结构为 `回填-未确认`；`scopeBackfillOpen>0` = 升级未完成。**每一行、每一缺口有 PM 决策后 N=0 才算该工作区升完。** 日报/待办不阻断。任意工作区须先 3.26.0 再 3.27.0，不跳版本。

## A. 施工

| # | 文件 | 动作 | CR |
|---|---|---|---|
| A1 | CR/IA/本文件 | 治理 | 三 |
| A2 | refresh_views parse_todos | 投影 | 003 |
| A3 | 模板+relations+05/14/00/06/17/19/SKILL | 表边协议 | 004 |
| A4 | migrate 0.17.0；20；Portfolio V-15；contract；skill.json | 闸+联邦 | 005 |
| A5 | `_version.py` 3.27.0 / 0.17.0 + sync；CHANGELOG；README 961/40 | 锁步 | 三 |
| A6 | Module 86–88 | 回归 | 三 |
| A7 | baselines/3.27.0；删 AP；audit；打包 | 发布 | 三 |

## 验证

阻断：VW-001/002、REG-101、DER-001/002/003、EDG-001、FED-003、MIG-101/102/103、全量 961。audit 退出 0。schema 0.17.0。

## 收尾（2026-09-11）

用户核验通过，可投入使用。Grok 不代更。业务仓未代迁。

migrate 0.17.0：模板驱动建 `registers/`；`if target.exists(): continue` 不覆盖；抽取标「回填-未确认」并按来源/WP/批次去重。新工作区由 `chronopm_init` 建表+种子。AP 曾写的独立 `build_scope_register.py` 未落地，由上述两条路径覆盖。

存量工作区须先 3.26.0 再 3.27.0；`scopeBackfillOpen` 清零（N=0）前该工作区视为升级未完成。
