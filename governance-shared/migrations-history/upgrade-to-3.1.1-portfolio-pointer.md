# 升级到 3.1.1（ChronoPM-Portfolio 指针）

> 从 3.1.0 升级到 3.1.1
> 双包共用一条版本线。**主包为准**：请阅读
> `ChronoPM-Project/governance/migrations/upgrade-to-3.1.1.md`
>
> 本包本版：仅版本锁步 + 补齐 `governance/migrations/` 目录。规则/模板/只读契约零改动。
> Schema 变更：无。业务工作区零迁移。

## 变更摘要

开发仓重组（CR-G）。伴生包补齐升级执行目录；实质步骤见主包 upgrade 文件。

## 新增目录

- `ChronoPM-Portfolio/governance/migrations/`

## 新增文件

- 本指针文件

## 删除文件/目录

- 无

## 规则变更 / 模板变更 / 工作流变更

- 无（规则零改动）

## 验证检查

- [ ] 本包 `VERSION` == 主包 `VERSION` == 3.1.1
- [ ] 本文件存在且指向主包 upgrade
