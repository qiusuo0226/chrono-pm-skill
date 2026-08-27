# 技能缺口捕捉规则

由 P-SKILL-GAP 加载（SKILL.md「技能缺口」行；10 号技能缺口信号）。禁止未加载本文件就落 `需求-*.md`。禁止把本文件内容写成项目 REQ。

主包交叉点：闸 1 B 路、11 号批次、00 P-ALWAYS 第 4 步（只检测）、20 号版本字段。需求/WP 绑定仍在 07/00，与本文件无关。

## 1. 过程签名

| 项 | 值 |
|---|---|
| ProcID | P-SKILL-GAP |
| Home | 本文件 |
| Pre | 闸 1 = B 路；已载 11 |
| Calls | 必须 CALL P-OUTPUT（建 `ai/outputs/{YYYYMMDDHHMMSS}/` + 登记 outputs/index.md）。**Type=skill_gap 不建 manifest.md**，元数据写在需求文件 front matter |
| Writes | `{批次}/需求-{短标题}.md`（主文件，不走 draft.md） |
| Forbidden | 写 requirements/wps/plans/todos；当 REQ/待办；嵌套 SKILL.md；数据缺失走本过程；未达触发阈值落盘；问「要不要记」；写入或提议写入 `pm-decisions.md`；请 PM 确认本产物 |

P-ALWAYS 第 4 步只检测，不写文件。写文件只走 P-ROUTE → 本过程 → P-OUTPUT。

## 2. 要落盘（满足任一）

1. 用户明示：技能做不到 / 做不了 / 这是 skill 的问题 / 记成升级需求 / 记成技能缺口。
2. 同一意图本对话硬拒绝 ≥2 次（无合法路径，或必须违反硬约束且无替代）。
3. 10 号技能缺口信号命中，且过第 3 节排除清单。

简单查询（仅 05）不经 P-ALWAYS 第 4 步；但 Level 1 显式「记成升级需求」须改口加载本文件后落盘。

## 3. 不要落盘

- 缺数据 / 缺确认 → 19 / pm-decisions
- 换 Portfolio 或换项目对话就能做
- 规则已有、本轮未加载 → 先加载做完
- 纯格式口吻 → 21
- 口误已纠正
- 废弃 WP 等业务状态 → P-WP-RETIRE
- 用户追问、不满意、信息理解偏差（无明示词、无两次硬拒绝）

落盘文「三、定位 / 已排除」至少写 1 条排除。

## 4. 写时机

先写后告知。告知路径 + 一句话痛点。用户说不要记 → 该批次 Status=已取消，本对话同类不再写。禁止问「要不要记」。

不走 11 号 draft→final。主文件即 `需求-{短标题}.md`。禁止再问是否归档进事实源。本产物是 Skill 升级辅助记录，**不进** `pm-decisions.md`，不需要 PM 确认。改 Skill 仍走 16 号 AP/CR。

7 日内 `outputs/index.md` 已有 Type=skill_gap 且痛点指纹相同 → 追加原批次 `revisions/rev-NNN.md`，不新开批次（用户说另出一版除外）。

## 5. 编号与头

`sg_id: SG-{今天}-NNN`。NNN = 当日 Type=skill_gap 已有最大号 +1，无则 001。读 `ai/outputs/index.md`，禁止猜。落盘前再读 index：该 `sg_id` 已存在 = **级联失败**，不得写第二份同号（追加 revision 除外）。

YAML 必填：doc_type=skill-gap-demand；sg_id；skill_name；skill_version_installed（**只抄本包 `VERSION`，禁止手写/猜测**）；workspace_skill_version 与 workspace_schema（**只抄 `ai/.skill-version.json`**）；project；created_at；priority（AI 建议）；batch_id。建议：source_files。两行版本不一致须在正文写「版本差」。不另写 manifest.md。**读模板只读 Skill 包 `skill-gap-skill/assets/templates/` 与 `assets/templates/`，禁止以工作区 `ai/templates/` 为权威。**

落盘后检查：批次目录若出现 `manifest.md` = **级联失败**，删除该 manifest 并重写主文件 front matter。

短标题 ≤20 字，来自一句话痛点。

## 6. 正文

落盘前必读 `skill-gap-skill/assets/templates/skill-gap-demand-template.md`。**当前模板为唯一范本**。禁止以 `ai/outputs/**/需求-*.md` 历史批次为范本（旧批次可能缺 〇·五）。

节号 〇、〇·五、一～七，不得跳号、不得省 〇·五。单表 ≤6 列。流图用 mermaid。

必选：文首痛点、元信息、〇开场、〇·五示例图、一现象原话后果、二为何（含现状 vs 应有）、三定位、四时间证据链、七复现。
可选：五全景、六建议补丁（禁止完整 AP）。

〇·五：形态/图形/可视化类必须贴目标产出图（Mermaid/示意）。其它类节标题必须在，节内写「本条无目标产出形态图」。第二节数据流图不能代替 〇·五。

**落盘前结构自检（强制）**：对照模板节标题逐项打勾。缺节当场补全后再写文件、再登记 `outputs/index.md`。缺节仍落盘 = 级联失败。CALL P-OUTPUT 建批次后、更新 index 前完成自检。

## 7. 与 P-OUTPUT

先 P-OUTPUT 建批次（Type=skill_gap，Main File=需求-*.md，**不建 manifest**），再写主文件，再更新 index。缺任一步 = 级联未完成。批次内出现 `manifest.md` = 级联失败。宿主默认目录落到项目根 → 仍映射本批次（闸 1）。
