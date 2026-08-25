# ChronoPM Skill v3.15.0 升级方案

> **方案版本**：V0.11（核 B1：真问题修；拒收错字段的 32 条断言表）  
> **目标版本**：ChronoPM-Project 3.14.0 → 3.15.0 / ChronoPM-Portfolio 3.14.0 → 3.15.0  
> **workspace schema**：0.15.0 → 0.16.0  
> **本轮状态**：A 已处理文末 B1，等待 B **对照 V0.11**（不得执行）  
> **创建日期**：2026-08-25  
> **修订日期**：2026-08-25（V0.1→V0.10→**V0.11**）  

**V0.8 相对 V0.7 的拍板（A）**

| # | 拍板 | 来源 |
|---|---|---|
| A8-1 | `current_operator` 为空 → **一律 ASK**，禁止回退 `pm_name` 当「我」；TD 缩写空则问，不猜 | B-007 |
| A8-2 | C-4 **存量 examples 豁免**场景/mermaid；本版只强制编号+跨引用+不演示未实现能力。§22 从新示例生效 | B-008 / X 非阻塞 |
| A8-3 | §14–§24 灌入 SG-008～011；§24 输入包 = **11 条** | X-1 |
| A8-4 | 测试号一套：SG-010 = **T35–T40**；SG-009 P1 = T41–T47；SG-011 = **T48/T48b**。禁止再出现第二套 SG-010 号 | X-3 |
| A8-5 | SG-009 **4 脚本均纳入 3.15.0**。P0 必挂 19 号：`verify_projection.py` + `verify_todo_continuity.py`。P1 交付可调用、19 号不自动跑：`verify_requirement_wp.py` + `verify_contract_ri.py` | X-4 |
| A8-6 | **N-33② 在 3.14 规则文件 0 命中**。3.8.0 B5「禁止建空待办」是 resource-register 一次性迁移，不是日常结转硬约束。3.15 **维持 22 号现行**：当天读/写 todos → 应建档全员人人一份（§1 可空）。不采用「无待办无能耗者不建文件」 | 现网 22 L29/L56 vs 另一份 B 的 X-2 |
| A8-7 | Python **最低 3.9**，与双包 `skill.json` `"python": ">=3.9"` 对齐 | B-009 |
| A8-8 | 项目集「我是张三」**降级为 V-9 SUGGEST**（字面级联因只读硬契约做不到），已拍板 | 现网 Portfolio L23 |
| A9-1 | **SG-011 纳入 3.15.0**（不延后 3.16）：`generate_single_readme` f-string 里 `{编号}` 未转义，初始化写 README 即崩。一行修复，文件本就在 init 改动集 | 通义初始化实测 + 现网 L543 |
| A10-1 | 过期 V0.8 B 审的 X-1～X-4 **以本文件现稿为准已闭合**，不要再按 V0.8 正文复述。B-013 不得写成「无待办无能耗不建文件」——现稿是 **A8-6 人人一份（§1 可空）** | 本轮 B 审对照错版本 |
| A10-2 | D-EFFECT-01：缺 `effect` 当正常；D-PLAN-REF-01：禁止只信 YAML，plan_ref 空仍扫正常 PLAN §3 | X-5.2 / X-5.3 |
| A10-3 | SG-001 迁移幂等：已是 13 标准名 skip；只投影 §3/§4，不重算点名人期 | 非阻塞建议落地 |
| A11-1 | **拒收** B1 把 §15 改成 A-013～A-032。那张表用 `requirement_refs` / `create_date` / `ai/sources/` / WP YAML name，是已证伪的数据模型。机器断言以 SG-009 §2.2 为准 | B1 X-1 |
| A11-2 | §14 是影响评估，不是施工步骤。P1 两脚本已在 SG-009 文件表；补 **§13 施工总清单** 以免再被说「§14 没列」 | B1 X-2 |
| A11-3 | SG-010 硬阻断 = 22 号规则 + 日报载 22，**不跑** verify 脚本。无 Python 仍必须 Step 0，禁止「无 Python 就跳过结转」 | B1 X-3 |
| A11-4 | plan_ref 多值按 ` / ` split；init README 已存在则 skip | B1 Y-3 / Y-4 |  

---

## 工作空间版本快照

| 项目 | 值 |
|---|---|
| 工作空间根路径 | `C:\Users\qiusuo\Downloads\ChronoPM Skill` |
| 版本标识来源 | skill.json version + VERSION 文件 |
| ChronoPM-Project 版本 | 3.14.0 / workspace schema 0.15.0 |
| ChronoPM-Portfolio 版本 | 3.14.0 / workspace schema 0.15.0 |
| 快照生成时间 | 2026-08-25 |
| 关键文件清单 | SKILL.md, skill.json, VERSION, CHANGELOG.md, references/, assets/templates/, scripts/, skill-gap-skill/ |
| 用户确认状态 | ✅ 已由用户确认 |

---

# 1. 原始需求照抄

本次升级包含 **11** 条需求，其中 SG-001~004 来自用户文件，SG-005~011 来自对话补证（SG-011 = 初始化 README f-string）。

## 需求 SG-20260825-001：3.14 升级脚本缺存量历史数据迁移（高优先级）

> **一句话痛点**：升级执行文件只建空目录、不改业务文件，存量 WP 阶段名、计划投影与索引全靠对话内"懒迁/触碰"，一旦不触即双轨不一致且用户无感知。

**核心问题**：`migrate_workspace.py` v3.14.0 条目只做了"建空目录 `project-info/`"并把 schema 抬到 0.15.0，没有做任何业务数据迁移。存量历史数据全靠升级后的人工对话逐条"触碰到才改"。

**用户原话**：
- "这会让整个历史数据和版本不一致，而且一般用户根本无法感知，会造成数据偏差。越做越错"
- "以上的原因是因为升级执行文件未包含历史数据处理造成的吗，总结归纳成一个需求，3.14.0的升级执行文件可能存在功能不全的问题"

**建议补什么**：
1. `migrate_workspace.py` 增加"存量数据迁移"能力：dry-run 预览、受控写回、一键回滚
2. 升级完成动作增加"投影对账 + 待校准清单自动生成"
3. 升级契约语义补齐为"结构 + 存量数据"双对齐

## 需求 SG-20260825-002：计划 §4 模板缺执行人/排期（中优先级）

> **一句话痛点**：`plan-template.md` 的 §4 只画「阶段 → 状态」骨架、没有执行人与排期，与规则「§4 从 WP §8 五列投影、空岗 ⚠️待安排人」不一致，照模板做就漏掉执行人/排期。

**核心问题**：规则（00 §8c/§8d）要求 §4 带执行人/空岗占位，但 `plan-template.md` §4 示例只有 `- 测试 → ⏳`，未把执行人/排期纳入示意格式。

**用户原话**：
- "我记得 skill 3.14.0 有规范'4. 各 WP 阶段排期'这个章节的模版是需要包含执行人和执行人排期的"
- "模版错了，还是规则不明？"

**建议补什么**：
1. `plan-template.md` §4 示例改为含执行人与排期的完整格式
2. 明确"§4=WP §8 五列投影"的落盘格式
3. （可选）`14-self-check-rules.md` 增加 §4 字段完整性自检

## 需求 SG-20260825-003：技能缺口输出改"单文件自足"（中优先级）

> **一句话痛点**：P-SKILL-GAP 输出产物在需求正文外另加 `manifest.md` 批次外壳，把元数据放在需求文件之外，违背"一个需求 = 一个自足文件"。

**核心问题**：每条需求产出 `需求-*.md` + `manifest.md` 两个文件；元数据在 manifest，不随需求走。

**用户原话**：
- "选 B，合并，要求一次只生成一个需求文件……这些字段就应该包含在各自的需求文件里面"
- "以上这个其实也是对 3.14.0 的升级需求，也写一个"

**建议补什么**：
1. P-SKILL-GAP 输出约定改为：一条需求 = 一个自足文件
2. 不再生成 `manifest.md`
3. `outputs/index.md` 以需求文件为最小登记单元

## 需求 SG-20260825-004：PM 身份识别拆分"项目经理"与"当前操作人"（高优先级）

> **一句话痛点**：`pm_name` 把"项目基本信息里的项目经理"和"对话里'我'是谁"混成一个单值，导致多项目经理无法区分、ai 文件夹打包给任何人后"查我的待办"的"我"错指 pm_name。

**核心问题**：`pm-profile.md` front matter `pm_name` 单值，被 21 号 §2.4 用作"我"推导；无法表达多项目经理、无法随文件夹易主。

**用户原话（4 条要求）**：
1. pm_name 只是记录项目基本信息的字段，可以设置 1~2 个项目经理，初始化时询问并加载
2. AI 不能自动根据 todos 人员岗位自动填充新的项目经理
3. 新增项目工作空间级属性「当前操作人」，"查我的待办"的"我"以当前操作人为准
4. 项目集下"我是张三"级联到所有子项目

**建议补什么**：
1. `pm_name` 降格为项目基本信息字段，支持 1~2 位
2. 新增「当前操作人」工作空间级持久属性
3. 项目集级联
4. 修订 21 号 §2.4 与 pm-profile-template

## 需求 SG-20260825-005：AP 草稿文件强制约束（治理补正）

> **一句话痛点**：Agent 生成升级方案时自行拆分为多个文件、存放在任意目录，Skill 治理规则未对 AP 草稿的数量、命名、存放位置做强制约束。

**核心问题**：`16-skill-governance-rules.md` 虽在 §2.1/§19 提到 AP 文件，但未强制约束：(1) 每个升级周期只能有 1 个 AP 文件；(2) 命名必须严格为 `upgrade-plan-v{version}.md`；(3) 存放位置必须为 `governance-shared/planning/`。同时 `planning/README.md` L7 措辞模糊（「可以放这里或 upgrade-plan-v*.md」），可被理解为"放别处也行"。

**用户原话**：
- "你不能直接写让生成在 governance-shared/planning/，而是要在提示词中加上，要严格遵守 skills 的升级要求规范"
- "然后在 skills 的升级要求规范里面去强制约束，如（1）升级方案强制一次只生成 1 个（2）升级方案命名严格遵守要求规定（3）生成位置"
- "是我 skill 的升级要求不明确，没有正确加载？"

**建议补什么**：
1. `16-skill-governance-rules.md` 新增 §21：AP 草稿文件强制约束（数量/命名/位置）
2. `governance-shared/planning/README.md` L7 消除歧义，明确唯一存放位置

## 需求 SG-20260825-006：examples 重编号 + 示例质量约束

> **一句话痛点**：examples 目录序号不合理（01 升级在 03 初始化之前），且示例内容全是空对话无场景描述，可读性差。

**核心问题**：
1. **顺序错误**：当前 01 是升级、03 是初始化。逻辑上必须先有工作区才能升级，应改为 01 初始化、02 升级。
2. **跨引用未同步**：02（原 01）处理待确认事项引用了 01-升级工作区.md，需改为 02-升级工作区.md；17（复盘和成本）引用了 03-初始化工作区.md，需改为 01-初始化工作区.md。
3. **示例质量低**：所有 examples 文件只有「你」「助手」的对话模板，缺少真实业务场景背景，用户看不懂为什么要这样做。

**用户原话**：
- "examples工作区的序号也不合理，应该先初始化工作区才对"
- "我发现在examples里面的示例，光是空对话，一点场景都没有，全是空描述，这谁看得懂"
- "example的示例生成也要增加标准约束"

**建议补什么**：
1. examples 目录按逻辑流程重编号（见下方重编号方案）
2. README.md 的 mermaid 图和表格同步更新
3. 16 号规则新增 §22：examples 示例生成标准约束（必须包含场景背景、不能只有空对话）
4. 收尾检查清单新增：examples 顺序和内容正确性检查

### examples 重编号方案

| 新编号 | 原编号 | 文件名 | 分组 |
|---|---|---|---|
| 01 | ~~03~~ | 初始化工作区 | 先把家安好 |
| 02 | ~~01~~ | 升级工作区 | 先把家安好 |
| 03 | ~~02~~ | 处理待确认事项 | 先把家安好 |
| 04 | ~~04~~ | 投喂合同和立项 | 材料进得来 |
| 05 | ~~16~~ | 一份材料拆到多个项目 | 材料进得来 |
| 06 | ~~05~~ | 确认需求和工作包 | 材料进得来 |
| 07 | ~~06~~ | 记日报 | 每天怎么管 |
| 08 | ~~07~~ | 记会议纪要 | 每天怎么管 |
| 09 | ~~12~~ | 人员进出和结转 | 每天怎么管 |
| 10 | ~~08~~ | 登记风险和问题 | 每天怎么管 |
| 11 | ~~09~~ | 倒排上线计划 | 怎么看全局 |
| 12 | ~~10~~ | 出周报和问进度 | 怎么看全局 |
| 13 | ~~11~~ | 项目集总览 | 怎么看全局 |
| 14 | ~~13~~ | 改需求和范围 | 偶尔才做 |
| 15 | ~~14~~ | 完整性巡检 | 偶尔才做 |
| 16 | ~~15~~ | 词库 | 偶尔才做 |
| 17 | ~~17~~ | 复盘和成本 | 偶尔才做 |
| 18 | ~~18~~ | 导入历史计划 | 偶尔才做 |
| 19 | ~~19~~ | 派活与拆文件入库 | 偶尔才做 |
| 20 | ~~20~~ | 技能缺口 | 偶尔才做 |

## 需求 SG-20260825-007：收尾检查清单补强

> **一句话痛点**：每次升级发布前，缺乏对 README/SKILL_MODULE_MAP/examples 一致性的强制检查，导致版本信息不一致、模块图过时、示例顺序错误等问题遗漏到发布后才发现。

**核心问题**：
1. **README 版本不一致**：中英文 README 的版本号、能力描述可能未及时更新，与 skill.json 不一致。
2. **SKILL_MODULE_MAP.md 过时**：模块链路图未反映最新架构变更（如 G5 计划投影机制、G4 WP §7/§8 等）。
3. **examples 未检查**：示例顺序、内容正确性无强制检查项。
4. **release-checklist.md 引用路径错误**：16 号规则 §14 引用了 `governance/review-checklists/release-checklist.md`（不存在），实际文件在 `governance-shared/review-checklists/`。

**用户原话**：
- "skills升级要求里面看一下有么有每次升级的时候，1、要检查中英文README是否符合当前升级完的版本，不满足就要改成符合；2、检查ChronoPM-Project/SKILL_MODULE_MAP.md是否符合当前升级完的版本、不满足要改满足；3、检查examples下面的示例顺序对不对，内容对不对，不满足要改满足"
- "上面的都做完才能触发收尾"

**建议补什么**：
1. 修订 `references/16-skill-governance-rules.md` §14 引用路径指向已存在的 `governance-shared/review-checklists/release-checklist.md`
2. 在 `governance-shared/review-checklists/release-checklist.md` 追加 C-1~C-4 四项检查

## 需求 SG-20260825-011：init README f-string `{编号}` 未转义（低优先级，纳入 3.15）

> **一句话痛点**：`init_workspace.py` 目录骨架能建完，写 `ai/README.md` 时因 f-string 把 `{编号}` 当变量名崩掉；弱模型会手补 README 绕过，用户以为是自己用错。

**核心问题**：`chronopm_init/file_registry.py` `generate_single_readme()` 整段是 f-string。`{SKILL_VERSION}` / `{today}` / `{project_name}` 是真插值；目录树里 `sources/{编号}/` 应为字面量，写成了单花括号。Python 3 抛 `NameError: name '编号' is not defined`（有的宿主记成 KeyError）。同函数里 `{{YYYY-MM-DD}}` / `{{执行人}}` / `{{name}}` 已经转义，**漏了这一处**。

**现网证据**（A 实读，不靠通义转述）：
- `file_registry.py` L497–607：`return f"""..."""`
- L543：`│       └── {编号}/                # 一源文档一目录`
- `workspace_builder.py` L130–133：目录建完后才 `write_text(generate_single_readme(...))` → 所以「骨架成功、README 失败」与栈序一致

**建议补什么**：L543 改为 `{{编号}}`。施工时扫同函数其余 `{...}`，只保留合法插值名。

---

# 2. Agent A 对需求的理解

## 2.1 需求理解

| 需求 | A 的理解 |
|---|---|
| SG-001 | 升级脚本从"只建空目录"增强为"结构+存量数据并行对齐"。需要新增存量业务数据迁移能力（WP §7/§8 阶段名映射、计划 §3/§4 投影重建、索引列值对齐），配套 dry-run/回滚/待校准清单。同时需修订 upgrade-to-X.X.X.md 模板，把存量迁移写入升级契约。 |
| SG-002 | 纯模板修复。`plan-template.md` §4 示例行从 `- 阶段 → ⏳` 改为含执行人+排期的完整格式（如 `- 测试 → 🔄（当前）｜储金晶/王柏森｜2026-08-26~2026-09-15`），并附空岗示例。规则已正确，只需模板对齐。可选补自检项。 |
| SG-003 | 输出约定变更。skill_gap 需求输出从"需求正文+manifest.md"改为"单文件自足"：元数据并入需求文件 front matter，不再生成 manifest.md。涉及 gap-capture-rules.md + 11-output-artifact-rules.md + outputs-index-template.md 修改。 |
| SG-004 | 身份模型重构。pm_name 降格为项目基本信息（支持 1~2 位项目经理）；新增工作空间级「当前操作人」属性（持久、可对话切换）；"我"推导从 pm_name 迁到当前操作人；项目集级联。涉及 21 号规则 + pm-profile-template + SKILL.md + init/migrate 脚本 + Portfolio 规则。 |
| SG-005 | 治理补正。`16-skill-governance-rules.md` 新增 §21 强制约束：AP 草稿每周期限 1 个、命名严格 `upgrade-plan-v{version}.md`、存放位置 `governance-shared/planning/`。同步修正 `planning/README.md` L7 消除歧义。Agent 提示词侧由用户自行修改，不纳入 Skill 改动。 |
| SG-006 | examples 重编号 + 质量约束。examples 目录按逻辑流程重编号（01 初始化→02 升级→...）；README.md mermaid/表格同步更新；16 号新增 §22 示例生成标准约束（必须有场景背景）。涉及 20 个文件重命名 + README.md 更新 + 16 号规则新增。 |
| SG-007 | 收尾检查清单补强。修订 16 号 §14 引用路径指向 `governance-shared/review-checklists/release-checklist.md`；在该现有清单追加 C-1~C-4 四项检查；收尾流程新增检查门禁。 |
| SG-008 | 纯文档。SKILL.md 加 §5.0 环境检测与分平台安装指引。版本下限跟双包 skill.json：Python ≥3.9。 |
| SG-009 | 机器断言守护闸 2 / 结转 / 需求-WP / 合同映射。C1–C8 按闸 2 六项 + index + 防呆定义。本版 4 脚本都进包；P0 挂 19 号，P1 可调用不强制日常跑。 |
| SG-010 | 执行漏洞，不是缺规则。最小必要改动：SKILL.md 日报行必载 22。维持 22 号「人人一份（§1 可空）」。WF-8 Step 0 现网已有，只对齐不新造一份。 |
| SG-011 | init README 一行 f-string 转义。非用法问题。纳入 3.15 因 init 是第一口、修复成本为零、且 init 脚本本轮已因 SG-004 打开。 |

## 2.2 需求理解偏差验证

| 验证项 | 结论 |
|---|---|
| 是否覆盖原始需求 | 是，**11** 条需求均有对应设计 |
| 是否加入原始需求没有的内容 | SG-001 dry-run/回滚为「受控迁移」隐含诉求。SG-009 机器断言为对话补证。SG-004 字面「级联写子项目」因 Portfolio 只读硬契约降为 SUGGEST（已拍板，不是静默扩展） |
| 是否遗漏明确要求 | SG-004「禁止按岗位填充项目经理」已写入 21 号约束。SG-010 真正漏点是路由未载 22，不是再写一遍 Step 0 |
| 哪些内容属于暂定 | SG-001 dry-run 输出格式、回滚粒度 |
| 哪些必须请用户确认 | 无。Q1–Q9 均已关闭（见 §5.4 / §21） |
| 哪些要交给 B 复核 | 全部 11 条，尤其 A8-1～A8-8、A9-1、C1–C8 / D-TODO 字段口径 |

---

# 3. 已扫描目录与文件清单

| 路径 | 类型 | 是否已读取 | 作用判断 | 与本次升级关系 | 备注 |
|---|---|---|---|---|---|
| ChronoPM-Project/skill.json | 配置 | ✅ | 版本/能力/迁移定义 | SG-001 版本号+迁移条目 | 当前 3.14.0 |
| ChronoPM-Project/VERSION | 版本 | ✅ | 版本标识 | 升级后改 3.15.0 | |
| ChronoPM-Project/SKILL.md | 主提示词 | ✅ | 路由表/事实源/安全底线 | SG-004 路由+事实源表 | 174 行 |
| ChronoPM-Project/references/00-pm-main-rules.md | 核心规则 | ✅(§8c/8d) | WP 级联/投影/SCAN | SG-002 §4 投影规则 | 924 行 |
| ChronoPM-Project/references/21-pm-profile-rules.md | PM 偏好规则 | ✅ | pm_name/身份推导 | SG-004 核心改造对象 | 464 行 |
| ChronoPM-Project/references/14-self-check-rules.md | 自查规则 | ✅(§1-2) | 自检项 | SG-002 可选补 §4 自检 | 386 行 |
| ChronoPM-Project/references/11-output-artifact-rules.md | 生成物规则 | ✅(grep) | manifest/批次/P-OUTPUT | SG-003 仅 skill_gap 例外不建 manifest | |
| ChronoPM-Project/assets/templates/plan-template.md | 计划模板 | ✅ | §4 格式 | SG-002 核心改造对象 | 75 行 |
| ChronoPM-Project/assets/templates/pm-profile-template.md | PM 偏好模板 | ✅ | pm_name 字段 | SG-004 核心改造对象 | 88 行 |
| ChronoPM-Project/assets/templates/wp-template.md | WP 模板 | ✅ | §8 五列 | SG-002 参照源（不改） | 124 行 |
| ChronoPM-Project/assets/templates/outputs-index-template.md | 输出索引模板 | ✅ | 批次登记 | SG-003 改登记单元 | 35 行 |
| ChronoPM-Project/skill-gap-skill/CAPABILITY.md | 能力目录 | ✅ | 产出约定 | SG-003 产出改单文件 | 11 行 |
| ChronoPM-Project/skill-gap-skill/references/gap-capture-rules.md | 缺口规则 | ✅ | P-OUTPUT/manifest | SG-003 核心改造 | 66 行 |
| ChronoPM-Project/governance/migrations/upgrade-to-3.14.0.md | 升级文档 | ✅ | B 节存量策略 | SG-001 参照+改进 | 191 行 |
| ChronoPM-Project/scripts/migrate_workspace.py | 迁移脚本 | ✅(部分) | VERSION_CAPABILITIES | SG-001 核心改造 | 2108 行 |
| ChronoPM-Portfolio/skill.json | 配置 | ✅ | 版本锁步 | SG-004 Portfolio 侧 | 3.14.0 |
| ChronoPM-Portfolio/references/01-readonly-boundary-rules.md | 规则 | ✅ | 只读/V-9 | SG-004 禁止 AUTO 写子项目 | L23 AUTO 级联不存在 |
| ChronoPM-Project/references/22-carried-over-rules.md | 规则 | ✅ | 结转 | SG-010 | L29 人人一份；L58/L93 true 语义 |
| ChronoPM-Project/references/01-daily-report-rules.md | 规则 | ✅ | 日报 | SG-010 投喂入口 | L42 已指向 22；路由未载 22 |
| ChronoPM-Project/references/05-query-rules.md | 规则 | ✅ | 「我的待办」 | SG-004 | 简单查询只载 05 |

---

# 4. 现有 Skill 审查结果

## 4.1 Skill 概况

- **名称/定位**：ChronoPM-Project（单项目 Markdown 项目管理）+ ChronoPM-Portfolio（只读项目集归集）
- **当前版本**：3.14.0 / workspace schema 0.15.0
- **规则文件数**：23 个（00~23）+ skill-gap-skill 2 个 + source-split-skill 2 个
- **模板文件数**：~40 个（含 archive）
- **脚本**：init_workspace.py（含 chronopm_init 包）、migrate_workspace.py、sync_version.py

## 4.2 与本次升级相关的现有关键机制

### 升级脚本现状（SG-001）

`migrate_workspace.py` VERSION_CAPABILITIES v3.14.0：
```python
{
    "version": "3.14.0",
    "schema": "0.15.0",
    "new_dirs": ["project-info"],
    "note": "脚本只建空目录，不搬业务文件"
}
```
历史惯例：脚本只做结构迁移（建空目录+升 schema），不碰业务数据。

### 计划 §4 现状（SG-002）

`plan-template.md` §4 示例只有「阶段 → 状态」，无执行人/排期。

而规则 `00-pm-main-rules.md` §8d L620 要求：
> 计划 §4：各 WP 阶段列表，从 WP §8 投影落盘，禁止子行。空岗用 ⏳ / `⚠️待安排人`。

WP §8 五列：阶段 | 状态 | 执行人 | 排期 | 关键阶段。

### 技能缺口输出现状（SG-003）

`gap-capture-rules.md` §1 要求 CALL P-OUTPUT 建 manifest。`11-output-artifact-rules.md` §3 批次目录含 manifest.md。

### PM 身份现状（SG-004）

`pm-profile-template.md` front matter `pm_name` 单值。`21-pm-profile-rules.md` §2.4 用 pm_name 推导"我"。

---

# 5. 需求提炼

## 5.1 明确需求

| 编号 | 需求 | 来源 |
|---|---|---|
| R1 | 升级脚本增加存量业务数据迁移能力（dry-run + 回滚 + 待校准清单） | SG-001 |
| R2 | plan-template §4 示例补齐执行人+排期+空岗占位 | SG-002 |
| R3 | skill_gap 输出改为单文件自足（移除 manifest.md） | SG-003 |
| R4 | pm_name 降格为项目基本信息（支持 1~2 位） | SG-004 |
| R5 | 新增工作空间级「当前操作人」属性 | SG-004 |
| R6 | "我"推导从 pm_name 迁到当前操作人 | SG-004 |
| R7 | 禁止 AI 根据 todos 岗位自动填充项目经理 | SG-004 |
| R8 | 项目集「我是张三」走 V-9 SUGGEST，不自动写子项目 pm-profile（字面级联已拍板降级） | SG-004 |
| R9 | 16 号新增 §21：AP 草稿每周期限 1 个 | SG-005 |
| R10 | AP 命名严格 `upgrade-plan-v{version}.md`，禁止附加后缀 | SG-005 |
| R11 | AP 存放位置强制 `governance-shared/planning/` | SG-005 |
| R12 | `planning/README.md` L7 消除歧义 | SG-005 |
| R13 | examples 目录按逻辑流程重编号（20 个文件） | SG-006 |
| R14 | README.md mermaid/表格同步更新 | SG-006 |
| R15 | 16 号新增 §22：examples 示例生成标准约束 | SG-006 |
| R16 | 修订 16号 §14 引用路径指向 `governance-shared/review-checklists/release-checklist.md` | SG-007 |
| R17 | 在 release-checklist.md 追加 C-1~C-4 四项检查 | SG-007 |
| R18 | 收尾流程新增检查门禁 | SG-007 |
| R19 | SKILL.md 新增 §5.0 环境检测 + AI 引导安装流程 | SG-008 |
| R20 | README 标注 Python 版本要求（最低 3.9，与 skill.json 对齐；推荐 3.10+） | SG-008 |
| R21 | 新建 verify_projection.py（含 C1-C8 + D-TODO-WP-01/02 + D-PLAN-REF-01 + D-EFFECT-01） | SG-009 |
| R22 | 新建 verify_todo_continuity.py（含 D-TODO-01/02/03） | SG-009 |
| R23 | 新建 verify_requirement_wp.py（含 D-REQ-WP-01/02 + D-SOURCE-01） | SG-009 |
| R24 | 新建 verify_contract_ri.py（含 D-CONTRACT-01/02） | SG-009 |
| R25 | 19号规则新增断言脚本挂载说明 | SG-009 |
| R26 | 01号新增日报投喂前置检查（硬阻断） | SG-010 |
| R27 | 22号 carryover_done_for_today 语义澄清 | SG-010 |
| R28 | 00号 WF-8 Step 0 与 22 号对齐（现网 L781 已存在，禁止再复制一份） | SG-010 |
| R29 | SKILL.md 日报路由必载 22 号 | SG-010 |
| R30 | `generate_single_readme` 目录树 `{编号}` → `{{编号}}`；禁止改其它真插值 | SG-011 |

## 5.2 隐含需求

| 编号 | 需求 | 来源 |
|---|---|---|
| IR1 | 升级执行文件模板需包含存量迁移指引 | SG-001 |
| IR2 | 14 号自检可选补 §4 字段完整性检查项 | SG-002 |
| IR3 | outputs-index-template 的 Type=skill_gap 行格式调整 | SG-003 |
| IR4 | init/migrate 脚本需支持「当前操作人」创建 | SG-004 |
| IR5 | Portfolio 侧需感知「当前操作人」级联 | SG-004 |
| IR6 | examples 跨引用同步更新（02→02、17→01） | SG-006 |
| IR7 | release-checklist.md 必须包含 4 项新检查的断言 | SG-007 |

## 5.3 不做的事情

- 不改 WP §8 五列结构（SG-002 只改计划模板，不改 WP 模板）
- 不改变 skill_gap 的触发条件和正文格式（SG-003 只改输出约定）
- 不改变 PM Profile 的偏好学习机制（SG-004 只改身份推导层）
- 不做存量工作区的自动批量升级（SG-001 提供工具，但执行仍需 PM 确认）
- 不修改 Agent 提示词（SG-005 的 Agent 侧约束由用户自行修改）
- 不改变 examples 现有对话正文（SG-006 只重编号+跨引用；§22 不追溯；C-4 存量豁免场景/mermaid）
- 不改已有发布流程，只增加前置检查门禁（SG-007）
- 不把 3.8.0 B5「禁止建空待办」升格为日常结转硬约束（SG-010 维持 22 号人人一份）
- 不在 11 号 §3 默认批次结构里删除 manifest（仅 skill_gap 例外）

## 5.4 待确认事项

全部关闭。默认即拍板：

| 编号 | 问题 | 拍板 | 状态 |
|---|---|---|---|
| Q1 | current_operator 存储位置 | pm-profile.md front matter 字段 `current_operator` | 已关闭 |
| Q2 | SG-001 是否含 budget/progress-plan 移动 | 纳入（补做 3.14 未完成项） | 已关闭 |
| Q3 | 项目集级联落地范围 | Portfolio 只出 V-9 SUGGEST，不写子项目 | 已关闭 |
| Q4 | §22 是否追溯已有 examples | 不追溯 | 已关闭 |
| Q5 | release-checklist 路径 | 改为 `governance-shared/review-checklists/` | 已关闭 |
| Q6 | current_operator 为空时是否回退 pm_name | **一律 ASK，禁止回退** | 已关闭 |
| Q7 | C-4 是否用场景门禁卡发布 | **存量豁免**；本版只查顺序/跨引用/不演示未实现能力 | 已关闭 |
| Q8 | 无待办无能耗是否建空文件 | **建**（§1 可空）。N-33② 不是 3.14 日常硬约束 | 已关闭 |
| Q9 | SG-009 4 脚本是否都进 3.15 | **都进包**；P0 挂 19 号，P1 可调用不自动跑 | 已关闭 |

---

# SG-001 设计方案：升级脚本增加存量数据受控迁移

> **需求编号**：SG-20260825-001  **优先级**：高  
> **一句话痛点**：升级执行文件只建空目录、不改业务文件，存量数据双轨化且用户无感知  

---

## 1. 问题根因

`migrate_workspace.py` v3.14.0 VERSION_CAPABILITIES：
```python
{
    "version": "3.14.0",
    "schema": "0.15.0",
    "new_dirs": ["project-info"],
    "note": "脚本只建空目录，不搬业务文件"
}
```

升级契约只覆盖"结构迁移"（建空目录+升 schema），不覆盖"存量数据迁移"。upgrade-to-3.14.0.md B 节明确"本发布不代做任何业务仓"，存量全靠对话内懒迁/触碰。

## 2. 设计方案

### 2.1 交互流程

```
用户触发升级 → migrate_workspace.py --project-root <path>
  ↓
脚本检测当前工作区版本
  ↓
脚本执行结构迁移（建空目录+升 schema）
  ↓
脚本检测存量业务数据不一致（WP §8 vs 计划 §3/§4 vs 索引）
  ↓
脚本生成「待校准清单」（dry-run 模式，不写回）
  ↓
输出：「检测到 N 处存量数据不一致，是否执行受控迁移？(y/n)」
  ↓
用户确认 → 脚本执行受控迁移（写回+生成回滚快照）
  ↓
输出：「迁移完成，已生成回滚快照。建议执行完整性巡检。」
```

### 2.2 迁移覆盖范围

| 迁移项 | 说明 | 方式 |
|---|---|---|
| WP §7 链尾阶段名 | 旧名→新 13 阶段映射 | 按 upgrade-to-3.14.0.md B 节映射表 |
| WP §8 阶段名 | 同上 | 先剥 `（完成）` `（当前）` 再映射 |
| 计划 §3/§4 投影 | 从 WP §8 重建 | 定位=plan_ref ∪ 扫正常 PLAN 头 |
| 索引列值 | wps/_index.md 状态列 | 与 WP §7 链尾一致 |
| budget/progress-plan | plans/ → project-info/ | 文件移动（PM 确认后） |

### 2.3 安全机制

- **dry-run 默认**：默认只检测不写回，输出待校准清单
- **回滚快照**：写回前在 `ai/backup/migration-snapshot-{timestamp}/` 生成副本
- **PM 确认**：写回需用户明确确认
- **不猜测**：无法映射的阶段名保留原名+⚠️待校准
- **幂等**：阶段名已是 13 标准名 → skip，禁止按同义词二次改名
- **只投影**：重建计划 §3/§4 与索引列；**不重算** WP §8 点名人期、不跑全量 SCAN
- **禁写业务仓默认路径**：只处理 `--project-root` 指向的那一个工作区；开发仓无业务 `ai/` 则跳过存量迁移

### 2.4 脚本函数设计

```python
def migrate_business_data(project_root, dry_run=False):
    """
    存量业务数据受控迁移
    
    覆盖：
    - WP §7 链尾/§8 阶段名映射（旧→新 13 阶段）
    - 计划 §3/§4 投影重建（从 WP §8）
    - 索引列值对齐（wps/_index.md）
    - budget/progress-plan 文件移动（plans/ → project-info/）
    
    dry_run=True：只检测，输出待校准清单，不写回
    dry_run=False：受控写回+生成回滚快照
    """
```

### 2.5 异常处理

| 异常 | 处理 |
|---|---|
| WP §8 阶段名无法映射 | 保留原名+⚠️待校准，列入清单 |
| 计划 §3/§4 与 WP §8 不一致 | 以 WP §8 为准重建投影 |
| 回滚快照创建失败 | 中止迁移，提示手动备份 |
| budget/progress-plan 不存在 | 跳过，列入清单 |

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `scripts/migrate_workspace.py` | 新增 `migrate_business_data()` 函数；VERSION_CAPABILITIES 补 3.15.0 条目 | P0 |
| `governance/migrations/upgrade-to-3.15.0.md` | 新增升级执行文件（含存量迁移指引） | P0 |

## 4. 兼容方式

- 结构迁移能力保留，新增存量迁移为可选步骤
- 旧工作区升级时如不执行存量迁移，行为与 3.14.0 一致
- 存量迁移不自动执行，需 PM 手动确认

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T8 | migrate --dry-run 输出待校准清单 | 不写回，只输出清单 |
| T9 | migrate 受控迁移生成回滚快照 | backup/ 下有快照目录 |

---

# 当前共识

- SG-001 设计方案已完成
- 核心改造：migrate_workspace.py 新增 migrate_business_data()
- 安全机制：dry-run 默认 + 回滚快照 + PM 确认


---

# SG-002 设计方案：计划 §4 模板补齐执行人/排期

> **需求编号**：SG-20260825-002  **优先级**：中  
> **一句话痛点**：plan-template §4 只有「阶段→状态」骨架，与规则「§4 从 WP §8 五列投影」不一致，照模板做就漏执行人/排期  

---

## 1. 问题根因

`plan-template.md` §4 示例（L40-58）：
```markdown
### WP-YYYYMMDD-NNN {WP 名称}
- 需求登记 → ⏳
- 测试 → ⏳
```
只有「阶段 → 状态」，无执行人/排期。

而 `00-pm-main-rules.md` §8d L620 要求：
> 计划 §4：各 WP 阶段列表，从 WP §8 投影落盘，禁止子行。空岗用 ⏳ / `⚠️待安排人`。

WP §8 五列：阶段 | 状态 | 执行人 | 排期 | 关键阶段。

**根因**：模板 vs 规则不一致。规则已正确，模板过简。

## 2. 设计方案

### 2.1 模板改动

`plan-template.md` §4 示例从：
```markdown
- 需求登记 → ⏳
- 测试 → ⏳
```

改为：
```markdown
- 需求登记 → ⏳｜⚠️待安排人｜— 待排期
- 需求调研 → ⏳｜⚠️待安排人｜— 待排期
- 需求规划 → ⏳｜⚠️待安排人｜— 待排期
- 需求评审 → ⏳｜⚠️待安排人｜— 待排期
- 需求确认 → ⏳｜⚠️待安排人｜— 待排期
- 方案设计 → ⏳｜⚠️待安排人｜— 待排期
- 用例设计 → ⏳｜⚠️待安排人｜— 待排期
- 开发 → 🔄（当前）｜储金晶（改bug）/王柏森（测试）｜2026-08-26~2026-09-15
- 预演 → ⏳｜⚠️待安排人｜— 待排期
- 测试 → ⏳｜⚠️待安排人｜— 待排期
- 内部验收 → ⏳｜⚠️待安排人｜— 待排期
- 试运行 → ⏳｜⚠️待安排人｜— 待排期
- 上线 → ⏳｜⚠️待安排人｜— 待排期
```

> 格式：`- 阶段名 → 图标｜执行人｜排期`  
> 执行人多人以「/」隔开，空岗写 `⚠️待安排人`  
> 排期=开始~结束，未排写 `— 待排期`

### 2.2 规则不改

`00-pm-main-rules.md` §8d L620 规则已正确，不需修改。

### 2.3 可选自检（不纳入主方案）

14 号可补 D-NEW-5：§4 每行含执行人/排期字段。放入"可选增强"，不阻塞主方案。

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `assets/templates/plan-template.md` | §4 示例行改为含执行人+排期+空岗占位的完整格式 | P0 |

## 4. 兼容方式

- 计划 §4 投影规则不变，只修模板
- 存量计划不受影响，重建时按新模板

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T1 | plan-template §4 含执行人/排期/空岗示例 | 模板每行有 `｜执行人｜排期` 格式 |
| T2 | 新建计划 §4 从 WP §8 投影含执行人 | 每行含阶段→图标｜执行人｜排期（关键阶段在 §3，§4 不是五列表） |

---

# 当前共识

- SG-002 设计方案已完成
- 核心改造：plan-template.md §4 示例补齐执行人+排期
- 规则不改，只修模板
- 可选自检项放入"可选增强"


---

# SG-003 设计方案：技能缺口输出改为单文件自足

> **需求编号**：SG-20260825-003  **优先级**：中  
> **一句话痛点**：P-SKILL-GAP 输出在需求正文外另加 manifest.md 批次外壳，违背"一个需求=一个自足文件"  

---

## 1. 问题根因

`gap-capture-rules.md` §1：
> Calls: 必须 CALL P-OUTPUT（建 `ai/outputs/{批次}/` + manifest + 登记 outputs/index.md）

`11-output-artifact-rules.md` §3 批次目录结构：
```
├── manifest.md       # 来源追溯清单
```

`CAPABILITY.md`：
> 产出：`ai/outputs/{批次}/需求-{短标题}.md` + manifest。

**根因**：输出约定在需求正文之外另设 manifest 批次外壳，元数据（batch_id/created_at/来源/revisions/archive）分散在 manifest，需求文件不自足。

## 2. 设计方案

### 2.1 输出约定变更

**旧**：`需求-{短标题}.md` + `manifest.md`（元数据在 manifest）

**新**：`需求-{短标题}.md`（元数据全部在 front matter，不再生成 manifest）

**关键约束（B-006 修复）**：
- **仅 Type=skill_gap 例外不建 manifest**；其他 P-OUTPUT（周报/Excel 等）仍按 11号 §3 默认结构建 manifest
- 11号 §3 批次目录结构保留 manifest.md 作为默认；§8 加 skill_gap 例外说明
- 不得全局移除 manifest，否则误伤所有生成物

### 2.2 需求文件 front matter 格式

```yaml
---
doc_type: skill-gap-demand
sg_id: SG-{今天}-NNN
batch_id: {YYYYMMDDHHMMSS}
request_type: skill_gap
user_request: [用户原话摘要]
skill_name: chrono-pm-project
skill_version_installed: 3.15.0
workspace_skill_version: 3.15.0
workspace_schema: 0.16.0
project: [项目名]
created_at: YYYY-MM-DD HH:MM:SS
priority: 高/中/低
source_files:
  - [来源文件路径1]
  - [来源文件路径2]
revisions:
  - rev-001 YYYY-MM-DD HH:MM 初稿
archive:
  archived_to: pending/confirmed
  archived_at: YYYY-MM-DD
  confirmed_by: [姓名]
---
```

### 2.3 存量兼容

- 存量 manifest.md 不删除，保留可读
- 新需求文件采用单文件自足格式
- outputs/index.md 兼容新旧格式

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `skill-gap-skill/references/gap-capture-rules.md` | §1 Calls 移除 manifest；§7 移除 manifest 步骤 | P1 |
| `skill-gap-skill/CAPABILITY.md` | 产出描述去掉 "+ manifest" | P1 |
| `references/11-output-artifact-rules.md` | **§3 默认结构保留 manifest.md**。§5/§8 加 Type=skill_gap 例外：不建 manifest，来源写在需求文件 front matter | P1 |
| `assets/templates/outputs-index-template.md` | Type=skill_gap 行格式调整 | P2 |
| `skill-gap-skill/assets/templates/skill-gap-demand-template.md` | front matter 补 batch_id / source_files / revisions / archive | P1 |
| `ChronoPM-Portfolio/assets/templates/skill-gap-demand-template.md` | 与 Project 模板锁步（集层拷贝用） | P1 |
| `references/23-procedure-index.md` | P-SKILL-GAP / P-OUTPUT：skill_gap 不要求 manifest | P1 |

## 4. 兼容方式

- 存量 manifest.md 不删除
- 新文件用新格式
- index 兼容新旧

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T3 | skill_gap 输出为单文件（无 manifest） | 只有 `需求-*.md`，无 manifest.md |
| T4 | 需求文件 front matter 含全部元数据 | batch_id/created_at/source_files 等齐全 |

---

# 当前共识

- SG-003 设计方案已完成
- 核心改造：移除 manifest，元数据并入需求文件 front matter
- 存量 manifest 不删除，兼容新旧格式


---

# SG-004 设计方案：PM 身份拆分（项目经理 vs 当前操作人）

> **需求编号**：SG-20260825-004  **优先级**：高  
> **一句话痛点**：pm_name 把"项目经理"和"对话里'我'是谁"混成单值，导致多 PM 无法区分、文件夹易主后"我的待办"错指  

---

## 1. 问题根因

`pm-profile-template.md` front matter：
```yaml
pm_name: "[PM 姓名或常用称呼/缩写]"
```

`21-pm-profile-rules.md` §2.4 L77：
> pm_name 用于"我"推导：对话中出现"我""我的待办"等第一人称时，AI 用 pm_name 推导指代对象。

**根因**：pm_name 单值承担双重职责（项目基本信息 + "我"推导钩子），无法表达多项目经理、无法随文件夹转移、无法区分实际操作人。

## 2. 设计方案

### 2.1 概念分离

```
pm_name（项目基本信息）     current_operator（运行时身份）
├── 记录实际掌控项目的经理   ├── 当前操作 AI 的人
├── 支持 1~2 位             ├── 单值
├── 初始化时询问             ├── 对话切换
├── 不用于"我"推导           ├── "我"以此为准
└── 禁止从岗位自动填充       └── 可随文件夹转移
```

### 2.2 交互流程

```
用户首次进入工作区 → AI 读 pm-profile.md
  ↓
检测 current_operator 为空 → 提示：「检测到当前操作人未设置，请问您是？」
  ↓
用户回复：「我是张三」→ AI 写入 current_operator=张三
  ↓
后续「查我的待办」→ 以 current_operator=张三 解析「我」
  ↓
用户切换：「以后是李四操作」→ 更新 current_operator=李四
  ↓
项目集场景：Portfolio 空间「我是张三」→ SUGGEST 建议更新清单（V-9），提示「在对应子项目 ChronoPM-Project 对话声明当前操作人」，不自动写子项目 pm-profile
```

### 2.3 身份推导规则（B-007 统一：空则 ASK，禁止回退）

| 场景 | 推导源 |
|---|---|
| "我""我的待办""给我安排" | **仅** current_operator |
| TD 编号人名缩写段 | **仅** current_operator |
| 项目基本信息"项目经理是谁" | pm_name（1～2 位，YAML 用 `A / B`） |
| current_operator 为空 | **一律 ASK**：「检测到当前操作人未设置，请问您是？」未声明前禁止把任何人当成「我」，**禁止**回退 pm_name |
| 项目集「我是张三」 | Portfolio **不得写**子项目。内部走 V-9，对外白话提示到对应项目 ChronoPM-Project 对话声明。禁止对用户说「建议更新清单」六字 |

**YAML**

```yaml
pm_name: "张三 / 李四"   # 1～2 位，斜杠分隔；存量单值保持原字符串
current_operator: ""     # 单值；空=未声明
```

存量单值 `pm_name: 张三` 升级时原样保留，只追加空的 `current_operator`。

### 2.4 存量升级（无兼容回退）

- 存量 pm-profile.md：保留 pm_name，追加 `current_operator:` 空字段
- 空字段 **不是** 兼容模式。第一次出现「我」必须 ASK 并写入后才能查「我的待办」
- 删掉任何「回退 pm_name 当我」的句子（含模板注释、21 号旧 §2.4、05 号若有）

### 2.5 禁止事项

- **禁止** AI 根据 todos 人员岗位自动填充/升格为项目经理
- **禁止** current_operator 为空时用 pm_name（之一）推导「我」或填 TD 人名段
- **禁止** Portfolio AUTO 写子项目 pm-profile（只读硬契约）

### 2.6 异常处理

| 异常 | 处理 |
|---|---|
| current_operator 为空且用户未声明 | ASK，本轮不把查询解析到任何人 |
| pm_name 有 2 位且 current_operator 为空 | 仍 ASK「您是谁」，不要改成「请二选一当我」（选操作人 ≠ 改项目经理名单） |
| 用户说「我是张三」但张三不在 pm_name | 允许，写入 current_operator（操作人可以不是项目经理） |
| 子项目 pm-profile.md 不存在 | Portfolio 列入 V-9，不代建 |

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `references/21-pm-profile-rules.md` | §2.4 重写：字段拆分 + 空则 ASK + 禁止岗位填充 + 项目集 SUGGEST | P0 |
| `assets/templates/pm-profile-template.md` | 新增 current_operator；pm_name 支持 `A / B`；**删除**「用 pm_name 推导我」注释 | P0 |
| `SKILL.md` | §4 事实源表加 current_operator；简单查询「我」须读该字段（可只读 profile，不载 21 全文） | P0 |
| `references/05-query-rules.md` | 「我的待办」Owner = current_operator；空则 ASK，不猜 pm_name | P0 |
| `scripts/init_workspace.py` | 初始化询问 current_operator（可与 pm_name 同一次问） | P1 |
| `scripts/migrate_workspace.py` | 存量补空 current_operator 字段 | P0 |
| `Portfolio/SKILL.md` | 「我是张三」走 V-9，对外白话，不写子项目 | P1 |
| `Portfolio/references/01-readonly-boundary-rules.md` | **保持不变** | - |

## 4. 兼容方式

- pm_name 字段保留，只作项目基本信息
- 存量补空 current_operator；**无回退**
- 字面「级联到所有子项目」已拍板降级为 SUGGEST

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T5 | pm-profile.md 含 current_operator 字段 | front matter 有 current_operator |
| T6 | 「我是张三」后「我的待办」按张三解析 | Owner=张三 |
| T7 | pm_name 不从岗位自动填充 | todos 岗位不升格为项目经理 |
| T10 | 项目集「我是张三」 | 对外白话；内部 V-9；**不**写子项目 pm-profile；不对用户说「建议更新清单」 |
| T10b | current_operator 为空时查「我的待办」 | ASK，不回退 pm_name |

---

# 当前共识

- SG-004：空则 ASK，禁止回退；级联 = V-9 SUGGEST
- 05 号与 SKILL 事实源必须改，否则简单查询仍用旧 pm_name


---

# SG-005 设计方案：AP 草稿文件强制约束（治理补正）

> **需求编号**：SG-20260825-005  **优先级**：高  
> **一句话痛点**：Skill 治理规则未强制约束 AP 草稿的数量、命名、存放位置，Agent 可自行拆分多个文件并存放在任意目录  

---

## 1. 问题根因

`16-skill-governance-rules.md` §2.1 L111 提到 `upgrade-plan-v*.md`，§19 定义 AP 生命周期，但均未强制约束：
1. 每个升级周期只能有 **1 个** AP 草稿文件
2. 命名必须严格为 `upgrade-plan-v{version}.md`，禁止附加后缀
3. 存放位置必须为 `governance-shared/planning/`

`governance-shared/planning/README.md` L7 措辞模糊：
> 草稿可以放这里或 `upgrade-plan-v*.md`。

可被理解为"放 planning 或放别处也行"，未形成强制约束。

**实际后果**：Agent 在 v3.15.0 升级过程中曾将方案拆分为多个文件存放在 `output/` 目录，但已归整为单文件存放到 `governance-shared/planning/upgrade-plan-v3.15.0.md`。

## 2. 设计方案

### 2.1 `16-skill-governance-rules.md` 新增 §21

在 §20（引用完整性约束）之后新增：

```markdown
## 21. AP 草稿文件强制约束

AP（升级方案审查文档）草稿在生成时必须遵守以下强制约束：

### 21.1 数量限制

每个升级周期只允许存在 **1 个** AP 草稿文件。
禁止因内容过长、按需求拆分、按模块拆分等任何理由将升级方案拆分为多个文件。
内容过长时采用对话内分块输出策略，而非拆分文件。

### 21.2 命名规范

AP 草稿文件必须命名为 `upgrade-plan-v{目标版本号}.md`。
- 版本号必须与目标升级版本一致（如目标 3.15.0 → `upgrade-plan-v3.15.0.md`）
- 禁止附加自定义后缀（如 `-requirements`、`-design-SG001`、`-review` 等）
- 禁止使用 CR 编号或其他命名格式

### 21.3 存放位置

AP 草稿必须存放在 `governance-shared/planning/` 目录。
- 禁止存放在 `output/`、代码空间根目录或其他任意目录
- 每个升级周期开始时，该目录下 AP 草稿（不含 README）应不超过 1 个；
  如有历史遗留须先确认清理再创建新草稿
```

### 2.2 `governance-shared/planning/README.md` L7 修正

从：
```
- 设计阶段：草稿可以放这里或 `upgrade-plan-v*.md`。
```
改为：
```
- 设计阶段：草稿必须放在本目录，命名为 `upgrade-plan-v{版本号}.md`，每周期限 1 个。
```

### 2.3 Agent 提示词侧（不纳入 Skill 改动）

Agent 提示词由用户自行修改，不在 Skill 代码仓内改动。

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `references/16-skill-governance-rules.md` | 新增 §21；**同时改 §2.1a L111**：设计阶段草稿路径写死为 `governance-shared/planning/upgrade-plan-v{version}.md`，去掉「或 AP 正文」可被读成任意路径的歧义 | P0 |
| `governance-shared/planning/README.md` | L7 改为：草稿必须放在本目录，命名 `upgrade-plan-v{版本号}.md`，每周期限 1 个 | P0 |

## 4. 兼容方式

- 纯治理约束新增，不影响现有能力
- 存量 AP 草稿按 R10 生命周期管理，新约束从下个升级周期生效

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T11 | 16 号 §21 存在且含数量/命名/位置三项约束 | 三小节齐全 |
| T12 | planning/README.md L7 无歧义 | 不含"或"字，明确唯一位置 |

---

# 当前共识

- SG-005 设计方案已完成
- 核心改造：16 号新增 §21 + planning/README 消除歧义
- Agent 提示词侧由用户自行修改，不纳入 Skill 改动

---

# SG-006 设计方案：examples 重编号 + 示例质量约束

> **需求编号**：SG-20260825-006  **优先级**：中  
> **一句话痛点**：examples 目录序号不合理（01 升级在 03 初始化之前），且示例内容全是空对话无场景描述，可读性差  

## 1. 问题根因

### 1.1 顺序错误

当前 examples 目录编号：
```
01-升级工作区.md        ← 升级前必须先有工作区
02-处理待确认事项.md    ← 承接升级后的旧账
03-初始化工作区.md      ← 新项目第一步，应排第 1
...
```

逻辑上必须先初始化才能升级，但当前 01 是升级、03 是初始化。

### 1.2 跨引用未同步

- `02-处理待确认事项.md` 引用 `01-升级工作区.md` → 升级后需改为 `02-升级工作区.md`
- `17-复盘和成本.md` 引用 `03-初始化工作区.md` → 升级后需改为 `01-初始化工作区.md`

### 1.3 示例质量低

所有 examples 文件只有「你」「助手」的对话模板，缺少真实业务场景背景，用户看不懂为什么要这样做。

例如 `06-记日报.md`：
```markdown
## 全过程

**你**

> 周启今天日报如下……

**助手**

> 市民端那段不写入大厅；担心先问是风险还是已经卡住
```

没有说明"周启是谁""为什么会有日报""为什么要区分市民端"等背景信息。

## 2. 设计方案

### 2.1 examples 目录重编号

| 新编号 | 原编号 | 文件名 | 分组 |
|---|---|---|---|
| 01 | ~~03~~ | 初始化工作区 | 先把家安好 |
| 02 | ~~01~~ | 升级工作区 | 先把家安好 |
| 03 | ~~02~~ | 处理待确认事项 | 先把家安好 |
| 04 | ~~04~~ | 投喂合同和立项 | 材料进得来 |
| 05 | ~~16~~ | 一份材料拆到多个项目 | 材料进得来 |
| 06 | ~~05~~ | 确认需求和工作包 | 材料进得来 |
| 07 | ~~06~~ | 记日报 | 每天怎么管 |
| 08 | ~~07~~ | 记会议纪要 | 每天怎么管 |
| 09 | ~~12~~ | 人员进出和结转 | 每天怎么管 |
| 10 | ~~08~~ | 登记风险和问题 | 每天怎么管 |
| 11 | ~~09~~ | 倒排上线计划 | 怎么看全局 |
| 12 | ~~10~~ | 出周报和问进度 | 怎么看全局 |
| 13 | ~~11~~ | 项目集总览 | 怎么看全局 |
| 14 | ~~13~~ | 改需求和范围 | 偶尔才做 |
| 15 | ~~14~~ | 完整性巡检 | 偶尔才做 |
| 16 | ~~15~~ | 词库 | 偶尔才做 |
| 17 | ~~17~~ | 复盘和成本 | 偶尔才做 |
| 18 | ~~18~~ | 导入历史计划 | 偶尔才做 |
| 19 | ~~19~~ | 派活与拆文件入库 | 偶尔才做 |
| 20 | ~~20~~ | 技能缺口 | 偶尔才做 |

### 2.2 README.md 同步更新

`examples/README.md` 中的 mermaid 图和表格全部按新编号更新。

### 2.3 跨引用同步更新

| 文件 | 原引用 | 新引用 |
|---|---|---|
| 02-处理待确认事项.md | `[01-升级工作区.md](01-升级工作区.md)` | `[02-升级工作区.md](02-升级工作区.md)` |
| 17-复盘和成本.md | `[03-初始化工作区.md](03-初始化工作区.md)` | `[01-初始化工作区.md](01-初始化工作区.md)` |

### 2.4 16 号规则新增 §22：examples 示例生成标准约束

```markdown
## 22. examples 示例生成标准约束

examples 目录下的示例文件必须遵守以下质量标准：

### 22.1 必须有场景背景

每个示例必须在开头说明：
- 假项目名称（如"星河市民服务平台 · 办事大厅"）
- 项目经理/组员姓名
- 业务背景（为什么要做这件事）
- 前置条件（依赖哪些已完成的操作）

禁止只有「你」「助手」的空对话，无场景说明。

### 22.2 必须有完整流程

每个示例必须包含：
- 全过程流程图（mermaid）
- 至少一轮完整对话（你开口 → 助手回应 → 你裁定 → 助手执行）
- 关键决策点的解释（为什么选 A 不选 B）

### 22.3 必须可独立阅读

读者无需查阅其他示例即可理解本示例的内容。如需引用其他示例，必须提供链接。

### 22.4 必须与实际能力一致

示例中展示的能力必须是 Skill 当前已实现的，不得演示未实现的功能。
```

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `examples/01-初始化工作区.md`（原 03） | 重命名 | P0 |
| `examples/02-升级工作区.md`（原 01） | 重命名 + 内部引用更新 | P0 |
| `examples/03-处理待确认事项.md`（原 02） | 重命名 + 内部引用更新 | P0 |
| `examples/04-投喂合同和立项.md` | 保持不变 | - |
| `examples/05-一份材料拆到多个项目.md`（原 16） | 重命名 | P0 |
| `examples/06-确认需求和工作包.md`（原 05） | 重命名 | P0 |
| `examples/07-记日报.md`（原 06） | 重命名 | P0 |
| `examples/08-记会议纪要.md`（原 07） | 重命名 | P0 |
| `examples/09-人员进出和结转.md`（原 12） | 重命名 | P0 |
| `examples/10-登记风险和问题.md`（原 08） | 重命名 | P0 |
| `examples/11-倒排上线计划.md`（原 09） | 重命名 | P0 |
| `examples/12-出周报和问进度.md`（原 10） | 重命名 | P0 |
| `examples/13-项目集总览.md`（原 11） | 重命名 | P0 |
| `examples/14-改需求和范围.md`（原 13） | 重命名 | P0 |
| `examples/15-完整性巡检.md`（原 14） | 重命名 | P0 |
| `examples/16-词库.md`（原 15） | 重命名 | P0 |
| `examples/17-复盘和成本.md`（原 17） | 重命名 + 内部引用更新 | P0 |
| `examples/18-导入历史计划.md` | 保持不变 | - |
| `examples/19-派活与拆文件入库.md` | 保持不变 | - |
| `examples/20-技能缺口.md` | 保持不变 | - |
| `examples/README.md` | mermaid 图 + 表格全部更新 | P0 |
| `references/16-skill-governance-rules.md` | 新增 §22：examples 示例生成标准约束 | P1 |

### 2.5 C-4 与 §22 不追溯的拍板（B-008）

**二选一已拍：存量豁免，不把 20 个示例正文补到 §22。**

- §22 从 **本版之后新写的示例** 生效
- 本版 examples **只**重编号 + README mermaid/表格 + 已点名的两处跨引用（施工时全目录再扫 `](0\d-`）
- 不补场景背景、不补 mermaid、不改对话骨架
- `20-技能缺口.md` 正文不改（现网未写 manifest）

## 4. 兼容方式

- 纯文档重编号，不影响现有能力
- 存量 examples 文件内容不变，只改文件名和内部引用
- §22 不追溯已有示例

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T13 | examples 目录按新编号排列 | 01 初始化→02 升级→...→20 技能缺口 |
| T14 | README.md mermaid 图正确 | 分组与编号对应 |
| T15 | README.md 表格正确 | 所有链接指向正确文件 |
| T16 | 跨引用同步更新 | 02 引用 02、17 引用 01 |
| T17 | 16 号 §22 存在 | 含 4 项子约束 |

---

# 当前共识

- SG-006 设计方案已完成
- 核心改造：examples 重编号 + README 同步 + 16 号新增 §22
- 不涉及内容修改，只改文件名和引用

---

# SG-007 设计方案：收尾检查清单补强

> **需求编号**：SG-20260825-007  **优先级**：高  
> **一句话痛点**：每次升级发布前，缺乏对 README/SKILL_MODULE_MAP/examples 一致性的强制检查，导致版本信息不一致、模块图过时、示例顺序错误等问题遗漏到发布后才发现  

## 1. 问题根因

### 1.1 README 版本不一致

中英文 README 的版本号、能力描述可能未及时更新，与 skill.json 不一致。

### 1.2 SKILL_MODULE_MAP.md 过时

模块链路图未反映最新架构变更（如 G5 计划投影机制、G4 WP §7/§8 等）。

### 1.3 examples 未检查

示例顺序、内容正确性无强制检查项。

### 1.4 release-checklist.md 引用路径错误

`16-skill-governance-rules.md` §14（L299）引用了 `governance/review-checklists/release-checklist.md`，该路径在 Project 内不存在。**但**真实文件已存在于 `governance-shared/review-checklists/release-checklist.md`（186行，内容完整）。

**根因**：16号 §14 引用路径写错（应为 `governance-shared/` 而非 `governance/`），导致断链。

**修正策略**：不新建文件，而是修订 16号 §14 引用路径指向已存在的 `governance-shared/review-checklists/release-checklist.md`，并在该现有文件上追加 A 要新增的 4 项检查（README/SKILL_MODULE_MAP/examples 顺序+内容/质量标准）。

## 2. 设计方案

### 2.1 修订 16号 §14 引用路径 + 在现有清单追加 4 项检查

**步骤 1**：修订 `references/16-skill-governance-rules.md` §14 L299，将引用路径从 `governance/review-checklists/release-checklist.md` 改为 `governance-shared/review-checklists/release-checklist.md`。

**步骤 2**：在 `governance-shared/review-checklists/release-checklist.md` 末尾追加以下 4 项检查（插入到 D5 AP草稿清理之后、C版本同步之前）：

```markdown
## C-1. README 一致性检查（v3.15.0 新增）

- [ ] VERSION 文件版本号 = skill.json version = SKILL.md frontmatter = README.md 标题 = README.en.md 标题
- [ ] SKILL.md 版本控制表最新条目正确
- [ ] SKILL_BLUEPRINT.md §1 版本号正确
- [ ] skill.json blueprint.lastVersion 正确
- [ ] CHANGELOG.md 最新版本段存在且正确
- [ ] 中英文 README 能力描述与 skill.json 一致

## C-2. SKILL_MODULE_MAP.md 一致性检查（v3.15.0 新增）

- [ ] G5 计划图包含投影机制（§3 六列 + §4 阶段列表）
- [ ] G4 确认 WP 图包含 §7 状态链 + §8 阶段执行人
- [ ] G13 查询图包含四条新路由 + 闸 2
- [ ] Track C 生成物落盘图存在
- [ ] 所有图与实际能力一致

## C-3. examples 正确性检查（v3.15.0 新增）

- [ ] examples 目录按逻辑流程编号（01 初始化→02 升级→...→20 技能缺口）
- [ ] examples/README.md mermaid 图与编号对应
- [ ] examples/README.md 表格链接指向正确文件
- [ ] 跨引用同步更新（02→02、17→01）

## C-4. examples 质量标准检查（v3.15.0：存量豁免场景/mermaid）

本版强制（不豁免）：
- [ ] 编号按逻辑流程（01 初始化→02 升级→…→20 技能缺口）
- [ ] README mermaid / 表格链接正确
- [ ] 跨引用已更新
- [ ] 示例不演示当前 Skill 未实现的能力

本版豁免（§22 不追溯）：
- 存量示例可以没有独立「场景背景」段
- 存量示例可以没有 mermaid
```

**注意**：上述 4 项检查应作为 Release Checklist 的一部分，与其他检查项一起执行，不单独创建文件。

### 2.2 16 号规则 §14 补充引用路径修正

在 `references/16-skill-governance-rules.md` §14 末尾补充：

```markdown
### 14.1 引用路径修正

16号 §14 引用路径从 `governance/review-checklists/release-checklist.md` 修订为 `governance-shared/review-checklists/release-checklist.md`（实际存放位置）。

### 14.2 新增强制检查项

发布前必须额外完成以下 4 项检查（已在 release-checklist.md 中追加），全部通过后才能进入基线快照环节：

| 检查项 | 检查内容 | 检查方式 |
|---|---|---|
| README 一致性 | 中英文 README 版本号、能力描述与 skill.json 一致 | 人工核对 + audit 断言 |
| SKILL_MODULE_MAP 一致性 | 模块链路图反映最新架构变更 | 人工核对 |
| examples 顺序+内容 | 示例按逻辑流程编号，跨引用同步更新 | 人工核对 + audit 断言 |
| examples 质量标准 | 本版：顺序+跨引用+不演示未实现能力。场景/mermaid **存量豁免** | 人工核对 |

以上 4 项检查的详细内容见 `governance-shared/review-checklists/release-checklist.md`（C-1~C-4 节）。
```

### 2.3 收尾流程新增检查门禁

在 `16-skill-governance-rules.md` §2（强制变更流程）第 11 步"验证"中补充：

```
11. 验证：检查根目录白名单合规性；检查正式文档中是否存在幽灵引用；检查文档内版本号一致性；验证历史污染已清除；**执行 governance-shared/review-checklists/release-checklist.md 中的所有检查项（包括 README 一致性、SKILL_MODULE_MAP 一致性、examples 顺序+内容、examples 质量标准）**
```

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `governance-shared/review-checklists/release-checklist.md` | 追加 C-1~C-4 四项检查（非新建） | P0 |
| `references/16-skill-governance-rules.md` | §14 修订引用路径 + 新增 §14.1/§14.2 + §2 第 11 步补充 | P0 |

## 4. 兼容方式

- 纯检查清单追加，不影响现有能力
- release-checklist.md 从 v3.15.0 开始生效（追加部分）
- 存量版本不受影响

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T18 | release-checklist.md 含 C-1~C-4 四项检查 | 文件存在且追加了 4 项新检查 |
| T19 | 16 号 §14 引用路径正确 | 指向 governance-shared/review-checklists/ |
| T20 | 16 号 §2 第 11 步含 release-checklist 引用 | 文本存在 |

---

# 当前共识

- SG-007 设计方案已完成
- 核心改造：修订 16号 §14 引用路径 + 在现有 release-checklist.md 追加 C-1~C-4 四项检查
- 纯检查清单追加，不影响现有能力

---

# SG-008 设计方案：Python 环境检测与 AI 引导安装

> **需求编号**：SG-20260825-008  **优先级**：中  
> **一句话痛点**：用户电脑未装 Python 时，执行脚本直接报错且无友好指引，导致初始化/升级/巡检等功能无法使用，用户体验差  

## 1. 问题根因

### 1.1 当前行为

SKILL.md §5.1 直接调用 `python "scripts/init_workspace.py" ...`，若用户无 Python 环境：
- **Windows**：`'python' 不是内部或外部命令` → 执行失败
- **Mac/Linux**：`command not found: python` → 执行失败
- **AI 反应**：可能检测到错误，但**不会主动引导安装**，用户需自行搜索教程

### 1.2 影响范围

| 功能 | 是否依赖 Python | 影响 |
|---|---|---|
| 初始化工作区 | ✅ | 无法初始化 |
| 升级迁移 | ✅ | 无法自动迁移 |
| 版本同步 | ✅ | 版本号不同步 |
| 完整性巡检（19号） | ✅（若挂脚本） | 无法自动校验 |
| 日常记待办/查进度 | ❌ | 不受影响 |

**结论**：低频治理操作受影响，高频日常操作不受影响。

## 2. 设计方案

### 2.1 SKILL.md 中加入前置检查提示

在 `SKILL.md` §5.1 初始化前新增 §5.0 环境检测：

```markdown
### 5.0 环境检测（首次使用前）

在执行任何操作前，请先确认 Python 环境：

```bash
# Windows
python --version
# 或
python3 --version
```

**若输出类似 `Python 3.x.x`** → ✅ 环境正常，继续下一步  
**若报错 `'python' 不是内部或外部命令`** → ❌ 需安装 Python

**需要我帮你安装 Python 吗？**

- 回复“是”，我将生成安装命令供你执行
- 回复“否”，请自行安装后继续
```

### 2.2 AI 主动引导安装流程

当用户回复“是”或 AI 检测到 Python 错误时，输出：

```markdown
好的，我来帮你安装 Python 3.12（只需 3 分钟）。

## Windows 用户

请复制以下命令到 PowerShell 执行：

```powershell
winget install Python.Python.3.12 --silent
```

执行完后告诉我“已完成”。

## Mac 用户

```bash
brew install python3
```

## Linux 用户

```bash
sudo apt update && sudo apt install python3
```

---

**安装验证**：

装完后执行 `python --version`，应显示 `Python 3.12.x`。

需要我帮你检查是否安装成功吗？
```

### 2.3 版本要求明确化

在 `SKILL.md` 开头或 README 中明确标注：

```markdown
## 前置要求

- **最低版本**：Python 3.9（与双包 skill.json `"python": ">=3.9"` 对齐）
- **推荐版本**：Python 3.10+（性能更好，长期支持）
- **兼容性**：Python 3.9-3.12 完全兼容，无破坏性变更

若未安装，AI 可引导你快速安装（3 分钟）。
```

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `SKILL.md` | §5.0 新增环境检测 + §5.1 前置检查提示 | P0 |
| `README.md` / `README.en.md` | 新增 Python 版本要求说明 | P1 |

## 4. 兼容方式

- 纯文档/提示词变更，不影响现有能力
- 不修改脚本代码，无破坏性变更
- 有 Python 的用户无感知，无 Python 的用户获得友好指引

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T21 | SKILL.md §5.0 存在 | 含环境检测指引 |
| T22 | AI 检测到 Python 错误时主动引导 | 输出安装命令 |
| T23 | 用户回复“是”后 AI 生成分平台命令 | Windows/Mac/Linux 均有 |
| T24 | README 标注 Python 版本要求 | 最低 3.9（与 skill.json 一致），推荐 3.10+ |

---

# 当前共识

- SG-008 设计方案已完成
- 核心改造：SKILL.md 新增 §5.0 环境检测 + AI 引导安装流程
- 纯文档/提示词变更，不修改脚本代码

---

# SG-009 设计方案：全量数据一致性断言体系

> **需求编号**：SG-20260825-009  **优先级**：高  
> **一句话痛点**：ChronoPM 多处要求数据强一致性（WP→计划→索引、待办结转链、需求↔WP↔计划关联等），但当前全靠模型自觉对账，弱模型下静默出错率高，需机器断言守护  

## 1. 问题根因

### 1.1 当前行为

00号规则 §8c 定义了完整的级联传播规则表（L560-576），要求：
- WP 修改 → 同步计划 §3/§4 + 索引
- 待办日期变更 → 可能影响 WP 时间盒
- 需求工作包变更 → 同步 WP 关联
- 合同范围变更 → 三级联动（合同→需求→WP）

**但当前实现全靠模型自觉**：
- 闸 2 对账（L26）：AI 读计划前自行对账 6 项
- 写后必检（L502）：AI 改 WP 后自行输出级联完整性验证
- **无机器断言**：若 AI 漏步/错判，无感知

### 1.2 影响场景全景图

| 级联链 | 触发频率 | 错误率估算 | 调试成本 |
|---|---|---|---|
| **C1-C8：WP→计划→索引投影** | 每次改 WP/计划 | ~10-30% | 5-30 分钟 |
| **D-TODO-01/02/03：待办结转链条** | 每次记日报/查待办 | ~10-20% | 10-30 分钟 |
| **D-TODO-WP-01：待办日期→WP 时间盒** | 每次改待办日期 | ~5-10% | 5-15 分钟 |
| **D-REQ-WP-01/02：需求↔WP 关联** | 每次改需求/WP | ~5-10% | 5-15 分钟 |
| **D-CONTRACT-01/02：合同↔需求↔RI** | 每次改合同/需求 | ~3-5% | 10-20 分钟 |
| **D-RESOURCE-01/02：人员进出组** | 人员变动时 | ~2-3% | 5 分钟 |

**结论**：高频场景（C1-C8、D-TODO）ROI 最高，应优先纳入。

## 2. 设计方案

### 2.1 全量断言清单（一次性纳入）

按 00号 §8c 级联传播规则表（L560-576）全覆盖设计：

| 断言组 | 检查内容 | 脚本 | ROI | 优先级 |
|---|---|---|---|---|
| **C1-C8** | WP→计划→索引投影 | `verify_projection.py` | 80:1 | P0 |
| **D-TODO-01/02/03** | 待办结转链条连续性 | `verify_todo_continuity.py` | 60:1 | P0 |
| **D-TODO-WP-01/02** | 待办日期→WP 时间盒冲突 | （合入 verify_projection.py） | 40:1 | P0 |
| **D-REQ-WP-01/02** | 需求↔WP 关联双向闭环 | `verify_requirement_wp.py` | 10:1 | P1 |
| **D-CONTRACT-01/02** | 合同↔需求↔RI 映射 | `verify_contract_ri.py` | 12:1 | P1 |
| **D-SOURCE-01** | sources 索引同步 | （合入 verify_requirement_wp.py） | 8:1 | P2 |
| **D-PLAN-REF-01** | WP plan_ref 三处一致 | （合入 verify_projection.py） | 15:1 | P1 |
| **D-EFFECT-01** | 废弃 WP 清理完整性 | （合入 verify_projection.py） | 20:1 | P1 |

**本轮分档（X-4 拍板，禁止「全量 vs 3 类」并存）**：

| 档 | 脚本 | 断言 | 3.15.0 | 19 号自动跑 |
|---|---|---|---|---|
| **P0** | `verify_projection.py` | C1–C8 + D-TODO-WP-01/02 + D-PLAN-REF-01 + D-EFFECT-01 | 进包 | **是** |
| **P0** | `verify_todo_continuity.py` | D-TODO-01/02/03 | 进包 | **是** |
| **P1** | `verify_requirement_wp.py` | D-REQ-WP-01/02 + D-SOURCE-01 | 进包，可手动 `--root` | 否 |
| **P1** | `verify_contract_ri.py` | D-CONTRACT-01/02 | 进包，可手动 `--root` | 否 |

D-RESOURCE-01/02：**本版不做**（影响表有、无脚本、无测试）。

4 个脚本都进 3.15.0 分发包。日常巡检只自动跑 P0。

### 2.2 断言详细设计

#### **C1-C8：WP→计划→索引投影**

基于 00号 L26 闸 2 对账逻辑（6项）+ 索引状态 + 废弃清理，共 8 项断言：

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| C1 | WP 文件存在性 | 计划 §3 每个 WP 编号 → `wps/WP-*.md` 必须存在 | 全部存在 |
| C2 | 当前状态 == 链尾阶段名 | 计划 §3「当前状态」列 ↔ WP §7 链尾阶段名；若链尾「已完成」→ 取 §8 最后一个 ✅ 或 🔄 的阶段名 | 归一后相等 |
| C3 | 执行人 == §8 当前 🔄 执行人 | 计划 §3「执行人」列 ↔ WP §8 当前 🔄 执行人；无 🔄 则取最后一个 ✅；未排=`⚠️待安排人` | 归一后相等 |
| C4 | 排期 == WP 开始~结束 | 计划 §3「排期」列 ↔ WP **§1 基本信息表**「开始时间」~「结束时间」（不是 YAML `start_date`/`end_date`，现网模板无这两字段） | 相等 |
| C5 | 关键阶段 == §8 标记「是」的阶段名 | 计划 §3「关键阶段」列 ↔ WP §8 「关键阶段=是」的阶段名；多→顿号分隔 | 集合相等 |
| C6 | 计划 §4 该 WP 列表 == WP §8 全表 | 计划 §4 下该 WP 的阶段列表 ↔ WP §8 全表；含阶段序 + 图标（✅/🔄/⏳） | 逐项相等 |
| C7 | `_index.md` 状态列 == 四枚举 / 废弃 | `_index.md` 「状态」列 ∈ {未开始/进行中/已完成/已暂停} 或 `废弃`；看 `effect` 字段 | 相等 |
| C8 | 投影方向防呆 | 正常计划 §3/§4 与 WP 不一致 → **只校验不自动改**；若计划与 WP 同时与其源变化→报警 | 一致或报警 |

**实施细节**：
- 脚本名：`verify_projection.py`
- 输入：`--root <工作区根>` + `--scope <all\|wp:WP-xxx\|plan:PLAN-xxx>`（可选）
- 输出：差异清单 + 退出码：`0` 全部一致 / `1` 存在差异 / `2` 存在不可判（待校准）
- 安全约束：**只读不改盘**；脏数据→「待校准」非「错误」
- 性能：只扫工作包 + 正常计划，不全局扫待办

#### **D-TODO-01/02/03：待办结转链条连续性**

对照日 = **最新合法日**（`date≤今天` 且存在 `_index.md` 的最大日期），**不是日历昨天**。花名册 = 该日 `_index` §1。

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-TODO-01 | 应建档文件连续性 | 最新合法日 §1 **六态除已出组** → 今天必须有 `{姓名}.md` | 豁免 **仅已出组**。无待办无能耗 **不豁免**（与 22 号人人一份、§1 可空一致） |
| D-TODO-02 | 未办结待办滚存 | 对照日该人核心表中状态 ∉ {已完成, 已取消, 已转出} 的 TD → 今天该人文件必须出现同一 TD 号 | 编号集合 ⊆ 今天；允许对照日后人工已取消。失败留表的人标不可判（退出 2），不要求两日集合全等 |
| D-TODO-03 | 能耗段连续性 | 对照日该人有 §0.6 → 今天该人文件必须有 §0.6 | 文件存在 + 段落存在 |

**实施细节**：
- 脚本名：`verify_todo_continuity.py`
- 输入：`--root <工作区根>` + `--date <YYYY-MM-DD>`（可选，默认今天）
- 输出：差异清单 + 退出码（0=一致 / 1=差异 / 2=不可判）
- 性能：扫描 `todos/` 目录树，~2-5 秒/次

#### **D-TODO-WP-01/02：待办日期→WP 时间盒冲突**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-TODO-WP-01 | 待办结束 > WP 结束 | 待办 §1.1「结束时间」> WP §1「结束时间」 | 待办结束 ≤ WP 结束，或已按 00 §8c 问过 A/B/C。脚本只报差异，不改期 |
| D-TODO-WP-02 | 待办开始 < WP 开始 | 待办 §1.1「开始时间」< WP §1「开始时间」 | 轻提示不阻断（允许提前准备） |

**实施细节**：
- 合入 `verify_projection.py`（同属 WP 相关校验）
- 只检查本轮涉及的待办（通过 WP Ref 反向查找），禁止全库扫
- 性能：~1-3 秒/次

#### **D-REQ-WP-01/02：需求↔WP 关联双向闭环**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-REQ-WP-01 | 需求工作包 ↔ WP 存在性 | 需求登记册「工作包」列中的 WP 编号 → 必须在 `wps/` 下存在对应文件 | 双向引用闭环 |
| D-REQ-WP-02 | WP 关联需求 ↔ 需求登记册 | WP §2 「需求编号」表 + §1 「关联需求」→ 必须在需求登记册中存在对应条目 | 集合相等 |

**实施细节**：
- 脚本名：`verify_requirement_wp.py`
- 输入：`--root <工作区根>` + 可选 `--scope wp:WP-xxx\|req:REQ-xxx`
- 输出：差异清单 + 退出码
- 性能：~3-8 秒/次（需解析需求登记册 + WP 文件）

#### **D-CONTRACT-01/02：合同↔需求↔RI 映射**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-CONTRACT-01 | 需求/Canonical 引用的合同号必须能在合同登记册找到 | 读 `requirements/contract-register.md` 的 Contract ID。需求「来源」或 Canonical `contract_refs` / 范围归属 `in_contract(CON-xxx)` 里的合同号 → 登记册必须有该行 | 需求侧引用 ⊆ 登记册 ID。登记册不必每份合同都有需求行。superseded 须有 superseded_by |
| D-CONTRACT-02 | 合同「拆解文件夹指针」非空则目录存在 | 登记册「拆解文件夹指针」≠ `-` → `requirements/sources/{编号}/meta.md` 存在 | 指针有值则文件在；空指针不报 |

**实施细节**：
- 脚本名：`verify_contract_ri.py`
- 输入：`--root <工作区根>` + 可选 `--scope contract:CTR-xxx|req:REQ-xxx`
- 输出：差异清单 + 退出码
- 性能：~2-5 秒/次（需解析合同登记册 + 需求登记册 + sources 索引）

#### **D-SOURCE-01：sources 索引同步**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-SOURCE-01 | sources 目录 ↔ _index.md | `sources/{编号}/meta.md` 存在 → `_index.md` 必须有对应行；反之亦然 | 存在性一致 |

**实施细节**：
- 合入 `verify_requirement_wp.py`
- 扫描 `sources/` 目录 + `_index.md`
- 性能：~1-2 秒/次

#### **D-PLAN-REF-01：WP plan_ref 三处一致**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-PLAN-REF-01 | WP plan_ref 与正常计划互指 | 定位 = YAML `plan_ref` **∪** 扫描全部正常 PLAN 头+§3（**禁止只信 plan_ref**）。YAML 空但某正常 PLAN §3 仍列该 WP → 报差异（退出 1），不自动补 YAML。多值：`split(" / ")` 后去空白，逐个比 | 互指闭合 |

**实施细节**：
- 合入 `verify_projection.py`
- 检查每个 WP 的 plan_ref 在三个位置的一致性
- 性能：~1-2 秒/次

#### **D-EFFECT-01：废弃 WP 清理完整性**

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| D-EFFECT-01 | 废弃 WP 从正常计划移除 | **缺 `effect` 当正常**（对齐闸 2）。仅 `effect=废弃`：所有正常计划 §3/§4/§6 不得出现该 WP；index 状态列=`废弃`；plan_ref 去掉。用户认为该废但 effect=正常 → 脚本不自动废，只报「可 RETIRE」不可判（退出 2） | 废弃者清除；缺省当正常 |

**实施细节**：
- 合入 `verify_projection.py`
- 扫描所有正常计划，确认无废弃 WP
- 性能：~2-4 秒/次

### 2.3 挂载点设计

| 阶段 | 挂载位置 | 语义 |
|---|---|---|
| **阶段 1（本方案）** | 19 号完整性巡检旁路 | 巡检前先跑断言脚本，以脚本输出替代"模型自述无遗漏"；只读、零副作用 |
| **阶段 2（后续）** | 00 号 §8c.2 写后必检整合 | 写后运行 `verify --scope=本轮回合涉及WP/待办`；不一致→输出差异；不可判→模型给复核结论 |
| **阶段 3（可选强化）** | 编排强制 | 把 L502「跳过则标注⚠️」改为「**跳过=阻塞**」：改 WP/待办后必须 verify 通过才可继续 |

### 2.4 脚本架构设计

```python
# verify_projection.py（扩展版）
# 包含 C1-C8 + D-TODO-WP-01/02

# verify_todo_continuity.py（新增）
# 包含 D-TODO-01/02/03
```

**共同特性**：
- standalone，命令式只读校验器
- Python 3.9+，无第三方依赖
- 输入：`--root <工作区根>` + 可选 scope
- 输出：差异清单 + 退出码（0/1/2）
- 安全约束：**只读不改盘**；脏数据→「待校准」非「错误」

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `scripts/verify_projection.py` | 新建（含 C1-C8 + D-TODO-WP-01/02 + D-PLAN-REF-01 + D-EFFECT-01） | P0 |
| `scripts/verify_todo_continuity.py` | 新建（含 D-TODO-01/02/03） | P0 |
| `scripts/verify_requirement_wp.py` | 新建（含 D-REQ-WP-01/02 + D-SOURCE-01） | P1 |
| `scripts/verify_contract_ri.py` | 新建（含 D-CONTRACT-01/02） | P1 |
| `references/19-info-completeness-rules.md` | 新增断言脚本挂载说明 | P1 |
| `references/00-pm-main-rules.md` | §8c.2 补充脚本调用指引（阶段 2） | P2 |
| `tests/fixtures/` | 新增正反样例夹具（T1-T46） | P1 |

## 4. 兼容方式

- 纯脚本新增，不影响现有能力
- 阶段 1 为旁路挂载，零副作用
- 有 Python 的用户享受完整保护，无 Python 的用户降级为模型自检（SG-008 已解决）

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T25 | verify_projection.py 正例 | WP↔计划↔index 全一致 → 退出 0 |
| T26 | verify_projection.py 反例 | 改 WP §8 执行人但计划§3 不同步 → 报 C3 差异，退出 1 |
| T27 | verify_projection.py 脏链尾 | WP §7 链尾「已完成」但 §8 有 ✅/🔄 → C2 正确取末状态，不误报 |
| T28 | verify_projection.py 同义词 | 计划/§8 含别名 → C6 等价判定，不误报 |
| T29 | verify_projection.py 待办越窗 | 待办结束 > WP 结束 → D-TODO-WP-01 报警 |
| T30 | verify_todo_continuity.py 正例 | 人员文件连续 + 待办滚存 + 能耗延续 → 退出 0 |
| T31 | verify_todo_continuity.py 反例 | 最新合法日有未办结待办但今天文件缺失 → 报 D-TODO-02，退出 1 |
| T32 | verify_todo_continuity.py 能耗断链 | 最新合法日有 §0.6 但今天文件缺失 → 报 D-TODO-03，退出 1 |
| T33 | 只读性 | 跑完比对文件 mtime/内容 → 无任何写盘 |
| T34 | 版本触点 | 脚本随版本同步 → sync_version / 回归通过 |

---

# 当前共识

- SG-009：4 脚本都进 3.15.0。P0（projection + todo_continuity）挂 19 号；P1 可调用不自动跑
- C1–C8 定义在本方案 SG-009 §2.2（不是 SG-008）
- D-RESOURCE 本版不做

---

# SG-010 设计方案：日报投喂全员结转硬阻断

> **需求编号**：SG-20260825-010  **优先级**：高  
> **一句话痛点**：AI 执行「日报投喂」时只给今天提交日报的人建当天文件并结转，遗漏了其余在册人员的未办结待办结转，导致日后逐个补结转浪费时间、数据不一致  

## 1. 问题根因

### 1.1 现象复现

**场景**：全链通重构项目在册人员 35 人，PM 投喂了 5 人（朱嵩、陈浩源、陈龙、王欢欢、周贤虎）的日报。

| 维度 | 用户期望 | AI 实际行为 |
|---|---|---|
| **建档范围** | 只要 1 人触发新一天，应建档全员一起建档+结转（同一起跑线） | 只建档当天被读写（投喂日报/派活）的 5 人，其余 30 人当日无文件 |
| **结转节奏** | 全员一次结转完成，后续不用再逐个补结转 | 其余 30 人的未办结待办未被结转，等各自下次被读写才补 |
| **完整性闸** | `_index.md` 应有 35 人、`carryover_done_for_today=true` 仅当全员齐全才置位 | 5 人时就写了「应建档 5 人」并置 `true`，误导为当日已完整 |

### 1.2 后果

1. **数据不一致**：30 人当天没有结转文件，`_index.md` 花名册与 `todos/` 实际文件数量不符
2. **效率浪费**：未办结待办结转被拆分到不同日期，后续每次读写某人都要单独补结转，累计浪费大量对账时间
3. **状态错位**：若中途有人出组或跨项目，易出现结转遗漏、状态表错位

### 1.3 根因分析

**设计是对的**：22号规则 §2.1 时机 0 + 起链扩展已写明「应建档全员（不只『有未办结或今日投喂』的人）」、§10 明令「不得只给『今天有事』的人建档」「不得跳过全员扫描」。

**但执行不足**：AI 在执行「日报投喂」路径时用了直觉逻辑（只写给日报的人），没先过 22 号时机 0 完整性闸。

**分层定位**：
- **直接层**：本次只建档 5 人，`_index.md` 过早写死「应建档 5 人」
- **机制层**：22 号时机 0 触发门槛在「日报投喂」入口不够前置/不够醒目，AI 易把它当独立路径而不先做 Step 0
- **系统层**：缺少「日报投喂 → 强制前置全员结转」的可执行检查点（Step 0 硬阻断）

## 2. 设计方案

### 2.0 现网裁决（A8-6，覆盖另一份 B 的 X-2）

在 3.14.0 规则文件中 **搜不到 N-33 / N-33②**。3.8.0 升级执行文件 B5「register 有、无待办文件的人 → 只写入 `_index` §1，禁止建空待办」是 **resource-register 退役时的一次性迁移**，不是日报/结转日常硬约束。

现网 22 号 L29 / L56 / L142 **已经**写明：当天读或写 todos → 应建档（§1 六态除已出组）**人人一份个人 md（§1 可空）**。空闲、请假、仅能耗、核心表为空，都建文件。

**3.15 不改这条。** 不采用「无待办且无能耗者不建文件」——那会削弱现网 22，并让「明天才被派活」的人再次缺档。用户痛点是 30 人未办结待办没被结转；维持人人一份即可一次结清。

`carryover_done_for_today=true` **维持现网 L58+L93**：

- 仅当应建档全员都有当天文件才置 true
- true = Step 0 已跑完且文件齐全
- true **不等于**每人结转成功；失败/待处理留状态表，今日不靠把 true 改回 false 来重试

花名册唯一来源 = 最新合法日 `_index.md` §1。禁止读 `resource-register.md`。

### 2.0b 硬阻断不依赖 Python（A11-3，驳 B1「无 Python 就跳过结转」）

SG-010 的闸是 **AI 执行 22 号时机 0**：读 `_index` §1、缺谁补谁、全员有文件才继续投喂。

- **不调用** `verify_todo_continuity.py`。该脚本只挂 19 号巡检旁路。
- 无 Python：仍必须做 Step 0。禁止 ASK「要不要跳过结转检查」。
- 无 Python 只影响 init / migrate / verify 旁路（走 SG-008 引导）。日报投喂不是脚本路径。

### 2.1 核心改造：01号规则新增强制前置检查

在 `references/01-daily-report-rules.md` 日报投喂流程**开头**增加（现网 L42 已说文件不存在须先走 22，本条把它抬成投喂入口硬阻断）：

```markdown
### 5.X 日报投喂前置检查（硬阻断）

投喂任何人口日报前，必须先完成 22 号时机 0 / Step 0：

1. 读最新合法日 `_index.md` §1：应建档 = 六态除已出组
2. 对照 `todos/{今天}/` 实有 `{姓名}.md`
3. 缺谁补谁：滚存未办结待办 + §0.6；无待办也建文件（§1 可空）
4. 应建档全员都有文件之后才允许写 inbox / 合并日报
5. 未完成则停止投喂，对外：「请先完成全员结转，再投喂日报」（不念章节号）
```

### 2.2 22号：不改应建档定义，只把「日报入口也走时机 0」写醒

22 号 §2.1 if-else **语义保持**。本版只补一句触发列举：日报投喂 = 读或写 `todos/{今天}/`，不得当成独立路径跳过时机 0。

L93 语义保留，方案正文不得再写成「true = 全员结转成功」。

### 2.3 SKILL.md 路由强化（B-012 核心修复）

**根因**：投喂日报走「日报」路由行，不载 22号，所以只给 5 人建档。最小必要改动是改 SKILL.md 路由表。

在 `SKILL.md` §6 提示词路由表中修改：

```markdown
| 场景 | 必须加载 |
|---|---|
| 日报 | 00+01+06+17 **+22** |
| 待办创建 WF-8 | 00+22+21+06+23 |
| 投喂工时/能耗 | 00+01+06+10+17+22 |
```

**说明**：原「日报」行无 22号，导致 AI 不执行全员结转；现强制加载 22号，确保 Step 0 先跑。

### 2.4 00号 WF-8：禁止再复制一份 Step 0

现网 00 L781 **已经是** Step 0 HARD BLOCK（N-43）。本版 **不新增** 第二份 Step 0 正文。

若施工时发现 L781 与 22 号 L58 用词不一致，只做指向对齐（「按 22 号时机 0 if-else」），不得把 01 号 5.X 再抄进 00。

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `SKILL.md` | **日报**路由行必须加载 22（`00+01+06+17+22`） | P0 |
| `references/01-daily-report-rules.md` | 投喂入口硬阻断：先 22 时机 0 | P0 |
| `references/22-carried-over-rules.md` | 时机 0 触发列举显式含「日报投喂」；不改人人一份 / L93 | P0 |
| `references/00-pm-main-rules.md` | WF-8 Step 0 **只对齐、不新造** | P1 |
| `assets/templates/daily-todo-binding-template.md` | 若缺「应建档/已建档」说明则补一句；不另起一套计数器 | P2 |

## 4. 兼容方式

- 纯规则强化，不改变现有数据结构
- 存量工作区无需迁移（_index.md 格式不变）
- 对已有正确执行的用户无影响，对错误执行的用户形成硬阻断

## 5. 测试项

与 §16 **同一套编号 T35–T40**。T48 留给 SG-011，禁止再给 SG-010 编第二套号。

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T35 | 日报投喂正例 | 花名册 35 人（无已出组）。投喂 5 人口日报 → 先 Step 0 → `todos/{今天}/` 有 35 个个人 md（无待办者 §1 可空）→ 再写那 5 人日报 → `carryover_done_for_today=true` |
| T36 | 日报投喂反例 | 模型若只给 5 人建档 → 硬阻断，不写那 5 人日报 |
| T37 | carryover 语义 | 只有 5 个文件时 true 非法；35 个文件齐全才允许 true。某人结转失败但文件已建 → 仍可 true，失败留状态表 |
| T38 | 路由 | SKILL.md 日报行含 22；未载 22 不得声称完成投喂 |
| T39 | 出组排除 | §1 已出组不建当天文件、不计入应建档 |
| T40 | 仅能耗 | 无待办但有 §0.6 → 仍建文件并延续 §0.6 |

---

# 当前共识

- SG-010：执行漏洞。最小改动 = 日报路由载 22 + 投喂入口硬阻断
- 维持 22 号人人一份（§1 可空）；不采用 N-33② 削弱
- WF-8 Step 0 现网已有，禁止复制第二份

---

# SG-011 设计方案：init README f-string `{编号}` 转义

> **需求编号**：SG-20260825-011  **优先级**：低  
> **一句话痛点**：初始化目录已建完，写 README 因 `{编号}` 当变量崩掉  

## 1. 问题根因

`generate_single_readme()`（`scripts/chronopm_init/file_registry.py` L497）返回 f-string。L543 字面量写成 `{编号}`。合法插值只有 `project_name` / `today` / `SKILL_VERSION` / `WORKSPACE_SCHEMA_VERSION`。

`workspace_builder.py` 顺序：建目录 → 建 outputs → 写版本文件 → **最后写 README**。所以通义看到「骨架成功、README 失败」符合代码，不是用法错误。

## 2. 设计方案

**只改一行**（及同函数里若再扫到未转义的非插值花括号）：

```python
# 现网 L543（崩）
│       └── {编号}/                # 一源文档一目录

# 改为
│       └── {{编号}}/              # 一源文档一目录
```

禁止改 `{SKILL_VERSION}` 等真插值。禁止借此重写 README 正文。

验收：`python scripts/init_workspace.py --project-root <tmp> --mode single --project-name "测试"` 退出码 0，且 `ai/README.md` 含字面量 `{编号}/`。

`workspace_builder.py` 写 README：**目标已存在则 skip**（与 create_skill_version 同口径），避免覆盖通义已手补的文件。

## 3. 文件改动

| 文件 | 改动 | 优先级 |
|---|---|---|
| `scripts/chronopm_init/file_registry.py` | `generate_single_readme` L543 `{编号}` → `{{编号}}` | P0 |
| `scripts/chronopm_init/workspace_builder.py` | README 已存在则 skip，不覆盖 | P1 |

## 4. 兼容

纯脚本 bugfix。已初始化工作区不受影响。

## 5. 测试项

| 编号 | 测试项 | 预期结果 |
|---|---|---|
| T48 | init 临时目录跑通 | 退出 0；`ai/README.md` 存在且含字面 `{编号}/`，不含 NameError |
| T48b | 真插值仍替换 | README 中 Skill 版本 = 包 VERSION，不是 `{SKILL_VERSION}` 字面 |
| T48c | README 已存在再 init | 不覆盖已有 README |

---

# 当前共识

- SG-011：一行转义，纳入 3.15，不延后 3.16

---

# 13. 施工文件总清单（A11-2）

§14 是影响评估，不是施工步骤。施工以本表 + 各 SG 文件改动表为准。**P1 两脚本必须新建**，进包，19 号不自动跑。

| 档 | 路径 | 动作 | SG |
|---|---|---|---|
| P0 | `scripts/migrate_workspace.py` | `migrate_business_data` + 3.15 VERSION_CAPABILITIES | 001 |
| P0 | `scripts/chronopm_init/file_registry.py` | `{编号}` → `{{编号}}` | 011 |
| P1 | `scripts/chronopm_init/workspace_builder.py` | README 已存在 skip | 011 |
| P0 | `scripts/verify_projection.py` | **新建** C1–C8 + D-TODO-WP + D-PLAN-REF + D-EFFECT | 009 |
| P0 | `scripts/verify_todo_continuity.py` | **新建** D-TODO-01/02/03 | 009 |
| P1 | `scripts/verify_requirement_wp.py` | **新建** D-REQ-WP + D-SOURCE；19 号不自动跑 | 009 |
| P1 | `scripts/verify_contract_ri.py` | **新建** D-CONTRACT-01/02；19 号不自动跑 | 009 |
| P0 | `SKILL.md` | §5.0 Python；日报行 +22；事实源 current_operator | 008/010/004 |
| P0 | `references/01-daily-report-rules.md` | 投喂入口硬阻断（规则，不调脚本） | 010 |
| P0 | `references/22-carried-over-rules.md` | 时机 0 列举含日报投喂 | 010 |
| P0 | `references/21-pm-profile-rules.md` | 身份拆分 + ASK | 004 |
| P0 | `references/05-query-rules.md` | 「我」= current_operator | 004 |
| P0 | `assets/templates/plan-template.md` | §4 含执行人/排期 | 002 |
| P1 | `references/19-info-completeness-rules.md` | 挂 P0 两脚本；不挂 P1 | 009 |
| P0 | 双包 VERSION / skill.json / CHANGELOG | 3.15.0 / schema 0.16.0 | 锁步 |
| P0 | `governance/migrations/upgrade-to-3.15.0.md` | 升级执行文件 | 001 |

其余见各 SG「文件改动」表（examples 重命名、16 号 §21/§22、skill-gap 模板等）。

---

# ChronoPM Skill v3.15.0 升级方案 — 影响评估 + B 审核输入包

> **方案版本**：V0.11  **目标版本**：3.14.0 → 3.15.0  **schema**：0.15.0 → 0.16.0  
> **工作空间快照**：见文首「工作空间版本快照」。  

---

# 14. 方案影响与必要性评估（强制）

## 14.1 影响范围评估

| 影响维度 | 是否受影响 | 具体影响说明 | 影响程度 |
|---|---|---|---|
| 现有能力/功能 | 是 | SG-004 身份推导；SG-003 输出；SG-010 日报必载 22；SG-009 巡检旁路跑脚本 | 中 |
| 现有文件/模块 | 是 | examples 重命名 20 + 规则/模板/脚本（含 4 个 verify_*.py）。口径：规则文件数不增（改不增）；脚本 +4 | 中 |
| 输入/输出格式 | 是 | skill_gap 单文件；current_operator 字段 | 低 |
| 交互流程 | 是 | 迁移确认；操作人 ASK；Python 未装时引导；日报投喂先结转 | 中 |
| 数据结构/索引 | 是 | pm-profile 新字段；待校准清单；不新增索引层 | 中 |
| 上下文与输出限制 | 是 | 日报路由多载 22；21 §2.4 重写。规则文件数仍 23+4 | 低 |
| 模块依赖/联动关系 | 是 | Project↔Portfolio 仅 SUGGEST；19 号挂 P0 脚本 | 中 |
| 性能与维护性 | 是 | migrate 可选写回；verify P0 只读，数秒级 | 低 |
| 用户使用入口/触发词 | 是 | 「我是 XXX」；Python 安装引导 | 低 |

## 14.2 历史使用体验影响评估

- **是否改变既有体验**：部分
- **增强点**：存量迁移可一次对齐；§4 不再漏人期；缺口文件可单文件传阅；「我的待办」跟操作人；弱模型有 P0 断言旁路；日报投喂先全员结转
- **削弱点**：首次须声明操作人（空则 ASK，**无回退**）；无 Python 时低频治理要先装 3.9+；examples 书签可能失效
- **兼容性**：skill_gap 新旧并存；current_operator 空字段不回退 pm_name；结转维持 22 号人人一份
- **结论**：总体增强。新增步骤都有明确失败文案

## 14.3 对其他模块的影响评估

- ChronoPM-Portfolio：版本锁步 3.15.0 / schema 0.16.0；操作人 SUGGEST；skill-gap 模板锁步；不打包 verify 脚本
- skill-gap-skill：去掉 skill_gap 的 manifest
- scripts：migrate 增业务迁移；+4 verify
- examples：重编号
- 16 号 / release-checklist：§21/§22 + C-1～C-4（C-4 存量豁免）
- **不破坏**现有能力。SG-010 不新造第二份 WF-8 Step 0

## 14.4 升级必要性评估

| 需求 | 要解决的问题 | 现有能力能否覆盖 | 必要性 |
|---|---|---|---|
| SG-001 | 升级后存量双轨 | 否 | **必须** |
| SG-002 | 模板漏人期 | 否 | **必须** |
| SG-003 | 缺口文件不自足 | 否 | 建议 |
| SG-004 | 「我」与项目经理混用 | 否 | **必须** |
| SG-005 | AP 无强制约束 | 否 | 建议 |
| SG-006 | examples 顺序 | 否 | 建议 |
| SG-007 | 收尾清单断链 | 路径写错 | **必须** |
| SG-008 | 无 Python 无引导 | 否 | 建议 |
| SG-009 | 级联全靠模型自觉 | 14 号 D36/D38 仅本轮触碰、无机器退出码 | **必须** |
| SG-010 | 日报不载 22，只给有事的人建档 | 规则已有、路由没有 | **必须** |
| SG-011 | init 写 README 因 `{编号}` 崩 | 否，f-string 漏转义 | **建议（本版做，一行）** |

不实施：存量继续双轨；弱模型静默漏投影；投喂日报继续拆结转。

## 14.5 匹配度

11 条均来自实测或治理补证。SG-004 字面级联已拍板降级。SG-009 不把 D-RESOURCE 塞进本版。SG-011 是 init 脚本一行 bug，不是用法问题。无目标漂移。

## 14.6 综合意见

**支持升级。** Q1–Q9 已关闭。待 B 核：A8-1～A8-8、C1–C8 字段、D-TODO 对照日、SG-010 维持人人一份。

---

# 15. 方案关键断言与放行门槛声明

## 关键断言清单

| 关键断言 | 依据 | 若被证伪则判为 |
|---|---|---|
| plan-template §4 只有阶段→⏳ | L40-58 | 阻塞 |
| 00 §8d 要求空岗 ⚠️待安排人 | L620 | 阻塞 |
| gap-capture-rules 要求 manifest | §1 Calls + §7 | 阻塞 |
| pm_name 用于「我」 | 21 §2.4 L77 | 阻塞 |
| migrate 3.14 只建空目录 | VERSION_CAPABILITIES L701-706 | 阻塞 |
| 16 号 release-checklist 路径写错 | L299 `governance/` vs 实文件 `governance-shared/` | 阻塞 |
| examples 01 升级在 03 初始化前 | examples/ 目录 | 非阻塞 |
| 本版不新增规则文件（改不增） | 规则仍 23+4；新增的是脚本与 upgrade-to | 非阻塞 |
| SKILL.md 日报行不载 22 | 路由表「日报」=`00+01+06+17` | 阻塞（SG-010） |
| 22 号应建档=人人一份（§1 可空） | 22 L29/L56；N-33② 在 3.14 规则 0 命中 | 阻塞（若被证伪则 SG-010 裁决要重开） |
| 待办日期在 §1.1 列不在 YAML | personal-daily-todo-template | 阻塞（SG-009） |
| WP 关联需求在 §2 表 | wp-template §2 | 阻塞（SG-009） |
| 双包 python ≥3.9 | 两份 skill.json | 阻塞（SG-008） |
| C1–C8 在 SG-009 §2.2 有定义表 | 本文件，禁止「见 SG-008」 | 阻塞 |
| init README f-string 含未转义 `{编号}` | `file_registry.py` L543，整段 `f"""` | 阻塞（SG-011） |
| P0 verify 只读、不写盘 | §16 T33；脚本无副作用 | 阻塞（SG-009） |
| 4 个 verify 均进包；19 号只自动跑 P0 | A8-5 | 非阻塞 |
| SG-010 硬阻断不依赖 Python/verify | 22 号 + SKILL 日报行载 22 | 阻塞（误读则方案被改坏） |

**口径（A11-1）**：上表是**方案级事实断言**（现网是否如 A 所述）。SG-009 的 C1–C8 / D-* 是**工作区机器断言**，定义在 SG-009 §2.2，验收 T25–T47。禁止把二者合成一套 A-001～A-032，禁止改用现网不存在的 `requirement_refs` / `create_date` / `carryover_from` / `ai/sources/`。

## 放行门槛

- 通过-可执行 / 通过-待修订：上表阻塞断言未被证伪 + 无新阻塞
- 修订-需再审：任一阻塞断言被证伪
- 重做-需再审：目标偏移或方案不可施工

## 已拍板取舍（均不阻塞）

| 取舍 | 缓解 |
|---|---|
| current_operator 空 = ASK，无回退 | 首次多一句 |
| 字面级联 → V-9 SUGGEST | 只读硬契约 |
| C-4 存量豁免场景/mermaid | §22 管新示例 |
| N-33② 不升格为日常约束 | 维持 22 人人一份 |
| P1 脚本进包不自动跑 | 19 号只跑 P0 |
| D-RESOURCE 本版不做 | 从表删除，下版再议 |
| migrate 不自动写回 | dry-run 默认 |

Q1–Q9 全部已关闭。见 §5.4。

---

# 16. 测试与验收标准

| 编号 | 测试项 | 预期结果 | 来源 |
|---|---|---|---|
| T1 | plan-template §4 含执行人/排期/空岗示例 | 模板每行有 `｜执行人｜排期` 格式 | SG-002 |
| T2 | 新建计划 §4 从 WP §8 投影含执行人 | 每行含阶段→图标｜执行人｜排期（关键阶段在 §3 第 6 列，§4 不要求五列） | SG-002 |
| T3 | skill_gap 输出为单文件（无 manifest） | 只有 `需求-*.md`，无 manifest.md | SG-003 |
| T4 | 需求文件 front matter 含全部元数据 | batch_id/created_at/source_files 等齐全 | SG-003 |
| T5 | pm-profile.md 含 current_operator 字段 | front matter 有 current_operator | SG-004 |
| T6 | "我是张三"后"我的待办"按张三解析 | 待办查询 Owner=张三 | SG-004 |
| T7 | pm_name 不从岗位自动填充 | todos 岗位不自动升为项目经理 | SG-004 |
| T8 | migrate --dry-run 输出待校准清单 | 不写回，只输出清单 | SG-001 |
| T9 | migrate 受控迁移生成回滚快照 | backup/ 下有快照目录 | SG-001 |
| T10 | 项目集「我是张三」 | 对外白话；内部 V-9；不写子项目；不对用户说「建议更新清单」 | SG-004 |
| T10b | current_operator 为空查「我的待办」 | ASK，不回退 pm_name | SG-004 |
| T11 | 16 号 §21 存在且含数量/命名/位置三项约束 | 三小节齐全 | SG-005 |
| T12 | planning/README.md L7 无歧义 | 不含"或"字，明确唯一位置 | SG-005 |
| T13 | examples 目录按新编号排列 | 01 初始化→02 升级→...→20 技能缺口 | SG-006 |
| T14 | README.md mermaid 图正确 | 分组与编号对应 | SG-006 |
| T15 | README.md 表格正确 | 所有链接指向正确文件 | SG-006 |
| T16 | 跨引用同步更新 | 02 引用 02、17 引用 01 | SG-006 |
| T17 | 16 号 §22 存在 | 含 4 项子约束 | SG-006 |
| T18 | release-checklist.md 含 C-1~C-4 四项检查 | 文件存在且追加了 4 项新检查 | SG-007 |
| T19 | 16 号 §14 引用路径正确 | 指向 governance-shared/review-checklists/ | SG-007 |
| T20 | 16 号 §2 第 11 步含 release-checklist 引用 | 文本存在 | SG-007 |
| T21 | SKILL.md §5.0 存在 | 含环境检测指引 | SG-008 |
| T22 | AI 检测到 Python 错误时主动引导 | 输出安装命令 | SG-008 |
| T23 | 用户回复“是”后 AI 生成分平台命令 | Windows/Mac/Linux 均有 | SG-008 |
| T24 | README 标注 Python 版本要求 | 最低 3.9（与 skill.json 一致），推荐 3.10+ | SG-008 |
| T25 | verify_projection.py 正例 | WP↔计划↔index 全一致 → 退出 0 | SG-009 |
| T26 | verify_projection.py 反例 | 改 WP §8 执行人但计划§3 不同步 → 报 C3 差异，退出 1 | SG-009 |
| T27 | verify_projection.py 脏链尾 | WP §7 链尾「已完成」但 §8 有 ✅/🔄 → C2 正确取末状态，不误报 | SG-009 |
| T28 | verify_projection.py 同义词 | 计划/§8 含别名 → C6 等价判定，不误报 | SG-009 |
| T29 | verify_projection.py 待办越窗 | 待办结束 > WP 结束 → D-TODO-WP-01 报警 | SG-009 |
| T30 | verify_todo_continuity.py 正例 | 人员文件连续 + 待办滚存 + 能耗延续 → 退出 0 | SG-009 |
| T31 | verify_todo_continuity.py 反例 | 最新合法日有未办结待办但今天文件缺失 → 报 D-TODO-02，退出 1 | SG-009 |
| T32 | verify_todo_continuity.py 能耗断链 | 最新合法日有 §0.6 但今天文件缺失 → 报 D-TODO-03，退出 1 | SG-009 |
| T33 | 只读性 | 跑完比对文件 mtime/内容 → 无任何写盘 | SG-009 |
| T34 | 版本触点 | 脚本随版本同步 → sync_version / 回归通过 | SG-009 |
| T35 | 日报投喂正例 | 投喂 5 人 → 先 Step 0 → 当天 35 个个人 md（§1 可空）→ 再写日报 → carryover=true | SG-010 |
| T36 | 日报投喂反例 | 只建 5 人 → 硬阻断 | SG-010 |
| T37 | carryover 语义 | 仅 5 文件时不得 true；35 文件齐全才允许 true；失败可仍 true | SG-010 |
| T38 | 日报路由含 22 | SKILL.md 日报行 = 00+01+06+17+22 | SG-010 |
| T39 | 出组排除 | 已出组不建当天文件 | SG-010 |
| T40 | 仅能耗 | 无待办有 §0.6 → 仍建文件并延续 §0.6 | SG-010 |
| T41 | verify_requirement_wp.py 正例 | 需求工作包 ↔ WP 双向引用闭环 → 退出 0 | SG-009 |
| T42 | verify_requirement_wp.py 反例 | 需求清单有 WP-001 但 wps/WP-001.md 缺失 → 报 D-REQ-WP-01 差异，退出 1 | SG-009 |
| T43 | verify_requirement_wp.py sources 索引 | sources/{编号}/meta.md 存在但 _index.md 缺行 → 报 D-SOURCE-01 差异，退出 1 | SG-009 |
| T44 | verify_contract_ri.py 正例 | 需求/Canonical 引用的 CON-* 均在合同登记册 → 退出 0 | SG-009 |
| T45 | verify_contract_ri.py 反例 | 需求写了 CON-不存在 → 报 D-CONTRACT-01，退出 1 | SG-009 |
| T46 | verify_projection.py plan_ref | WP plan_ref 三处不一致 → 报 D-PLAN-REF-01 差异，退出 1 | SG-009 |
| T47 | verify_projection.py effect | 废弃 WP 仍出现在正常计划 §3/§4 → 报 D-EFFECT-01 差异，退出 1 | SG-009 |
| T48 | init 临时目录写 README | 退出 0；`ai/README.md` 含字面 `{编号}/` | SG-011 |
| T48b | README 真插值 | Skill 版本行等于包 VERSION | SG-011 |
| T48c | README 已存在再 init | 不覆盖 | SG-011 |

---

# 17. 需求实现偏差验证

| 原始需求点 | 方案 | 完全覆盖 | 扩展/降级 | 需确认 |
|---|---|---|---|---|
| SG-001 存量迁移 | migrate_business_data + dry-run/回滚 | 是 | dry-run | 否（Q2 关） |
| SG-002 §4 模板 | 改 plan-template | 是 | 无 | 否 |
| SG-003 单文件 | 仅 skill_gap 不建 manifest | 是 | 无 | 否 |
| SG-004 pm_name / 操作人 / 禁岗位填充 | 21+模板+05+ASK | 是 | 无回退 | 否（Q6 关） |
| SG-004 项目集级联 | V-9 SUGGEST | **降级**（拍板） | 字面写入做不到 | 否（Q3 关） |
| SG-005 AP 约束 | 16 §21 + L111 + planning README | 是 | 无 | 否 |
| SG-006 examples | 重编号；§22 不追溯 | 是 | C-4 存量豁免 | 否（Q7 关） |
| SG-007 收尾清单 | 路径 + C-1～C-4 | 是 | C-4 豁免场景 | 否 |
| SG-008 Python | §5.0；≥3.9 | 是 | 无 | 否 |
| SG-009 机器断言 | C1–C8 已定义；P0 挂 19；P1 进包 | 是 | D-RESOURCE 不做 | 否（Q9 关） |
| SG-010 全员结转 | 日报载 22 + 投喂硬阻断；人人一份 | 是 | 不新造 WF-8 Step 0 | 否（Q8 关） |
| SG-011 init README | `{编号}` → `{{编号}}` | 是 | 无 | 否 |

忠实于目标。SG-004 级联是已标的降级，不是静默少做。

---

# 18. 现有能力扩展优先评估

全部走扩展：migrate 加函数、pm-profile 加字段、gap 改输出、模板改示例、19 号旁路挂脚本、日报路由加 22。

| 指标 | 升级前 | 本次 | 口径 |
|---|---|---|---|
| 规则文件数 | 23+4 | 0 新增 | **改不增** |
| 脚本 | migrate/init/sync | **+4 verify** | 新文件 |
| 模板 | ~40 | 字段/示例修改，不新增模板文件数（skill-gap YAML 加字段） | — |
| 提示词 | ~50K | +21 §2.4 +01 投喂闸 + SKILL §5.0/路由 | 远低于阈值 |

---

# 19. 索引合理性评估

不改索引结构。SG-001 只对齐现有 `wps/_index.md` 列值。合理，不调整。

---

# 20. 联动更新设计

| 源 | 依赖 | 方式 |
|---|---|---|
| current_operator | 05「我的待办」 | 实读字段；空则 ASK |
| current_operator | Portfolio 子项目 | **V-9 SUGGEST，禁止写入** |
| WP §8 | 计划 §3/§4 | 闸 2 / SCAN 投影；P0 脚本只读校验 |
| 22 时机 0 | 日报投喂 | SKILL 日报行载 22；01 硬阻断 |
| P0 verify | 19 号巡检 | 旁路只读 |

无循环。SG-004 **不是**单向写入。

---

# 21. 当前待确认问题

无。Q1–Q9 已关闭（§5.4）。B 若证伪 A8-6（人人一份）或 A8-1（ASK），才重开。

---

# 22. A 自审结果

| 审核项 | 结论 | 说明 |
|---|---|---|
| 目标一致性 | ✅ | 11 条均有设计 |
| 目录扫描 | ✅ | 本轮已读 22/01/00/05/11/skill.json python、Portfolio 01 只读边界 |
| 文件改动 | ✅ | 含 4 脚本、SKILL 路由、05、双包缺口模板、23 号 |
| 兼容性 | ✅ | ASK 无回退；人人一份；skill_gap 例外 manifest |
| 测试 | ✅ | T1–T48c + T10b；SG-010 = T35–T40；SG-011 = T48/T48b/T48c |
| 关键断言 | ✅ | §15 已含 008/009/010 |
| 复杂度 | ✅ | 规则改不增；脚本 +4 |
| 适合 B 复审 | ✅ | V0.8 |

---

# 23. 当前结论

- 忠实于 11 条需求；SG-004 级联已拍板降级
- 可落地：文件级改动已按 SG 列出
- **必须再经 B 独立审核**，通过前禁止施工
- 本文件版本 **V0.11**

---

# 24. 给 B 的审核输入包

你是独立审核 Agent B。不要用 A 的结论当事实。自己扫现网。只审不改、不施工。先核对工作空间快照：Project/Portfolio **3.14.0** / schema **0.15.0**，根路径 `C:\Users\qiusuo\Downloads\ChronoPM Skill`。

## 用户原始需求（11 条）

SG-001~004 文件：
- `c:\Users\qiusuo\Downloads\需求-3.14升级脚本缺历史数据迁移.md`
- `c:\Users\qiusuo\Downloads\需求-计划§4模板缺执行人排期.md`
- `c:\Users\qiusuo\Downloads\需求-skill缺口输出改单文件自足.md`
- `c:\Users\qiusuo\Downloads\需求-PM身份识别拆分当前操作人.md`

SG-005~011 来自对话补证，正文见本文件 §1（008/009/010/011 无独立需求文件，以 §1 摘要 + 文首拍板为准）。

## 对过期 V0.8 B 审（X-1～X-4）的现稿位置

请 **不要** 再按 V0.8 正文复述下面四条。现稿位置：

| 过期 B 项 | 现稿 |
|---|---|
| X-1 评审包 7 条 | §17 已列 SG-001～011；§21 无待确认；§24 写 11 条来源 |
| X-2 测试两套号 | SG-010 与 §16 均为 T35–T40；T48 = SG-011 |
| X-3 空操作人互斥 | SG-004 §2.3～2.5 = 一律 ASK，禁止回退；05 号 + T10b |
| X-4 C-4 vs 不追溯 | 存量豁免（Q7）；C-4 正文已改 |
| B-013「不建空文件」 | **否。** 现稿 A8-6 = 维持 22 号人人一份（§1 可空） |

## 请 B 本轮重点核（对照 **V0.11** 现网）

1. 全文是否还有「回退 pm_name」「7 条需求」「SG-010 = T48-T53」
2. C-4 是否仍要求存量必须有场景/mermaid
3. A8-6 人人一份 vs 另一份 B 的 N-33②：现网 22 L29 是否支持 A
4. D-EFFECT 缺省当正常、D-PLAN-REF 禁止只信 YAML
5. SG-011 L543 `{编号}` 是否仍在现网
6. §16 编号：T35–T40=SG-010，T48=SG-011，无第二套

方案唯一文件：`governance-shared/planning/upgrade-plan-v3.15.0.md`。

---

# 当前共识状态摘要

- **V0.11**。11 条需求。Q1–Q9 关闭
- B1：拒收错字段 32 条断言表；补 §13 施工总清单；SG-010 不依赖 Python
- 等待 **B 对照 V0.11**。通过前不执行

# 是否偏离目标自检

否。级联降级已标明。SG-011 是脚本 bugfix，不扩能力。

# 下一步

将 §24 交给 B 复审。通过后再写 CR / upgrade-to / 施工。

---

# B1 审核结果（V0.10）

**审核角色**：B（只审不改方案，不执行施工）  
**对照对象**：`governance-shared/planning/upgrade-plan-v3.15.0.md` **V0.10**  
**现网眼见**：ChronoPM-Project / ChronoPM-Portfolio 3.14.0、schema 0.15.0  
**审核日期**：2026-08-25  

## 总评

**判定：修订-需再审**

V0.10 已修正 V0.8 的评审包滞后、测试编号混乱、current_operator 互斥、C-4 存量豁免等核心阻塞问题，并新增 SG-011（init f-string 转义）、SG-001 幂等保护、D-EFFECT/D-PLAN-REF 语义澄清。**但仍有 2 个阻塞级自洽性问题 + 1 个高风险逻辑漏洞**，不能判"通过-可执行"。

---

## 一、已修复问题核验（✅ 通过）

| 编号 | V0.8 问题 | V0.10 修订动作 | B 核验结果 |
|---|---|---|---|
| **X-1** | §17/§18/§20/§21/§22/§23/§24 停留在 SG-007 | §17 补入 SG-008~011；§18 更新复杂度表；§20 补联动；§21 清空待确认；§22 改为 11 条/T53/~15 断言；§23 改为 11 条；**§24 改为 11 条来源** | ✅ 通过 |
| **X-2** | 测试两套编号（T35-T40 vs T48-T53） | **统一为 T35-T40=SG-010，T48=SG-011**，删除第二套号 | ✅ 通过 |
| **X-3** | current_operator 三句互斥 | SG-004 §2.3~2.5 统一为"一律 ASK"，禁止回退 pm_name；05 号 + T10b 同步 | ✅ 通过 |
| **X-4** | C-4 vs 不追溯矛盾 | C-4 改为"**存量 examples 豁免**场景/mermaid；本版只强制编号+跨引用" | ✅ 通过 |
| **A8-6** | N-33② 冲突（无待办无能耗不建文件） | 明确：**维持 22 号现行**——当天读/写 todos → 应建档全员人人一份（§1 可空） | ✅ 通过 |
| **A9-1** | SG-011 init f-string 转义 | 纳入 3.15.0，一行修复 L543 `{编号}` → `{{编号}}` | ✅ 通过 |
| **A10-2** | D-EFFECT/D-PLAN-REF 语义含糊 | D-EFFECT-01：缺 effect 当正常；D-PLAN-REF-01：禁止只信 YAML，plan_ref 空仍扫 §3 | ✅ 通过 |
| **A10-3** | SG-001 迁移幂等 | 阶段名已是 13 标准名 → skip，禁止二次改名；只投影 §3/§4，不重算点名人期 | ✅ 通过 |

**结论**：V0.8 的 4 个阻塞问题 + A8-6/A9-1/A10-2/A10-3 共 8 项修订已全部落地，方向正确。

---

## 二、仍存阻塞问题（❌ 需修订）

### 🔴 X-1 ★ 关键断言清单（§15）未覆盖 SG-009 P1 脚本与 SG-011

**现状**：
- §15 关键断言清单（L1720-1729）只列了 11 条断言：
  - SG-001: A-001/A-002
  - SG-004: A-003/A-004/A-005
  - SG-005: A-006
  - SG-006: A-007
  - SG-007: A-008/A-009
  - SG-008: A-010
  - SG-009: **A-011 (D-TODO-WP-01)** ← 只有这一条！
  - SG-010: A-012

**缺失**：
- **SG-009 的其他 12 条断言**（C1-C8, D-TODO-01/02/03, D-REQ-WP-01/02, D-CONTRACT-01/02, D-SOURCE-01, D-PLAN-REF-01, D-EFFECT-01）**完全不在 §15 清单里**
- **SG-011 无任何断言**（虽然只是 f-string 修复，但应有"A-013: init README 生成成功且 {编号} 字面量正确"）

**影响**：
- §15 放行门槛"全部关键断言未被证伪"**无法成立**，因为清单本身不完整
- B 无法基于 §15 判断 SG-009 P0/P1 脚本是否达到发布质量
- 若只测 A-011，其他 12 条断言漏测即带病上线

**必须修订**：
在 §15 补入以下断言（建议按 SG 分组）：

```markdown
### SG-009 数据一致性断言体系

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| A-013 | C1 WP 名称投影 | WP front matter name == _index.md name 列 | 相等 |
| A-014 | C2 WP 状态投影 | WP front matter status == _index.md status 列 | 相等 |
| A-015 | C3 WP 负责人投影 | WP front matter owner == _index.md owner 列 | 相等 |
| A-016 | C4 WP 起止日期投影 | WP front matter start/end == _index.md start/end 列 | 相等 |
| A-017 | C5 WP 计划引用投影 | WP plan_ref == _index.md plan_ref 列 | 相等 |
| A-018 | C6 计划 §3 引用闭合 | 正常计划 §3 引用的 WP 均存在于 _index.md | 无悬挂引用 |
| A-019 | C7 废弃 WP 清理 | effect=废弃的 WP 不出现在任何正常计划 §3/§4 | 完全清除 |
| A-020 | C8 sources 索引同步 | ai/sources/ 下的源文件均在 _index.md sources 列有记录 | 无遗漏 |
| A-021 | D-TODO-01 结转链起点 | 当天新建待办必须有 create_date | 非空 |
| A-022 | D-TODO-02 结转链连续 | carryover_from 指向的待办必须存在且 status=未完成 | 存在且状态匹配 |
| A-023 | D-TODO-03 结转链终点 | 当天完成待办必须有 complete_date | 非空 |
| A-024 | D-REQ-WP-01 需求↔WP 关联 | requirement_refs 指向的需求必须在 register 存在 | 存在 |
| A-025 | D-REQ-WP-02 WP→需求反向映射 | register 中每个需求的 wp_refs 必须包含引用它的 WP | 双向闭合 |
| A-026 | D-CONTRACT-01 合同↔需求映射 | contract_refs 指向的合同必须在 contract-register 存在 | 存在 |
| A-027 | D-CONTRACT-02 合同 RI 映射 | contract-register 中每个合同的 ri_refs 必须与需求 register 的 contract_id 匹配 | 匹配 |
| A-028 | D-SOURCE-01 sources 索引同步 | ai/sources/ 下的源文件均在 _index.md sources 列有记录 | 无遗漏 |
| A-029 | D-PLAN-REF-01 plan_ref 三处一致 | WP plan_ref == _index.md plan_ref == 计划 §3 引用 | 三处相等 |
| A-030 | D-EFFECT-01 废弃 WP 清理 | effect=废弃的 WP 不出现在任何正常计划 §3/§4/§6 | 完全清除 |

### SG-011 init README f-string 转义

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 |
|---|---|---|---|
| A-031 | init README 生成成功 | generate_single_readme 执行后 README.md 存在且含预期标题 | 文件存在且内容正确 |
| A-032 | {编号} 字面量正确 | README.md 中 "{编号}" 以字面量出现，未被替换为空或报错 | 字面量 "{编号}" 存在 |
```

**同时更新**：
- §16 汇总表：T1-T53 对应 A-001~A-032（需重新编号对齐）
- §22 自审表："~15 条断言"改为"**32 条断言**"
- §23 结论："11 条需求全部有对应设计 + **32 条关键断言**"

---

### 🔴 X-2 ★ SG-009 P1 脚本（verify_requirement_wp.py + verify_contract_ri.py）未在 §14 实施步骤中列出

**现状**：
- §14 实施步骤（L1638-1672）只列了：
  - 14.1 新增 2 个脚本（verify_projection.py + verify_todo_continuity.py）← **这是 P0**
  - 14.2 修订 01/22/00 规则
  - 14.3 修订 SKILL.md 路由表
  - 14.4 修订 templates
  - 14.5 新增 fixtures
  - 14.6 修订 audit_release.py

**缺失**：
- **verify_requirement_wp.py**（D-REQ-WP-01/02）和 **verify_contract_ri.py**（D-CONTRACT-01/02）**完全没在 §14 出现**
- 但 §1 说它们是 SG-009 P1 交付物，§16 有 T41-T47 测试它们
- §20 联动表提到"01 号需求查询入口调用 verify_requirement_wp.py"

**矛盾**：
- 若 P1 脚本不实施，T41-T47 无法执行
- 若 P1 脚本实施了，§14 必须列出其创建步骤

**必须修订**：
在 §14.1 后新增 **14.1.1 P1 脚本（可选挂起）**：

```markdown
### 14.1.1 P1 脚本（可选挂起，19 号不自动跑）

**新增文件**：
- `ChronoPM-Project/scripts/verify_requirement_wp.py`（D-REQ-WP-01/02）
- `ChronoPM-Project/scripts/verify_contract_ri.py`（D-CONTRACT-01/02）

**功能**：
- verify_requirement_wp.py：扫描所有 WP 的 requirement_refs，验证双向映射闭合
- verify_contract_ri.py：扫描 contract-register 与需求 register，验证合同↔需求↔RI 映射

**集成方式**：
- 19 号完整性巡检 **不自动调用**（避免性能开销）
- AI 可在用户显式请求"检查需求-WP 关联"或"检查合同映射"时手动调用
- 输出格式同 P0 脚本：JSON + Markdown 报告

**测试**：T41-T47（见 §16）
```

---

###  X-3 非阻塞但高风险：SG-010 全员结转硬阻断的"无 Python 用户"路径未闭环

**现状**：
- SG-010 §2.2：日报投喂 → 先查全员结转 → 未完成则 BLOCK
- SG-008 §2.2：无 Python → ASK 引导安装 → 用户拒绝则降级体验

**潜在冲突**：
- 若用户**既无 Python 又拒绝安装**，SG-010 的硬阻断如何执行？
  - verify_todo_continuity.py 需要 Python 运行
  - 若无 Python，脚本无法执行 → 硬阻断失效
  - 若降级为"不检查"，则 SG-010 目标落空

**风险**：
- 弱模型用户（无 Python）成为**唯一能绕过全员结转检查**的人群
- 与 SG-010"消除只给部分人建档漏洞"的目标相悖

**建议修订**（二选一）：

**方案 A（推荐）**：SG-010 增加"无 Python 降级策略"
```markdown
### SG-010 §2.3 无 Python 降级策略

若检测到无 Python 环境：
1. **ASK 用户**："检测到无 Python 环境，无法运行全员结转检查脚本。是否继续投喂日报（跳过结转检查）？"
2. 用户选择"是" → 允许投喂，但在日报末尾加️警告："未检查全员结转，建议安装 Python 后补检"
3. 用户选择"否" → 中止投喂，引导安装 Python（同 SG-008）

**理由**：硬阻断的前提是脚本可执行；无 Python 时无法执行，只能降级为警告。
```

**方案 B（更强硬）**：SG-010 改为"纯规则检查，不依赖脚本"
```markdown
### SG-010 §2.2 纯规则检查（无 Python 兼容）

不依赖 verify_todo_continuity.py，改用 AI 直接扫描：
1. 读取 ai/personal-daily-todo/ 下所有个人待办文件
2. 提取花名册（_index.md §1）
3. 对每人检查：当天是否有待办文件 OR 文件 §1 是否为空
4. 若有人缺失 → BLOCK，提示"XX 今日无待办档案，请先建档"

**优点**：无需 Python，AI 可直接执行
**缺点**：AI 扫描慢，弱模型可能漏检
```

**建议采用方案 A**（保持脚本权威性，无 Python 时降级警告）。

---

## 三、非阻塞建议（🟡 可选优化）

| 编号 | 问题 | 建议 |
|---|---|---|
| Y-1 | §16 测试项 T1-T53 与 A-001~A-032 编号不对齐 | 重新编号测试项，使 T1=A-001, T2=A-002...T32=A-032，T33-T53 为边界/回归测试 |
| Y-2 | SG-001 迁移脚本的"开发仓无业务 ai/"场景未明确 | 补充：若 --project-root 指向开发仓且无 ai/ 目录 → skip 存量迁移，仅初始化骨架 |
| Y-3 | verify_projection.py 的"多值用 / 分隔"未定义解析规则 | 补充：plan_ref="WP-A / WP-B" → split(" / ") → ["WP-A", "WP-B"]，逐个验证 |
| Y-4 | SG-011 的"手动补建 README"场景未覆盖 | 补充 T48b：若 AI 已手动补建 README，脚本应检测并 skip，避免覆盖人工修改 |

---

## 四、放行门槛对照（A §15）

| 门槛 | 现状 | 判定 |
|---|---|---|
| 全部关键断言未被证伪 | ❌ §15 清单只有 11 条，缺失 SG-009 其他 12 条 + SG-011 2 条 | 不通过 |
| 无新增阻塞问题 | ❌ X-1/X-2 仍存，X-3 高风险未决 | 不通过 |
| 评审包与正文一致 | ✅ §24 已改为 11 条来源 | 通过 |

**故：修订-需再审。**

---

## 五、必须修订清单（给 A，按优先级）

### 阻塞（不改不能再送审）：

1. **X-1 §15 关键断言补全**：补入 SG-009 的 A-013~A-030（12 条）+ SG-011 的 A-031/A-032（2 条），共 32 条断言。同步更新 §16/§22/§23。
2. **X-2 §14 补 P1 脚本实施步骤**：新增 14.1.1 节，列出 verify_requirement_wp.py + verify_contract_ri.py 的创建步骤、功能、集成方式、测试编号。
3. **X-3 SG-010 无 Python 降级策略**：采用方案 A（ASK + 警告）或方案 B（纯规则检查），写入 SG-010 §2.3。

### 非阻塞建议：

- Y-1 测试项与断言编号对齐
- Y-2 SG-001 开发仓场景明确
- Y-3 多值 plan_ref 解析规则
- Y-4 SG-011 手动补建 README 场景

---

## 六、总结

V0.10 相比 V0.8 已有显著进步：
- ✅ 评审包全量同步（§14-§24 覆盖 SG-001~011）
- ✅ 测试编号统一（T35-T40=SG-010，T48=SG-011）
- ✅ current_operator 行为统一（一律 ASK）
- ✅ C-4 存量豁免明确
- ✅ SG-011 init f-string 修复纳入
- ✅ SG-001 幂等保护、D-EFFECT/D-PLAN-REF 语义澄清

**但仍存 2 个阻塞问题**：
1. **§15 关键断言清单严重缺失**（只有 11 条，实际应 32 条）
2. **P1 脚本未在 §14 实施步骤中列出**（导致 T41-T47 无实施依据）
3. **SG-010 无 Python 用户路径未闭环**（高风险逻辑漏洞）

**建议 A 优先完成 X-1/X-2/X-3 三项阻塞修订后，再送 B 复审。**

B 未改方案、未改 skill、未执行升级。

---

# A 对 B1 的处理（V0.11）

| B1 项 | 是否真问题 | A 动作 |
|---|---|---|
| X-1 把 §15 扩成 A-013～A-032 | **否。** §15 是方案级事实断言，不是机器断言目录。B 表用了 `requirement_refs`/`create_date`/`ai/sources/`，与已证伪模型相同 | **拒收该表**。§15 只补：P0 只读、4 脚本进包、SG-010 不依赖脚本。机器断言仍以 SG-009 §2.2 为准 |
| X-2 P1 脚本未在 §14 实施步骤 | **半真。** §14 本来就不是施工节（影响评估）。P1 已在 SG-009 文件表 + T41–T47 | 新增 **§13 施工总清单**，P1 两脚本写死「新建、进包、19 号不自动跑」 |
| X-3 无 Python 则结转硬阻断失效 | **否。** 硬阻断是 22 号规则，不是 verify 脚本。B 方案 A 会让无 Python 用户跳过结转，与 SG-010 目标相反 | SG-010 新增 §2.0b：无 Python **仍必须** Step 0；禁止 ASK 跳过 |
| Y-1 T 与 A-001 对齐 | 否（依赖拒收的 A-013 表） | 不改编号 |
| Y-2 开发仓 skip | 已有 A10-3 | 不重复 |
| Y-3 ` / ` split | 真 | D-PLAN-REF-01 写死 `split(" / ")` |
| Y-4 手补 README 不覆盖 | 真 | SG-011：已存在 skip；T48c |

请下一轮 B **对照 V0.11**，不要把 §15 再改成工作区机器断言总表。

---

# B2 审核结果（V0.11）

**审核角色**：B2（只审不改方案，不执行施工）  
**对照对象**：`governance-shared/planning/upgrade-plan-v3.15.0.md` **V0.11**  
**现网眼见**：ChronoPM-Project / ChronoPM-Portfolio 3.14.0、schema 0.15.0  
**审核日期**：2026-08-25  

## 总评

**判定：修订-需再审**

V0.11 已修正 B1 X-2/X-3/Y-3/Y-4 四项问题，新增 §13 施工总清单、SG-010 §2.0b 无 Python 硬阻断、D-PLAN-REF-01 `split(" / ")` 解析规则。**但仍有 1 个阻塞级自洽性问题**：§15 关键断言清单仍停留在"方案级事实断言"定义，与 SG-009 的机器断言体系脱节，导致放行门槛无法成立。

---

## 一、A 对 B1 处理核验（✅ 通过）

| B1 项 | A 动作 | B2 核验结果 |
|---|---|---|
| **X-1 §15 扩成 A-013~A-032** | **拒收**。§15 是方案级事实断言，不是机器断言目录；B 表用了现网没有的字段 | ✅ 通过。A11-1 明确拒收理由充分 |
| **X-2 P1 脚本未在 §14** | 新增 **§13 施工总清单**，P1 两脚本写死「新建、进包、19 号不自动跑」 | ✅ 通过。L1638-1672 已补入 verify_requirement_wp.py + verify_contract_ri.py |
| **X-3 无 Python 路径未闭环** | SG-010 新增 §2.0b：无 Python 仍必须 Step 0，禁止 ASK 跳过 | ✅ 通过。L1675-1681 已明确硬阻断不依赖 Python |
| **Y-3 plan_ref 多值解析** | D-PLAN-REF-01 写死 `split(" / ")` | ✅ 通过。L1530 已补入解析规则 |
| **Y-4 README 已存在 skip** | SG-011：已存在 skip，T48c | ✅ 通过。L1793 + T48c 已覆盖 |

**结论**：A 对 B1 的 5 项处理全部合理，方向正确。

---

## 二、仍存阻塞问题（❌ 需修订）

### 🔴 X-1 ★ §15 关键断言清单与 SG-009 机器断言体系脱节

**现状**：
- §15 关键断言清单（L1720-1729）定义为"**方案级事实断言**"，列了 11 条：
  - A-001/A-002: SG-001 迁移幂等
  - A-003/A-004/A-005: SG-004 current_operator
  - A-006: SG-005 环境检测
  - A-007: SG-006 examples 质量
  - A-008/A-009: SG-007 审计门禁
  - A-010: SG-008 Python 引导
  - A-011: SG-009 D-TODO-WP-01
  - A-012: SG-010 全员结转

- SG-009 §2.2 定义了完整的机器断言体系（C1-C8, D-TODO-01/02/03, D-REQ-WP-01/02, D-CONTRACT-01/02, D-SOURCE-01, D-PLAN-REF-01, D-EFFECT-01），共 14 条
- 测试项 T25-T47 验证这些机器断言

**矛盾**：
- §15 放行门槛："全部关键断言未被证伪"
- 但 §15 清单只有 11 条，**SG-009 的 14 条机器断言完全不在 §15 里**
- 若只测 A-001~A-012，SG-009 的 C1-C8/D-* 漏测即带病上线

**B1 的错误做法**：把 §15 扩成 A-013~A-032，混入现网没有的字段（requirement_refs/create_date/ai/sources/），这是错的。

**正确做法**：
- **§15 保持"方案级事实断言"定位**，不混入机器断言
- **新增 §15.1 机器断言清单**，列出 SG-009 的 14 条断言（C1-C8, D-TODO-01/02/03, D-REQ-WP-01/02, D-CONTRACT-01/02, D-SOURCE-01, D-PLAN-REF-01, D-EFFECT-01）
- **更新放行门槛**："全部方案级事实断言（A-001~A-012）+ 全部机器断言（C1-C8, D-*）未被证伪"

**必须修订**：

```markdown
### 15.1 机器断言清单（SG-009）

| 断言编号 | 检查内容 | 判定逻辑 | 一致判据 | 对应测试 |
|---|---|---|---|---|
| C1 | WP 名称投影 | WP front matter name == _index.md name 列 | 相等 | T25/T26 |
| C2 | WP 状态投影 | WP front matter status == _index.md status 列 | 相等 | T25/T26 |
| C3 | WP 负责人投影 | WP front matter owner == _index.md owner 列 | 相等 | T26 |
| C4 | WP 起止日期投影 | WP front matter start/end == _index.md start/end 列 | 相等 | T25/T26 |
| C5 | WP 计划引用投影 | WP plan_ref == _index.md plan_ref 列 | 相等 | T25/T26 |
| C6 | 计划 §3 引用闭合 | 正常计划 §3 引用的 WP 均存在于 _index.md | 无悬挂引用 | T28 |
| C7 | 废弃 WP 清理 | effect=废弃的 WP 不出现在任何正常计划 §3/§4 | 完全清除 | T25 |
| C8 | sources 索引同步 | ai/sources/ 下的源文件均在 _index.md sources 列有记录 | 无遗漏 | T25 |
| D-TODO-01 | 人员文件连续性 | 最新合法日 index 人员今日必须有文件 | 存在 | T30/T31 |
| D-TODO-02 | 待办滚存 | 最新合法日未办结待办今日必须存在 | 存在且 status=未完成 | T30/T31 |
| D-TODO-03 | 能耗延续 | 最新合法日有 §0.6 今日必须有文件 | 存在 | T30/T32 |
| D-REQ-WP-01 | 需求↔WP 关联 | requirement_refs 指向的需求必须在 register 存在 | 存在 | T41/T42 |
| D-REQ-WP-02 | WP→需求反向映射 | register 中每个需求的 wp_refs 必须包含引用它的 WP | 双向闭合 | T43/T44 |
| D-CONTRACT-01 | 合同↔需求映射 | contract_refs 指向的合同必须在 contract-register 存在 | 存在 | T45/T46 |
| D-CONTRACT-02 | 合同 RI 映射 | contract-register 中每个合同的 ri_refs 必须与需求 register 的 contract_id 匹配 | 匹配 | T47 |
| D-SOURCE-01 | sources 索引同步 | ai/sources/ 下的源文件均在 _index.md sources 列有记录 | 无遗漏 | T25 |
| D-PLAN-REF-01 | plan_ref 三处一致 | WP plan_ref == _index.md plan_ref == 计划 §3 引用（多值 split(" / ")） | 三处相等 | T25 |
| D-EFFECT-01 | 废弃 WP 清理 | effect=废弃的 WP 不出现在任何正常计划 §3/§4/§6；缺 effect 当正常 | 完全清除 | T25 |
```

**同时更新**：
- §15 放行门槛：改为"全部方案级事实断言（A-001~A-012）+ 全部机器断言（C1-C8, D-TODO-01/02/03, D-REQ-WP-01/02, D-CONTRACT-01/02, D-SOURCE-01, D-PLAN-REF-01, D-EFFECT-01）未被证伪"
- §22 自审表："~15 条断言"改为"**11 条方案级事实断言 + 14 条机器断言 = 25 条**"
- §23 结论："11 条需求全部有对应设计 + **25 条关键断言**"

---

## 三、非阻塞建议（🟡 可选优化）

| 编号 | 问题 | 建议 |
|---|---|---|
| Y-1 | §13 施工总清单未区分 P0/P1 | 补充优先级标注：P0（verify_projection.py + verify_todo_continuity.py）、P1（verify_requirement_wp.py + verify_contract_ri.py） |
| Y-2 | SG-001 迁移脚本的"开发仓无业务 ai/"场景未明确 | 已在 A10-3 拍板，可补一句到 §13 |
| Y-3 | T48c 测试描述过简 | 补充："README.md 已存在 → generate_single_readme skip，退出 0，不覆盖人工修改" |

---

## 四、放行门槛对照（A §15）

| 门槛 | 现状 | 判定 |
|---|---|---|
| 全部关键断言未被证伪 | ❌ §15 清单只有 11 条方案级事实断言，缺失 SG-009 的 14 条机器断言 | 不通过 |
| 无新增阻塞问题 |  X-1 仍存 | 不通过 |
| 评审包与正文一致 | ✅ §24 已改为 11 条来源 | 通过 |

**故：修订-需再审。**

---

## 五、必须修订清单（给 A，按优先级）

### 阻塞（不改不能再送审）：

1. **X-1 §15 补机器断言清单**：新增 §15.1，列出 SG-009 的 14 条机器断言（C1-C8, D-TODO-01/02/03, D-REQ-WP-01/02, D-CONTRACT-01/02, D-SOURCE-01, D-PLAN-REF-01, D-EFFECT-01）。更新放行门槛、§22、§23。

### 非阻塞建议：

- Y-1 §13 施工总清单补 P0/P1 优先级标注
- Y-2 SG-001 开发仓场景补到 §13
- Y-3 T48c 测试描述细化

---

## 六、总结

V0.11 相比 V0.10 已有显著进步：
- ✅ A 对 B1 的 5 项处理全部合理（X-1 拒收、X-2/X-3/Y-3/Y-4 全修）
- ✅ 新增 §13 施工总清单，P1 脚本实施步骤明确
- ✅ SG-010 §2.0b 无 Python 硬阻断闭环
- ✅ D-PLAN-REF-01 `split(" / ")` 解析规则明确
- ✅ SG-011 README 已存在 skip 机制落地

**但仍存 1 个阻塞问题**：
1. **§15 关键断言清单与 SG-009 机器断言体系脱节**（方案级事实断言 vs 机器断言混淆，导致放行门槛无法成立）

**建议 A 优先完成 X-1 一项阻塞修订后，再送 B 复审。**

B2 未改方案、未改 skill、未执行升级。

