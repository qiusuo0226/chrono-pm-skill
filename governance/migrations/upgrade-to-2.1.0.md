# 升级到 2.1.0

> 从 2.0.0 升级到 2.1.0
> 发布日期：2026-08-18
> Schema 变更：无（workspace schema 保持 0.8.0，skill schemaVersion 保持 0.6.0）
> CR 编号：—（未走独立 CR，参照 2.0.0 先例；升级方案 V0.42 定稿经双 Agent 十三轮审核放行，13 个需求，实质已固化于本文件 + baselines/2.1.0/ + CHANGELOG 2.1.0 段）

## 变更摘要

个人待办体系与工作区路径整合(Minor/capability_change)：双 Agent 十三轮审核收敛（V0.1→V0.42，13 个需求）。新增 22 号待办结转规则（结转 3 时机 + Step 0 HARD BLOCK + 编号硬约束 + E1~E5 + 状态机）；配套机制承载于既有规则：§0 六字段录入规范（岗位/姓名/联系方式/负责模块/进组日期/离组日期，模板 §0 + 18 号引导）+ T+1 沿用与冲突仲裁（以 resource-register 为准，00 号 §4d + 09 号 §1.3）+ 进度↔状态双轨仲裁（01 号 D-26）；删除 project-daily-template.md（项目日报按需生成无独立模板，模板 36→35）；18 号向导 Step 5 新增 §0 引导；04 号 DF-002 PM 确认门禁（关闭需编号+佐证+关联影响+PM 确认，日报/周报后批量罗列候选）；09 号人员信息双层数据流微调 + 可用性/排期聚合=动态视图硬约束（实时计算不落盘，禁止写入 shared-resource-index）；11/12/13/20 号 outputs/→ai/outputs/ 全链路更新；13 号 continuity/→context/ 路径迁移 + carryover-register 保留澄清。路径整合：continuity/*→context/（4 文件）、工作区根 outputs/→ai/outputs/（D-8/D-9，migrate_v210_paths）；历史报告迁移 §7.3.2b（个人日报内容级入 todos §3 工作日志段 + 项目日报/周报文件级规范化，检测→迁移→验证→删除，空源登记跳过，migrate_v210_reports）；VERSION_CAPABILITIES 补齐 29 个历史版本缺口（0.1.0~2.1.0 全 50 版本）。workspace schema 保持 0.8.0，skill schemaVersion 保持 0.6.0。

## 新增目录

- `outputs/`（位于 `ai/` 内，即 `ai/outputs/`）— AI 生成物输出目录，v2.1.0 起从工作区根移入 ai/ 内（D-8）

## 新增文件

- 无预建文件（`ai/outputs/index.md` 与 `.templates/manifest-template.md` 由 init/migrate 脚本按需补齐）

## 删除文件/目录

- `continuity/`（目录本身）— 4 个文件全部搬入 `context/` 后删除空目录（D-9）
- 工作区根 `outputs/`（目录本身）— 内容全部搬入 `ai/outputs/` 后删除空目录（D-8）
- `projects/*/reports/daily/personal/`（旧结构文件）— 内容级迁移进待办 §3 工作日志段并验证后删除，不进 archive（§7.3.2b）
- `projects/*/reports/daily/project/` 与 `projects/*/reports/weekly/` 下的 **v1.x 旧结构文件**（非 YYYYMM 单级 / 非 YYYY/YYYY-Wxx.md 标准结构）— 规范化迁移并验证后删除；目录本身为 v2 活跃路径，保留（V0.35 更正）

## 规则变更

- `references/22-carried-over-rules.md`：**新建**。待办结转规则：结转触发时机（3 时机）、Step 0 执行流程（HARD BLOCK，创建待办前 MANDATORY 读取前一天 _index.md 全员扫描）、编号硬约束与场景区分、E1~E5 错误处理、状态机与 AI 自检清单。配套机制承载于既有规则：§0 六字段录入规范（岗位/姓名/联系方式/负责模块/进组日期/离组日期，personal-daily-todo-template §0 + 18 号 Step 5 引导）、T+1 沿用与冲突仲裁（00 号 §4d + 09 号 §1.3）、进度↔状态双轨仲裁（01 号 D-26）
- `references/18-init-wizard-rules.md`：Step 5 新增 v2.1.0 §0 引导（向导不建待办文件，首次出现时引导填写 §0 + T+1 沿用 + 冲突以 register 为准）
- `references/04-risk-issue-rules.md`：§9.1 新增 DF-002 PM 确认门禁（关闭=编号+佐证+关联影响+PM 确认四要素；日报/周报流程后主动批量罗列可关闭候选）
- `references/09-portfolio-rules.md`：§1.3 人员信息双层数据流微调（register 为唯一事实源，shared-resource-index 为指针索引）；§5.4 **可用性/排期聚合=动态视图硬约束**（实时计算输出，禁止写入 shared-resource-index 或任何索引落盘）
- `references/11-output-artifact-rules.md` / `12-excel-generation-rules.md` / `20-workspace-version-rules.md`：outputs/ → ai/outputs/ 全链路路径更新
- `references/13-continuity-rules.md`：continuity/ → context/ 路径迁移；carryover-register.md 保留并随并入 context/（承载跨阶段结转，与 22 号日常待办结转互不干涉）
- `references/00/01/05/06/21 号`：联动微调（PM 偏好、日报流程、查询路由、路径书写、§0 引用等，详见升级方案 §6 清单）

## 模板变更

- `assets/templates/personal-daily-todo-template.md`：核心执行表新增"进度"列（7→8 列，D-24 硬上限）+ 新增 §2 日报存档段（D-25 两步流程）
- `assets/templates/pm-profile-template.md`：DF-001~DF-006 内置默认偏好预填
- `assets/templates/daily-todo-binding-template.md`：`_index.md` 新增 §2 结转追溯标记 + 参与人员表"来源（新建/结转）"列
- `assets/templates/portfolio-weekly-template.md`：项目集周报联动微调
- `assets/templates/project-daily-template.md`：**删除**。v1 项目日报模板（§7.3.2 删除清单/A-9，S-5 确认删除安全）；项目日报按需生成、无独立模板（01 号规则 §2.2）；config.py ALL_TEMPLATE_FILES 同步移除，模板总数 36→35

## 工作流变更

- 日报处理流程（01 号）：两步流程——日报原文先逐字存档到待办文件 §2 日报存档段，再映射加工进 §3 工作日志段与待办字段（D-25）
- 待办结转 Step 0：创建待办前 MANDATORY 读取前一天 `_index.md` 全员扫描（22 号承载）
- 进度↔状态双轨仲裁（D-26）：状态列为唯一权威源；状态=已完成 ⇒ 进度必须 100%（自动修正）；进度=100% 但状态≠已完成 ⇒ 不自动提升状态，仅输出建议（终态需 PM 确认）

## 迁移执行步骤（AI + 脚本分工，严格执行顺序）

### 步骤 1：路径整合（脚本执行）

```
python scripts/migrate_workspace.py --project-root <工作区根> --dry-run   # 先检测
python scripts/migrate_workspace.py --project-root <工作区根>             # 确认后执行
```

脚本自动完成（migrate_v210_paths，不覆盖合并）：
1. `continuity/*.md` → `context/*.md`（project-lineage/legacy-sources/carryover-register/import-log 共 4 文件；同名已存在则保留源文件并提示人工合并）
2. 工作区根 `outputs/*` → `ai/outputs/*`
3. 搬空后删除空目录

> PM 确认要求（§7.1）：执行前 AI 向 PM 罗列将被搬移的文件清单，确认后执行。

### 步骤 2：历史报告迁移（§7.3.2b，检测 → 迁移 → 验证 → 删除）

**2a. 检测**（脚本 dry-run 输出三类旧路径文件数与清单）：

| 数据类型 | v1.x 旧路径 | 迁移策略 | 迁移目标 |
|---|---|---|---|
| 个人日报 | `projects/*/reports/daily/personal/` | **内容级迁移**（AI 执行，按月分批） | 对应日期 `todos/{date}/{owner}.md` §3 工作日志段 |
| 项目日报 | `projects/*/reports/daily/project/` | **文件级规范化**（脚本执行） | `reports/daily/project/YYYYMM/YYYY-MM-DD-[project]-项目日报.md` |
| 周报 | `projects/*/reports/weekly/` | **文件级规范化**（脚本执行） | `reports/weekly/YYYY/YYYY-Wxx.md` |

**空源处理**：源目录不存在或无文件 → 该迁移项登记"无数据，跳过"（context/import-log.md），不阻断其余迁移项。**禁止因"方案中为假设举例"而跳过检测或验证——源有无数据都按实际检测结果处理并登记。**

**2b. 个人日报内容级迁移（AI 执行，无窗口限制，按月分批）**：
1. 按月份从早到晚分批，每批输出迁移条数与覆盖日期清单，PM 确认进度
2. 解析个人日报内容，**逐字**合并进对应日期待办文件 `todos/{date}/{owner}.md` §3 工作日志段（禁止摘要化/加工压缩）
3. 对应日期待办文件不存在时，基于 `personal-daily-todo-template.md` 创建（仅含 §0 人员信息段 + §3 工作日志段，待办清单段留空），frontmatter 增加 `migration-source: v1-personal-daily` + 标题标注"迁移归档文件（无活跃待办）"
4. 迁移记录标注 `[迁移自 v1.x 个人日报: {原文件路径}]`
5. 工作日志已存在时追加合并，不覆盖已有内容
6. 当月迁移验证通过后，分批删除对应源文件

**2c. 项目日报/周报文件级迁移（脚本执行）**：由 `migrate_v210_reports` 完成搬移与命名规范化（日期解析失败的文件保留原名并提示人工核对）。

**2d. 验证（MANDATORY，验证结果登记 context/import-log.md）**：
- 文件级迁移（项目日报/周报）：文件数核对（迁移目标文件数 = 源文件数）
- 内容级迁移（个人日报）：（日期, 人员）覆盖核对（每个源日报的日期+人员组合在目标 §3 工作日志段均有落点）
- 抽样核验：每类随机抽 3 个文件核验内容完整性
- 空源情形验证口径：登记"无数据，跳过"日志条数 = 空源迁移项数

**2e. 删除旧结构**：验证通过后，三类旧路径下的 v1.x 旧结构文件全部物理删除，**不进 archive、不留任何历史缓存**；报告类数据不进入 `archive/v1-legacy/`。验证失败：保留旧结构，输出差异清单，人工介入后重试。

### 步骤 3：存量待办文件进度值提取（需求十三）

扫描存量 `todos/{date}/{owner}.md` 核心执行表备注列中的百分比值（如"10%"），迁移到新增的"进度"列；无法确定归属的保留备注原样并提示 PM。

### 步骤 4：版本信息与收尾

1. 更新 `.skill-version.json` → `skillVersion: 2.1.0`（脚本自动）
2. `logs/migration-log.md` 追加迁移记录（脚本自动）
3. 生成/更新 `.workspace-health.md`（脚本自动）
4. 遗留路径引用禁令生效：≥2.1.0 工作区禁止读写 v1.x 遗留路径（06 号禁用清单 + 05 号查询排除 + 20 号版本拦截）；检测到禁用路径存在文件 → 触发迁移补做而非就地维护

## 验证检查

- [ ] `context/` 下 4 文件齐备（project-lineage/legacy-sources/carryover-register/import-log），`continuity/` 已不存在
- [ ] `ai/outputs/` 存在且含 index.md；工作区根 `outputs/` 已不存在
- [ ] 个人日报：源目录已删除，或已登记"无数据，跳过"；（日期, 人员）覆盖核对通过 + 抽样 3 个核验
- [ ] 项目日报/周报：目标结构（YYYYMM/、YYYY/YYYY-Wxx.md）文件数 = 源文件数 + 抽样 3 个核验；旧结构文件已删除
- [ ] 验证结果已登记 `context/import-log.md`（含空源跳过记录）
- [ ] 存量待办文件备注列百分比已提取到"进度"列（或标注无法归属）
- [ ] `.skill-version.json` → 2.1.0；`.workspace-health.md` 状态 healthy
- [ ] 工作区不存在 v1.x 禁用路径文件（06 号禁用清单全项）
