# 升级到 3.3.0

> 从 3.2.0 升级到 3.3.0
> 发布日期：2026-08-20
> Schema 变更：无
> CR 编号：CR-20260820-004
> 施工依据：方案 §5e + §5j + §5l（CR-C）；V0.16：TD 格式统一、缩写拆独立小表、05 双键反查
> 本次范围：仅 CR-C。不执行 CR-D～F。

## 变更摘要

关联待办（§1.3 列，WF-Linked SUGGEST）+ 工作日志 TD Ref + 人员缩写治理小表（项目内唯一、冲突 ASK、历史别名反查）。存量零强制迁移。截止条件：首次 WF-8/进组前完成本项目缩写回填。

## 新增目录 / 删除文件

- 无。上一份包内 upgrade（3.2.0）已归档 `governance-shared/migrations-history/`。

## 规则变更

- `00`：WF-Linked；WF-8 缩写查重；§8a.2 关联待办检查；§5a 溯源条款
- `01`：§3 工作日志强制 TD Ref
- `05`：TD 编号反查双键（现行缩写 → 历史别名）
- `22`：§3.1a 进组缩写查重
- 伴生包 `05-resource-shared-rules.md`：跨项目按中文名归并

## 模板变更

- `personal-daily-todo-template.md`：§1.3 加「关联待办」列；§3 加 TD Ref
- `resource-register-template.md`：新增「TD 编号治理」小表
- `daily-todo-binding-template.md`：缩写列抄自 register

## 工作流变更

- 待办终态 → WF-Linked SUGGEST，禁止 AUTO
- 新号前人名段必须取 register 现行缩写
- 写 §3 必须带 TD Ref 或待归属

## 存量工作区

- 无关联待办列 = 无关联；无 TD Ref = 未关联
- 缩写列 AI 辅助回填：清单 → PM 确认 → 写入；冲突不猜测。截止条件 = 首次 WF-8/进组前
- Q14：全链通储金晶等业务数据修正不进 Skill 包，发布后在业务工作区走回填+裁定

## 明确不做

- CR-D～F；不重编旧 TD 号；不新建独立缩写注册表文件
