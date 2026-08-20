# 升级到 3.4.0

> 从 3.3.0 升级到 3.4.0
> 发布日期：2026-08-20
> Schema 变更：无（timeline/ 懒建不预建）
> CR 编号：CR-20260820-005
> 施工依据：方案 §5n CR-D（含启动前三项检查、R9、判重四案）

## 变更摘要

报告存根范式：项目日报/周报/时间线报从 todos 实时汇聚，生成即存根。废止 R-3 缓存、§3.1 每日草稿、§4.1/§4.2 索引（含 config `reports/daily/index.md` / Task Sync = R9）。月报=时间线报自然月特例，不复活 monthly/。非精确重合一律整段重汇聚。

## 新增目录

- 无（`reports/timeline/` 首次生成时懒建）

## 规则变更

- 01：§2 存根语义；§3.1 五步区间汇聚；§4 判重四案；§4a 时间线报
- 05：历史日报先查存根；时间线/月报路由
- 06：todos 历史不可变；timeline 不进标准结构；§7.1 同步索引废弃
- 14：停维 YYYYMM/index.md；新增 D23
- 11/19/20：月报→时间线报；缺 timeline/ 非 P0
- 伴生包 04：临时摘改指向 todos §3

## 脚本变更

- config.py：删除 `reports/daily/index.md` 预建模板（R9）
- init **不**预建 timeline/

## 模板变更

- index-formats.md：存根 YAML 头；原日报索引标废弃

## 存量

已生成日报/周报 = 天然存根，原地不动。旧 index.md 停维不删。

### 旧缓存术语自检清单

缓存 / 落盘缓存 / 每日累积周报草稿 / Todo Sync / Task Sync 作为现行机制 → 改为存根 / 区间汇聚。CQ-5「实读禁缓存」指禁止凭记忆作答，保留。

### 多存根并存

文件名扫描无精确重合 → 整段从 todos 重汇聚，禁止拼接。

## 明确不做

- CR-E/F；不升 schema；不预建 timeline/；不复活 reports/monthly/
