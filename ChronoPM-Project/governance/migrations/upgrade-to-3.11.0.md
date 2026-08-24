# 升级到 3.11.0

> 从 3.10.0 升级到 3.11.0  
> 发布日期：2026-08-24  
> Schema 变更：**不升**，workspace schema 保持 **0.14.0**  
> CR：CR-20260824-001  
> 施工依据：CR-20260824-001 + 本文件。禁止再引用 upgrade-plan 路径。  
> 适用范围：仅 ChronoPM 开发仓 3.10.0 → 3.11.0。  
> 用户拍板：开始执行；每节点 annotated tag（中文）推 origin 与 github；全部完成后再审核。

## 变更摘要

工作包包内状态链（当前=链尾）+ 阶段清单与阶段执行人；词库感应；生成物只进 `ai/outputs/`；计划清爽 5 节只绑 WP，投影三层闸，`正常|废弃`。

## 施工禁区

- 禁止写入/迁移/删除任何业务工作区路径
- 禁止升 schema
- 禁止新建规则文件、新增多份计划模板、索引加列
- 禁止写死项目名 / 包号 / 包数 / 具体 xlsx 文件名
- 禁止改写 WP §7 历史行
- Portfolio 只锁步版本号，不改能力

---

## A. 技能包施工

### A1. 治理与记录（节点1）

| # | 文件 | 动作（写死） |
|---|---|---|
| A1.1 | `governance-shared/change-requests/CR-20260824-001.md` | 本 CR |
| A1.2 | 本文件 | 本施工清单 |
| A1.3 | `governance-shared/impact-analysis/IA-20260824-001.md` | 本 IA |
| A1.4 | `governance-shared/migrations-history/upgrade-to-3.11.0.md` | 拷贝本文件 |
| A1.5 | `ChronoPM-Project/governance/migrations/README.md` | 当前文件改为 upgrade-to-3.11.0.md |
| A1.6 | `ChronoPM-Portfolio/governance/migrations/upgrade-to-3.11.0.md` | 指针文件 |

### A2. 运行时规则（节点2）

| # | 文件 | 动作（写死） |
|---|---|---|
| A2.1 | `00-pm-main-rules.md` | P-ALWAYS 三钩；WP §7 链+§8 阶段+执行人；11 行映射；§8c 扩投影闸；入口⑤块 8「还没写等准许」；WF-7 落库先读 plan-template、5 节、不灌待办 |
| A2.2 | `01-daily-report-rules.md` | §1.2b：本轮问过的缩写 PM 答复后 T2；T4 攒批不阻塞日报 |
| A2.3 | `05-query-rules.md` | WP 状态读链尾+变化线；进度=待办求和；计划查询闸 2；废弃过滤；未入包清单 |
| A2.4 | `06-file-rules.md` | 写前闸门指针；根只留 ai/；PLAN 5 节/`正常\|废弃`/§3 六列；WP 必含 §7 |
| A2.5 | `10-update-trigger-rules.md` | 状态变更须写 §7；出文件 vs 入库二分；计划生成先读模板 |
| A2.6 | `11-output-artifact-rules.md` | 触发改类；点名覆盖 final workspace folder；禁区=根/与 ai 平级 |
| A2.7 | `14-self-check-rules.md` | D33 链；D34 根散落；D35 PLAN 结构；D36 投影全量；D37 plan_ref 互指 |
| A2.8 | `17-domain-glossary-rules.md` | T1–T4；T2 上下文；§17.2 首次感应无文件必须建 |
| A2.9 | `SKILL.md` | 安全底线第 13 条；出文件必载 11、xlsx 升 12；倒排加 06；WP 路由一句状态历史见 00 |

### A3. 模板（节点3）

| # | 文件 | 动作（写死） |
|---|---|---|
| A3.1 | `wp-template.md` | §7 五列状态历史（只追加）；§8 阶段清单+执行人指针；plan_ref 多值；§1 所属计划回显；§3 与 §7/§8「阶段」划界注释 |
| A3.2 | `plan-template.md` | 整表替换为清爽 5 节；status 正常/废弃；§3 六列投影 |

### A4. Portfolio 与示例（节点4）

| # | 文件 | 动作（写死） |
|---|---|---|
| A4.1 | Portfolio 规则 | **零能力改动** |
| A4.2 | `examples/05-确认需求和工作包.md` | 确认切法加一句「状态历史已记」 |
| A4.3 | `examples/09-倒排上线计划.md` | 落库展示 5 节 PLAN，无待办行 |

### A5. 回归（节点5）

| # | 动作（写死） |
|---|---|
| A5.1 | 模块 60 SH-001~018 |
| A5.2 | 模块 61 GL-001~009 |
| A5.3 | 模块 62 OP-001~007 |
| A5.4 | 模块 63 PT-001~010 |
| A5.5 | 模块 64 PS-001~011 |
| A5.6 | 合计 **470→525**（新增 55） |
| A5.7 | 改 WC-001 / BS-003 / BS-005 / BS-013 口径（§7 已追加；落库 5 节） |

### A6. 脚本（节点6）

| # | 文件 | 动作（写死） |
|---|---|---|
| A6.1 | `scripts/_version.py` | SKILL_VERSION=3.11.0；schema 0.14.0 |
| A6.2 | 跑 `sync_version.py` | 双包 VERSION / SKILL.md / skill.json |
| A6.3 | `chronopm_init/config.py` | **零改动**（模板按文件名拷贝） |

### A7. 版本触点（节点6）

| # | 文件 | 动作（写死） |
|---|---|---|
| A7.1 | CHANGELOG 双包 | 3.11.0 段 |
| A7.2 | BLUEPRINT | 3.11.0 行 |
| A7.3 | skill.json 回归基线 525 | |

### A8. 基线与发布（节点7–8）

| # | 动作（写死） |
|---|---|
| A8.1 | `baselines/3.11.0/` 双子树全量快照 |
| A8.2 | `audit_release.py` 退出码 0 |
| A8.3 | 每完成一个节点：annotated tag（中文说明）推 origin 与 github |
| A8.4 | AP 草稿：基线拍完后删除（`planning/` 仅 README） |
| A8.5 | 全部完成后请用户审核；不提前打断 |

---

## B. 业务工作区

**本发布不代做任何业务仓。**

通用算法（执行时对当时打开的工作区，禁路径常量）：

1. WP 缺 §7：清单→PM 确认→分批回填（证据链，不猜日期）。
2. 计划非 `PLAN-NNN-*.md`：清单→PM 确认→按 5 节规范化。
3. 工作区根非 `ai/` 的生成物：清单→PM 确认→迁 `ai/outputs/{ts}/files/`。

## C. 验证检查

- [ ] `_version.py` 3.11.0 / 0.14.0
- [ ] audit 退出码 0
- [ ] 回归 525
- [ ] 未改业务验证仓
- [ ] 本文件无 upgrade-plan 路径
- [ ] 模板数仍 37

## D. 发布

每完成一个节点：annotated tag（中文说明）推 origin（Gitee）与 github。

完整升级后：打 `v3.11.0`，请用户审核后再替换安装区 / 打发行包。
