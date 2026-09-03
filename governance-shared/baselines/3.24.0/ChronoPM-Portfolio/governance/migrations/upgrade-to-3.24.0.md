# 升级到 3.24.0（Portfolio 锁步）

> 与 ChronoPM-Project 3.24.0 共用版本线。施工主清单见开发仓 `ChronoPM-Project/governance/migrations/upgrade-to-3.24.0.md`。  
> 本包行为：材料投喂统一入口（01 §2.1）：识别 → 无条件落 `reports/ingest/{batch}/` 原件+抽出行 → 写集层日志 → 分类；仅成员实体走 V-9。禁止问要不要落库。禁止写 `projects/*/ai`。禁止 `portfolio/cache/`。schema **0.16.0**。
