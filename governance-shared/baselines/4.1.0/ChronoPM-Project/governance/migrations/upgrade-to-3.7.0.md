# 升级到 3.7.0

> 从 3.6.0 升级到 3.7.0
> 发布日期：2026-08-21
> Schema 变更：workspace schema 0.11.0 → 0.12.0
> CR：CR-20260820-008（H）+ CR-20260821-001（I）+ CR-20260821-002（J）
> 施工依据：`governance-shared/upgrade-plan-v3.7.0.md` V0.5+P9（B 终审通过-可执行）
> 用户确认：QI-1=α；QI-2=分流+先归档后删+模块级 WP 骨架；QJ-1=仅威胁向；QJ-2=映射+启发式+P9 出口；QJ-3=短号 R-NNN/I-NNN

## 变更摘要

三 CR 同版并轨、目标独立闭环：

- **CR-H**：拆解增强（对账/重拆/parse-log/ledger 扩列/分片/REQ 编号/术语节流/零清重建）。
- **CR-I**：废弃 `context/entity-registry.md`；实体行落地 WP §3b；推导链迁 `project-context`。
- **CR-J**：风险/问题识别判定卡 + 登记册分表重构（≤7 列）+ 短号 + 仅高等级强制绑定。

## 新增 / 删除（Skill 包）

| 路径 | 操作 |
|---|---|
| `assets/templates/source-parse-log-template.md` | 新增 |
| `assets/templates/source-atoms-index-template.md` | 新增 |
| `source-split-skill/SKILL.md` + `references/` | 新增（清单性，非运行时加载） |
| `assets/templates/entity-registry-template.md` | 删除 |

模板数 37→38。回归用例 350→380（Module 54/55/56）。

## 存量（业务工作区，AI 出清单 + PM 确认；脚本不自动改数据）

### CR-H 零清重建（替代 3.6.0 一次性迁移）

保护：`requirement-register` / `contract-register` / `source-type-registry` / `change-log`；**已建 `sources/{编号}/` 不删**。

删（先归档 `ai/archive/v3.7.0-legacy-split-{date}/` 再删）：`{type}-source/`、平铺 `atoms/`、`canonical/`（子项目 3 处 + 集层 1 处）。

Step 1 盘点 → 2 归档 → 3 删除 → 4 重喂拆解 → 5 重链 REQ → 6 验证（D24）→ 7 归档清理（验证通过 + PM 确认才删快照）。

未完成零清：禁止新拆解/对账/RI 判定。

### CR-I entity-registry 分流

§2/§3 → project-context 项目级推导规则；§1 模块名核对模块表；§1 实体行 → WP §3b（无 WP 则按 registry 模块段落各建一个 WP 骨架再迁行；禁一实体一 WP、禁全项目一个 WP）。旧 T-xxx 标待校准。列漂移：状态→当前状态，评审→评审状态。先归档 `ai/archive/entity-registry-{date}.md` 再删原文件。验证通过后随 P9 清归档副本。

### CR-J 登记册

宽表行或已有条目块 → 索引+条目详情块。枚举：识别中→开放、已发生→转为问题、待处理→开放；紧急/高/中/低→P0–P3；极高→高。自由文本状态标待解析。短号续用；时间戳号保留。旧格式检测：15 列表头 / 缺时间线 / 旧枚举。过渡期至本项目迁移验证通过为止（D26 检出即报，不允许无限期共存）。备份只进 `ai/archive/`。

## P9 归档清理闭环

验证未通过不清理。通过 + PM 确认后删除 `ai/archive/v3.7.0-*` 与 `entity-registry-{date}.md`。脚本不自动删。

## 明确不做

- 业务工作区代清零/代迁
- 拆解能力真拆第二 Skill 包
- SRC-NNN 作互认键
- 机会型风险、邻近度
- AUTO 写待办
