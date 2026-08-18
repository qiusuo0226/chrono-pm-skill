# 升级到 1.18.1

> 从 1.18.0 升级到 1.18.1
> 发布日期：2026-08-15
> Schema 变更：无
> CR 编号：—

## 变更摘要

打包分发包命名标准化(Patch)：新增 tools/pack-skill/scripts/pack.py 本机主打包入口（产物命名 {BrandName}-Skill-v{version}.zip），排除模型实读 pack.ps1（单一事实源）；pack.ps1 增加 displayName 品牌提取 + 无 displayName 拒绝打包 + 标注跨平台参考实现；audit_release.py 新增断言11 命名漂移守门；SKILL.md 与 tools/SKILL.md 补充 Python 主路径与产物命名规范；版本失步修正（blueprint.lastVersion / SKILL_BLUEPRINT 当前版本）+ baselines/1.18.1 基线补档。无规则/模板/能力变更，无需工作区迁移。Blueprint Impact metadata-only。

## 新增目录

- 无

## 新增文件

- 无

## 删除文件/目录

- 无

## 规则变更

详见下方 CHANGELOG 摘录（1.18.1 段）。

## 模板变更

- 见下方 CHANGELOG 摘录中模板相关条目

## 工作流变更

- 无

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查（.skill-version.json → 1.18.1）


## CHANGELOG 摘录

## 1.18.1 — 2026-08-15（已发布 · released）

> 发布归档：Patch（打包命名标准化）。双 Agent 审核收敛（A 命名漂移诊断 → B 审核发现改错对象 → V3 修正为 pack.py 主路径 + 排除模型单一事实源）。核心升级：新增 Python 打包入口 pack.py，产物统一为 `{BrandName}-Skill-v{version}.zip`；排除模型实读 pack.ps1（唯一事实源）；audit_release.py 新增“命名漂移守门”断言；修复 v1.18.0 版本失步（blueprint.lastVersion / SKILL_BLUEPRINT 当前版本）+ 补 baselines/1.18.1 基线。无规则/模板/能力变更，无 workspace schema 变更，无需工作区迁移。

Blueprint Impact: metadata-only

### Added
- **pack.py 本机主打包入口**：`tools/pack-skill/scripts/pack.py`，产物命名 `{BrandName}-Skill-v{version}.zip`，排除模型实读 pack.ps1 四组数组（单一事实源），无 displayName 时拒绝打包。

### Changed
- **pack.ps1**：新增 displayName 品牌提取（按 `—`/`(` 切）+ 无 displayName 拒绝打包 + 头部标注“跨平台参考实现”。
- **audit_release.py**：新增断言 11“命名漂移守门”（仓库根禁止 `{name}-{version}.zip` 类产物）。
- **SKILL.md / tools/pack-skill/SKILL.md**：补充 Python 主路径与产物命名规范。
- **README.md / README.en.md**：新增“分发包命名规范”说明，版本号同步 1.18.1。
- **版本触点修正**：skill.json blueprint.lastVersion、SKILL_BLUEPRINT 当前版本与演进表同步 1.18.1。

### Notes
- 新增 `governance/baselines/1.18.1/` 基线快照。

---
