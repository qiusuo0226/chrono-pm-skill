# 升级到 3.10.0

> 从 3.9.0 升级到 3.10.0  
> 发布日期：2026-08-23  
> Schema 变更：**不升**，workspace schema 保持 **0.14.0**  
> CR：CR-20260823-001  
> 施工依据：CR-20260823-001 + 本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.9.0 → 3.10.0。  
> 用户拍板：Q1–Q11。C4-1（无人打开的日子可以没有目录）随准许施工认可。

## 变更摘要

对话日志改成每条用户消息一行（摘要/动作/文件/出处）；项目集真正写 `portfolio/logs/`，查成员日志按管理路径推导；投喂成本写入个人待办能耗段（缺节插入、人+日去重、异常列）；当天读或写待办则除已出组外全员建档；查询待办必须给 TD 编号；待办结束超出工作包结束须 ASK。

## 施工禁区

- 禁止写入/迁移/删除：`C:\Users\qiusuo\Downloads\市监重构项目管理`
- 禁止升 schema、禁止新建 `todos/archive/` 或 `*-energy.md`
- 禁止写死公司列名 / 7.5 / 迭代名 / 金额列
- 禁止无确认改业务待办（残缺日补齐与越界扫描只出清单）
- 禁止把对话日志当进度事实源
- 禁止预建 ops / 集层日志实例
- Portfolio 两份新日志模板**不进** Project `ALL_TEMPLATE_FILES`

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260823-001.md` | 本 CR |
| A1.2 | 本文件 | 本施工清单 |
| A1.3 | `governance-shared/impact-analysis/IA-20260823-001.md` | 本 IA |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.10.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.10.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.10.0.md` | 指针文件，指向主包 |

### A2. 运行时规则（节点2）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | CQ-4：1/2/3 只用于裁定选项，查询待办必须 TD。作废 L667「无待办不建空文件」。改写 L179：读最新已存在文件（当天应建档则当天已有）。WF-8 落库验证加：硬判定待办结束>WP 结束则 ASK A 拉长 WP / B 压缩待办 / C 挂起（pm-decisions 块 8，查重键=TD）；开始提前仅轻提示；选包 ASK 与越界能算则同一轮问完。对外不说章节号 |
| A2.2 | `01-daily-report-rules.md` | 作废 N-44 B「只追加最新文件/禁止回写历史日」。改为：有该日文件写该日能耗段；缺节插入；人+日已有值不覆盖、异常=重复待裁定、问 PM；累计不含重复待裁定；日表 5 列含「异常」；分次仍 5 列；禁止与 §1.2 互推。改写 L100：人员流入后若当日读/写 todos 则建当天个人文件（§1 可空） |
| A2.3 | `05-query-rules.md` | 待办清单第 7 条：每行必须 TD 编号（缩写取当天 `_index` §6 现行缩写），禁止 1/2/3 代替。改写 L339 身份/流转路由：应建档者读个人 §0/§0.5；已出组或不在应建档才只读花名册；禁止仅为查询给已出组建档。先读全行再改，勿按简写找错行 |
| A2.4 | `06-file-rules.md` | §2.8：表 A 改对话列；有用户消息就写；禁止全未知行；用量宿主给了才写否则「—」。旧日文件冻结，当天续记用同日 p2 新列。能耗补录回写已有历史日文件=受控例外（登记 pm-decisions + 存根影响）。禁止 `*-energy-*.md`。改写 L87：应建档人员进出组写当天 §0.5；已出组只改花名册 |
| A2.5 | `10-update-trigger-rules.md` | Level1 补整理/补全/回填/记录一下；同一句又像分析又像记录→按入库。Level2 补电子表格/工时表；拆完禁止沉默，必须 ASK 是否同步个人待办成本。过程日志信号改对话内容 |
| A2.6 | `13-continuity-rules.md` | 改写 L123：人员资源导入后应建档名单若当日读/写 todos 则建档（§1 可空）；已出组不建 |
| A2.7 | `14-self-check-rules.md` | 能耗补录回写已有日文件不报违规（须已登记 pm-decisions）。禁止 energy 专档。新增：已绑 WP 待办结束越界存量检测（与 D21 同族，限局部扫描）；pm-decisions 已有该 TD 挂起/裁定的不重复报 |
| A2.8 | `18-init-wizard-rules.md` | 改写 L146：init 当日即为花名册应建档全员建个人 md，§1 可空 |
| A2.9 | `19-info-completeness-rules.md` | 改写 L182：应建档缺当天文件=巡检问题；空 §1 不算违规；已出组仍不建、不因缺 §0 报 P0 |
| A2.10 | `22-carried-over-rules.md` | 逐条作废/改写 L29/L40/L57-58/L72/L74/L86/L98/L120/L136/L254 与 §3.4 标题 N-38。应建档=§1 六态除已出组。时机：当日读或写 todos 即全员建档。标记 true 但缺文件=未完成。空闲检测只扫曾有 §1 待办行；仅能耗/空 §1 不进空闲台账。休息日建档仍做。N-37 保留。T+1 能耗不整表拷历史日表，只带累计+当天行+孤儿行 |
| A2.11 | `SKILL.md` | 触发词含整理/补全/回填；logs 定位=对话过程留痕；版本 3.10.0。投喂入库路由加载 00+01+06+10+17+22 |
| A2.12 | `skill-contract.md` | ops 描述改为对话留痕；非进度事实源不变 |

### A3. 模板（节点3）

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `ops-log-template.md` | 表 A 七列：时间 / 用户摘要 / 本轮动作 / 改动文件 / 结果 / 出处 / 用量。注释：有消息就写；禁止全未知；用量可选「—」。表 B 保留给拆解抽空 |
| A3.2 | `ops-log-index-template.md` | 场景摘要=当天对话要点，不是「收尾」 |
| A3.3 | `personal-daily-todo-template.md` | 删除 L38「禁止回写历史日」。§0.6 日表加「异常」列（5 列）；缺节插入；仅能耗 §1 可空；T+1 不整表拷；累计不含重复待裁定。不加金额列 |
| A3.4 | `project-context-template.md` | 外部填报映射加筛选行；仍无默认列名 |

### A4. Portfolio 与示例（节点4）

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | Portfolio `ops-log-template.md` | 新增，与项目同列，路径写 portfolio/logs |
| A4.2 | Portfolio `ops-log-index-template.md` | 新增，集层日期指针 |
| A4.3 | Portfolio `project-index-template.md` | **不加列** |
| A4.4 | `01-readonly-boundary-rules.md` | portfolio/logs 按日懒建可写；禁止抄成员正文；成员 ai 零写 |
| A4.5 | `03-mount-awareness-rules.md` | V-1 仍只 ASK 收编；不写日志指针。收编后查询按管理路径探测 |
| A4.6 | `02-aggregation-query-rules.md` | 查成员日志=管理路径推导；跨项目待办列表每行：项目名 + 该项目 TD 编号 |
| A4.7 | `04-portfolio-report-rules.md` | 集周报仍不得用过程日志当进度 |
| A4.8 | `05-resource-shared-rules.md` | 外部工时表在集层：分析+V-9，不写成员 §0.6；集层日志记「已请某项目入库」 |
| A4.9 | Portfolio `SKILL.md` | 结构树 logs=集层对话懒建；查成员日志=管理路径推导 |
| A4.10 | `examples/06-记日报.md` | 追加「投喂工时表」一段（假项目名；拆完要问或写） |
| A4.11 | `examples/11-项目集总览.md` | 集层对话有日志；指令出处 |

### A5. 回归（节点5）

| # | 动作（写死） |
|---|---|
| A5.1 | 改 OL-002：无 token 接口 → 主列有摘要/动作/文件；用量为 —；禁止全未知行 |
| A5.2 | 改 V3-014：能耗补录不建中间空日目录；废除「空窗永不占位」作为结转通则；当天读/写 todos 则全员建档 |
| A5.3 | 改 PC-009：有该日文件写该日；无则不建空日目录，孤儿行写最新；累计不含重复待裁定 |
| A5.4 | 新增 OL-010~015、FE-001~016、FE-018~022。FE-017 空号（N-37 由 FE-020 覆盖）。FE-019 覆盖 init 当日全员建档 |
| A5.5 | 合计 **443→470**（新增 27，改 3 不计） |

### A6. 脚本（节点6）

| # | 文件 | 动作（写死） |
|---|---|---|
| A6.1 | `chronopm_init/config.py` | 不追加 energy 模板。注释：ops/集层日志实例懒建 |
| A6.2 | `migrate_workspace.py` / init 其余 | 不预建 ops/集层日志实例；**不升 schema** |
| A6.3 | Portfolio 两新模板 | 不进 ALL_TEMPLATE_FILES |

### A7. 版本触点（节点6）

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | `_version.py` | SKILL_VERSION=3.10.0；WORKSPACE_SCHEMA_VERSION=0.14.0 |
| A7.2 | 跑 `sync_version.py` | 同步 VERSION / SKILL.md / skill.json |
| A7.3 | skill.json 双包 | 回归 470；不改历史 schemaHistory 条 |
| A7.4 | CHANGELOG 双包 | 3.10.0 段；Blueprint Impact: metadata-only（能力地图补对话日志/全员建档/时间盒，若 Blueprint 有能力表则改对应行） |
| A7.5 | BLUEPRINT | 3.10.0 行 |

### A8. 基线与发布（节点7）

| # | 动作（写死） |
|---|---|
| A8.1 | `baselines/3.10.0/` 双子树全量快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 发行包打到 `C:\Users\qiusuo\Downloads\` |
| A8.4 | 每完成一个节点：annotated tag（中文说明）推 origin 与 github |
| A8.5 | AP 草稿：基线拍完后删除（`planning/` 仅 README） |

---

## B. 业务工作区

**本发布不代做市监仓。**

存量动作（执行文件要求，禁无确认改数据）：

1. 残缺日补齐：扫各项目 `todos/{date}/` 有 `_index` 但对不上应建档名单的日期，覆盖全部可枚举残缺日（2026-08-23 必含、不是唯一）。清单→PM 确认→补建。
2. Q11 存量越界：已绑 WP 且待办结束 > WP 结束。清单→PM 确认→A/B/C（C 写入 pm-decisions，查重键=TD）。

## C. 验证检查

- [x] `_version.py` 3.10.0 / 0.14.0
- [x] audit 退出码 0
- [x] 回归 470
- [x] 未改验证仓
- [x] 本文件无 upgrade-plan 路径
- [x] 旧 ops 文件不回写
- [x] Portfolio 新模板不在 Project ALL_TEMPLATE_FILES

## D. 发布

每完成一个节点：annotated tag（中文说明）推 origin（Gitee）与 github。

完整升级后：打 `v3.10.0`，发布包到 Downloads。

收尾（用户确认核验后）：

- [x] RR 已生成（`rr-20260823-3.10.0`）
- [x] CR 已斩断 AP 草稿路径；状态 completed
- [x] AP 已删；`planning/` 仅 README
- [x] 分发包已写入 Downloads
- [x] Trae（`~\.trae-cn\skills`）与 Grok（`~\.grok\skills`）已替换为 3.10.0
- [x] C4-1 用户追认；F2 基线 README 已登记；F3 迁移历史已补 3.6.0/3.7.0
