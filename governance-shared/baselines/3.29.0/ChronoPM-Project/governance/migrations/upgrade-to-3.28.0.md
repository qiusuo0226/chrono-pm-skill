# 升级到 3.28.0

> 从 3.27.0 升级到 3.28.0  
> 发布日期：2026-09-11  
> Schema：**0.17.0（不变）**  
> CR：CR-20260911-001  
> IA：IA-20260911-001  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（SKILL.md / 00）。  
> 回归合计 **964**。  
> 用户拍板：开始升级，一直升级完。B2：通过-可执行。

## 变更摘要

对外拍板禁止技能黑话：SKILL 底线 19（分段 + 五句自检）；00 确认专节拆段并补词典；问答规范加本翻车对错例；查询待办编号除外；升级健康报告只许出现在汇报段；Portfolio 同口径一句。无目录变更、无 migrate。

## 施工禁区

- 禁止新规则文件 / 新 ProcID / 新 DF
- 禁止脚本扫描对外正文；禁止每轮加载 reply-norm 全文
- 禁止入口堆翻译表；五句只在底线 19
- 禁止改 `skill-contract.md` 正文；禁止改 examples/02、03
- 禁止改写 `baselines/3.27.0/`
- 正式文档不得引用 upgrade-plan 路径
- 禁止写入业务库；Grok 安装区不代更
- 05 L5 节题「与 SKILL 底线 14–16 同文」**保留不动**
- README 用例数按行替换该行全部 `961`（B2-N1：L118/L117 每行两处）

## 工作区迁移

无。schema 仍 0.17.0。不跑 `migrate_workspace.py`。3.27.0 工作区直接按新规则对话即可。

## A. 施工

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR / IA / 本文件 | 治理 |
| A2 | Project `SKILL.md` §7 | 底线 19；L98/L198 字面 |
| A3 | `00-pm-main-rules.md` §5.0 | 拆段、词典 5 行、L218 字面、失败标准 |
| A4 | reply-rules / CAPABILITY / capability-boundary | 硬规则指针、对错例、L12/L18/L44 |
| A5 | `05-query-rules.md` | 正文 19 指针；清单第 7 条除外；节题不动 |
| A6 | `20-workspace-version-rules.md` | 健康报告=汇报段 |
| A7 | `23-procedure-index.md` | P-REPLY Forbidden |
| A8 | Portfolio `SKILL.md` §8；`06` §6 | 同口径一句 |
| A9 | `tests/regression-suite.md` | Module 89 + 统计 964 |
| A10 | `SKILL_MODULE_MAP.md` L245 | 14-16+19 |
| A11 | `_version.py` 3.28.0 → `sync_version.py` → README×2 手改 964 → CHANGELOG / BLUEPRINT | C9 |
| A12 | baselines / audit / 打包 | 发布 |

## 验证

阻断：RN-012、RN-013、RN-003、待办 TD 编号（RN-014）。施工只认 **964**。audit 退出 0。schema 0.17.0。全仓 grep `961` 在现行 README/统计表/SKILL 版本触点为零（历史 CHANGELOG/基线保留）。

## C9 顺序

1. 改 `scripts/_version.py` `SKILL_VERSION = "3.28.0"`（schema 行不动）
2. `python ChronoPM-Project/scripts/sync_version.py`
3. 手改 README.md L102/L114/L118 与 README.en.md L101/L113/L117 **该行全部** 961→964
4. `python governance-shared/scripts/audit_release.py` 全绿

## 收尾（2026-09-11）

audit 17/17 通过。B3 施工结果合格。用户授权收尾提交、tag、分发包。Grok 不代更。业务仓未代迁。schema 仍 0.17.0。现场抽题由使用方在真实工作区核验。
