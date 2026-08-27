# 升级到 3.18.0

> 从 3.17.0 升级到 3.18.0  
> 发布日期：2026-08-27  
> Schema 变更：无（保持 **0.16.0**）  
> CR：CR-20260827-001～005  
> IA：IA-20260827-001～005  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.17.0 → 3.18.0。  
> 用户拍板：执行升级；每节点 annotated tag（中文）推 origin 与 github；全部完成后再请用户核验。  
> contract_change：是。方案 V1.0（B1/B2 通过-待修订，A 已消化至 V1.0）。  
> 按 16 §4 拆 **5** 个 CR。施工只认回归 **706**，禁用 691/692/700。

## 变更摘要

建包联动按计划分章重建工作包图；WP 结构闸 + SCAN 冻结 + §8b 人期溯源；skill-gap 落盘前自检；完成/废弃 index 归档且 B 节强制处理历史项目；结转 Step 0 脚本（拷贝后裁剪）；对外问答规范能力目录。双包同号 3.18.0。schema 0.16.0。

## 施工禁区

- 禁止升 workspace schema；禁止搬 `wps/WP-*.md`
- 禁止新建 `references/NN-*.md`（允许 `reply-norm-skill/` 能力目录，禁止其内 `SKILL.md`）
- 禁止图走 P-OUTPUT / `ai/outputs/`
- 禁止一条待办多个 WP Ref
- 禁止 SCAN 清空 §8 ✅ 行执行人；禁止改人期不写 §8b
- 禁止自动出组；禁止脚本 exit 0 后手搓全员
- 禁止 `retired_at` 把最近编辑日当废弃日
- 正式文档不得引用 upgrade-plan 草稿路径
- 禁止写入业务工作区（开发仓无 `ai/wps/` 则 B 节 skip）

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作 |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260827-001.md`～`005.md` | 五 CR |
| A1.2 | `governance-shared/impact-analysis/IA-20260827-001.md`～`005.md` | 五 IA |
| A1.3 | 本文件 | 本施工清单 |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.18.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为本文件 |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.18.0.md` | 指针 |

### A2. 图形态与建包联动（节点2，CR-001）

见 CR-001。11 §17.2 分章；指纹改 plan_ref+日期+当前阶段；10 L3 补 `_wp-chart.md`；SKILL WP 创建载 23；8c.2 含图；P-WP-CHART 含新建；默认图不含废弃/已完成。

### A3. 结构闸 / SCAN / 8b / skill-gap（节点3，CR-002）

见 CR-002。§5 条件必填；禁混排；§3b 覆盖；§8b；S1–S6；gap 落盘前自检；verify `--check-wp-structure`。

### A4. 归档与历史 B 节（节点4，CR-003）

见 CR-003。index 三段 12 列；YAML 日期；migrate_business 3.18；B 节强制分类+回填+重建图。

### A5. 结转脚本（节点5，CR-004）

见 CR-004。`carryover_step0.py`；拷贝后裁剪含 §1.5/§4/§5；exit≠0 仅 E5 失败人。

### A6. 问答规范（节点6，CR-005）

见 CR-005。`reply-norm-skill/` 无 SKILL.md；SKILL 底线 14–16 与 05 短条同步。

### A7. 版本触点（节点7）

| # | 文件 | 动作 |
|---|---|---|
| A7.1 | `_version.py` | 3.18.0；schema 0.16.0 |
| A7.2 | `sync_version.py` | 双包触点 |
| A7.3 | CHANGELOG 双包 + BLUEPRINT + 根 README×2 | 3.18.0；回归 **706** |
| A7.4 | `tests/regression-suite.md` | Module 72（WPC/WPS/SKG-011+/ARC/CO-S/RN） |
| A7.5 | `migrate_workspace.py` VERSION_CAPABILITIES | 3.18.0 schema 0.16.0 |
| A7.6 | Portfolio 锁步 + 02 一句三段 index |

### A8. 基线与发布（节点8）

| # | 动作 |
|---|---|
| A8.1 | `baselines/3.18.0/` 双子树 |
| A8.2 | `audit_release.py` 退出 0 |
| A8.3 | 每节点 annotated tag 推 origin 与 github |
| A8.4 | 终 tag `v3.18.0` |
| A8.5 | 删除 AP 草稿；分发包；全部完成后再请用户核验 |

---

## B. 存量工作区（强制处理历史完成/废弃）

有 `ai/wps/` 的业务仓必须处理。开发仓无 wps/ → skip。

先 dry-run 清单，PM 确认后 `--migrate-business`（写前 `ai/backup/migration-snapshot-*`）。

分类（先读 WP 文件）：

1. `effect=废弃` 或 index 状态=`废弃` → §3 废弃归档
2. 头 `status=已完成` 或 §7 自下而上最近一条到状态=`已完成` → §2 已完成归档
3. 其余 → §1 进行中

时间：`completed_at` = YAML 已有合法日，否则 §7 自下而上最近「到状态=已完成」的时间列，否则 `—`+⚠️。`retired_at` = YAML 或 §6 废弃行日期；**不得**用无法证明等于废弃当日的 `updated`。

写：YAML 缺补日期 → 重写 `_index.md` 三段 12 列 → 覆盖 `_wp-chart.md`（仅进行中段、新形态）。不搬 WP 文件，不改 §7。幂等。

---

## C. 验证检查

- [x] `_version.py` 3.18.0 / schema 0.16.0
- [x] 11 §17 分章；默认图无废弃/已完成
- [x] WP 创建载 23；8c.2 含图与 8b
- [x] §8d 含 S1–S6 逐步表
- [x] gap-capture 落盘前自检；禁旧批次范本
- [x] index 模板三段 12 列
- [x] carryover_step0.py 五函数；exit≠0 仅 E5
- [x] reply-norm-skill 无 SKILL.md；底线 14–16 与 05 同步
- [x] 回归 706；audit 0
- [x] 无业务仓路径写入；正式文档不引用 upgrade-plan
- [x] 双包 3.18.0
