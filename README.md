# ChronoPM v3.7.0 — ChronoPM-Project 单项目 + ChronoPM-Portfolio 只读集

**让 AI 帮你管项目，而不是帮你写文档。**

装上 Skill，把日报、纪要、合同丢给 AI。事实写在 Markdown 里，确认后才生效。人走知识留在文件夹里。

> **双包**：日常录入用 **ChronoPM-Project**。跨项目进度 / 风险 / 合同 / 周报用 **ChronoPM-Portfolio**（只读，不写成员项目）。

## 你可能正在这样耗时间

| 痛点 | ChronoPM 怎么接 |
|---|---|
| 换个 PM，标准全变 | 统一规则兜底，不靠个人习惯 |
| 日报、风险、待办对不上 | 待办文件是唯一事实源，报表都是派生 |
| 交接甩一包文件，接手找不到北 | 移交 `ai/` 文件夹，AI 读完就能接 |
| 通用 AI 听不懂项目黑话 | 词库 + 项目记忆，越用越准 |
| 「有风险」四个字就被登进登记册 | v3.7.0 判定卡：先三问，确认才写 |

## 开口就能用

| 你说 | AI 做 |
|---|---|
| 「今天的日报」 | 存档、映射待办、该问的风险先出判定卡 |
| 「纪要点如下…」 | 纪要 + 行动项落到责任人待办 |
| 「这个需求在不在合同里」 | 合同 → 招投标 → 条款，带证据链 |
| 「这周进展怎么样」 | 从待办汇聚周报，不编造 |
| 「跨项目整体状态」 | 换 ChronoPM-Portfolio 只读归集 |

**写只写待办文件** `todos/{日期}/{人}.md`。日报/周报/进度/倒排都从它实时汇总。任务包 `WP-NNN` 管分组和里程碑；进度 = 下辖待办完成比例，不另存一份过时数字。

终态（完成/关闭）要你确认。AI 不替你改事实。

## v3.7.0 这一版多了什么

- **拆解合同/标书**：同源识别、二次拆解增量覆盖、拆解历史可查；大文档自动分片，AI 读得动。
- **实体进度跟 WP 走**：不再单独维护 entity-registry；模块/市场主体状态写在工作包 §3b。
- **风险先判定再登记**：见「有…风险」不直接入库；登记册改成条目块 + 时间线（单表不超过 7 列）；新号 `R-NNN` / `I-NNN`。
- **高等级风险必须有应对待办**（建议给你确认，不会偷偷写）。

## 两种用法

- **单项目**：一个 `ai/` 管一个项目。
- **项目集**：Portfolio 只读汇总多个项目；跨项目数字查询时现算，不落盘。

## 装上就能跑

1. 把 `ChronoPM-Project/`（跨项目再加 `ChronoPM-Portfolio/`）复制到 AI 工具的 Skill 目录。不要复制整个仓库根。
2. 对 AI 说：「帮我初始化项目工作区」。
3. 日常把材料丢给它，像跟助手说话。

开发仓打包：`python tools/pack-skill/scripts/pack.py --skill-root ChronoPM-Project`  
发布前：`python governance-shared/scripts/audit_release.py` 必须通过。

## 包含什么

| 内容 | 数量 | 说明 |
|---|---|---|
| 规则文件 | 22 份 | 定义 AI 在各类场景下该怎么做事 |
| 文档模板 | 38 个 | 日报、周报、会议纪要、风险登记册、WP、源文档拆解 |
| 自动化脚本 | 5 个 | 初始化、迁移、版本同步 |
| 回归测试 | 380 个用例 | 确保每次更新不破坏已有功能 |

```
ChronoPM Skill/
├── ChronoPM-Project/     # 单项目 Skill 包根（打包根；内含 SKILL.md / references / assets / scripts / tests 回归测试套件（380 个用例） / governance/migrations 当前 upgrade）
├── ChronoPM-Portfolio/   # 只读项目集伴生包
├── governance-shared/    # 仓库级共享（不进分发包）：baselines / CR / IA / RR / audit
├── tools/                # 打包工具
├── README.md
├── README.en.md
└── LICENSE.txt
```

## 版本信息

| 项目 | 值 |
|---|---|
| Skill 版本 | 3.7.0 |
| 工作区 Schema | 0.12.0 |
| 规则文件 | 22 份 |
| 文档模板 | 38 个 |
| 回归用例 | 380 个 |

发布产物：`ChronoPM-Project-Skill-v3.7.0.zip` + `ChronoPM-Portfolio-Skill-v3.7.0.zip`。

升级日志：[ChronoPM-Project/CHANGELOG.md](ChronoPM-Project/CHANGELOG.md)
