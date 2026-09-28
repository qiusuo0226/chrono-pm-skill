---
doc_type: wp-chart
derived: true
source: wps/_index.md 进行中段 + wps/WP-*.md
generated_at: YYYY-MM-DD HH:mm
---

# 工作包总览图（派生视图）

> 非事实源、非生成物。真相 = 各 `wps/WP-*.md` 与 `wps/_index.md`。禁止把手改当真相；数据变则覆盖重写。
> 按正常计划分章节，每章一个 mermaid。废弃与已完成归档不入默认图。连线只认前置/后置且两端同章。
> 排列：有关联横向（超 3 换行用子图级边+标签）；无关联装入「独立（无关联绑定）」竖排。细则 11 §17.2 / §17.2.1。

### PLAN-YYYYMMDD-NNN：{计划名称}

有关联、≤3，单行链：

```mermaid
graph TD
  subgraph chain1 ["链1"]
    direction LR
    WP_A["WP-YYYYMMDD-001<br/>名称A<br/>2026-03-01 ~ 2026-08-31<br/>💻 开发"] --> WP_B["WP-YYYYMMDD-002<br/>名称B<br/>2026-03-01 ~ 2026-09-15<br/>🧪 测试"] --> WP_C["WP-YYYYMMDD-003<br/>名称C<br/>2026-03-01 ~ 2026-10-07<br/>📋 需求规划"]
  end
  style chain1 fill:none,stroke:none,stroke-width:0px
```

有关联、>3 换行（行间子图级边；禁止 `WP_C --> WP_D`）：

```mermaid
graph TD
  subgraph chain1r1 ["链1·第1行"]
    direction LR
    WP_A["WP-YYYYMMDD-001<br/>名称A<br/>2026-03-01 ~ 2026-08-31<br/>💻 开发"] --> WP_B["WP-YYYYMMDD-002<br/>名称B<br/>2026-03-01 ~ 2026-09-15<br/>🧪 测试"] --> WP_C["WP-YYYYMMDD-003<br/>名称C<br/>2026-03-01 ~ 2026-10-07<br/>📋 需求规划"]
  end
  style chain1r1 fill:none,stroke:none,stroke-width:0px
  subgraph chain1r2 ["链1·第2行"]
    direction LR
    WP_D["WP-YYYYMMDD-004<br/>名称D<br/>2026-03-01 ~ 2026-10-31<br/>🔄 需求登记"]
  end
  style chain1r2 fill:none,stroke:none,stroke-width:0px
  chain1r1 -->|"WP-YYYYMMDD-003→WP-YYYYMMDD-004"| chain1r2
```

> 图注：`完整链序：WP-YYYYMMDD-001→WP-YYYYMMDD-002→WP-YYYYMMDD-003→WP-YYYYMMDD-004（超 3 换行，跨行依赖已标注在行间连线上）`

分支（边全在子图内）：

```mermaid
graph TD
  subgraph chain2 ["链2"]
    direction LR
    WP_E["WP-E<br/>名称E<br/>— ~ —<br/>💻 开发"] --> WP_F["WP-F<br/>名称F<br/>— ~ —<br/>🧪 测试"]
    WP_E --> WP_G["WP-G<br/>名称G<br/>— ~ —<br/>🧪 测试"]
  end
  style chain2 fill:none,stroke:none,stroke-width:0px
```

无关联竖排 + 同章混合时链与独立并列、组间无边：

```mermaid
graph TD
  subgraph chain1 ["链1"]
    direction LR
    WP_006["WP-006<br/>名称<br/>2026-09-15 ~ 2026-10-31<br/>🔄 需求登记"] --> WP_x["WP-YYYYMMDD-002<br/>名称<br/>— ~ —<br/>🔄 需求登记"]
  end
  style chain1 fill:none,stroke:none,stroke-width:0px
  subgraph rInd ["独立（无关联绑定）"]
    direction LR
    WP_002["WP-002<br/>名称<br/>— ~ —<br/>🔄 需求登记"]
    WP_005["WP-005<br/>名称<br/>2026-09-15 ~ 2026-10-31<br/>🔄 需求登记"]
  end
  style rInd fill:none,stroke:none,stroke-width:0px
```

### 未绑定计划

```mermaid
graph TD
  subgraph rInd ["独立（无关联绑定）"]
    direction LR
    WPyyy["WP-YYYYMMDD-NNN<br/>包名<br/>— ~ —<br/>🔄 需求登记"]
  end
  style rInd fill:none,stroke:none,stroke-width:0px
```
