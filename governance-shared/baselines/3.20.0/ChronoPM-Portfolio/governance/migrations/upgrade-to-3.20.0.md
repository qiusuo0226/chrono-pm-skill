# 升级到 3.20.0（ChronoPM-Portfolio）

> 主包：`ChronoPM-Project/governance/migrations/upgrade-to-3.20.0.md`
>
> 本包：版本锁步 3.20.0 / workspace schema 0.16.0。施工含 **V-14 混报拆分** 与 **弱结构投喂（乙案落盘）**，不只指针。
>
> CR：CR-20260829-002。禁止写入成员项目 `projects/*/ai`。

## 本包必改

| 文件 | 动作 |
|---|---|
| `references/01-readonly-boundary-rules.md` | L11 限定语加例外；§2 增 `reports/ingest/**` 与 `context/ingest-maps.md` |
| `references/02-aggregation-query-rules.md` | 标题含 V-13/V-14；V-14 打分；弱结构投喂槽位+映射（不写死列号） |
| `SKILL.md` | V-1～V-14；路由加混报/弱结构投喂 |
| `assets/templates/daily-dispatch-template.md` | 新建分发稿 |
| `assets/templates/ingest-map-template.md` | 新建列映射档 |

## 乙案路径（写死）

- 集层原件+抽出行：`ai/portfolio/reports/ingest/{batch}/`
- 映射档：`ai/portfolio/context/ingest-maps.md`
- 成员 `sources/{编号}/original.*`+`rows.md`：**仅 Project 收下后写**
- 禁止 `portfolio/batches/` 与直写 `projects/*/ai`

## 高置信（文本混报）

最高分 ≥5，比第二名 ≥2，且 C(P) 非空；或正文项目名精确命中。表内已绑 `project` 槽走弱结构投喂，不走本打分。

## 收尾

用户 2026-08-29 核验通过。Grok 安装区不代更。主包见 `ChronoPM-Project/governance/migrations/upgrade-to-3.20.0.md`。
