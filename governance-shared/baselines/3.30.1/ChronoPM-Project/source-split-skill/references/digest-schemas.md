# 单源主题页规格（digest-schemas）

由 P-SPLIT 收尾编译 `_digest.md` 时**同轮加载**。查询不加载本文件（05 只读页 / `source_digest_status`）。

主题页 = `requirements/sources/{编号}/_digest.md`。派生，不是价款/工期/范围唯一证据。取证回 ATOM 或原文指针。禁止进 `outputs/`。禁止 `[[wikilink]]`。相对 Markdown 链接。

## 谁写

工人只写 atoms/facts 分片与抽出图。**协调者收尾编译** `_digest.md`。

## frontmatter

```yaml
doc_type: source-digest
source_id: CON-…
source_type: contract
source_category: contractual
authority: L1
source_fingerprint: <与 ledger 原件指纹同>
slice_fingerprint: <见下>
compiled_at: YYYY-MM-DD
digest_schema: contractual
```

`authority` 抄本项目 `source-type-registry.md`，禁止与 registry 不一致。

无 `doc_type: source-digest` = 旧摘要：查询可读，不得当已编主题页。

## slice_fingerprint

纳入：`atoms.md`、`atoms/part-*.md`、`facts.md`、`facts/part-*.md`。  
排除：`facts/local_only.md`、`facts/local_only/**`。混合 part 内行级 `local_only=true` **整文件仍入哈希**。

算法与 `refresh_views.py` `_file_sha` 相同：SHA256 文件字节；路径排序后按 `aggregate_fp` 拼接。

有 Python：`python scripts/refresh_views.py --print-slice-fp --source-dir <sources/编号>` **只打印一行 hex，零写盘**，写入页头。

无 Python 页头 `slice_fingerprint` **必须**用同一格式（与 `compute_slice_fp_fallback` 逐字节一致）：

- 文件集合与纳入/排除规则同上，遍历顺序 = `iter_slice_files`（先 `atoms.md`、`facts.md`，再 `atoms/`、`facts/` 下 `sorted(glob **/*)` 的 `.md`）。
- 每条：`{POSIX相对路径}:{size字节}:{mtime秒}`（`mtime` = `int(st_mtime)`，路径用 `/`，不用反斜杠）。
- 多条用 `|` 连接，无首尾 `|`，无空格。
- 例：`atoms.md:1200:1726800000|facts.md:80:1726800000`

查询无 Python：按上式重算，与页头整串相等才算切片未过期。

`local_only` facts **不入**主题页正文。共享页只编共享切片。共享副本禁止二编；改页回首拆项目。

## 过期（查询侧）

脚本 `collect_source_digest_status` 写入 `.state.json.source_digest_status`。**禁止**并入 `facts_fingerprint`。脚本只报告、不重编页。

| status | 条件 |
|---|---|
| missing_page | 无 `_digest.md` |
| old_digest | 无 `doc_type: source-digest` |
| stale | 原件指纹或切片哈希与页头不一致 |
| ok | 双指纹一致 |

原件指纹：读该源 `ledger.md` 表列 `source_fingerprint`（首条非空、非 —），与页头 `source_fingerprint` 比对。两边都有值且不等 → `stale` / `reason=source`。ledger 缺失或该列空 → 跳过原件层，只比切片。

切片：页头 `slice_fingerprint` 与磁盘重算值不等 → `stale` / `reason=slice`。先判原件，再判切片。

05：有 Python 读该字段；`stale`/`old_digest` 声明过期后读 atoms。无 Python：切片用上文属性串；原件用页头 vs ledger 表列明文比对。失败则声明过期。

## 栏目骨架（顺序固定；缺栏写「本源未见」，不得删栏）

| source_category | 栏目 |
|---|---|
| contractual | 这是什么 / 当事人 / 标的与价款 / 工期与质保 / 硬约束 / 范围依据 / 切片索引 / 已绑需求与工作包 |
| procurement | 这是什么 / 采购身份 / 门槛与评分 / 承诺与偏离 / 与合同衔接 / 切片索引 / 已绑 |
| approval | 这是什么 / 批复或结论 / 建设内容 / 投资与工期 / 约束 / 切片索引 / 已绑 |
| compliance | 这是什么 / 评测对象 / 必须满足 / 门禁与证据 / 切片索引 / 已绑 |
| technical | 这是什么 / 边界 / 功能与规则 / 接口与数据 / 非功能 / 切片索引 / 已绑（声明不进范围判定） |
| operational | 这是什么 / 约定事项 / 时点 / 责任 / 切片索引 / 已绑 |
| generic | 这是什么 / 要点 / 切片索引 / 已绑 |

未登记 source_type：先提示不静默归类；页用 generic 并标明待登记。

## 特化（在 category 上加栏，不另起文件）

| source_type | 加栏 |
|---|---|
| contract | 付款与验收门 |
| tender_doc | 评分办法 |
| bid_doc | 偏离与承诺清单 |
| design_spec | 实现视图指针（不进范围判定） |
| security_req | 门禁与证据（页头标明 L4 强制门禁） |

## 硬规则

- 条款性句子必须链 ATOM 锚点。禁止无链硬约束。
- 已绑只写编号。节首固定：「绑定状态以登记册 / 工作包第二节为准，本节可能延迟。」
- 软顶 200 行：栏目改要点，**切片索引整表保留**。
- 超 400 行：收口为要点+完整切片索引 = **降级成功、算交付**。
- 仅完全未产出页才失败。失败不回滚已写 atoms/ledger/REQ。回执：「页未编成，查询直走 atoms」。
- `weak_ingest` / 薄源无条款：一页声明无需求条款，禁止编造栏目事实。
- 权威冲突以 `authority` 更高者为提示，仍须回 ATOM。
- 编译不进 `pm-decisions`。Confirmed By 不适用。
