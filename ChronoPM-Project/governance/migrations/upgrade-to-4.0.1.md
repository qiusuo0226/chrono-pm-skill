# 升级到 4.0.1

> 从 4.0.0 升级到 4.0.1  
> 发布日期：2026-09-28  
> Schema：**0.17.0（不变）**  
> CR：CR-20260928-001  
> IA：IA-20260928-001  
> 施工依据：本文件。  
> Patch。回归合计 **1072**（1041+31）。  
> 用户拍板：执行升级吧。

## 变更摘要

1. 切片 meta 头可选 `doc_kind`。`reference` 不查需求、不查工包、不计缺口，摘要页标明非需求类。
2. 成功写出的摘要页增加「参见」。只收已存在的编号，以及标题完全相同的其他源。
3. 口述日报进每人当天待办。甩来的日报文件、开会文件拆进 `sources/`，并仍提取进展或行动项。
4. 出文件前运行 `scripts/check_output_path.py`。名单在 11 号标记块。
5. 技能缺口与「生成报告/导出」同现时走技能缺口行。

## 施工禁区

- 禁止升 schema；禁止新建 `ai/wiki/`；禁止 `[[链接]]`
- 禁止按文件名或生命周期阶段猜测 `doc_kind`
- 禁止按用词相近自动建参见
- 禁止删除「除非用户明示拆进 sources/」
- 禁止改 `baselines/4.0.0/`
- 禁止查询热路径调用 `refresh_views.py --all`
- 不代更 Grok 安装区，不写业务仓

## 工作区存量（强制）

- **谁执行**：既有 `compile_source_digests.py`，由 `migrate_workspace.py` / `enforce_workspace_upgrade.py` 在盖戳前调用。不另写一套编译。
- **怎么变**：meta 头已是 `doc_kind: reference` 的已拆源，摘要页已绑写「非需求类」，并写参见，不计缺口。没有该字段的，与 4.0.0 相同。
- **不做**：不扫文件名，不看生命周期阶段，不改市监业务仓，不新建需求或工作包。
- **失败**：需求类缺口或无法识别的 `doc_kind` 仍在，则退出码非 0，不改 `skillVersion`，不得写「可以投入使用」。
- **版本链**：4.0.0 的说法表合并仍由 `needs_v400` 负责。本版不新增数据变换分支。`VERSION_CAPABILITIES` 增加 4.0.1 行，`new_dirs` 与 `new_files` 为空。

## 版本链

4.0.0→4.0.1 直接执行本文件。更早版本先走到 4.0.0，再执行本文件。

## 验证

`python ChronoPM-Project/tests/test_doc_kind_v401.py` 与 `python ChronoPM-Project/tests/test_output_path.py` 打印 ok。既有 `test_enforce_workspace_upgrade.py` 仍通过。`python governance-shared/scripts/audit_release.py` 全绿。

## 回滚

还原标签 v4.0.0。schema 无回退。reference 声明留在 meta 里无害，旧编译器会重新记需求缺口。
