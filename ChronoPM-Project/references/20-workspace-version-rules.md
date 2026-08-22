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
| `skillName` | 包名：`chrono-pm-project`（兼容识别旧值 `chrono-pm`） |
| `mode` | 工作区模式（本包仅 `single`） |
| `initializedAt` | 初始化时间 |
| `lastMigratedAt` | 最近一次迁移时间（null 表示从未迁移）|

**双层 `.skill-version.json`：**
- **项目级**（`ai/.skill-version.json`）管本项目 ai，读写以本文件为准。
- **集级**（联邦工作区根级，若存在）管整体挂载健康，由 ChronoPM-Portfolio 读取。
- 各自生效：**集级只读降级不蔓延进项目内正常单项目操作**。本包在项目 ai 内按项目级文件判断。
- `skillName`：`chrono-pm` 与 `chrono-pm-project` 视为同一 Project 包，兼容识别。

**版本兼容性判断规则：**

1. AI 读取 Skill 包中的 `VERSION` 文件获取当前 Skill 版本。
2. 对比当前 Skill 版本与工作区的 `skillVersion`。
3. 根据 `CHANGELOG.md` 中的 Upgrade Notes 判断是否需要迁移。
4. 按以下策略处理：

| 版本差异情况 | AI 行为 |
|---|---|
| 版本一致 | 正常处理 |
| Skill 版本更新但 schema 未变 | 按新规则处理，提示用户"当前规则版本为 x.x.x，工作区由 x.x.x 初始化，规则已升级但目录结构无需迁移" |
| **Skill 版本 < 工作区 `.skill-version.json`** | **反向校验**：立即提示「工作区由更高版本 Skill 创建，请下载不低于 {工作区版本} 的 Skill」并进入**只读降级**（可查询、禁止写入/升级，防止低版本规则破坏高版本结构） |
| schema 版本不同（Skill ≥ 工作区） | 提示用户需要迁移，输出迁移建议，不自行执行迁移 |
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
| 0.3.0+（仅旧工作区升级探测） | **不再**把 `resource-register.md` / `transfer-log.md` 当作必有事实源。若仍见这两文件或集层 `portfolio/resources/` 实体文件，按 3.8.0 行提示改读待办体系（不阻断单项目查询） |
| 0.4.0+ | `context/project-brief.md` 是否存在 |
| 0.5.0+ | `outputs/` 目录是否存在（v2.1.0+ 位置为 `ai/outputs/`，工作区根目录不再有 outputs/） |
| 0.7.0+ | 是否还在用 `YYYY/MM` 旧目录结构 |
| 0.8.0+ | `continuity/` 目录和保留文件（project-lineage/legacy-sources/import-log）是否存在（v2.1.0+ 已合并入 `context/`，见 2.1.0+ 行） |
| 1.9.0+ | 本项目 `context/pm-profile.md` 是否存在 |
| 2.0.0+ | 本项目 `todos/` 目录（每人每日待办文件 + 绑定文件 `_index.md`）是否存在；旧待办索引（personal/daily/weekly-todo-index、history-index）已废弃，存在时提示可清理 |
| 2.1.0+（v2.1.0 新增） | ① `outputs/` 已移入 `ai/outputs/`（工作区根目录只留 `ai/`）；② `continuity/` 已合并入 `context/`（carryover-register/import-log/legacy-sources/project-lineage 4 文件）；③ v1.x 遗留禁用路径（见 `06-file-rules.md` §12 禁用清单）不得存在文件；④ `governance/migrations/` 升级文件体系可用 |
| 3.4.0+ | **不要**把缺 `reports/timeline/` 当健康检查失败或 P0（懒建，不入 06 标准结构） |
| 3.5.0+ / schema 0.10.0 | `wps/` 与 `wps/_index.md` 应存在；缺则提示按 upgrade-to-3.5.0.md 建目录并做一次性抽取。计划仍内嵌 WP 详情 → 截止条件：首次周报/新建待办前必须抽取 |
| 3.6.0+ / schema 0.11.0 | `requirements/sources/` 与 `_index.md` 应存在。 |
| 3.7.0+ / schema 0.12.0 | ① 存量 `{type}-source/` / 平铺 atoms/canonical **零清门禁**：未完成零清前禁止新拆解/对账/RI 判定（upgrade-to-3.7.0.md）；已建 `sources/{编号}/` 不删。② 发现未迁 `context/entity-registry.md` → 门禁阻断并输出分流清单。③ 登记册旧 15 列/缺时间线 → D26 限期迁移 |
| 3.9.0+ / schema 0.14.0 | ① 有 `pending-changes.md` → 全文迁 `pm-decisions.md`，原件进 backup。② 缺需求索引不致命，触碰时按模板建。③ ops 日志懒建 |
| 3.8.0+ / schema 0.13.0 | ① 缺 `backup/` → **建空目录**（脚本只建空目录 + 升 schema，不改业务文件）。② 人员仍读 `resource-register` / `transfer-log` → 提示改读待办体系（最新合法 `_index` §1 花名册 + 个人 §0 / §0.5 / §0.6）。③ `v1-legacy` 等升级垃圾应由分类器建议搬出 archive 进 backup，本包不代搬 |

3b. 检查 `ai/templates/` 参考模板库完整性：对比工作区 `ai/templates/` 下的文件与 Skill 包 `assets/templates/` 目录中的模板清单（`ALL_TEMPLATE_FILES`），如有缺失模板，在健康报告的“缺失能力”表中列出并建议执行迁移补齐。同时检查 `ai/outputs/.templates/manifest-template.md` 是否存在。

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
| 2.0.0 | 待办查询体系 | todos/ 目录（待办文件+绑定文件） | 查询待办时会回退到全量扫描模式 |
| 1.1.0 | 历史导入快照 | snapshots 目录 | 无法回查导入的历史计划和偏差 |

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
6. **反向校验优先**：若 Skill 版本 < 工作区版本，跳过「建议升级工作区」，改为提示升级 Skill + 只读降级；集级只读降级不蔓延进本项目正常单项目操作。

## 3. 功能触发时检查（Feature-Triggered Check）

当用户触发某个需要特定目录/文件的能力，但该目录/文件不存在时，AI 不得直接退化为全量扫描，必须先提示工作区可能未升级：

**示例：用户问"我明天的待办是什么"，但 `todos/{date}/` 目录不存在**

AI 应输出：

```markdown
我准备按快速查询规则读取 PM 待办文件，但当前工作区缺少：

`ai/todos/`

这通常表示当前 `ai/` 目录还停留在旧版本结构。

当前建议：
1. 先执行工作区升级检查
2. 补齐 `todos/` 待办目录（待办文件 + 绑定文件 _index.md）
3. 可选将旧索引/看板中的在办事项迁入待办文件
4. 再回答"明天待办"

是否现在生成升级计划？

如果你暂时不升级，我也可以进入兼容模式，从日报和会议纪要中查询，但会更慢且可能不完整。
```

**规则：**
1. 不得在缺少待办目录/索引时直接创建临时脚本全量扫描。
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
- 快速查询：退化为逐文件扫描 todos/（较慢）
- 待办直读/倒排每日矩阵：不可用（依赖 todos/{date}/ 绑定文件与待办文件）
- PM 待办全景视图：仅列出 PM 个人任务

如需使用完整能力，请执行：
python scripts/migrate_workspace.py --project-root .
```

## 5. 兜底逻辑

当工作区缺少某些能力对应的目录/文件时，AI 不得报错中断，按以下兜底策略处理：

| 缺失能力 | 兜底策略 |
|---|---|
| 绑定文件 `_index.md` 缺失 | 退化为直接扫描 `todos/{date}/` 各人待办文件，但提示较慢 |
| snapshots/ 缺失 | 退化为读取日报索引，但提示无法对比计划偏差 |
| continuity/ 缺失 | v2.1.0 起连续性文件在 `context/`（carryover-register/import-log/legacy-sources/project-lineage）；缺失时跳过历史衔接功能，提示用户初始化 |
| project-brief.md 缺失 | 退化为读取 project-context.md |
| outputs/ 缺失 | 在 `ai/outputs/` 下自动创建（v2.1.0 起不再创建于工作区根目录） |
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

## 10. 归档 vs 备份（v3.8.0 拆开；原 archive 豁免并入）

**归档**（06 §9 活历史 + change-log 月归档 + parse-log/project-notes）：

1. 只读、**可按索引查**、不巡检分片字段、不改原文
2. 索引受控路由：先读 index，按指向读分片，禁止遍历 `archive/` 目录
3. 发现需更正的历史内容应在活跃事实源中登记更正记录，不改写归档原文
4. `v1-legacy` 等升级垃圾**不应**留在 archive；应由分类器建议搬入 `backup/`

**备份** `backup/`（升级垃圾与退役人员文件）：

1. **不读、不巡检、不改、不作源**
2. 用户显式单次解封或本次迁移步骤除外
3. `logs/migration-log.md` 标记「视为 backup」的根级目录（工作区根 `backup-*` / `*-pre-*upgrade*` 等）与 `backup/` **同效力**，不搬入 `ai/backup/`

巡检豁免：归档分片与 `backup/` 均不参与 `14-self-check-rules.md` 字段完整性巡检。活跃数据源禁令与 `06-file-rules.md` §1.7 / §12 联动。

## 11. 版本不一致检测与升级触发规则（v2.1.0 新增，MANDATORY）

**触发条件**：AI 启动 Skill 时，或 PM 指示"升级工作区"时。

**强制流程**：
1. 读取工作区 `.skill-version.json` 中的 `skillVersion`
2. 读取 Skill 包 `VERSION` 文件获取目标版本
3. 若不一致 → 读取 `governance/migrations/README.md` 获取版本链
4. 确定从当前版本到目标版本需要经过哪些升级文件
5. 逐个读取并执行每个 `upgrade-to-{version}.md`
6. 每级执行完毕后更新 `.skill-version.json` 为该级版本
7. 全部执行完毕后验证工作区完整性（按升级文件"验证检查"段逐项确认）

**禁止**：跳过中间版本直接升级（如从 1.0.0 直接跳到 2.0.0）。本规则与 §1 "AI 不得自行执行迁移"的关系：升级文件的具体执行仍需 PM 确认后启动，本节定义的是确认后的执行路径（逐级按升级文件执行，而非一把梭）。

## 12. 禁用路径版本层拦截（v2.1.0 新增，需求十二）

工作区版本 ≥ 2.1.0 时，AI 必须对 `06-file-rules.md` §12 禁用清单执行版本层拦截：

1. 检测到禁用路径存在文件 → 阻断相关操作，提示"迁移未完成"并按 `governance/migrations/upgrade-to-2.1.0.md` 补做迁移（报告类迁移走 §7.3.2b 检测→迁移→验证→删除）
2. 检测到 AI 试图引用禁用路径（读/写/创建）→ 阻断并输出警告，指向 v2 替代入口
3. 拦截与 05 号查询路由排除（05 号 §2.5 查询性能规则第 5 条）、06 号禁止读写构成三层禁令闭环
