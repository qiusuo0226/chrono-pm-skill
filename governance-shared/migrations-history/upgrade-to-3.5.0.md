# 升级到 3.5.0

> 从 3.4.0 升级到 3.5.0
> 发布日期：2026-08-20
> Schema 变更：workspace schema 0.9.0 → 0.10.0（新增 `wps/` 目录）
> CR 编号：CR-20260820-006
> 施工依据：方案 §5g/§5h/§5i CR-E（需求六～八）

## 变更摘要

WP 独立存储：`wps/WP-NNN.md` + `wps/_index.md`（查找加速器，非存在性判据）。计划 §3 瘦身为 4 列引用简表。编号保持短号 `WP-NNN`/`PLAN-NNN`（改制已否决）。写后必检 + 级联完整性验证 + D20/D21。WF-8 增加绑定检测（限局部扫描）、创建溯源、DF-019 简洁输出。pending 主动推送。

## 新增目录

| 路径 | 说明 | 验证 |
|---|---|---|
| `wps/` | WP 独立目录，与 plans/todos 同级 | 目录存在；`.skill-version.json` schema=0.10.0 |

## 新增文件

| 路径 | 说明 | 验证 |
|---|---|---|
| `wps/_index.md` | WP 索引（8 列） | 含 8 列表头 |
| Skill `assets/templates/wp-template.md` | WP 独立文件模板 | 前元数据短号 + §1~§6 |
| Skill `assets/templates/wp-index-template.md` | 索引模板 | 8 列 |

## 规则变更

- 00：计划→WP→待办三层；WF-8 强制流程（待绑定 / 局部扫描 / 溯源 / 计划回填 / 级联验证）；§8b 自动识别+未绑定检测+pending 推送；§8c 写后必检；DF-019
- 05：§1a pending 前置输出简洁化；§6.7 先读 `wps/_index.md`
- 06：标准结构新增 `wps/`；§2.1 增 WP 文件；§7.4 索引加速器语义
- 14：D20 WP 数据一致性巡检；D21 WP 绑定完整性（限局部）
- 20：schema 0.10.0 对照行；缺 `wps/` 在 3.5.0+ 提示抽取；缺 timeline/ 仍非 P0
- 21：§5.1a 新增 DF-019
- 10：倒排/新建 WP 落点改 `wps/WP-*.md` + 索引，PLAN 只留简表

## 脚本变更

- `_version.py`：Skill 3.5.0；WORKSPACE_SCHEMA_VERSION 0.10.0
- `config.py`：init 预建 `wps/` + `_index.md`；ALL_TEMPLATE_FILES +2
- `file_registry.py`：结构树补 `wps/`
- `migrate_workspace.py`：3.5.0 能力项 schema 0.10.0；建 `wps/` + `_index.md`；打印一次性抽取入口（脚本不自动删计划内嵌表）

## 模板变更

- `plan-template.md`：§3 改为 4 列引用简表（编号/名称/状态/里程碑）
- 新增 `wp-template.md`、`wp-index-template.md`
- `pm-profile-template.md`：预填 DF-019 行

## 存量数据处理

1. **编号**：存量 `WP-NNN`/`PLAN-NNN` 零迁移。
2. **结构**：migrate 建空 `wps/` + `_index.md`，升 schema 0.10.0。
3. **一次性抽取（非逐步）**：扫描计划文件内嵌 WP → 输出抽取清单（含关联需求候选列）→ PM 确认 → 建独立 WP 文件+索引 → **先迁后验**（数量核对+抽样）→ 验证通过才删计划内嵌表。
4. **截止条件**：首次生成周报或新建待办前，本项目必须完成抽取。未完成 → 阻断并提示，禁止边用边抽导致双结构永久共存。
5. **抽取完成前 fallback**：未抽取 WP 查询读 plans 嵌入清单，避免查询丢失。
6. **索引语义**：文件存在性以 `wps/WP-*.md` 为准；索引缺行补行不删除。
7. **存量待办 WP Ref 空值**：不强制全库回填；D21 仅局部扫描登记 pending。
8. **存量 WP 关联需求为空**：不强制回填；抽取清单提示 PM 补绑。

## 明确不做

- CR-F（通用来源文档拆解 / schema 0.11.0）
- 编号改制（时间戳号已否决）
- 04 号风险/问题回指 WP
- 市监等业务工作区代为迁移
- 向计划简表加「关联需求」列
- 全库扫描待办 WP Ref
- 改待办 WP Ref 时回写 WP 文件 §4
