# 升级到 3.25.1

> 从 3.25.0 升级到 3.25.1  
> 发布日期：2026-09-04  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260904-002  
> IA：IA-20260904-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.25.0 → 3.25.1。  
> 用户拍板：开始升级，一次全升级完再交用户审核。  
> contract_change：是（SKILL.md / skill.json 匹配文案 + §2 三态硬闸）。  
> 施工只认回归套件合计 **905**（基线 891 + Module 82 的 14 条）。

## 变更摘要

提高开源仓 Project 第一跳：日常裸词归 Project；集层裸词 + 混报/无表头进度表归 Portfolio；双方互写包名并导流安装。SKILL.md §2 工作区三态硬闸（只看当前根 / `--project-root`，禁止向上翻）：集根 Project 停写，材料交 Portfolio §2.1→§2.2 CALL 成员根。不改 00–23、不改 Portfolio 01–06 手递白名单、不升 schema。双包同号 3.25.1。

## 施工禁区

- 禁止升 workspace schema；禁止新建规则文件 / V-15
- 禁止改手递白名单 / 只读五条语义 / 日报 inbox
- 禁止两边「触发：」裸词互写日报
- 禁止把裸 xlsx 放进 Portfolio「触发：」
- 禁止向上翻父目录判定集根
- 禁止改 pack 品牌提取；displayName 必须保留 `ChronoPM-Project —` / `ChronoPM-Portfolio —`
- 禁止改 `SKILL_MODULE_MAP.md`
- 禁止代更 Grok 安装区
- 正式文档不得引用 upgrade-plan 草稿路径（发布删 AP）

---

## A. 技能包施工

### A1. 治理与记录

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260904-002.md` | 本 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260904-002.md` | 本 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.25.1.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.25.1.md` | 锁步指针 |

### A2. 入口文案与硬闸

**Project SKILL.md**

- description / H1 按 CR 拟定全文
- §2 工作模式：三态硬闸替换「换 Portfolio 对话」段
- front matter version → 3.25.1（sync_version）

**Project skill.json**

- displayName：`ChronoPM-Project — 项目管理（日报/待办/合同）`
- description：市场卡片拟定全文
- versionHistory 头插 3.25.1

**Portfolio SKILL.md**

- description / H1 按拟定全文（「须同时安装 ChronoPM-Project」只一次）
- §2 末追加三态反闸（含 xlsx/csv 不论表头）
- 不改 §4 / §9 只读五条原文

**Portfolio skill.json**

- displayName：`ChronoPM-Portfolio — 跨项目归集（须先装 Project）`
- description：市场卡片拟定全文

### A3. 版本锁步

- `scripts/_version.py` SKILL_VERSION=3.25.1
- `python ChronoPM-Project/scripts/sync_version.py`
- 两包 CHANGELOG 3.25.1 段；Blueprint Impact: metadata-only
- SKILL_BLUEPRINT §1 当前版本（sync）
- README×2 标题版本（sync）

### A4. 回归

`tests/regression-suite.md` 新增 Module 82 TR-001～014。合计 **905**。阻断：TR-001/002/006/009/011。

### A5. 发布

- 基线 `governance-shared/baselines/3.25.1/` 双子树
- 删除 `planning/upgrade-plan-v3.25.1.md`
- `python governance-shared/scripts/audit_release.py` 退出 0
- 打包两 zip；Grok 安装区不代更

## 验证检查

| # | 检查 | 预期 |
|---|---|---|
| V1 | 两包 VERSION / skill.json | 3.25.1 |
| V2 | F description 须同时安装 | 仅开头一次 |
| V3 | F「触发：」 | 无裸词日报/xlsx/csv/入库/投喂/粘贴；有混报/无表头进度表 |
| V4 | 双方 description | 含 ChronoPM-Project 与 ChronoPM-Portfolio |
| V5 | pack 品牌前缀 | ChronoPM-Project / ChronoPM-Portfolio |
| V6 | audit | 退出 0 |
| V7 | schema | 0.16.0 |
