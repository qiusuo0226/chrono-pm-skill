# 升级到 4.1.1

> 从 4.1.0 升级到 4.1.1  
> 发布日期：2026-09-29  
> Schema：**0.17.0（不变）**  
> CR：CR-20260929-002  
> IA：IA-20260929-002  
> 施工依据：本文件。  
> Patch。回归合计 **1099**（1094+5）。  
> 用户拍板：可以升级了。

## 变更摘要

1. 已拆源对不上恰好一条已有需求时，已绑写「独立」，不写需求边，不新建需求，不问挂哪一条。材料头写成 `requirement` 时同样处理。
2. 能对上的已有编号写入参见，多条需求编号也写入。切片正文点到另一份已拆源时，对方参见写回这一份，只做这一跳。
3. 恰好一条已有需求仍补来源指针和文档链接。没有在用工作包时仍建待确认包。没有需求编号不建包。
4. 4.1.0「已有摘要页不重写」在本版放松为：不重写原子、事实、图，不调用整页重写；允许更新已绑和参见。`upgrade-to-4.1.0.md` 不回改。

## 施工禁区

- 禁止升 schema；禁止新建目录；禁止新建 `ai/wiki/`；禁止 `[[链接]]`
- 禁止批量重拆旧源；禁止按用词相近自动建参见；禁止把参见收成传递闭包
- 禁止按文件名猜测材料是不是需求
- 禁止没有需求编号就建包或建需求
- 禁止改 `baselines/4.1.0/` 及更早基线
- 不代更 Grok 安装区，不写市监业务仓

## 工作区存量（强制）

- **谁执行**：盖戳前仍走现有的一次 `ensure_stock_compiled`。`needs_v411` 只打印一行，不第二次调用编译，不重拆。从低于 4.1.0 升上来时，`needs_v410` 的补包保持原样，先于这次编译。
- **怎么变**：已经有摘要页、且没有 `split_profile: 4.1.0` 的已拆源，不调用整页重写，不改原子、事实、图。页上已经有「已绑」节、且这份源仍然是唯一绑定时，该节保持。独立的源，或页上还没有「已绑」节时，写入已绑。不是硬缺口的页都写参见。参见在写盘前算完正向和反向，一次编译后直接引用的两端都在。
- **不做**：不整库重拆，不改旧切片，不新建需求，不新建目录，不建 `ai/wiki/`，不改市监业务仓。`new_dirs` 与 `new_files` 仍为空。
- **失败**：切片没有章节或页码、`doc_kind` 无法识别、恰好一条需求但补完仍没有在用包，仍然使退出码非 0，不改 `skillVersion`。对不上恰好一条需求不再记缺口。盖戳不读 `pm-decisions.md`。本次编译返回 0 就放行。历史行里的「没有可确定的需求」不参与退出码，本版也不清除那些行。独立源不追加新的待裁定行。
- **版本链**：`VERSION_CAPABILITIES` 增加 4.1.1 行，schema 仍 0.17.0，`new_dirs` 与 `new_files` 为空。

## 版本链

4.1.0→4.1.1 直接执行本文件。更早版本先走到 4.1.0，再执行本文件。

## 验证

`python ChronoPM-Project/tests/test_doc_kind_v401.py`、`python ChronoPM-Project/tests/test_split_bind_v410.py`、`python ChronoPM-Project/tests/test_wiki_link_v411.py` 打印 ok。`python ChronoPM-Project/tests/test_compile_source_digests.py`、`python ChronoPM-Project/tests/test_enforce_workspace_upgrade.py`、`python ChronoPM-Project/tests/test_output_path.py` 仍通过。`python governance-shared/scripts/audit_release.py` 全绿。

## 回滚

还原标签 v4.1.0。schema 无回退。已经写出的「独立」和参见可以留下。旧编译器不认识「独立」这节规则，但没有把它写进旧包要读取的新字段。已经建出的待确认包可以留下。
