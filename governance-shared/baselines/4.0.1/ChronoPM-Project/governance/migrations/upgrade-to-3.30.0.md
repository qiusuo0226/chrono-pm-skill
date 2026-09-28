# 升级到 3.30.0

> 从 3.29.0 升级到 3.30.0  
> 发布日期：2026-09-20  
> Schema：**0.17.0（不变）**  
> CR：CR-20260920-001  
> IA：IA-20260920-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（SKILL.md 底线 17、00 P-CORRECT/P-VIEWS）。capability_change：是。  
> 回归合计 **996**（980+16）。  
> 用户拍板：执行升级，每步打 tag 推远程，全部完成后再审。

## 变更摘要

标准文档拆完后 `_digest.md` 按 6 个来源大类编成单源主题页。查询先读页。过期由 `refresh_views.py` 写入 `.state.json.source_digest_status`（独立字段，不并入 `facts_fingerprint`）。脚本只检测、不重编页。纠偏改切片必须同轮重编页。schema 不变。无 migrate。双包同号。集层不编页。

## 施工禁区

- 禁止新建 `ai/wiki/` 必填目录；禁止升 schema；禁止 migrate
- 禁止新 ProcID；禁止 Obsidian `[[wikilink]]`
- 禁止 `sources/_index.md` 加第 8 列
- 禁止把 atoms/facts 并入 `collect_facts` / `facts_fingerprint`
- 禁止脚本自动重写 `_digest.md`
- 禁止跨源主题页、账本 Wiki、集层编页
- 禁止改写 `baselines/3.29.0/`
- 正式文档不得引用 upgrade-plan 路径
- 禁止写入业务库；Grok 安装区不代更
- 05 L5 节题「与 SKILL 底线 14–16 同文」**保留不动**
- README 用例数按行替换该行全部 `980`（每行两处的都换）

## 工作区迁移

无。schema 仍 0.17.0。不跑 `migrate_workspace.py`。3.29.0 工作区直接按新规则对话。存量 `_digest.md` 无 `doc_type: source-digest` 合法，查询可读不得当已编主题页。

## A. 施工

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR-001 / IA-001 / 本文件 | 治理 |
| A2 | `source-split-skill/references/digest-schemas.md` | 新建：6 类骨架 + 5 特化 + 双指纹 + 行顶 + local_only + 禁 wikilink |
| A3 | split-rules / CAPABILITY / capability-boundary | 协调者收尾编译 `_digest`；禁 outputs；加载 digest-schemas；模板五份 |
| A4 | source-doc-meta-template | `_digest` 改 source-digest frontmatter |
| A5 | 05 | 源文档行读 `source_digest_status`；无 Python 属性串比对 |
| A6 | 06 | digest=派生，禁止当价款/范围唯一证据；§7.5 保持 7 列 |
| A7 | 07 | 六件套句：digest 为主题页 |
| A8 | 10 | 「编成页」仅已拆源（SRC/CON）；待办/计划/WP 不触发 |
| A9 | 23 | P-SPLIT Calls+=编译；P-CORRECT Calls+=改切片则重编 |
| A10 | 00 | P-CORRECT 同轮重编；P-VIEWS：brain 仍比 facts 指纹；主题页过期读独立字段 |
| A11 | SKILL.md | 底线 17 加 `_digest`/主题页；拆解产出半句；不新路由 |
| A12 | 19 §3.3b | 存量旧摘要不判死 |
| A13 | `refresh_views.py` | `collect_source_digest_status`；skip 只补字段；`--print-slice-fp` 只打印。view-spec 不动 |
| A14 | tests Module 92 | SW-001～016；合计 996 |
| A15 | examples/04、19 | `_digest.md` + facts；可读页 |
| A16 | Portfolio VERSION / skill.json / CHANGELOG | 仅锁步 3.30.0，能力零改动 |

## C9 顺序

1. 改 `scripts/_version.py` `SKILL_VERSION = "3.30.0"`（schema 行不动）
2. `python ChronoPM-Project/scripts/sync_version.py`
3. 手改 README.md 与 README.en.md **该行全部** 980→996
4. Portfolio 三文件 metadata
5. `python governance-shared/scripts/audit_release.py` 全绿

施工只认 **996**。禁止沿用 980。

## 验证

阻断：SW-001、SW-003、SW-004、SW-005、SW-009、SW-012、SW-015。SW-016 必过。FIG/ING/SD/RN 不回退。audit 退出 0。schema 0.17.0。

## 回滚

还原基线 3.29.0。已编译页按旧摘要读。无工作区回退。

## 收尾（2026-09-20）

audit 17/17 通过。用户授权执行、步 tag 推远程。Grok 不代更。业务仓未代迁。schema 仍 0.17.0。AP 已删。分发包 131+46。现场抽题由使用方核验。
