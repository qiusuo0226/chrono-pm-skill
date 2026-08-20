# 升级到 3.1.1

> 从 3.1.0 升级到 3.1.1
> 发布日期：2026-08-20
> Schema 变更：无（workspace schema 保持 0.9.0；skill schemaVersion 保持 0.7.0）
> CR 编号：CR-20260820-002
> 施工依据：`governance-shared/upgrade-plan-v3.1.0.md` V0.17 **§5m CR-G**（Q15/Q16/Q17 已定案）
> 本次执行范围：**只重组开发仓**。业务工作区零迁移；不执行 CR-B～F。

## 变更摘要

Skill 开发仓库三目录重组（收尾 v3.0.0 G-5）：`ChronoPM-Project/` 包根自足 + `ChronoPM-Portfolio/` 补齐 migrations 指针 + `governance-shared/` 承载基线/CR/IA/RR/audit/历史升级链。分发包只带当前这一份 upgrade。PATCH，不改能力、不改 workspace schema。

## 新增目录

- `ChronoPM-Project/` — 单项目 Skill 包根（打包根）
- `governance-shared/` — 仓库级共享（不进任何分发包）
- `governance-shared/migrations-history/` — 全历史 upgrade 归档
- `ChronoPM-Project/governance/migrations/` — 包内只留当前 upgrade
- `ChronoPM-Portfolio/governance/migrations/` — 伴生包指针

## 新增文件

- `ChronoPM-Project/governance/migrations/upgrade-to-3.1.1.md`（本文件）
- `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.1.1.md`（指针，主包为准）
- `governance-shared/change-requests/CR-20260820-002.md`
- `governance-shared/impact-analysis/IA-20260820-002.md`
- `governance-shared/regression-reports/rr-20260820-3.1.1.md`
- `governance-shared/baselines/3.1.1/ChronoPM-Project/` + `ChronoPM-Portfolio/`（双子树）

## 删除文件/目录

- 仓库根不再放置 Project 包文件（已迁入 `ChronoPM-Project/`）
- 仓库根 `governance/` 已拆空删除（内容迁入包内 governance 或 `governance-shared/`）
- 包内 **不保留** 历史 `upgrade-to-0.2.0.md`～`upgrade-to-3.1.0.md`（已归档 `governance-shared/migrations-history/`）

## 规则变更

- 无能力规则变更。`06` 号若引用历史 upgrade 路径，安装后的权威执行源为本目录当前文件；完整历史链仅开发仓 `governance-shared/migrations-history/`。

## 模板变更

- 无

## 工作流变更

- **开发仓安装/换装**：从仓库复制 Skill 时，复制 `ChronoPM-Project/`（及伴生包 `ChronoPM-Portfolio/`），不要复制整个仓库根。
- **分发包 zip 内部布局不变**：zip 顶层仍是 `SKILL.md`（不是再套一层 ChronoPM-Project/）。从 zip 安装的用户无需改操作。
- **打包**：`python tools/pack-skill/scripts/pack.py --skill-root ChronoPM-Project`（在仓库根运行；自动打 Portfolio 第二包；zip 默认写仓库根）。
- **审计**：`python governance-shared/scripts/audit_release.py`
- **init/migrate**：工作目录改为包根 `ChronoPM-Project/`，命令仍是 `python scripts/init_workspace.py ...` / `python scripts/migrate_workspace.py ...`

## 脚本变更

- `tools/pack-skill/scripts/pack.ps1`：`$includeExceptions` 增加 `governance/migrations/` 前缀放行（Q16：仅当前版 upgrade 入包）。
- `tools/pack-skill/scripts/pack.py`：pack.ps1 定位改为向上找仓库根；伴生包改为兄弟目录 `ChronoPM-Portfolio/`；默认 zip 输出到仓库根。
- `governance-shared/scripts/audit_release.py`：双根定位（仓根 vs `ChronoPM-Project/` 包根）；基线读 `governance-shared/baselines/`；3.1.1+ 要求双子树。
- `ChronoPM-Project/scripts/sync_version.py`：包内触点在包根，README×2 在仓根，并锁步 Portfolio 版本。
- `_version.py` / `chronopm_init` 相对定位：随 scripts 迁入包根后，既有 `parent.parent` 仍指向包根，无需改算法。

## 验证检查

- [ ] 仓库根无 `SKILL.md`；`ChronoPM-Project/SKILL.md` 存在
- [ ] `ChronoPM-Project/governance/migrations/` 仅含当前 `upgrade-to-3.1.1.md`（+ 可选 README）
- [ ] `governance-shared/migrations-history/` 含 `upgrade-to-3.1.0.md` 及更早链
- [ ] 分发包含 `governance/migrations/upgrade-to-3.1.1.md` 与 `governance/contracts/skill-contract.md`，不含历史 upgrade、不含 baselines
- [ ] `python governance-shared/scripts/audit_release.py` 13/13 PASS
- [ ] workspace schema 仍 0.9.0；业务工作区未改

## 存量工作区

**零文件迁移**。`.skill-version.json` 日后可由 migrate 只升元数据 skillVersion → 3.1.1。

## 明确不做

- CR-B～F
- 不改业务工作区（市监）
- 不把历史 49+ 份 upgrade 打进 zip
- 不改 ≤3.0.0 与 3.1.0 已冻结基线的内部布局（3.1.0 仍为 CR-A 时的旧快照形态；双子树从 3.1.1 起）
