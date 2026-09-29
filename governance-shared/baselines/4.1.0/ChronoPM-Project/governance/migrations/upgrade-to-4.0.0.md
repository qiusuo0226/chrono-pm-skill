# 升级到 4.0.0

> 从 3.30.3 升级到 4.0.0  
> 发布日期：2026-09-23  
> Schema：**0.17.0（不变）**  
> CR：CR-20260923-001  
> IA：IA-20260923-001  
> 施工依据：本文件。  
> Major。回归合计 **1041**（1028+13）。  
> 用户拍板：执行升级吧。

## 变更摘要

1. 查询收进 `query-skill/`。提问运行 `query_locate.py`，只哈希命中的那一个文件。
2. Portfolio 收进 `portfolio-skill/`。仓库根不再保留独立技能。只打 Project 一个包。
3. `domain-glossary.md` 第 1 表为 7 列（编号、说法、登记名、路径、状态、来源、热度），附注另表也是 7 列。并入旧别名。`needs_v400` 做完才允许盖戳。
4. 集根仍不能当单项目写入。投喂和跨项目查询加载 `portfolio-skill`，不再提示另装技能。

## 施工禁区

- 禁止升 schema；禁止新建 `ai/wiki/`；禁止 `[[链接]]`
- 禁止把说法表路径写成「对话 / 文件 / 系统」
- 禁止查询热路径调用 `refresh_views.py --all`
- 禁止给 `refresh_views.py` 增加 `--read-only`
- 禁止改 `baselines/3.30.3/`
- 禁止用名为 MIGRATIONS 的字典。入口是 `VERSION_CAPABILITIES` 与 `needs_v400`
- 低版本技能不得改高版本工作区
- 不代更 Grok 安装区，不写业务仓

## 工作区存量（强制）

- **谁执行**：`migrate_workspace.py` 的 `needs_v400`，以及 `enforce_workspace_upgrade.py` 在盖戳前调用同一套函数。
- **成员根**：把词库、`context/active-entities.json` 的 `alias_index`、工作包解析出的名称/编号/功能点/supersedes 并进第 1 表。按权威清单写 `fact_stamps`。集层文件不写戳。少一键或读失败则退出码非 0，不改 skillVersion。
- **集根**：不编主题页，不建说法表。各成员合并成功后重写 `portfolio/context/glossary-index.md` 的指针。成员未完成则集根也不盖戳。
- **版本已等于 4.0.0**：仍检查第 1 表是否为 7 列，以及戳是否写上。没完成不得当成功。
- **失败**：不得写「可以投入使用」。

## 版本链

3.30.3→4.0.0 直接执行本文件。`VERSION_CAPABILITIES` 补上 3.28.0 至 3.30.3 的空条目，否则 `get_capabilities_since("3.30.3")` 对不上 4.0.0。

## 验证

`python ChronoPM-Project/tests/test_query_locate_v400.py` 打印 ok。`python governance-shared/scripts/audit_release.py` 全绿。

## 回滚

还原基线 3.30.3 的 Project 与 Portfolio。schema 无回退。说法表多出的列可留。
