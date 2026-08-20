# Upgrade to 3.5.1（Patch · 措辞残留修复）

> 源版本：3.5.0 → 目标版本：3.5.1
> workspace schema：0.10.0（**不变**）
> 性质：纯措辞修复，无行为/结构变化。

## 变更内容

- project-brief 模板 §4 人员路由统一为本项目 `resources/`（删除 `projects/{子项目}/`、`portfolio/resources/shared-resource-index.md` 存储路径，仅留禁止性说明）
- 14 号自检规则：月度索引 4 处表述改「停维/存量可留」口径（对齐「v3.4.0 停维」）
- outputs-index / output-manifest 模板：清理 portfolio_weekly_report 等枚举残留
- project-notes 模板位置指针、workspace-health 模板停维标注对齐

## 业务工作区升级步骤

**无**。本版本不涉及任何工作区目录结构、文件格式或流程行为变化：

- 不需要运行 `migrate_workspace.py`（schema 仍为 0.10.0）
- 不需要修改任何业务数据文件
- 直接替换 Skill 包即可（VERSION / skill.json / SKILL.md 版本号更新为 3.5.1）

## 注意事项

- 若你的工作区曾按旧模板写过 `projects/{子项目}/resources/` 或 `portfolio/resources/shared-resource-index.md` 指针，属历史存量，可保留不动；新记录一律走本项目 `resources/resource-register.md` / `resources/transfer-log.md`，跨项目共享人力查询用 ChronoPM-Portfolio。
- 存量 `reports/daily/YYYYMM/index.md` 月度索引可留不删，不再追加、不做一致性校验（D8 不因此报错）。
