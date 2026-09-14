# 升级到 3.29.0

> 从 3.28.0 升级到 3.29.0  
> 发布日期：2026-09-13  
> Schema：**0.17.0（不变）**  
> CR：CR-20260913-001（投喂一次做完）/ CR-20260913-002（源图佐证）  
> IA：IA-20260913-001 / IA-20260913-002  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> contract_change：是（SKILL.md 底线 20、00/01/04）。capability_change：是。  
> 回归合计 **980**（964+16）。  
> 用户拍板：执行升级吧，升级完一步就打 tag 推远程，一直完全升级完。B2：通过-待修订（V0.3 已并入 B2-1/B2-2）。

## 变更摘要

投喂当场一次写完（原文、能绑的唯一进行中包、已发生卡住）；经理不裁投喂绑包题；口述加待办仍问。拆文件抽出佐证图落到该源 `figures/`，条款可出示。通用槽位。schema 不变。无 migrate。

## 施工禁区

- 禁止新规则文件 / 新 ProcID / 新 DF
- 禁止废止 BS-018/019；禁止新造「未绑包」标记
- 禁止把源抽出图写入 `requirements/artifacts/`；禁止把外链原型截图写入 figures/
- 禁止改 SKILL.md §8 加 FIG 实体；禁止 Obsidian wikilink
- 禁止升 schema；禁止工作区迁移；禁止改写 `baselines/3.28.0/`
- 正式文档不得引用 upgrade-plan 路径
- 禁止写入业务库；Grok 安装区不代更
- 禁止重写 22 if-else 而弱化缺人闸；01 L42 闸不拆
- 05 L5 节题「与 SKILL 底线 14–16 同文」**保留不动**
- README 用例数按行替换该行全部 `964`（每行两处的都换）

## 工作区迁移

无。schema 仍 0.17.0。不跑 `migrate_workspace.py`。3.28.0 工作区直接按新规则对话即可。存量 sources 无 figures 合法。

## A. 施工（CR-001 投喂）

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR-001 / IA-001 / 本文件 | 治理 |
| A2 | Project `SKILL.md` §7 | 底线 20：投喂一次做完；分路径；不经 Q-7 回落 WF-8 问绑 |
| A3 | `01-daily-report-rules.md` §1.4 / Q-7 / L42 | 投喂唯一包 auto 绑否则待归属不问；切断 Q-7→WF-8；L42 对齐既有跳过、缺人仍阻断 |
| A4 | `22-carried-over-rules.md` §2.1 | 澄清 ELSE：只追加且已完成且齐全走 ELSE；缺人闸一句不得弱化 |
| A5 | `04-risk-issue-rules.md` §1.2.5.5 | 卡住高置信单条 auto 不问认；关闭仍确认；四档总闸不变 |
| A6 | `00-pm-main-rules.md` §5.0 | 投喂提问白名单指针；不复述五句 |
| A7 | `23-procedure-index.md` | P-HANDOFF Forbidden：下次再对包；多项目一任务；再打开原件打分 |
| A8 | 个人待办模板 | 沿用待归属；不造未绑包；Q-7 不在本文件旁注 |
| A9 | Portfolio `SKILL.md` | 投喂一次做完 + 按项目禁止合并 |
| A10 | Portfolio `01` §2.1/2.2 | 抽出行=交接 SSOT；每项目独立写任务；低置信问归属保留；卡住切片 auto |
| A11 | Portfolio `02` V-14 | 禁止抽出后再当混报理解；打分不得重开 original |
| A12 | tests Module 90 | ING-101～111；声明 BS-018/019 预期不变 |

## B. 施工（CR-002 存图）

| # | 文件 | 动作 |
|---|---|---|
| B1 | CR-002 / IA-002 | 治理 |
| B2 | `source-split-skill` split-rules + 模板 | figures/ 目录、文件名、抽图、失败降级、与 artifacts/ 互斥 |
| B3 | `06-file-rules.md` §2.1 | 登记 `sources/{编号}/figures/` + `requirements/artifacts/` |
| B4 | `07-requirement-rules.md` §8.10.3 | 点1–3 保留；补点4 源抽出图走 figures/ |
| B5 | ATOM 模板 / 底线 18 短指针 | evidence 可引相对路径；汇报可出示图；拍板仍 19 |
| B6 | tests Module 91 | FIG-001～005 |

## C9 顺序

1. 改 `scripts/_version.py` `SKILL_VERSION = "3.29.0"`（schema 行不动）
2. `python ChronoPM-Project/scripts/sync_version.py`
3. 手改 README.md 与 README.en.md **该行全部** 964→980
4. `python governance-shared/scripts/audit_release.py` 全绿

施工只认 **980**。禁止沿用 964。

## 验证

阻断：ING-101、ING-102、ING-104、ING-111、ING-109、FIG-001、FIG-005、RN-012。BS-018/019 判定不变。audit 退出 0。schema 0.17.0。

## 收尾（2026-09-13）

audit 17/17 通过。用户授权执行、tag、分发包。Grok 不代更。业务仓未代迁。schema 仍 0.17.0。AP 已删。分发包 129+46。现场抽题由使用方在真实工作区核验。

## 收尾补记（2026-09-14）

用户指示收尾。升级可以投入使用。Grok 安装区不代更。业务仓未代迁。施工核对 `review-20260913-3.29.0.md`：通过-升级成功。基线已同步本补记，无功能补丁。
