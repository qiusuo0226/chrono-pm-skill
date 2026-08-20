# 升级到 {version}

> 从 {prev_version} 升级到 {version}
> 发布日期：{date}
> Schema 变更：{schema_from} → {schema_to}（无变更则填"无"）
> CR 编号：CR-YYYYMMDD-NNN（推导依据文件）

## 变更摘要

{一句话描述，与 skill.json versionHistory summary 保持一致}

## 新增目录

- `path/to/new/dir/` — 用途说明
- （无则填"无"）

## 新增文件

- `path/to/new/file.md` — 用途说明（模板：`template-name.md`）
- （无则填"无"）

## 删除文件/目录

- `path/to/old/file.md` — 废弃原因 → 处置（归档/删除）
- （无则填"无"）

## 规则变更

- `references/XX-name-rules.md`：具体变更描述
- （无则填"无"）

## 模板变更

- `assets/templates/xxx-template.md`：具体变更描述
- （无则填"无"）

## 工作流变更

- WF-X：具体变更描述
- （无则填"无"）

## 验证检查

- [ ] 新增目录存在检查
- [ ] 新增文件存在检查
- [ ] 删除路径已清理检查
- [ ] 版本信息同步检查
