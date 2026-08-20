# 升级到 3.2.0

> 从 3.1.1 升级到 3.2.0
> 发布日期：2026-08-20
> Schema 变更：无（workspace schema 保持 0.9.0）
> CR 编号：CR-20260820-003
> 施工依据：`governance-shared/upgrade-plan-v3.1.0.md` V0.17 **§5c + §5d（CR-B）**；B 复审 P1：DF-007→P-WF-1+WF-8，DF-014→P-WF-2（含 22 号结转）
> 本次执行范围：仅 CR-B。不执行 CR-C～F。

## 变更摘要

DF-017 回复溯源标注 + DF-001~016 加载场景补标 + 按场景分类加载；PF 实例「加载场景」列（缺省 P-ALWAYS）；DF-018 主动识别习惯（每轮最多 1 条 SUGGEST）。标签存 Skill 主表，存量工作区零强制迁移。

## 新增目录

- 无

## 新增文件

- 本文件；`CR-20260820-003.md`；`IA-20260820-003.md`；`rr-20260820-3.2.0.md`；`governance-shared/baselines/3.2.0/`

## 删除文件/目录

- 无。上一份包内 upgrade（3.1.1）已归档 `governance-shared/migrations-history/`。

## 规则变更

- `references/21-pm-profile-rules.md`：§5.1a 主表加「加载场景」列 + DF-017/018；§2.2 按场景应用；§3.1 加载场景表；§5.1 主动观察 + SUGGEST 规范。DF-007 = P-WF-1+WF-8；DF-014 = P-WF-2（结转加载 22 号时同载）。
- `references/00-pm-main-rules.md`：§9.0 数据来源标注（查询出数据来源，写入出已写路径，禁罗列扫描过程）。

## 模板变更

- `assets/templates/pm-profile-template.md`：预填 DF-017/018；表头加「加载场景」列（DF 行填 —，PF 缺省 P-ALWAYS）。

## 工作流变更

- 回复涉及读/写文件必须标路径（DF-017，P-REPLY）。
- 每轮结束主动观察习惯（DF-018）；连续 3 次 → pending + 末尾 SUGGEST；每轮最多 1 条。

## 验证检查

- [ ] §5.1a 含 DF-001~018 且每行有加载场景
- [ ] 存量 pm-profile.md 不强制改；无加载场景列 → P-ALWAYS
- [ ] schema 仍 0.9.0
- [ ] `python governance-shared/scripts/audit_release.py` 13/13 PASS

## 存量工作区

零强制迁移。缺失 DF-017/018 行按 21 号 2a 从模板补行（disabled + 提示），不覆盖已有同义 PF。

## 明确不做

- CR-C～F（关联待办、存根范式、wps/、RI）
