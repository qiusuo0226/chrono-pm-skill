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
  PF[集层投喂] -->|实线| HO[P-HANDOFF-ACCEPT / P-SPLIT]
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
  NEW[新建WP 必有需求] -->|实线| H7[§7状态链 只追加]
  NEW -->|实线| H8[§8阶段+执行人]
  NEW --> PEND[待确认]
  PEND -->|粗线| B3[决策文件块3]
  B3 --> PM[项目经理确认]
  PM --> PLANED[已规划]
  PLANED -->|实线| TD[拆待办 恰好绑一个WP]
  TD --> OWNER[执行人当日文件]
  PLANED -.-> Z[WP可暂时0条待办]
  H7 -.-> CUR[当前=链尾]
  H8 -.-> MAP[阶段映射主状态]
```

## G5 计划

```mermaid
flowchart LR
  PM[项目经理定计划] -->|实线| PLAN[5节只引用WP]
  WP[链尾/阶段执行人排期/时间盒] -.-> S3[§3六列无子行加§4阶段列表]
  PLAN --> S3
  PLAN -.-> PROG[进度按WP聚合]
  PLAN -.-> X[不灌待办]
  Q[读或改] --> GATE[闸1定位 闸2对账§3§4 闸3写后]
  PLAN -->|废弃| FZ[冻结§3 去掉plan_ref]
  WP -->|effect废弃| RM[正常计划移出]
```

## G6 日报

```mermaid
flowchart LR
  P[执行人汇报] -->|实线| IN[inbox]
  IN -->|实线| MD[当日一人一份md]
  MD --> MAP[映射已有待办]
  MAP -->|够正式未匹配| NEW[自动建待办]
  P --> TMR[明日计划留当天原文]
  HO[集层手递] -->|实线| IN
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
  HO[集层风险清单] -->|实线| CARD[04判定卡]
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
  HO[集层排期] -->|粗线| V9[确认后手递 01口径]
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
  Q --> G2[闸2先对账]
  Q -.-> R[谁没做完/还差谁/在哪些计划/没进计划]
  Q -.-> AB[忽略废弃]
```

## G14 项目集

```mermaid
flowchart LR
  PF[Portfolio] -.-> FS[各项目事实源]
  PF -.-> DEC[决策文件开放计数]
  PF -.-> OPS[过程日志index]
  PF -->|实线| HO[§2.2 调用 Project 写过程]
  PF --> X[禁止工人手搓成员正文]
```

## G15 巡检

```mermaid
flowchart LR
  INSP[19/14发现缺口] -->|实线| DEC[决策文件对应块]
  INSP --> T[仅本轮触碰才写]
  INSP --> X[不在对话里说完就算]
```

## G16 生成物落盘

```mermaid
flowchart LR
  W[拟写路径] --> C{三路分类}
  C -->|A事实源| AI[ai/入库]
  C -->|B生成物| OUT[ai/outputs/批次]
  C -->|C禁止| STOP[硬中止]
  ROOT[项目根或与ai平级] --> STOP
  W -->|写后| SCAN[扫根散落须迁走]
```

## G17 词库感应

```mermaid
flowchart LR
  TALK[本轮用语] --> T{T1到T4}
  T -->|声明或确认| CF[同轮confirmed]
  T -->|重复未登记| PD[pending]
  T -->|不是术语| X[不写]
  NOF[无词库文件] -->|实线| CREATE[先按模板建]
```

## G18 派活

```mermaid
flowchart LR
  P[点名执行人做动作] --> D[查重]
  D -->|有| U[校正时间 不新建]
  D -->|无| S{多WP主题可分?}
  S -->|是| M[拆成多条 各绑一个WP]
  S -->|不清| ASK[问一次]
  M --> W[先写后告知]
  U --> BOX{结束超WP?}
  W --> BOX
  BOX -->|否| OK[不改期]
  BOX -->|是| PM[问A拉长包/B压缩待办/C挂起]
```

## G21 扫描推进

```mermaid
flowchart LR
  TD[写执行待办] -->|实线| SCAN[P-WP-SCAN 聚人期]
  SCAN -->|虚线| S8[WP §8 AI聚合]
  S8 -->|虚线| S3[正常计划§3行与§4列表]
  PEND[待确认已入计划或已有执行待办] -->|粗线| ADV[P-WP-ADVANCE]
  ADV -->|确认后只追加| H7[§7]
```

## G21 对外问答（能力目录，不是独立 Skill）

```mermaid
flowchart LR
  U[用户提问] --> R{简单查询?}
  R -->|是| S[SKILL底线14-16 + 05短条]
  R -->|写入/确认/方案/复杂| RN[reply-norm-skill reply-rules]
  RN --> C{真确认?}
  C -->|是| S50[00 5.0]
  C -->|纯查询| BAN[禁止问是否执行方案]
  X[reply-norm SKILL.md] --> BAN2[禁止误注册]
```

## G20 技能缺口

```mermaid
flowchart LR
  U[技能做不到/记升级需求] --> DET[P-ALWAYS第4步只检测]
  DET --> GAP[P-SKILL-GAP]
  GAP -->|实线| OUT[outputs 需求-md]
  X[requirements/wps/plans] --> BAN[禁止]
```

## G19 拆文件入库

```mermaid
flowchart LR
  F[拆文件/拆文档] --> SPLIT[source-split]
  SPLIT --> SRC[sources/编号/六件套]
  SRC --> REQ[需求清单 未确认]
  F -->|还要对外文件| OUT[再走 outputs]
  X[只出HTML不入库] --> BAN[禁止替代]
  PF[集层分法已定] -->|实线| SPLIT
```
