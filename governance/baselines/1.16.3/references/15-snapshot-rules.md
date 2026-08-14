# 璁″垝蹇収涓庡疄闄呮墽琛岃鍒?
鏈鍒欑敤浜庢敮鎸佸巻鍙茶鍒掑洖鏌ャ€佽鍒?vs 瀹為檯鍋忓樊瀵规瘮銆佸巻鍙茶鍒掓壒閲忓鍏ャ€傚綋鍓嶅緟鍔炴煡璇㈢敤绱㈠紩锛屽巻鍙茶鍒掑洖鏌ョ敤蹇収锛屾墽琛岀粨鏋滅敤 actuals銆?
---

## 1. 鏍稿績鍘熷垯

1. **褰撳墠寰呭姙鐢ㄧ储寮曪紝鍘嗗彶璁″垝鐢ㄥ揩鐓э紝鎵ц缁撴灉鐢?actuals銆?*
2. 蹇収鍦ㄦ瘡鏃ョ敓鎴?PM 寰呭姙鏃惰嚜鍔ㄥ垱寤猴紝鍐荤粨涓嶅彲闈欓粯瑕嗙洊锛涘巻鍙茶鍒掓壒閲忓鍏ョ敓鎴愮殑蹇収鍚屾牱鍐荤粨銆佷笌 AI 蹇収涓嶄簰鐩歌鐩栥€?3. 瀹為檯鎵ц鎽樿鍦ㄥ鐞嗙洰鏍囨棩鏈熸棩鎶ュ悗鑷姩鐢熸垚銆?4. 鐑暟鎹紙杩?7 澶?+ 鏈潵 14 澶╋級鍦?`daily-todo-index.md`锛屽喎鏁版嵁鍦?`snapshots/` 鍜?`actuals/`銆?5. 鍘嗗彶璁″垝鏌ヨ涓嶅緱榛樿鍏ㄩ噺鎵弿鏃ユ姤锛屽繀椤讳紭鍏堣鍙栧揩鐓у拰瀹為檯鎽樿銆?
---

## 2. 鐩綍缁撴瀯

```
ai/portfolio/todos/
鈹溾攢鈹€ personal-todo-index.md          # 褰撳墠鎸変汉寰呭姙绱㈠紩锛堢儹鏁版嵁锛屽彲鍙橈級
鈹溾攢鈹€ daily-todo-index.md             # 褰撳墠鎸夋棩鏈熷緟鍔炵储寮曪紙鐑暟鎹紝鍙彉锛?鈹溾攢鈹€ weekly-todo-index.md            # 褰撳墠鎸夊懆寰呭姙绱㈠紩锛堢儹鏁版嵁锛屽彲鍙橈級
鈹溾攢鈹€ history-index.md                # 鍘嗗彶蹇収绱㈠紩锛堝彲鍙橈紝杩藉姞锛?鈹溾攢鈹€ snapshots/                      # 璁″垝蹇収锛氬綋鏃惰鍒掑仛浠€涔堬紙鍐荤粨锛?鈹?  鈹溾攢鈹€ daily/
鈹?  鈹?  鈹溾攢鈹€ {YYYYMMDD}.md           # AI 鍓嶅悜鐢熸垚
鈹?  鈹?  鈹斺攢鈹€ imported-{YYYYMMDD}.md  # 鍘嗗彶璁″垝鎵归噺瀵煎叆锛坰ource_type=external_import锛?鈹?  鈹溾攢鈹€ weekly/
鈹?  鈹?  鈹斺攢鈹€ {YYYY}-W{WW}.md
鈹?  鈹斺攢鈹€ monthly/
鈹?      鈹斺攢鈹€ {YYYYMM}.md
鈹斺攢鈹€ actuals/                        # 瀹為檯鎵ц鎽樿锛氬綋澶?褰撳懆瀹為檯鍋氫簡浠€涔堬紙鍙拷鍔狅級
    鈹溾攢鈹€ daily/
    鈹?  鈹斺攢鈹€ {YYYYMMDD}.md
    鈹斺攢鈹€ weekly/
        鈹斺攢鈹€ {YYYY}-W{WW}.md
```

---

## 3. 鏂囦欢鎬ц川瀵规瘮

| 鏂囦欢 | 鎬ц川 | 鏄惁鍙彉 | 鐢ㄩ€?|
|---|---|---|---|
| `daily-todo-index.md` | 褰撳墠寰呭姙绱㈠紩 | 鍙彉 | 蹇€熸煡璇粖澶?鏄庡ぉ/杩戞湡寰呭姙 |
| `snapshots/daily/{date}.md` | 鍘嗗彶璁″垝蹇収 | 鍘熷垯鍐荤粨 | 鍥炴煡鏌愭棩褰㈡垚鐨勬鏃ヨ鍒?|
| `snapshots/daily/imported-{date}.md` | 瀵煎叆璁″垝蹇収 | 鍘熷垯鍐荤粨 | 鍥炴煡鎵归噺瀵煎叆鐨勫巻鍙茶鍒掞紙external_import锛?|
| `actuals/daily/{date}.md` | 瀹為檯鎵ц鎽樿 | 鍙拷鍔?| 瀵规瘮鏌愭棩瀹為檯瀹屾垚鎯呭喌 |
| `history-index.md` | 鍘嗗彶蹇収鐩綍 | 鍙彉锛堣拷鍔狅級 | 蹇€熷畾浣嶅巻鍙茶鍒?瀹為檯鏂囦欢 |
| `snapshots/weekly/{week}.md` | 鍛ㄨ鍒掑揩鐓?| 鍘熷垯鍐荤粨 | 鍥炴煡鏌愬懆鍘熻鍒?|
| `actuals/weekly/{week}.md` | 鍛ㄥ疄闄呮墽琛?| 鍙拷鍔?| 瀵规瘮鏌愬懆瀹為檯瀹屾垚 |

---

## 4. 鐑暟鎹笌鍐锋暟鎹垎绂?
`daily-todo-index.md` 鍙繚瀛樿繎鏈熺儹鏁版嵁锛?
- 杩囧幓 7 澶?+ 鏈潵 14 澶?
鏇存棭鍘嗗彶鏌ヨ杞悜锛?
```
history-index.md 鈫?snapshots/ + actuals/
```

---

## 5. 蹇収鐢熸垚鏃舵満

| 瑙﹀彂鍔ㄤ綔 | 鐢熸垚鏂囦欢 |
|---|---|
| 鐢熸垚 PM 鏄庢棩寰呭姙 | `snapshots/daily/{today}.md` + 鏇存柊 `history-index.md` |
| 澶勭悊涓汉鏃ユ姤涓殑鏄庢棩璁″垝 | 鏇存柊 `personal-todo-index.md` + `daily-todo-index.md` |
| 鐢熸垚鍛ㄨ鍒?| `snapshots/weekly/{week}.md` + 鏇存柊 `history-index.md` |
| 鍘嗗彶璁″垝鎵归噺瀵煎叆锛圧1锛?| `snapshots/daily/imported-{date}.md` + 鏇存柊 `history-index.md`锛堣 搂8a锛?|

---

## 6. 瀹為檯鎵ц鎽樿鐢熸垚鏃舵満

| 瑙﹀彂鍔ㄤ綔 | 鐢熸垚鏂囦欢 |
|---|---|
| 澶勭悊褰撳ぉ鏃ユ姤瀹為檯瀹屾垚 | `actuals/daily/{today}.md` |
| 鐢熸垚鍛ㄦ姤 | `actuals/weekly/{week}.md` |
| 浠诲姟鐘舵€佸彉鏇?| 鏇存柊 `personal-todo-index.md`锛屽繀瑕佹椂杩藉姞 `actuals` |

---

## 7. 蹇収鍐呭瑙勮寖

### 7.1 鏃ュ揩鐓у瓧娈?
| 瀛楁 | 璇存槑 |
|---|---|
| snapshot_date | 蹇収鐢熸垚鏃ユ湡锛堝綋澶╋級 |
| target_date | 璁″垝鐩爣鏃ユ湡锛堥€氬父涓烘鏃ワ紱瀵煎叆蹇収鍙负浠绘剰鍘嗗彶/鏈潵鏃ユ湡锛?|
| created_at | 鐢熸垚鏃堕棿 |
| source_type | 鏉ユ簮绫诲瀷锛坧ersonal_daily_reports / pm_todo / meeting / external_import锛?|
| status | frozen锛堝喕缁擄級 |

**source_type 璇箟锛堢粺涓€锛?*锛?- `personal_daily_reports`锛氫粠**涓汉鏃ユ姤**鏄庢棩璁″垝鎻愬彇鐢熸垚銆?- `pm_todo`锛氱敓鎴?PM 寰呭姙鏃剁敓鎴愩€?- `meeting`锛氫粠浼氳绾鎻愬彇鐢熸垚鐨勮鍒掋€?- `external_import`锛氫粠 `.pod`/Excel 绛夊閮ㄦ枃浠?*鎵归噺瀵煎叆**鐢熸垚锛堣 搂8a锛夛紝`daily_reports` 宸插苟鍏ヤ笂杩拌涔夛紝鍘嗗彶鏂囦欢涓殑 `daily_reports` 鎸?`personal_daily_reports` 鍏煎瑙ｈ銆?
### 7.2 蹇収绔犺妭

1. PM 鐩存帴浠诲姟
2. 鍏ㄥ洟闃熺洰鏍囨棩鏈熻鍒掞紙鎸夊瓙椤圭洰鍒嗙粍锛?3. 闇€璺熻繘椋庨櫓
4. 闇€璺熻繘闂
5. 閲岀▼纰戝叧娉?6. 璧勬簮鎻愰啋
7. 鏃犺鍒掗」鐩?
---

## 8. 瀹為檯鎵ц鎽樿鍐呭瑙勮寖

### 8.1 瀛楁

| 瀛楁 | 璇存槑 |
|---|---|
| actual_date | 瀹為檯鎵ц鏃ユ湡 |
| created_at | 鐢熸垚鏃堕棿 |
| source_type | 鏉ユ簮绫诲瀷锛坧ersonal_daily_reports锛涙部鐢ㄥ巻鍙?`daily_reports` 浜﹀吋瀹癸級 |
| status | draft / final |

### 8.2 绔犺妭

1. **瀹屾垚姹囨€?*锛氬師璁″垝瀹屾垚鎯呭喌锛圱odo ID / 璁″垝浠诲姟 / 瀹為檯缁撴灉 / 瀹屾垚鐘舵€?/ 璇佹嵁鏉ユ簮锛?2. **璁″垝澶栧伐浣?*锛氭湭鍦ㄨ鍒掍腑浣嗗疄闄呭畬鎴愮殑宸ヤ綔
3. **寤舵湡/缁撹浆**锛氬師璁″垝鏈畬鎴愶紝寤舵湡鍒颁綍鏃讹紝鍘熷洜

### 8.3 瀹屾垚鐘舵€佸彇鍊?
| 鐘舵€?| 璇存槑 |
|---|---|
| planned_done | 鍘熻鍒掍笖宸插畬鎴?|
| planned_not_done | 鍘熻鍒掍絾鏈畬鎴?|
| blocked | 鍘熻鍒掍絾琚樆濉?|
| cancelled | 鍘熻鍒掑彇娑?|
| carried_forward | 鍘熻鍒掑欢鏈?缁撹浆 |
| unplanned_done | 鏈鍒掍絾瀹為檯瀹屾垚 |
| no_evidence | 缂哄皯瀹為檯璇佹嵁 |

---

## 8a. 鍘嗗彶璁″垝鎵归噺瀵煎叆蹇収锛坋xternal_import锛孯1锛?
### 8a.1 瑙﹀彂涓庣洰鐨?
鐢ㄦ埛鎻愪緵鍘嗗彶璁″垝鏂囦欢锛坄.pod` OmniPlan / Excel 璁″垝琛級骞惰"瀵煎叆鍘嗗彶璁″垝 / 鍚屾杩涜鍒掍綋绯?鏃惰Е鍙戙€傜洰鐨勬槸鎶?*涓€娆℃€у洖婧亴鍏?*鐨勫巻鍙茶鍒掕惤涓哄揩鐓э紝渚涘洖鏌ヤ笌鍚庣画璁″垝鍙樻洿杩借釜锛?*鑰岄潪閫愭棩鍓嶅悜鐢熸垚**銆?
### 8a.2 鏁版嵁婧愪笌纭

1. 璇诲彇 `.pod`/Excel锛岃В鏋愯鍒掑瓧娈碉紙Task/Owner/Due Date锛屽鏂囦欢鍚巻鍙蹭换鍔＄骇鍒敤 `涓€绾?浜岀骇` 鏄犲皠鍒?Task锛夈€?2. 鐢熸垚**瀵煎叆鍊欓€?*锛堝惈 Original Due Date 鏄犲皠锛夛紝杈撳嚭"寤鸿瀵煎叆娓呭崟"銆?3. **浜哄伐纭鍚?*鎵嶈惤搴擄紙浜嬪疄婧愮‘璁ゅ師鍒欙級銆?4. 涓?`references/13-continuity-rules.md` 鍒掔晫锛?3 鍙风椋庨櫓/闂/闇€姹傜瓑杩囩▼璁板綍鐨勭粨杞紱R1锛堟湰灏忚妭锛?*鍙?*绠′换鍔¤鍒掓暟鎹殑鎵归噺瀵煎叆涓哄揩鐓э紝浜岃€呭苟琛屼笉閲嶅彔銆?
### 8a.3 鐢熸垚鏂囦欢涓庡懡鍚?
- 鏂囦欢锛歚snapshots/daily/imported-{date}.md`锛坉ate 涓鸿鍒掔洰鏍囨棩鏈燂級鎴栨寜鍛?`snapshots/weekly/imported-{week}.md`銆?- 鍛藉悕鐢?`imported-` 鍓嶇紑锛?*涓?AI 鍓嶅悜鐢熸垚鐨?`{date}.md` 鍖哄垎锛屼笉浜掔浉瑕嗙洊**銆?- frontmatter 瀛楁锛歚source_type: external_import` + `import_source`锛堝師濮嬫枃浠惰矾寰勶級+ `import_date`锛堝鍏ュ姩浣滄棩鏈燂級+ `status: frozen`銆?
### 8a.4 鍐荤粨涓庝慨璁?
- 瀵煎叆蹇収鍚屾牱**榛樿鍐荤粨**锛涗慨璁㈤€氳繃杩藉姞 `Revision Log`锛堣 搂11锛夛紝涓嶉潤榛樿鐩栥€?- 瀵煎叆鍚庡悓姝ョ櫥璁?`history-index.md`锛堟爣娉?source_type=external_import锛夈€?
### 8a.5 涓?board 鑱斿姩

瀵煎叆鐨勮鍒掕嫢闇€杩涘叆浠诲姟鐪嬫澘杩借釜鍙樻洿/寤舵湡锛圧2/R3锛夛紝灏嗚В鏋愮粨鏋滃洖濉?`tasks/board.md`锛圤riginal Due Date / Due Date / Plan Change Count / Delay Count锛夛紝瑙勫垯瑙?`references/03-task-board-rules.md`銆?
---

## 9. 璁″垝 vs 瀹為檯瀵规瘮瑙勫垯

褰撶敤鎴锋煡璇㈣鍒掑畬鎴愭儏鍐垫垨璁″垝鍋忓樊鏃讹紝AI 蹇呴』鍚屾椂璇诲彇锛?
1. 瀵瑰簲璁″垝蹇収 `snapshots/daily/{snapshot_date}.md`锛堝鍏ヨ鍒掍负 `imported-{date}.md`锛?2. 瀵瑰簲瀹為檯鎵ц `actuals/daily/{target_date}.md`

杈撳嚭瀵规瘮琛細

```markdown
## 璁″垝 vs 瀹為檯瀵规瘮 - {target_date}

| Todo ID | Owner | Planned Task | Actual Result | Completion Status | Evidence |
|---|---|---|---|---|---|
| TODO-20260810-001 | 闄堜匠鑿?| 鎺ュ彛鑱旇皟 | 宸插畬鎴愯仈璋?| planned_done | 鏃ユ姤 |
| TODO-20260810-002 | 鑳″悍鍒?| 淇璁よ瘉闂 | 绛夊緟鎺ュ彛鏂囨。 | blocked | 鏃ユ姤 |

### 鍋忓樊姹囨€?- 鍘熻鍒掞細5 椤?- 宸插畬鎴愶細3 椤癸紙60%锛?- 鏈畬鎴愶細1 椤癸紙闃诲锛?- 寤舵湡锛? 椤?- 璁″垝澶栧畬鎴愶細2 椤?```

---

## 10. 鍘嗗彶鏌ヨ璺敱

### 10.1 瑙﹀彂璇?
寰€鏃ヨ鍒掋€佸巻鍙茶鍒掋€佽繃鍘绘煇澶┿€佷箣鍓嶆煇澶┿€佹煇鏈堟煇鏃ュ師璁″垝銆佹煇鏈堟煇鏃ュ疄闄呭畬鎴愩€佽鍒掑畬鎴愭儏鍐点€佽鍒掑亸宸€佽鍒掓湁娌℃湁瀹屾垚銆佷笂鍛ㄨ鍒掑鐓с€佷笂鍛ㄤ簩澶у鍘熸潵瑕佸仛浠€涔堛€佹煇浜轰笂鍛ㄦ瘡澶╄鍒掋€佸鍏ョ殑鍘嗗彶璁″垝銆佸悓姝ヨ繘鏉ョ殑璁″垝

### 10.2 鏌ヨ椤哄簭

1. 璇诲彇 `history-index.md`
2. 瀹氫綅 `snapshots/daily/{date}.md` 鎴?`snapshots/weekly/{week}.md`锛堝鍏ヨ鍒掑畾浣?`imported-{date}.md`锛?3. 濡傛煡璇㈠疄闄呭畬鎴愶紝璇诲彇 `actuals/daily/{date}.md` 鎴?`actuals/weekly/{week}.md`
4. 濡傚揩鐓?瀹為檯鎽樿涓嶅瓨鍦紝璇诲彇瀵瑰簲鏈堜唤鏃ユ姤绱㈠紩
5. 鐢ㄦ埛纭鍚庢墠鍏佽鎵弿鍏蜂綋鏃ユ姤鏄庣粏

### 10.3 甯歌鏌ヨ璺敱

| 鐢ㄦ埛闂 | 璇诲彇璺緞 |
|---|---|
| 8鏈?0鏃ュぇ瀹跺師璁″垝鍋氫粈涔?| `history-index.md` 鈫?`snapshots/daily/20260809.md`锛坰napshot_date=08-09, target_date=08-10锛?|
| 8鏈?0鏃ュ疄闄呭仛浜嗕粈涔?| `actuals/daily/20260810.md` |
| 8鏈?0鏃ヨ鍒掑畬鎴愪簡鍚?| `snapshots/daily/20260809.md` + `actuals/daily/20260810.md` |
| 涓婂懆璁″垝鍋忓樊 | `snapshots/weekly/{week}.md` + `actuals/weekly/{week}.md` |
| 鏌愪汉杩囧幓涓€鍛ㄦ瘡澶╄鍒?| `history-index.md` 鈫?澶氫釜 daily snapshots |
| 瀵煎叆鐨勯偅鎵硅鍒?| `history-index.md` 鈫?`snapshots/daily/imported-{date}.md`锛坰ource_type=external_import锛?|

---

## 11. 蹇収鍐荤粨瑙勫垯

1. 蹇収鐢熸垚鍚庨粯璁ゅ喕缁擄紝涓嶅緱闈欓粯瑕嗙洊锛堝惈 external_import 瀵煎叆蹇収锛夈€?2. 濡傚彂鐜版娊鍙栭敊璇紝鍦ㄥ揩鐓ф湯灏捐拷鍔?`Revision Log`銆?3. 淇璁板綍鏍煎紡锛?
```markdown
## Revision Log
| Time | Change | Reason | Operator |
|---|---|---|---|
| 2026-08-09 22:10 | 琛ュ厖闄堜匠鑿佽鍒掗」 | 鍘熸棩鎶ヨˉ褰?| AI |
```

---

## 12. Todo ID 瑙勫垯

鏍煎紡锛歚TODO-{target_date}-{NNN}`

绀轰緥锛歚TODO-20260810-001`

- target_date锛氳鍒掔洰鏍囨棩鏈?- NNN锛氬綋鏃ュ簭鍙凤紙001~999锛?
濡傛灉浠诲姟杩涘叆鍚庣画澶氭棩婊氬姩锛屼繚鎸佸悓涓€涓?Todo ID锛屽湪 actuals 涓紩鐢ㄣ€?
---

## 13. 鍛ㄥ揩鐓т笌鍛ㄥ疄闄?
### 13.1 鍛ㄥ揩鐓?
姣忓懆涓€鎴栫敓鎴愬懆璁″垝鏃跺垱寤?`snapshots/weekly/{YYYY}-W{WW}.md`锛?
- 鏈懆鍚勫瓙椤圭洰閲嶇偣璁″垝
- 鍏抽敭閲岀▼纰?- 閲嶇偣椋庨櫓
- 璧勬簮瀹夋帓
- 璺ㄩ」鐩崗璋冧簨椤?
### 13.2 鍛ㄥ疄闄?
鍛ㄦ湯鎴栫敓鎴愬懆鎶ユ椂鍒涘缓 `actuals/weekly/{YYYY}-W{WW}.md`锛?
- 鏈懆瀹為檯瀹屾垚
- 鏈懆鍋忓樊
- 鏈畬鎴愬師鍥?- 涓嬪懆缁撹浆

---

## 14. 涓庡叾浠栬鍒欑殑鍏崇郴

| 瑙勫垯 | 鑱岃矗 |
|---|---|
| `05-query-rules.md` | 鍘嗗彶鏌ヨ璺敱銆佺儹/鍐锋暟鎹垎绂汇€佽仛鍚堣鏁扮绛?|
| `01-daily-report-rules.md` | 鏃ユ姤澶勭悊鏃剁敓鎴?snapshot 鍜?actuals |
| `10-update-trigger-rules.md` | 瑙﹀彂 snapshot/actuals 鏇存柊 |
| `06-file-rules.md` | 蹇収鍐荤粨瑙勫垯銆佺儹/鍐锋暟鎹竟鐣屻€乪xternal_import 鍛藉悕 |
| `14-self-check-rules.md` | 蹇収瀹屾暣鎬ф牎楠?|
| `03-task-board-rules.md` | 璁″垝鍙樻洿璁℃暟銆佸欢鏈熻鏁般€佽秴鏈熷垽瀹氾紙B 绫伙級 |
| `13-continuity-rules.md` | 涓?R1 鍒掔晫锛?3 绠＄粨杞紝R1 绠¤鍒掓暟鎹鍏ワ級 |

## 15. 瀛樺偍鐢熷懡鍛ㄦ湡

鐑暟鎹紙褰撳墠绱㈠紩涓紩鐢ㄧ殑蹇収/瀹為檯锛夛細淇濈暀鍦ㄥ師浣嶃€?娓╂暟鎹紙90 澶╁唴鐨勫揩鐓?瀹為檯鏂囦欢锛夛細淇濈暀鍦ㄥ師浣嶃€?鍐锋暟鎹紙>90 澶╃殑蹇収/瀹為檯鏂囦欢锛夛細
- 瑙﹀彂锛氭瘡鍛ㄦ鏌ヤ竴娆★紙鍦ㄥ懆鎶ョ敓鎴愭椂椤哄甫妫€鏌ワ級
- 鍔ㄤ綔锛氬皢 >90 澶╃殑鏂囦欢绉诲姩鍒?`snapshots/archive/YYYY/` 鍜?`actuals/archive/YYYY/`
- 鏇存柊 `history-index.md`锛氬綊妗ｆ潯鐩爣璁颁负 `[宸插綊妗`锛屼笉鍒犻櫎鏂囦欢

`history-index.md` 鑷韩鐦﹁韩锛?- >200 琛屾椂锛屽皢 >180 澶╃殑宸插畬鎴愭潯鐩Щ鑷?`history-index-archive.md`
