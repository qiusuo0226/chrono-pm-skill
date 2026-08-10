# ChronoPM Skill v1.10.2 发布说明

- **版本**：1.10.2（Patch 级 bugfix）
- **发布日期**：2026-08-11
- **Workspace Schema**：0.5.0（无迁移，保持不变）
- **上一个版本**：1.10.1
- **发布性质**：脚本层版本治理修复，无能力 / 契约 / 规则变更

---

## 一、本次修复内容

修复脚本层「版本号分散且不同步」与「`--target-version` 被忽略」两类工程缺陷（CR-20260810-009）。

### 1) 版本号分散且不同步（P0）

此前 `Skill 版本`在 5 个源中硬编码且互相失步：`VERSION`/`SKILL.md`/`skill.json` 为 1.10.1，但脚本层落后。

| 源 | 修复前 | 修复后 |
|---|---|---|
| `scripts/chronopm_init/config.py` | `1.9.0`（落后 2 版） | 从 `_version.py` 读取 |
| `scripts/migrate_workspace.py` | `1.6.0`（落后 4 版） | 从 `_version.py` 读取 |
| `scripts/chronopm_init/file_registry.py` README | 硬编码 `0.4.0` / `0.2.0`（差 7 版 / 3 schema） | `{SKILL_VERSION}` / `{WORKSPACE_SCHEMA_VERSION}` 插值 |

**核心**：新建 `scripts/_version.py` 作为 `SKILL_VERSION` / `WORKSPACE_SCHEMA_VERSION` 的**单一版本源**，所有脚本统一从该源读取。

### 2) `--target-version` 参数被忽略（P0）

`update_version_file()` 与 `append_migration_log()` 内部硬编码 `CURRENT_SKILL_VERSION`，不接收目标版本，导致打印显示 `--target-version` 但 `.skill-version.json` 与 `migration-log.md` 实际写入旧常量。现已修复：两函数接受 `skill_version` 参数并实际写入（缺省回落单一版本源）。

### 3) `VERSION_CAPABILITIES` 表不完整（P1）

能力检测表仅到 1.6.0，缺少 1.7.0/1.8.0/1.9.0/1.10.0/1.10.1 条目，迁移脚本无法检测这些版本的新增文件。已补全并对齐 CHANGELOG（含 1.10.0 与 1.1.0 的历史索引去重标注）。

---

## 二、变更清单

### 修改的文件

| 文件 | 变更 |
|---|---|
| `scripts/_version.py` | **新增**：单一版本源（SKILL_VERSION=1.10.2、WORKSPACE_SCHEMA_VERSION=0.5.0） |
| `scripts/chronopm_init/config.py` | 版本常量改从 `_version.py` 导入并转发符号（消除 1.9.0 落后） |
| `scripts/migrate_workspace.py` | 版本源收敛 + 修复 target-version 写入 + 补全 VERSION_CAPABILITIES |
| `scripts/chronopm_init/file_registry.py` | README 硬编码版本改为 f-string 插值 |
| `governance/review-checklists/release-checklist.md` | 新增「Script Version Consistency」检查项 |
| `tests/regression-suite.md` | 新增回归用例 SC-1G~1K |
| `VERSION` | 1.10.1 → 1.10.2 |
| `SKILL.md` | frontmatter `version` → 1.10.2 |
| `skill.json` | 顶层 `version`、`blueprint.lastVersion`、`versionHistory` 头部 → 1.10.2 |
| `CHANGELOG.md` | 顶部新增 1.10.2 条目 |
| `governance/change-requests/CR-20260810-009.md` | **新增**：CR 归档 |
| `governance/regression-reports/rr-20260810-1.10.2.md` | **新增**：回归报告 |

### 未变更的内容

- 能力点：CAP-001 ~ CAP-024 全部保持不变（无增删）。
- 规则层：`references/00-21` 完全未改动。
- 模板层：`assets/templates/` 完全未改动。
- 健康检查准确性（问题 4）：本次不修，另开 CR 处理（遵循用户范围界定）。

---

## 三、兼容性

- Workspace Schema 0.5.0 不变，**无迁移**。
- 不改变任何事实源结构、规则语义或查询行为。
- 脚本向后兼容：`config.SKILL_VERSION` / `migrate_workspace.CURRENT_SKILL_VERSION` 符号保留，既有调用无改动。
- 对既有项目工作区完全向后兼容。

---

## 四、回归结论

- 执行回归（脚本契约 SC-1G~1K + 版本触点/README 渲染/编译）：**12 项全部通过，0 失败**（详见 `governance/regression-reports/rr-20260810-1.10.2.md`）。
- 端到端验证：`migrate --target-version 1.9.0` 实际写入 1.9.0；无 target 回落 1.10.2；能力表驱动迁移正确创建 pm-profile。
- 版本触点一致性：`_version.py` / `VERSION` / `SKILL.md` / `skill.json` 四处全部为 1.10.2，已核验。
- 脚本编译：`py_compile` 全部通过。

---

## 五、升级建议

- 当前使用 v1.10.1 的用户可直接平滑升级到 v1.10.2，无任何数据或配置迁移动作。
- 建议升级时确认脚本可通过 `python scripts/migrate_workspace.py --help` 正常调用。
- 若旧工作区 `.skill-version.json` 存在历史缺漏版本号（0.2.0/0.6.0/1.3.0~1.5.0），迁移检测可能返回空（既有行为），后续维护 CR 将补全。

---

*本说明由 ChronoPM 治理流程生成，对应 CR-20260810-009。*
