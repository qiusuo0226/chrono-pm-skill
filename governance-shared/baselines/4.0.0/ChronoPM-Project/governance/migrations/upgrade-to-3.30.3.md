# 升级到 3.30.3

> 从 3.30.2 升级到 3.30.3  
> 发布日期：2026-09-22  
> Schema：**0.17.0（不变）**  
> CR：CR-20260922-001  
> IA：IA-20260922-001  
> 施工依据：本文件。  
> Patch。回归合计 **1028**（1011+17）。  
> 用户拍板：执行升级吧。

## 变更摘要

1. 会话钩子启动 `scripts/enforce_workspace_upgrade.py`。程序自己比版本、串已拆标准文件、决定能不能改版本号。
2. 已拆标准文件的链：切片的章节或页码 → 已有需求的来源指针和文档链接 → 已有工作包编号。串不完不改该工作区的 skillVersion。
3. `stamp_skill_version()` 是新建包装，内部才调用 `update_version_file()`。迁移脚本不再提前写 skillVersion。

## 施工禁区

- 禁止升 schema；禁止新建 `ai/wiki/`；禁止 `[[链接]]`
- 禁止新建需求或工作包；禁止按模糊标题猜测
- 禁止改 `refresh_views.py` 的合格判定；禁止日常 `--all` 重写 `_digest.md`
- 禁止改 05 查询口径
- 禁止改写 `baselines/3.30.2/`
- README 用例数该行全部 1011→1028
- 低版本技能不得改高版本工作区

## 工作区存量（强制）

本版把已拆标准文件的串联算进完成条件。

- **谁执行**：会话钩子，或 `python ChronoPM-Project/scripts/enforce_workspace_upgrade.py --root <项目根>`。联邦根不在集根本身编页，对每个带 `ai/.skill-version.json` 的成员根各跑一次。
- **做什么**：有拆解条目的源，能确定的写入来源指针、文档链接和主题页已绑。还没拆且登记里没有编号的，已绑写 `无登记边`。
- **对不上**：写入 `ai/logs/migration-log.md` 和 `pm-decisions.md`。退出码非 0。不改 skillVersion。
- **失败**：exit ≠ 0 → 不得更新该工作区 `.skill-version.json` 的 skillVersion，不得写「可以投入使用」。
- **钩子**：项目内 `.grok/hooks/chronopm-upgrade.json`。用户级路径：Windows 为 `%USERPROFILE%\.grok\hooks\chronopm-upgrade.json`，其他系统为 `~/.grok/hooks/chronopm-upgrade.json`。超时 120 秒，与 `20-workspace-version-rules.md` 同一数字。
- **限度**：钩子超时、崩溃、项目未受信任时会话仍会开始，版本号保持原样。工具钩子是尽力而为。
- **版本链**：3.30.2→3.30.3 直接执行本文件。

## 宿主

宿主要能在会话开始时运行命令钩子。做不到时按 20 号的限度处理，不另写未经核实的宿主版本号。

## C9 顺序

1. 改 `scripts/_version.py` `SKILL_VERSION = "3.30.3"`（schema 行不动）
2. `python ChronoPM-Project/scripts/sync_version.py`
3. README.md 与 README.en.md **该行全部** 1011→1028
4. `ChronoPM-Project/governance/migrations/README.md` 当前文件改为本文件
5. Portfolio 版本锁步 + CHANGELOG
6. `python governance-shared/scripts/audit_release.py` 全绿

施工只认 **1028**。禁止沿用 1011。

## 验证

阻断：UE-002、UE-003、UE-004、UE-007、UE-010、UE-014、UE-015、UE-016、UE-017，以及 UG-S02。`python ChronoPM-Project/tests/test_enforce_workspace_upgrade.py` 与 `python ChronoPM-Project/tests/test_compile_source_digests.py` 打印 ok。

## 回滚

还原基线 3.30.2。已写上的来源指针可留。无 schema 回退。
