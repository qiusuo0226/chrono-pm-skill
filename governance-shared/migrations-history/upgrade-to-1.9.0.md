# 升级到 1.9.0

> 从 1.8.4 升级到 1.9.0
> 发布日期：2026-08-10
> Schema 变更：无
> CR 编号：—

## 变更摘要

PM Profile 用户习惯学习(CR-20260810-007, Minor/contract_change)：新增 CAP-023、references/21-pm-profile-rules.md、assets/templates/pm-profile-template.md；复用 domain-glossary 的 pending→confirmed 状态机；AI 被动观察用户行为，3次一致后写入pending，确认后升为confirmed，影响输出格式/交互风格/信息侧重；新增Level 2.5规则优先级；SKILL.md/00核心契约增量修改；init/migrate脚本支持PM Profile创建

## 新增目录

- 无

## 新增文件

- `portfolio/context/pm-profile.md`
- `context/pm-profile.md`

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.9.0 段）。

## 模板变更

- 信息不全

## 工作流变更

- 信息不全

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.9.0）


## CHANGELOG 摘录

## 1.9.0 — 2026-08-10

### Added
- 新增 CAP-023：PM Profile 用户习惯学习与偏好适配
- 新增 `references/21-pm-profile-rules.md`：PM Profile 学习规则全量定义（定位、边界、5 类偏好分类、九步学习流程、五状态机、确认交互、应用规则、异常处理、扩容规则、禁止事项）
- 新增 `assets/templates/pm-profile-template.md`：PM Profile 文件模板（偏好映射表 + 待确认表 + 已否决/已废弃表 + 索引 + Change Log）
- 新增 PM Profile 数据文件：`ai/portfolio/context/pm-profile.md`（项目集模式）/ `ai/context/pm-profile.md`（单项目模式）
- 新增规则优先级 Level 2.5：PM Profile confirmed 偏好（软偏好，项目规则未指定时生效）
- 新增触发词："我的偏好""习惯设置""PM Profile""偏好学习""以后按这种格式"

### Changed (contract_change)
- `SKILL.md` 增加 PM Profile 路由说明、触发词、Level 2.5 优先级、§15 规则索引 21 号条目；frontmatter version → 1.9.0
- `references/00-pm-main-rules.md` §2.7 意图检测前增加 PM Profile 加载步骤；§6 规则优先级新增 Level 2.5
- `references/06-file-rules.md` 新增 §11 PM Profile 文件规范
- `references/20-workspace-version-rules.md` §2 健康检查新增 1.9.0+ 检查项；§5 兜底逻辑新增 pm-profile.md 缺失策略
- 初始化与迁移脚本支持 PM Profile 文件创建
- 修复 `scripts/chronopm_init/config.py` 中 `SKILL_VERSION` 长期滞后问题（自 v1.7.1 起未同步，1.7.0 → 1.9.0）

### Compatibility
- Workspace Schema 保持 0.5.0（不变）
- 不删除、不弱化 CAP-001 ~ CAP-022
- PM Profile 文件不存在时降级跳过，不影响既有流程
- 不影响事实源内容准确性和安全底线

### 回归测试
- `tests/regression-suite.md` 新增第 24 模块「PM Profile（用户偏好学习）」，含 PP-001 ~ PP-010（10 用例：7 正向 / 3 回归）
- 用例合计 122 → 132
- SK-1E 规则索引计数更新：00-20 → 00-21（共 22 条）
- VR-001 版本号更新：1.8.4 → 1.9.0

Blueprint Impact: full — §5.2 能力矩阵追加 CAP-023、§5.3 成熟度统计更新、§7.1/§7.2 规则清单与依赖图追加 21 号、§8 追加 PM Profile 数据流、§9.1 稳定能力列表追加、§10.1 边界表追加、§11.3 已落地变更追加 1.9.0 行、§1 基本信息（版本/文件总数/描述）

---
