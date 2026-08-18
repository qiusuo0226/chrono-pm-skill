# 升级到 1.17.1

> 从 1.17.0 升级到 1.17.1
> 发布日期：2026-08-15
> Schema 变更：无
> CR 编号：—

## 变更摘要

治理一致性修复(Patch)：修复分发包内幽灵引用（SKILL.md 路由表移除引用已排除 16 号规则的“Skill 变更治理”行，落实 1.16.2 移除意图）；版本失步修正（SKILL.md 版本表 1.16.0→当前值、skill.json blueprint.lastVersion、SKILL_BLUEPRINT 当前版本与 §11.3 演进表补 1.17.0/1.17.1 行并修正 1.16.2/1.16.3 行序）；README.md/README.en.md 回归用例数 185→225（共 6 处）+ 目录树 workspace-template 注释修正为“由 init 脚本程序化创建”；回归套件新增 Module 35 PM Preference Generalization（IR-001~010，10 用例，总计 225）；新增 governance/scripts/audit_release.py 发布前自动断言脚本（11 条机器可判检查，含分发包保留集幽灵引用捕获与基线存在性）；基线补档 1.16.2/1.16.3/1.17.0（自 git tag 重建）+ 1.16.1 缺档登记（无 tag）；release-checklist 接线 audit 脚本。无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。Blueprint Impact metadata-only。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.17.1 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.17.1）


## CHANGELOG 摘录

## 1.17.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（治理一致性修复）。双 Agent 审核驱动（A 方案 V0.2 经两轮 B 独立复核通过）：修复分发包内幽灵引用、版本/文档失步，补齐治理产物断档，新增发布前自动断言脚本。无 workspace schema 变更，无规则/模板/能力变更，无需工作区迁移。

### Fixed
- **分发包幽灵引用根治（SKILL.md）**：§6 路由表移除“Skill 变更治理 | 00 + 16”行——16 号规则被 pack.ps1 排除在分发包外，该行对分发包用户构成幽灵引用（落实 1.16.2“移除 16 号路由条目”的未除净部分；实测 references/ 其余 21 个运行时文件无任何 16 号引用，修复点唯一）。
- **版本失步修正**：SKILL.md 版本控制表“当前 1.16.0”→当前版本；skill.json `blueprint.lastVersion` 1.16.1→当前版本；SKILL_BLUEPRINT.md §1 当前版本 1.16.3→当前版本。
- **SKILL_BLUEPRINT.md §11.3 演进表**：补 1.17.0/1.17.1 行；修正 1.16.2/1.16.3 行序倒置。
- **README.md / README.en.md**：回归用例数 185→225（中英共 6 处）；目录树移除 workspace-template 注释（该目录 git 未追踪、无任何脚本引用），改为“ai/ 目录树由 init 脚本程序化创建”说明。

### Added
- **回归套件 Module 35 PM Preference Generalization（IR-001~010，10 用例，总计 215→225）**：补 v1.17.0 五个能力模块（日报集成审查/主动提问、跨实体联动、关闭佐证、委派跟踪、沟通质量规则 + 查询默认过滤）的对应用例，消除发布口径缺口。
- **governance/scripts/audit_release.py**：发布前自动断言脚本（11 条机器可判检查），覆盖版本四触点/blueprint 元数据/BLUEPRINT 版本/README 用例数/回归套件自洽/§15 索引覆盖/仓库内幽灵引用/分发包保留集幽灵引用（实读 pack.ps1 四类排除模型）/基线存在性/README 目录树真实性；任一失败退出码非零，接入 release-checklist，跑不过禁发。落位 governance/（分发包排除目录，不进包）。
- **基线补档**：自 git tag 重建 `governance/baselines/1.16.2/`、`1.16.3/`、`1.17.0/`；新建 `1.17.1/`；登记 1.16.1 缺档原因（无 v1.16.1 tag，无法精确重建）。
- **governance/regression-reports/rr-20260815-1.17.1.md**：本次发布回归报告。

### Changed
- **release-checklist.md**：新增“发布前自动断言”检查项，引用 `python governance/scripts/audit_release.py`。

### Notes
- 版本记录口径说明：1.16.3 之前合入的 README 补全类 commit 未在该版 CHANGELOG 中单独声明，本次不追溯改写历史条目。
- 无 workspace schema 变更，无模板/脚本（运行时）变更，无需工作区迁移。
- 本地 `assets/workspace-template/` 空目录（git 未追踪、无引用）可由用户自行删除，不影响任何功能。

---
