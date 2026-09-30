# 升级到 3.30.2

> 从 3.30.1 升级到 3.30.2  
> 发布日期：2026-09-21  
> Schema：**0.17.0（不变）**  
> CR：CR-20260920-003 / CR-20260920-004  
> IA：IA-20260920-003 / IA-20260920-004  
> 施工依据：本文件。禁止再引用 upgrade-plan 路径。  
> Patch。回归合计 **1011**（997+14）。  
> 用户拍板：可以了执行升级吧。

## 变更摘要

1. 结转先快扫三问，已过只改点名人；禁止用跑脚本或完整写代理当「查」。
2. 补完 3.30 主题页存量回填。升级执行写出 `source-digest` 页；做不完不得盖工作区戳。

## 施工禁区

- 禁止升 schema；禁止新目录/新 ProcID
- 禁止 `ai/wiki/`、Obsidian wikilink、跨源主题页
- 禁止日常 `refresh_views.py --all` 重编 `_digest.md`
- 禁止改 05 查询读 atoms 口径
- 禁止改写 `baselines/3.30.1/`
- README 用例数该行全部 997→1011
- 禁止因 `governance/migrations/README.md` 仍写 3.27.0 而重跑 3.27 或判缺链

## 工作区存量（强制）

本版改了页规格的完成判据，必须处理存量。

- **谁执行**：成员项目根跑 `python ChronoPM-Project/scripts/compile_source_digests.py --root <成员根>`。`migrate_workspace.py` 所有非拒绝路径先调用再写戳。
- **做什么**：`requirements/sources/*/` 中 `missing_page` / `old_digest` / `stale` 写出 `doc_type: source-digest` 页（栏目骨架 + 切片索引 + ATOM 链 + 已绑编号）。ok 页不重写。无 atoms 不空编。指纹函数 `import refresh_views`，禁止双实现。
- **集根**：不编成员页；各成员根各跑一次。
- **失败**：exit ≠ 0 → 不得更新该工作区 `.skill-version.json` 的 skillVersion，不得写「可以投入使用」。
- **日常**：`refresh_views.py` 仍只检测。
- **解除**：3.30.0 L23 / 3.30.1 L19「禁止脚本重编 `_digest.md`」**仅在升级执行时机解除**。日常检测禁写仍有效。
- **版本链**：3.30.1→3.30.2 直接执行本文件。`migrations/README.md` 仅为当前指针；漏登的 3.28.0～3.30.1 以同目录已有 `upgrade-to-*.md` 文件名为准，不因 README 仍写 3.27.0 而误判。

## A. 施工

| # | 文件 | 动作 |
|---|---|---|
| A1 | CR-003/004、IA-003/004、本文件 | 治理 |
| A2 | 22 / 00 / 23 / SKILL §5.0 / 01 L42 | 快扫三问 |
| A3 | Portfolio 01 §2.2 步骤 4/8；Portfolio SKILL 指针 | 手递快扫 |
| A4 | 16 / 20 / 19 / digest-schemas | 存量闸；升级可写页；P0 限戳 |
| A5 | `compile_source_digests.py` + migrate 两分支 | 执行器 |
| A6 | tests Module 93/94 + test_compile | 1011 |
| A7 | C9 | 见下 |

## C9 顺序

1. 改 `scripts/_version.py` `SKILL_VERSION = "3.30.2"`（schema 行不动）
2. `python ChronoPM-Project/scripts/sync_version.py`
3. README.md 与 README.en.md **该行全部** 997→1011
4. `ChronoPM-Project/governance/migrations/README.md` 当前文件改为本文件
5. Portfolio 版本锁步 + CHANGELOG
6. `python governance-shared/scripts/audit_release.py` 全绿

施工只认 **1011**。禁止沿用 997。

## 验证

阻断：NP-001、NP-002、NP-004、NP-005、UG-S01、UG-S02、UG-S03、UG-S06。旧阻断 ING-108/111、FE-018、PC-004、HO-004/005、ING-109、SW-001/010/012/015/017 不回退。`python ChronoPM-Project/tests/test_compile_source_digests.py` 打印 ok。

## 回滚

还原基线 3.30.1。已编译页可留。无 schema 回退。

## 收尾（2026-09-21）

audit 17/17 通过。脚本用例 ok。Grok 不代更。schema 仍 0.17.0。AP 无残留。tag `v3.30.2`。

## 收尾补记（2026-09-21）

用户指示收尾。升级可以投入使用。Grok 安装区不代更。业务仓未代迁。基线已同步本补记，无功能补丁。成员根存量回填需装包后自行 `compile_source_digests.py --root <成员根>`。分发包在 Downloads：`ChronoPM-Project-Skill-v3.30.2.zip`（134）+ `ChronoPM-Portfolio-Skill-v3.30.2.zip`（46）。README 发布产物已改为 v3.30.2。
