# 升级到 3.1.0

> 从 3.0.0 升级到 3.1.0
> 发布日期：2026-08-20
> Schema 变更：无（workspace schema 保持 0.9.0；skill schemaVersion 保持 0.7.0）
> CR 编号：CR-20260820-001
> 施工清单来源：`governance/upgrade-plan-v3.1.0.md` V0.17 **§21 AP-4**（禁止从方案 §7 整表抄施工）
> 本次执行范围：**只升级 Skill 包**（CR-A）。不处理业务工作区；不执行 CR-B～G。

## 变更摘要

路径残留纠偏 + 日报查询/更新路由补全 + 月报残留清理（Minor/fix）。个人日报内容默认落 `todos/{date}/{owner}.md`（§2+§3）；项目日报为按需生成的存根（可能不存在）。R1-R18 纠偏（**R9 除外**——config.py 日报索引 `Task Sync` 表头并入 CR-D）。存量零迁移。

## 新增目录

- 无

## 新增文件

- `governance/migrations/upgrade-to-3.1.0.md`（本文件）
- `governance/change-requests/CR-20260820-001.md`
- `governance/impact-analysis/IA-20260820-001.md`
- `governance/regression-reports/rr-20260820-3.1.0.md`
- `governance/baselines/3.1.0/`（Skill 包基线快照）

## 删除文件/目录

- 无（init 不再预建 `reports/monthly/`；存量工作区若已有该目录不强制删除）
- 活文档 `governance/upgrade-plan-v3.1.0.md` 待发布验证通过后按 R10 删除（本步不删）

## 规则变更

- `references/05-query-rules.md`：查询路由表新增「个人日报/某人某天汇报/昨天日报风险点问题→todos/{date}/{owner}.md §2+§3」，默认先读此路径、禁止先探测 `reports/daily/`；「项目日报查询」行补优先级（内容查询先 todos；仅明确要项目日报文件才读 `reports/daily/project/`；目录不存在=未生成，提示可按需生成，不报错）。
- `references/10-update-trigger-rules.md`：§5「本项目日报」拆两行（个人工作汇报→todos；项目日报存根→reports/daily/project/YYYYMM/）；删除「月报草稿生成」；§8.1「生成报告（周报/月报/状态报告）」去掉月报。
- `SKILL.md`：front matter 3.1.0；§3 `reports/` 注释改为「项目日报按需生成（存根，可能不存在）+周报；个人日报在 todos」；§5.2/5.3 补查询落点。禁止「缓存」措辞。
- `references/20-workspace-version-rules.md`：兼容模式「退化为读旧体系任务看板（tasks/board.md）」改为「退化为逐文件扫描 todos/（较慢）」。
- `references/13-continuity-rules.md`：纪要行动项路由 `tasks/`→`todos/`。
- `references/01-daily-report-rules.md`：归档读 `tasks/change-log.md`→`requirements/change-log.md`。不改 §3.1/§4.1/§4.2（属 CR-D）。
- `references/06-file-rules.md`：删除标准结构 `reports/monthly/` 路径；低风险更新「周报/月报草稿生成」改为「周报草稿生成」。§2.4 阈值拆分例外保留（保护清单）。
- `references/19-info-completeness-rules.md`：「生成日报、周报、月报」改为「生成日报、周报」。

## 模板变更

- `assets/templates/project-brief-template.md`：§7 文件路由速查整表重写为 v3 单项目路径；日报拆两行（个人→todos，项目日报存根→reports/daily/project/）；删除 `projects/{子项目}/` 与 `portfolio/risks|plans|meetings/` 指针。
- `assets/templates/outputs-index-template.md`：Related AI File 示例改为 `reports/weekly/YYYY/... 或 pending`。

## 工作流变更

- 日报类查询：默认先读 `todos/{date}/*.md` §2+§3，禁止先探测 `reports/daily/`。
- 日报类录入：「某某今日工作汇报」落 todos 两步流程，禁落 `reports/`。
- 项目日报文件：仅用户明确要生成文档时才读写 `reports/daily/project/`；目录不存在不报错。
- init：不再预建 `reports/monthly/`；新工作区 README/结构树无月报。

## 脚本变更

- `scripts/chronopm_init/config.py`：删除 `reports/monthly` 预建与月报索引模板。**不改**日报索引表头 `Task Sync`（R9 ∈ CR-D）。
- `scripts/chronopm_init/file_registry.py`：日报归档映射拆两行（禁整行改 todos）；结构树删 monthly、daily 加存根标注；生成工作区 README 文案删「月报」。
- `scripts/migrate_workspace.py`：`VERSION_CAPABILITIES` 增 3.1.0 条目（schema 仍 0.9.0，无新目录）。SCHEMA_010/020_DIRS 中的 `reports/monthly` **禁止改**（历史探测保护）。
- `governance/scripts/audit_release.py`：Case ID 正则兼容 `QR-DR-001` 类前缀（对齐既有 V3- 扩展先例）。

## 验证检查

- [ ] 05 号含个人日报正向路由，且「昨天日报风险点」不得指向 `reports/daily/` 为首跳
- [ ] 10 号日报拆两行；无「月报草稿生成」
- [ ] SKILL.md 无「缓存」；`reports/` 注释声明存根可能不存在
- [ ] file_registry L237 为两行（个人→todos，项目日报→reports/daily/project/），不是整行改 todos
- [ ] config.py 无 `reports/monthly` 预建；仍含 `Task Sync` 表头（R9 未动）
- [ ] 01 号无 `tasks/change-log.md`；20 号无 `tasks/board.md` 兜底；13 号纪要无 `tasks/`
- [ ] 06 号无 `reports/monthly/` 标准结构行
- [ ] project-brief §7 无 `projects/{子项目}/` 与 `portfolio/` 存储路径
- [ ] OA-005 引导切 Portfolio；QR-DR-001~003 在册；合计 302
- [ ] 版本六触点 = 3.1.0；workspace schema 仍 0.9.0
- [ ] 伴生包规则未改（仅版本锁步）；04 号 L35 仍为 CR-D 范围
- [ ] `python governance/scripts/audit_release.py` 13/13 PASS
- [ ] 存量若残留禁用路径：按 06 号 §12.5 既有机制触发迁移补做（本升级不跑业务工作区 migrate）

## 存量工作区

**零文件迁移**。规则重装载即生效。不跑 `migrate_workspace.py` 于业务工作区。`.skill-version.json` 的 skillVersion 在日后工作区升级时由 migrate 升为 3.1.0（仅元数据）。

## 明确不做（CR-B～G / R9）

- CR-B：DF-017/018、加载场景标签
- CR-C：关联待办、TD Ref、人员缩写注册表
- CR-D：报告存根范式统一、时间线报、R9 Task Sync、01 号 §4.1/§4.2/§3.1、11 号/伴生包 04 号缓存残留
- CR-E：wps/ 目录与 schema 0.10.0
- CR-F：RI 拆解产物目录化
- CR-G：开发仓三目录重组（3.1.1 PATCH，CR-A 后单独提交）
- 不把全链通「实名/实人认证」截图塞进本 CR
