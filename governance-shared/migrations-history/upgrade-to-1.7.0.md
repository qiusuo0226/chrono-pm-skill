# 升级到 1.7.0

> 从 1.6.1 升级到 1.7.0
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

初始化向导+迭代正式化+信息完整性巡检：18-init-wizard-rules.md(六步引导建档)、19-info-completeness-rules.md(7层P0-P3巡检)、iteration-register-template.md(ITR-NN迭代登记册)、6个模板增强(合同时间字段/迭代概览/所属迭代/迭代分配/迭代数列)、init脚本增强(生成迭代登记册+向导引导提示)、SKILL.md路由+编码+索引增强、00主规则意图检测增强、10更新触发+完整性检查机制

## 新增目录

- 无

## 新增文件

- `plans/iteration-register.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.7.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.7.0）


## CHANGELOG 摘录

## 1.7.0 — 2026-08-10

### Added
- 新增项目初始化向导能力：`references/18-init-wizard-rules.md`（六步引导流程：合同层→项目层→迭代层→需求层→资源层→里程碑层，含触发条件、跳过机制、进度记忆、断点续接、确认写入、文件上传解析规则）
- 新增项目信息完整性巡检与补全提醒能力：`references/19-info-completeness-rules.md`（7层检查维度：合同/项目/迭代/需求/任务/资源/里程碑，P0-P3分级提醒，强/弱触发场景，静默模式，完整性巡检报告）
- 新增迭代登记册模板：`assets/templates/iteration-register-template.md`（ITR-NN编码、迭代总览表、迭代详情、关联里程碑可选关联）
- 新增迭代 ID 编码 `ITR-NN`（SKILL.md §8）
- `SKILL.md` 路由表新增"项目初始化向导"和"项目信息完整性巡检"两个场景
- `SKILL.md` §5.1c 新增初始化向导工作流描述
- `SKILL.md` §15 规则索引新增 18 和 19 规则条目
- `SKILL.md` front matter 新增初始化向导/迭代管理/完整性巡检的触发关键词和描述
- `00-pm-main-rules.md` §2.7 默认意图检测新增"初始化"和"完整性巡检/补全提醒"两个意图类型
- `10-update-trigger-rules.md` 新增 §8 更新后关联字段完整性检查机制（检查时机、P0-P3分级、与14-self-check的协作边界）
- `init_workspace.py` 新增 `create_iteration_register()` 函数，单项目和项目集模式均生成 `plans/iteration-register.md`
- `init_workspace.py` 完成提示新增初始化向导引导（"对 AI 说：初始化项目"）
- `init_workspace.py` `ALL_TEMPLATE_FILES` 新增 `iteration-register-template.md`
- 6 个模板增强：
  - `project-context-template.md`：新增合同信息表（合同名称/总额/类型/范围摘要/立项时间/启动时间/计划完工时间/测算周期）
  - `project-brief-template.md`：新增立项时间字段、迭代概览一行摘要小节、completeness_status/last_completeness_check 可选字段
  - `project-index-template.md`：子项目清单新增迭代数列
  - `requirement-register-template.md`：总览表新增所属迭代列（ITR-NN / 未分配）
  - `resource-register-template.md`：新增迭代分配视图小节
  - `init_workspace.py` 中 `create_brief_file()` 和 `create_context_file()` 增加对应占位字段

### Changed
- Skill 版本升级 1.6.1 → 1.7.0（Minor：新增能力，向后兼容）
- `init_workspace.py` SKILL_VERSION 常量更新为 1.7.0（修正原 1.6.0 落后问题）
- `SKILL.md` front matter version 更新为 1.7.0
- `skill.json` version 更新为 1.7.0
- `skill.json` blueprint.lastVersion 更新为 1.7.0
- `skill.json` versionHistory 新增 1.7.0 条目
- `SKILL_BLUEPRINT.md` 版本号更新为 1.7.0，能力矩阵新增 CAP-020/CAP-021，规则清单新增 18/19，数据流新增初始化/巡检流程
- `skill-contract.md` Protected Capabilities 新增 INIT_WIZARD 和 COMPLENESS
- `tests/regression-suite.md` 新增 17. 初始化向导（IW-001~IW-005）和 18. 信息完整性巡检（IC-001~IC-005）模块

### Fixed
- 修复 portfolio 模式下 `ai/logs/` 目录缺失导致 `migration-log.md` 创建失败的预存 Bug
- 修复 `generate_portfolio_readme()` 中 `{子项目}` 被 f-string 解析为变量导致 `NameError` 的预存 Bug
- 修正 `init_workspace.py` SKILL_VERSION 常量从 1.6.0 更新至 1.7.0（原 1.6.0 落后于 VERSION 文件的 1.6.1）

### Not Changed
- schemaVersion 保持 0.5.0（不新增机器配置字段，不改变目录结构模式）
- 不删除、不弱化任何现有能力
- 路由表仅新增 2 行，不移除原有路由
- 14-self-check-rules.md 不修改职责，与 19-info-completeness-rules.md 保持边界分离

### Blueprint Impact
- full：新增 CAP-020（初始化向导）和 CAP-021（信息完整性巡检），规则清单新增 18/19，数据流新增初始化向导和完整性巡检流程，成熟度统计更新，已知局限更新
- workspace schema 不变

### Upgrade Notes
- 从 1.6.1 升级：Minor 版本，直接覆盖即可。
- workspace schema 不变（仍为 0.5.0），已有工作区无需迁移。
- **核心新增能力**：
  1. 初始化向导：用户说"初始化项目"即可启动六步向导，引导录入合同/项目/迭代/需求/资源/里程碑基线信息
  2. 迭代登记册：新增 `plans/iteration-register.md` 文件，正式管理迭代信息（ITR-NN 编码，可选关联里程碑）
  3. 信息完整性巡检：日常使用中自动检查字段缺失，P0/P1 缺失会主动提醒
- 旧工作区如需使用迭代登记册，可手动创建 `plans/iteration-register.md`（从模板复制）或对 AI 说"初始化项目"补录。
- 已有需求登记册中新增了"所属迭代"列，默认值为"未分配"，不影响现有数据。
- 已有资源登记册中新增了"迭代分配视图"小节，不影响现有资源清单表。

---
