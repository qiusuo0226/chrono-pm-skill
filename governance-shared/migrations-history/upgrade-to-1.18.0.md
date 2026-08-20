# 升级到 1.18.0

> 从 1.17.1 升级到 1.18.0
> 发布日期：2026-08-15
> Schema 变更：无
> CR 编号：—

## 变更摘要

推导基线(Minor)：引入推导基线(Reasoning Baseline)机制。00号新增§10推导规则（§10.1派生投影优先级+§10.2跨源矛盾处理+§10.3生命周期推导链6步+§10.4推导后动作规范SUGGEST+§8a+§10.5任务集4级降级关联）；05号新增§3(3)a终态事件豁免；01号§6.2新增里程碑事件维度+§3.3追加第5/6条实体枚举校验；03号新增§8.2推导触发级联；14号新增D14推导基线检查；19号新增§3.3a推导基线巡检维度；18号新增§7a可选步骤引导创建entity-registry；新增entity-registry-template.md数据模板；周报模板新增状态推导说明输出段；脚本层同步(config.py/migrate/file_registry)。无workspace schema变更，无需工作区迁移。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.18.0 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.18.0）


## CHANGELOG 摘录

## 1.18.0 — 2026-08-15（本次发布 · released）

> 发布归档：Minor（推导能力升级）。双 Agent 四轮审核收敛（A V0.1→V1.0，B1+B2 独立审核）。核心升级：引入推导基线（Reasoning Baseline）机制，新增 00号 §10 推导规则（生命周期推导链 + 跨源矛盾处理 + 推导后动作规范 + 任务集 4 级降级关联），新增 entity-registry 数据模板，05号 §3(3)a 终态事件豁免，周报/日报推导增强，脚本层同步。无 workspace schema 变更，无需工作区迁移。

Blueprint Impact: metadata-only（CAP 扩展条目 + 版本演进表行，无结构性变更）

### Added
- **推导基线规则（00号新增 §10）**：§10.1 推导基线定义（派生投影优先级）+ §10.2 跨源矛盾处理（里程碑终态事件豁免）+ §10.3 生命周期推导链（6 步通用推导链 + 项目覆盖机制）+ §10.4 推导后动作规范（SUGGEST + §8a 强制呈现 + 推导链路可追溯）+ §10.5 推导→任务集关联（4 级降级识别 + 作用域隔离）。
- **终态事件豁免（05号新增 §3(3)a）**：过程记录含里程碑终态事件时豁免"以事实源为准"规则，推导结论通过 SUGGEST 建议同步，不直接修改事实源。
- **日报/周报推导增强（01号）**：§6.2 集成审查新增"里程碑事件 vs 任务板状态"维度；§3.3 追加第 5/6 条（实体枚举校验 + 状态推导标注）。
- **任务板推导级联（03号新增 §8.2）**：Task 生命周期推导触发，复用 §8 级联传播机制。
- **自查清单新增 D14（14号）**：推导基线 entity-registry 完整性检查。
- **完整性巡检新增推导基线维度（19号 §3.3a）**：4 项检查（存在性/覆盖度/关联任务填充/状态一致性）。
- **初始化向导可选步骤（18号 §7a）**：多模块/多阶段项目引导创建 entity-registry。
- **entity-registry 数据模板**：新增 `assets/templates/entity-registry-template.md`（实体清单 + 项目级推导链覆盖 + 终态事件扩展 + 更新规则 + 回填触发）。
- **周报模板推导输出段**：`weekly-report-template.md` + `portfolio-weekly-template.md` 新增"状态推导说明"输出段。
- **project-context 推导基线引用**：`project-context-template.md` 末尾新增推导基线引用段。

### Changed
- **脚本层同步**：`config.py` ALL_TEMPLATE_FILES 追加 entity-registry-template.md；`migrate_workspace.py` template_map 追加 entity-registry 映射；`file_registry.py` 目录树追加 entity-registry.md 注释。
- **SKILL.md**：路由表新增"状态推导/跨源校验/生命周期推导"行；§15 规则索引更新 00/01/03/05/14/18/19 号描述；front matter version 同步。
- **SKILL_BLUEPRINT.md**：CAP 扩展条目（Reasoning Baseline）+ 版本演进表 1.18.0 行。

### Notes
- 00号属核心契约层，已标注 contract_change + 全量回归。
- 00号新增后约 ~541 行，已超 06号 >300 行瘦身参考阈值，列入后续版本瘦身候选（可评估独立为 22 号）。
- entity-registry 是事实源的派生投影，非独立事实源；统计表自动推导不得手工维护。
- W33 周报数据修复与本次 Skill 升级解耦，待单独确认执行。

---
