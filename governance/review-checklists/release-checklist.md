# Release Checklist

发布前必须确认所有检查项：

## Change Control

- [ ] 是否有 Change Request？
- [ ] 是否有明确可验证目标？
- [ ] 是否没有混入无关改动？
- [ ] 是否有 Impact Analysis？
- [ ] 是否已获得用户确认？

## Compatibility

- [ ] 是否影响核心契约？
- [ ] 是否影响 workspace schema？
- [ ] 是否需要迁移脚本？
- [ ] 是否影响旧工作区？

## Regression

- [ ] 是否运行正向用例？
- [ ] 是否运行反向用例？
- [ ] 是否运行旧功能回归用例？
- [ ] 是否没有失败用例？

## Documentation

- [ ] 是否更新 VERSION？
- [ ] 是否更新 skill.json？
- [ ] 是否更新 CHANGELOG.md？
- [ ] 是否更新 SKILL.md？
- [ ] 是否生成 regression report？
- [ ] SKILL_BLUEPRINT.md 是否已按版本级别更新（必更/应更/免更）？
- [ ] skill.json blueprint.lastVersion 是否与 VERSION 一致？
- [ ] CHANGELOG 是否标注 Blueprint Impact？

## Script Version Consistency（脚本层版本一致性）

- [ ] `scripts/_version.py` 的 `SKILL_VERSION` 是否为本次发布版本？
- [ ] `scripts/chronopm_init/config.py` 是否从 `_version` 导入且不再含版本字面量？
- [ ] `scripts/migrate_workspace.py` 是否从 `_version` 导入且不再含版本字面量？
- [ ] `scripts/chronopm_init/file_registry.py` README 是否使用 `{SKILL_VERSION}`/`{WORKSPACE_SCHEMA_VERSION}` 插值（无硬编码版本）？
- [ ] 是否已运行 `python scripts/sync_version.py`（自 `_version.py` 同步 `VERSION`/`SKILL.md` frontmatter/`skill.json`）？
- [ ] `VERSION` / `SKILL.md` / `skill.json` / `_version.py` 四处版本号是否一致？

## v1.13.0 架构精简改造专项检查（CR-20260812-001）

- [ ] 级联传播规则：确认 03/04/07/08/09/02 号文件的级联 §已添加且格式一致
- [ ] 归档治理：确认 06 号 §9 通用归档表、02 号 decision-log 归档、09 号 transfer-log 归档已就位
- [ ] 版本同步：确认 `_version.py` → VERSION/SKILL.md/skill.json 四触点一致
- [ ] 新建文件：确认 `assets/templates/decision-log-template.md` 和 `scripts/sync_version.py` 存在且内容正确
- [ ] 索引分级：确认 14 号 §2.4 三级分类（完全派生/增量维护/独立累积）已写入

## Project Cleanliness

- [ ] 根目录白名单合规性：对照 §18 白名单逐项检查，无非标准文件/目录？
- [ ] 治理目录无临时工作文件：`governance/` 下无 Agent 草稿或临时输出？
- [ ] 正式文档无幽灵引用：CR、IA、RR、基线 README、CHANGELOG 中引用的文件必须实际存在？
- [ ] 无构建缓存残留：`__pycache__/` 等已清除？
- [ ] 文档内版本号一致性：SKILL.md 版本控制表、CHANGELOG 最新版本号与 VERSION 一致？
- [ ] 白名单同步检查（如适用）：本次 CR 的 AP-4 包含根目录 `new_file` 时，白名单是否已新增该文件？

## Baseline

- [ ] 是否创建新版本基线？
- [ ] 是否保留上一版本回滚路径？

## Copy

- [ ] 是否复制到灵犀安装目录？

---

## 已知污染类型附录

> 本附录记录发布过程中发现的污染类型。每次发现新污染类型时追加到本附录，下一次 CR 中评估是否需要正式修订白名单（§18）或交付物类型控制（§19）。

| 编号 | 污染类型 | 发现版本 | 说明 |
|---|---|---|---|
| P-01 | Agent 工作草稿（根目录） | 1.11.0 | `A-升级方案-CR-*.md`，Agent 在根目录输出方案全文而非归档到 governance/ |
| P-02 | RELEASE-NOTES（根目录） | 1.11.0 | `RELEASE-NOTES-*.md`，Agent 自行创建发布说明，非治理流程要求的交付物 |
| P-03 | Agent 旧工作目录（根目录） | 1.11.0 | `CR-*/` 目录，早期 CR 执行时创建，完成后未清理 |
| P-04 | Python 构建缓存 | 1.11.0 | `__pycache__/`，运行脚本时自动生成 |
| P-05 | 幽灵引用 | 1.11.0 | 正式文档引用了不存在的文件或非标准产物（如引用 RELEASE-NOTES、A-升级方案） |
| P-06 | 陈旧版本号 | 1.11.0 | SKILL.md 版本控制表未随版本更新而刷新 |
