# 升级到 3.9.0

> 从 3.8.0 升级到 3.9.0  
> 发布日期：2026-08-22  
> Schema 变更：workspace schema **0.13.0 → 0.14.0**  
> CR：CR-20260822-002  
> 施工依据：CR-20260822-002 + 本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.8.0 → 3.9.0。  
> 用户拍板：Q-7/Q-8/P-N3/T-A6/T-A7/T-N1/T-N4/Q-1；Q-9 其余按建议。

## 变更摘要

过程日志（7 列、按日、flush 每步）；同人日报唯一 inbox + claim，合并恒可执行；需求只绑工作包、待办只绑工作包、计划只绑工作包；WP 待确认；PM 决策文件分块；关联待办处理方式；source-split 能力目录无 SKILL.md 完整进包；对外给文件不给章节号；已发布 AP 删除门=记录闭合。

## 施工禁区

- 禁止写入/迁移/删除：`C:\Users\qiusuo\Downloads\市监重构项目管理`
- 禁止把验证仓路径写进脚本默认参数
- 禁止把 BLUEPRINT / tests / 16 号 / SKILL_MODULE_MAP.md 打回发行包
- 禁止把 source-split-skill/SKILL.md 打进包（该文件应删除）
- 禁止漏打 source-split 规则与四模板
- 禁止引入 pytest 作为发布门槛
- 禁止新建共享 `_lease.md`
- 禁止 migrate 再「只补不覆盖」现行模板
- ops 日志仍懒建、不预建

---

## A. 技能包施工

### A1. 治理与记录

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260822-002.md` | 本 CR |
| A1.2 | 本文件 | 本施工清单 |
| A1.3 | `governance-shared/impact-analysis/IA-20260822-002.md` | 本 IA |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.9.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.9.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.9.0.md` | 指针文件，指向主包 |
| A1.7 | `references/16-skill-governance-rules.md` | §19：先 CR/upgrade-to 接思路 → 检查提醒 → 最后删 AP；准许后第一步写 CR |
| A1.8 | `governance-shared/review-checklists/release-checklist.md` | D5：记录闭合 + 检查清单后删 AP |
| A1.9 | `governance-shared/scripts/audit_release.py` | 第 14 条：有基线仍留该版 AP → FAIL；高于当前 VERSION 且无基线的在研 AP 至多 1。模拟 pack：不得含 tests/BLUEPRINT/16/MODULE_MAP；必须含 source-split 规则+四模板；除包根外禁止 SKILL.md；有 references 无 SKILL.md 仅当主 SKILL 未引用才 FAIL。ops/parse-log ≤7 列 |

### A2. 运行时规则

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | 对外词典（处理类列文件禁章节号）。WF-2/3 写 inbox 再 C'。WF-7 落库只写 WP+计划，废除按排期灌待办与「每个排期项必须已落待办」。§4b 计划变更只同步 WP 时间盒。WF-8：删除需求拆解入口；增加已规划 WP 拆待办；入口含风险跟踪待办。WP 状态加 `待确认`。无需求禁止建包。WF-Linked：有处理方式 AUTO，无则问一次并写入记录。pending-changes 全部改为 pm-decisions；横幅「有 N 件事等你裁定」。合并链不建待确认。工人禁写 pm-decisions；协调者按块追加、写前查重、禁止互盖 |
| A2.2 | `01-daily-report-rules.md` | inbox+C'；§1.5 待归属够正式则自动建待办；§1.4 行动即确认才建人；责任人入册。缺负责人进决策文件。N-37 维持。合并链不建 pending。对外禁章节号 |
| A2.3 | `02-meeting-rules.md` | 行动项 inbox→C'。缺负责人写入决策文件块 6。废除「未排期待办区块」指针 |
| A2.4 | `04-risk-issue-rules.md` | 责任人未入册则入册；无名下跟踪待办则建（SUGGEST 升本轮必做）。写入走 WF-8+inbox。禁止 04 直写 `{owner}.md`。禁止另为 PM 建跟进条。外部方不入册 |
| A2.5 | `05-query-rules.md` | 过程日志先 ops-index；不读 inbox；横幅读 pm-decisions；计划进度只聚合 WP。发现非空 inbox 本轮 AUTO 跑 C' |
| A2.6 | `06-file-rules.md` | ops 按日/300 行拆 -p2，跨月归档；inbox/claim/runs 生命周期与归零；§3 排除 inbox；模板权威=Skill 包；需求索引+分片；pm-decisions 归档；WP 索引含待确认 |
| A2.7 | `07-requirement-rules.md` | 拆解树改为需求→工作包。删除关联任务/拆成待办。确认状态独立（未确认=做不做/效果/方案）。来源强制文件+章节+页。一需求多 WP。无需求禁止建 WP。抽出拆文件节为指针（留守 RI 级联与 Notes） |
| A2.8 | `08-change-control-rules.md` | 变更批准走需求/WP，禁止跳过 WP 灌待办 |
| A2.9 | `10-update-trigger-rules.md` | 过程日志触发词；倒排写 WP+计划不灌待办；缺负责人→决策文件。倒排信号改指向 |
| A2.10 | `14-self-check-rules.md` | 查重/一一对应（仅块 8↔Change Log）/D11/7·14 天催办改绑 pm-decisions。D21/D22 写入对应块。收尾 inbox 空。D3 对齐 N-37 |
| A2.11 | `19-info-completeness-rules.md` | 缺口写入决策文件；7/14 天催办盯开放行；残留稿 AUTO 跑 C'；无模板类型；headings 契约 |
| A2.12 | `21-pm-profile-rules.md` | DF-017：处理类默认打印改动文件，禁止章节号。DF-005 范围=全部对外。不复述词典 |
| A2.13 | `22-carried-over-rules.md` | 空闲登记 pm-decisions 块 8（人员状态提醒） |
| A2.14 | `QODER_RULES.md` | 处理类禁止章节号；默认列出改动文件 |
| A2.15 | `skill-contract.md` | #5 登记 pm-decisions；目录含需求索引与决策文件；schema 0.14.0 |

### A3. 能力目录 source-split

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `source-split-skill/SKILL.md` | **删除** |
| A3.2 | `source-split-skill/CAPABILITY.md` | 新增：定位、仅拆文件时加载、禁止命名 SKILL.md |
| A3.3 | `source-split-skill/references/split-rules.md` | 07 抽出的拆文件正文（§8.6/8.9.5/8.11.1-2/8.12/8.13/8.11.4/8.14）；工人只写 part |
| A3.4 | `source-split-skill/assets/templates/` | 迁入 source-doc-meta / source-index / source-parse-log / source-atoms-index |
| A3.5 | `source-parse-log-template.md` | 8 列压成 7 列（迁入后改） |
| A3.6 | `source-split-skill/references/capability-boundary.md` | 模板表改新路径 |
| A3.7 | `SKILL.md` | 「源文档拆解」加载 `source-split-skill/references/split-rules.md`；日报不加载 |

### A4. 模板

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | `ops-log-template.md` | 新增表 A/B 七列 |
| A4.2 | `ops-log-index-template.md` | 新增月份指针 ≤7 列 |
| A4.3 | `requirement-register-template.md` | 删关联任务；确认状态+三项缺口；工作包可多编号；来源=文件+章节+页 |
| A4.4 | `requirement-index-template.md` | 新增检索 ≤7 列 |
| A4.5 | `wp-template.md` / `wp-index-template.md` | 头状态含待确认；关联需求只留编号 |
| A4.6 | `plan-template.md` | 禁止待办行；排期变更不灌 todos |
| A4.7 | `personal-daily-todo-template.md` | 新增关联处理记录表 |
| A4.8 | `pending-changes-index-template.md` | **删除** |
| A4.9 | `pm-decisions-template.md` | 新增八块开放项 + 决策记录，列 ≤7 |
| A4.10 | 现行模板中 pending-changes 路径 | 一律改 pm-decisions（历史 CHANGELOG 不改） |

### A5. 脚本

| # | 文件 | 动作（写死） |
|---|---|---|
| A5.1 | `chronopm_init/config.py` | 删 pending-changes-index；加 pm-decisions、requirement-index；四份 source-* 从能力目录拷贝；registry 仍在 Project templates。不预建 pm-decisions 实例 |
| A5.2 | `migrate_workspace.py` | `sync_templates` **覆盖同步**现行模板。pending-changes 与 portfolio/pending-changes（若存在）全文迁 pm-decisions，原件 backup。schema 0.14.0。source-index 模板根改能力目录 |
| A5.3 | `pack.ps1` / `pack.py` | 删 source-split-skill/SKILL.md 排除项；stdout 打印有意排除（tests/BLUEPRINT/16/MODULE_MAP）；不把 source-split 列入 excludeDirs |
| A5.4 | `tools/pack-skill/SKILL.md` | 缺 tests/BLUEPRINT/16/MODULE_MAP 不是 bug；source-split 应在包内且无嵌套 SKILL.md |

### A6. 入口与 Portfolio

| # | 文件 | 动作（写死） |
|---|---|---|
| A6.1 | Project `SKILL.md` | 结构树 pm-decisions、logs/ops；拆解路由；schema 0.14.0；底线：需求不写进工作包、计划不列待办、pending 改决策文件 |
| A6.2 | Portfolio `SKILL.md` / `02-aggregation-query-rules.md` | 读成员 ops-index；不读 inbox；未确认终态读成员 pm-decisions 块 8 |
| A6.3 | Portfolio `01-readonly-boundary-rules.md` | 禁写成员 pm-decisions；禁写清单 pending→pm-decisions |
| A6.4 | `suggested-update-list-template.md` | pending-changes → pm-decisions |
| A6.5 | Portfolio `04-portfolio-report-rules.md` | 集周报不把过程日志当进度事实 |

### A7. 模块图与 README

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | `ChronoPM-Project/SKILL_MODULE_MAP.md` | G0–G15 共 16 张 Mermaid 图，只要图+一行标题；禁止版本号与苍白解释 |
| A7.2 | 根 `README.md` / `README.en.md` | 「三个约定」后加可点链接；版本 3.9.0、schema 0.14.0、回归 443、模板 35 |

### A8. 测试

| # | 动作（写死） |
|---|---|
| A8.1 | 新增 OL-001～005、SH-001～009、MP-001～010、RQ-001～004、WP-001～005、PD-001～004、LK-001～002、PL-001～003、PL-004～005、PK-001～002、CL-005～006、SS-001～002、TM-001～003 |
| A8.2 | 修 DR-006、BS-021 为 N-37（明日计划只进当天原文） |
| A8.3 | 修 TD-002：无处理方式才问；有则 AUTO |
| A8.4 | PC-001 扩大禁章节号 |
| A8.5 | 合计 390→443（265/178） |

### A9. 版本触点

| # | 文件 | 动作（写死） |
|---|---|---|
| A9.1 | `_version.py` | SKILL_VERSION=3.9.0；WORKSPACE_SCHEMA_VERSION=0.14.0 |
| A9.2 | 跑 `sync_version.py` | 同步 VERSION / SKILL.md / skill.json |
| A9.3 | skill.json | schemaHistory 新增 0.13→0.14；回归数；**不改** L74/L245 历史条 |
| A9.4 | CHANGELOG 双包 | 3.9.0 段 |
| A9.5 | BLUEPRINT | 3.9.0 行；DEBT-02：机器不变量由 audit 覆盖 |
| A9.6 | `baselines/3.9.0/` | 双子树全量快照 |
| A9.7 | 发行包 | 打到 `C:\Users\qiusuo\Downloads\` |

---

## B. 业务工作区

脚本 migrate：覆盖同步模板；迁 pending；升 schema。**本发布不代做市监仓。**

---

## C. 验证检查

- [ ] `_version.py` 3.9.0 / 0.14.0
- [ ] audit 退出码 0
- [ ] pack dry-run 有意排除；zip 有 source-split 无嵌套 SKILL.md
- [ ] parse-log 与 ops 模板 ≤7 列
- [ ] 未改验证仓
- [ ] upgrade-to-3.8.0 无 upgrade-plan 路径
- [ ] 回归 443
- [ ] README 中英文有模块图链接
- [ ] 3.9.0 AP 在基线拍完、检查清单勾完后删除

## D. 发布

每完成一个节点：annotated tag（中文说明）推 origin（Gitee）与 github。

完整升级后：打 `v3.9.0`，发布包到 Downloads。
