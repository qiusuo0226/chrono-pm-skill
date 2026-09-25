---
doc_type: ingest-map
portfolio: [项目集名称]
updated: YYYY-MM-DDTHH:MM
---

# 弱结构投喂列映射档

> 运行时落 `ai/portfolio/context/ingest-maps.md`（无集层则 `ai/context/ingest-maps.md`）。
> 只存指纹 + 列→槽位 + `fill_down`。禁止把业务列名写进 Skill 规则文件。不含进度/人名事实。

## 映射表

| 指纹（列数+首行 token+种类词） | 列序号 | 槽位 | fill_down | 确认人 | 确认日 |
|---|---|---|---|---|---|
| 7\|前端,后端,产品\|未完成 | 1 | project | true | [姓名] | YYYY-MM-DD |
| 7\|前端,后端,产品\|未完成 | 3 | feature | false | [姓名] | YYYY-MM-DD |

槽位仅：`project` | `wp` | `feature` | `role:<名>` | `person` | `stage` | `status` | `note` | `date` | `group`。

同指纹再投不问列。行键命中只追加 note / 更新角色人，不新建 WP。
