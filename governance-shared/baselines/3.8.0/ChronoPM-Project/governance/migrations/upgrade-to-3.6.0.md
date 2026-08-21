# 升级到 3.6.0

> 从 3.5.1 升级到 3.6.0
> 发布日期：2026-08-20
> Schema 变更：workspace schema 0.10.0 → 0.11.0（新增 `requirements/sources/`）
> CR 编号：CR-20260820-007
> 施工依据：方案 §5k CR-F（需求十）；Q9/Q10/Q11 按方案默认

## 变更摘要

RI 演进为文档级拆解：`requirements/sources/{编号}/`（meta/_digest/atoms/facts/ledger）。ATOM kind 4→10 类。source-type 全生命周期基线包按需启用。台账索引加速器。D22 需求蔓延巡检（限局部）。共享文档互认键仍是簇固定号+指纹。

## 新增目录 / 文件

| 路径 | 说明 | 验证 |
|---|---|---|
| `requirements/sources/` | 源文档级拆解目录 | 存在；schema=0.11.0 |
| `requirements/sources/_index.md` | 7 列台账 | 含表头 |
| Skill `source-doc-meta-template.md` | 五件套骨架 | 含 meta/_digest/atoms/facts/ledger |
| Skill `source-index-template.md` | 台账模板 | 7 列 |

## 规则 / 脚本 / 模板

- 07：§8.4 kind 扩展；§8.6 落点改 sources/ + 术语入流；§8.9 拆解发生地改 sources/{编号}/；新增 §8.11
- 14：D22（限局部；与 WF-8 溯源不重复登记）
- 18：Step1 文档类型多选（只启用已选类型，不预建空拆解目录）
- 20：schema 0.11.0；缺 sources/ 提示抽取；首次新拆解/RI 判定前必须完成 `{type}-source/` 迁移
- 06：标准结构补 sources/
- init 预建 `requirements/sources/` + `_index.md`
- migrate 升 0.11.0；打印一次性迁移入口（脚本不自动删旧 `{type}-source/`）
- source-type-registry 基线包扩行；contract-register 拆解指针改 sources/{编号}/
- 伴生包 01/02：V-8 兼容期双形态（旧 `{type}-source/` 与 sources/ 都能读）

## 存量

1. `{type}-source/` **一次性迁移**：扫描→清单（原文档→新目录，簇 ID 冻结不重编）→PM 确认→搬移+补 meta/_digest→先迁后验→才删旧目录。
2. 未完成 fallback：查询仍读旧 `{type}-source/`。
3. **截止条件**：首次新拆解或首次 RI 范围判定前必须完成。
4. 旧 4 类 ATOM kind 全部兼容，不强制重标。
5. 基线包新类型**按需启用不预灌**。

## 明确不做

- 业务工作区代迁
- SRC-NNN 作跨项目互认键
- 二次拆解共享文档
- 向计划简表加列
- 全库扫 D22
