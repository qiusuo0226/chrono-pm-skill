# ChronoPM 模块链路图

图例：实线=写事实源；虚线=只读/聚合；粗线=等项目经理裁定。

## G0 总览

```mermaid
flowchart LR
  PM[项目经理说话] --> AI[AI]
  AI -->|实线| REQ[需求清单]
  AI -->|实线| WP[工作包]
  AI -->|实线| TD[待办]
  AI -->|实线| PLAN[计划]
  AI -->|实线| RI[风险问题]
  AI -->|粗线| DEC[决策文件]
```

## G1 投喂源文件

```mermaid
flowchart LR
  DOC[合同/招标/投标/立项] --> AI[AI拆解]
  AI -->|实线| ATOM[ATOM/Canonical]
  AI -->|实线| REQ[需求清单 未确认]
  REQ -->|粗线| B1[决策文件 需求未确认]
```

## G2 确认需求

```mermaid
flowchart LR
  B1[决策文件块1] -->|粗线| PM[项目经理裁定]
  PM -->|做不做/效果/方案齐| OK[已确认]
  PM -->|否| NO[已否决]
  OK -->|实线| LOG[决策记录]
  NO -->|实线| LOG
```

## G3 需求绑工作包

```mermaid
flowchart LR
  OK[已确认需求] -->|粗线| B2[决策文件块2]
  B2 --> PM[项目经理指定WP]
  PM -->|可多个编号| WP[工作包只存编号]
  PM -->|小需求合成/大需求拆开| WP
```

## G4 确认工作包再拆待办

```mermaid
flowchart LR
  NEW[新建WP 必有需求] --> PEND[待确认]
  PEND -->|粗线| B3[决策文件块3]
  B3 --> PM[项目经理确认]
  PM --> PLANED[已规划]
  PLANED -->|实线| TD[拆待办 多对一]
  TD --> OWNER[执行人当日文件]
```

## G5 计划

```mermaid
flowchart LR
  PM[项目经理定时间盒] -->|实线| PLAN[计划文件只引用WP]
  PLAN -.-> PROG[进度从待办按WP聚合]
  PLAN -.-> X[不灌待办行]
```

## G6 日报

```mermaid
flowchart LR
  P[执行人汇报] -->|实线| IN[inbox]
  IN -->|实线| MD[当日一人一份md]
  MD --> MAP[映射已有待办]
  MAP -->|够正式未匹配| NEW[自动建待办]
  P --> TMR[明日计划留当天原文]
```

## G7 会议

```mermaid
flowchart LR
  M[纪要] -->|有负责人| TD[正式行动项落待办]
  M -->|缺负责人| B6[决策文件块6]
  M -->|会上拍板| DL[会议决策日志 另一文件]
```

## G8 风险问题

```mermaid
flowchart LR
  PM[指定责任人] --> CHK{在册?}
  CHK -->|否| ROSTER[自动入册]
  CHK -->|是| TODO{有跟踪待办?}
  ROSTER --> TODO
  TODO -->|无| ADD[建跟踪待办挂责任人]
  PM -->|甲方厂商客户| X[禁止入执行花名册]
```

## G9 关联待办

```mermaid
flowchart LR
  PM[说明处理方式] -->|实线| REC[关联处理记录]
  REC -->|办结| AUTO[按记录AUTO]
  PM2[只建关联没说怎么办结] -->|粗线| B7[决策文件块7]
  B7 --> ASK[问一次再记下]
```

## G10 决策文件本身

```mermaid
flowchart LR
  MOD[各模块缺口] --> BLK[八块开放项]
  BLK --> BAN[横幅 有N件]
  BAN -->|粗线| PM[项目经理裁定]
  PM -->|实线| LOG[决策记录可归档]
  B8[块8已写等点头] -.-> CL[Change Log待确认]
```

## G11 人员

```mermaid
flowchart LR
  A[喂日报/点名加待办/进组/责任人] -->|实线| R[入册]
  B[旁人提及/参会名单/甲方客户] --> X[不入册]
  C[次日无待办无日报] -->|粗线| B8[块8空闲提醒]
```

## G12 变更

```mermaid
flowchart LR
  CHG[改需求] -->|实线| CR[变更单]
  CR --> PM[批准]
  PM -->|实线| REQ[需求清单]
  REQ --> WP[绑/改工作包]
  WP -->|已规划| TD[拆待办增量]
```

## G13 查询

```mermaid
flowchart LR
  Q[提问] -.-> IDX[先索引后分片]
  IDX -.-> FS[只读事实源]
  Q -.-> NX[不读inbox]
  Q -.-> ND[不把决策文件当进度]
```

## G14 项目集

```mermaid
flowchart LR
  PF[Portfolio] -.-> FS[各项目事实源]
  PF -.-> DEC[决策文件开放计数]
  PF -.-> OPS[过程日志index]
  PF --> X[禁止写成员项目]
```

## G15 巡检

```mermaid
flowchart LR
  INSP[19/14发现缺口] -->|实线| DEC[决策文件对应块]
  INSP --> T[仅本轮触碰才写]
  INSP --> X[不在对话里说完就算]
```
