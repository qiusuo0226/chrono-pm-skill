---
rule_id: 20
title: 工作区版本与迁移规则
category: 工作区管理
risk_level: 中
depends_on: [00]
version: 1.0
---

# 20 工作区版本与迁移规则

本规则定义工作区版本兼容性检查、健康检查、迁移模式和兼容模式的行为规范。

## 1. 工作区版本检查

AI 在进入任何工作区的处理流程前，**必须先读取 `ai/.skill-version.json`**（如存在），获取以下信息：

| 字段 | 说明 |
|---|---|
| `skillVersion` | 该工作区初始化时使用的 Skill 版本 |
| `workspaceSchemaVersion` | 该工作区的目录结构版本 |
| `mode` | 工作区模式（single / portfolio）|
| `initializedAt` | 初始化时间 |
| `lastMigratedAt` | 最近一次迁移时间（null 表示从未迁移）|

**版本兼容性判断规则：**

1. AI 读取 Skill 包中的 `VERSION` 文件获取当前 Skill 版本。
2. 对比当前 Skill 版本与工作区的 `skillVersion`。
3. 根据 `CHANGELOG.md` 中的 Upgrade Notes 判断是否需要迁移。
4. 按以下策略处理：

| 版本差异情况 | AI 行为 |
|---|---|
| 版本一致 | 正常处理 |
| Skill 版本更新但 schema 未变 | 按新规则处理，提示用户"当前规则版本为 x.x.x，工作区由 x.x.x 初始化，规则已升级但目录结构无需迁移" |
| schema 版本不同 | 提示用户需要迁移，输出迁移建议，不自行执行迁移 |
| 无 .skill-version.json | 提示"未检测到版本文件，可能由旧版本初始化。建议运行 init_workspace.py 重新初始化或手动创建版本文件" |

**版本不匹配时的提示格式：**

```markdown
## 版本兼容性检测

- 当前 Skill 版本：[版本号]
- 工作区初始化版本：[版本号]
- Workspace Schema 版本：[版本号]
- 差异说明：[根据 CHANGELOG.md 的 Upgrade Notes 说明差异]
- 是否需要迁移：是 / 否
- 迁移建议：[如需要，列出迁移步骤]
```

**规则：**

1. AI 不得在版本不匹配时自行执行迁移操作，必须输出迁移建议由用户确认。
2. AI 在版本不匹配但仍可正常处理时（schema 未变），应按新规则处理，同时提示版本差异。
3. 迁移完成后，用户需更新 `.skill-version.json` 中的 `lastMigratedAt` 字段。
4. 迁移历史记录在 `ai/logs/migration-log.md` 中。

## 2. 工作区健康检查（每次会话首次交互时执行）

AI 在每次会话**首次进入工作区**时（而非每次请求），必须执行工作区健康检查：

**检查步骤：**

1. 读取 `ai/.skill-version.json`，获取 `skillVersion` 和 `workspaceSchemaVersion`。
2. 读取 Skill 包 `VERSION` 文件，获取当前 Skill 版本。
3. 如果版本不一致，按版本差距检查以下内容是否存在：

| 版本范围 | 检查项 |
|---|---|
| 0.3.0+ | `portfolio/resources/resource-register.md` 和 `transfer-log.md` 是否存在 |
| 0.4.0+ | `context/project-brief.md` 是否存在 |
| 0.5.0+ | `outputs/` 目录是否存在 |
| 0.7.0+ | `reports/daily/personal/summaries/` 目录是否存在；是否还在用 `YYYY/MM` 旧结构 |
| 0.8.0+ | `continuity/` 目录和 4 个文件是否存在 |
| 0.9.0+ | `portfolio/todos/` 目录是否存在 |
| 1.1.0+ | `portfolio/todos/snapshots/` 和 `portfolio/todos/actuals/` 目录是否存在 |
| 1.1.0+ | `portfolio/todos/history-index.md` 是否存在 |
| 1.9.0+ | `portfolio/context/pm-profile.md`（项目集模式）或 `context/pm-profile.md`（单项目模式）是否存在 |

3b. 检查 `ai/templates/` 参考模板库完整性：对比工作区 `ai/templates/` 下的文件与 Skill 包 `assets/templates/` 目录中的模板清单（`ALL_TEMPLATE_FILES`），如有缺失模板，在健康报告的“缺失能力”表中列出并建议执行迁移补齐。同时检查 `outputs/.templates/manifest-template.md` 是否存在。

4. 如发现缺失，输出工作区健康报告。

**健康检查输出格式：**

```markdown
## 工作区健康检查

- 当前 Skill 版本：1.2.0
- 工作区版本：0.8.0
- Schema 版本：0.4.0 → 当前 0.5.0

### 缺失能力

| 版本 | 能力 | 缺失项 | 影响 |
|---|---|---|---|
| 0.9.0 | 快速查询+待办索引 | portfolio/todos/ 目录 | 查询待办时会回退到全量扫描 |
| 1.1.0 | 计划快照 | snapshots/actuals 目录 | 无法回查历史计划和偏差 |

### 建议

检测到工作区版本落后，缺少 2 个能力模块。

执行迁移：
```
python scripts/migrate_workspace.py --project-root .
```

或先查看差异（不执行）：
```
python scripts/migrate_workspace.py --project-root . --dry-run
```

是否现在执行迁移？
```

**规则：**

1. 健康检查在每次会话首次交互时执行，不重复执行。
2. 如版本一致且能力完整，不输出健康报告，直接正常处理。
3. 如版本不一致但有缺失，必须输出健康报告和建议。
4. AI 不得自行执行迁移，必须由用户确认。
5. 如用户拒绝迁移，AI 按当前可用的能力处理，缺失能力用兜底逻辑替代。

## 3. 功能触发时检查（Feature-Triggered Check）

当用户触发某个需要特定目录/文件的能力，但该目录/文件不存在时，AI 不得直接退化为全量扫描，必须先提示工作区可能未升级：

**示例：用户问"我明天的待办是什么"，但 `portfolio/todos/personal-todo-index.md` 不存在**

AI 应输出：

```markdown
我准备按快速查询规则读取 PM 待办索引，但当前工作区缺少：

`ai/portfolio/todos/personal-todo-index.md`

这通常表示当前 `ai/` 目录还停留在旧版本结构。

当前建议：
1. 先执行工作区升级检查
2. 补齐 `ai/portfolio/todos/` 索引目录
3. 可选从最近 7 天日报重建待办索引
4. 再回答"明天待办"

是否现在生成升级计划？

如果你暂时不升级，我也可以进入兼容模式，从任务看板和最近日报索引中查询，但会更慢且可能不完整。
```

**规则：**
1. 不得在缺少索引时直接创建临时脚本全量扫描。
2. 必须先提示工作区可能未升级。
3. 提示后用户可选择：升级 / 兼容模式 / 取消。

## 4. 兼容模式

当用户选择不升级时，AI 进入兼容模式：

1. 使用旧目录结构和兜底逻辑回答。
2. 明确提示新能力不可用或性能较低。
3. 不强行使用新版路径。
4. 在必要时提醒可升级。

**兼容模式提示格式：**

```markdown
⚠️ 兼容模式
当前工作区未升级到最新版本，以下能力降级运行：
- 快速查询：退化为读任务看板 + 日报索引（较慢）
- 计划快照：不可用
- PM 待办全景视图：仅列出 PM 个人任务

如需使用完整能力，请执行：
python scripts/migrate_workspace.py --project-root .
```

## 5. 兜底逻辑

当工作区缺少某些能力对应的目录/文件时，AI 不得报错中断，按以下兜底策略处理：

| 缺失能力 | 兜底策略 |
|---|---|
| todos/ 索引缺失 | 退化为读取 `tasks/board.md` + 最近日报索引，但提示较慢 |
| snapshots/ 缺失 | 退化为读取日报索引，但提示无法对比计划偏差 |
| continuity/ 缺失 | 跳过历史衔接功能，提示用户初始化 |
| project-brief.md 缺失 | 退化为读取 project-context.md |
| summaries/ 缺失 | 退化为逐日扫描该人日报 |
| outputs/ 缺失 | 在工作区根目录下自动创建 |
| pm-profile.md 缺失 | 跳过偏好加载，按默认行为处理，提示执行 `migrate_workspace.py --create-profile` 补建，不阻塞 |

## 6. 升级提醒频率控制

AI 不得每次都烦用户。升级提醒频率通过 `.workspace-health.md` 控制：

| 字段 | 说明 |
|---|---|
| `last_prompted_upgrade_at` | 上次提醒时间 |
| `ignored_until` | 忽略截止时间（用户选择"暂不提醒"时设置） |

**规则：**
1. 如 `ignored_until` 未到，不重复提醒。
2. 用户选择"暂不提醒一周"时，设置 `ignored_until` 为 7 天后。
3. 如用户主动问"检查工作区健康"，不受 `ignored_until` 限制。

## 7. 升级触发词

当用户输入包含以下表达时，必须触发工作区升级检查：

- 检查工作区版本 / 检查 ai 目录是否需要升级
- 升级当前 ai 工作区 / 迁移到最新版 Skill
- 同步最新版目录结构 / 补齐新版目录
- 重建索引 / 检查索引是否完整
- 为什么查询慢 / 为什么新功能不能用 / 为什么找不到待办
- 当前 ai 工作区健康吗 / 工作区状态

## 8. 工作区健康文件

升级检查或迁移完成后，应维护 `ai/.workspace-health.md`，记录：
- 版本状态
- 能力状态（ok / missing / degraded）
- 索引状态（fresh / stale / empty / missing）
- 推荐动作
- 升级提醒控制

AI 检查"工作区健康吗"时优先读取本文件。

## 9. 迁移模式

工作区迁移支持以下模式：

| 模式 | 说明 | 风险 | 默认 |
|---|---|---|---|
| `diagnosis-only` | 只诊断不修改 | 无 | - |
| `structure-only` | 只创建缺失目录和空索引 | 低 | ✅ |
| `recent-7-days` | 创建目录 + 从最近 7 天重建索引 | 中 | ✅ 推荐搭配 |
| `current-month` | 从当前月数据重建索引 | 中 | - |
| `full-rebuild` | 全量扫描重建索引 | 高 | 需用户明确要求 |

**规则：**
1. 结构迁移和索引重建必须分离。
2. 默认推荐 `structure-only` + 可选 `recent-7-days`。
3. 索引重建必须询问范围，未获确认不得全量扫描。
4. 事实源改写必须再次确认。
