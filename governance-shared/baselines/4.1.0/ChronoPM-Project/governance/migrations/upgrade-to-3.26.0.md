# 升级到 3.26.0

> 从 3.25.2 升级到 3.26.0  
> 发布日期：2026-09-10  
> Schema：保持 **0.16.0**  
> CR：CR-20260910-001（总闸）、CR-20260910-002（计划索引）  
> IA：IA-20260910-001 / IA-20260910-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（SKILL 路由 + 00 §2.7 / 写计划后更新 index；§3.3 否）。  
> 回归合计 **937**。  
> 用户拍板：开始执行升级；过程中 annotated tag 并推远程；完全执行完再交用户审核。

## 变更摘要

1. **CR-001**：相关性总闸。相关即拆存关联；L2 约定类+兜底薄源；L3 背景陈述走 journal；禁止「您希望我怎么做」。
2. **CR-002**：`plans/_index` 加速器 + YAML 可选锚点 + D43。查询缺 index 只提示重建。上线范围先读 index。

两 CR **分补丁提交**，同发 3.26.0。

## 施工禁区

- 禁止升 schema / 新规则文件 / 新 ProcID / Project ingest/
- 禁止查询中全量扫描建 plans/_index（14 §2.1）
- 禁止改 PLAN 号段、强制回填历史 YAML、用文件名编码批次
- 禁止用 superseded_by 表示互斥
- 禁止改写 `baselines/3.25.2/`
- 正式文档不得引用 upgrade-plan 路径（发布删 AP）
- 禁止写入市监业务库；Grok 安装区不代更

## A. 施工

| # | 文件 | 动作 | CR |
|---|---|---|---|
| A1 | CR-001/002、IA、本文件、migrations-history、Portfolio 锁步指针、migrations README | 治理 | 两 |
| A2 | 10/00§2.7/23/SKILL/split/CAPABILITY/06 兜底/07§8.8/reply/Portfolio 01/examples/19 | 总闸 | 001 |
| A3 | plan-template、plan-index-template、06§7.6、05、14 D43、00 写计划、view-spec、refresh_views、file_registry、examples/11 | 计划索引 | 002 |
| A4 | `_version.py` 3.26.0 + sync；两包 CHANGELOG/BLUEPRINT；README×2 用例 937 | 锁步 | 两 |
| A5 | Module 84 REL + EX-019；Module 85 PAN | 回归 | 两 |
| A6 | baselines/3.26.0；删 AP；audit；打包 | 发布 | 两 |

## 验证

阻断 11 条：REL-001/006/007/011/012、PAN-001/002/004/005/007/013。audit 退出 0。schema 0.16.0。
