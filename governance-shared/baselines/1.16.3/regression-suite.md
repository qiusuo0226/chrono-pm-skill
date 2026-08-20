# Regression Suite

> 鏈枃浠舵槸 ChronoPM Skill 鐨勬€诲洖褰掓祴璇曟竻鍗曘€傛瘡娆″彉鏇村繀椤诲０鏄庤嚦灏戣窇鍝簺鐢ㄤ緥銆?
---

## 1. Quick Query锛堝揩閫熸煡璇級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| QQ-001 | 鎴戞槑澶╃殑寰呭姙鏄粈涔?| 浼樺厛璇?`portfolio/todos/personal-todo-index.md`锛岃緭鍑?9 绔犺妭鍏ㄦ櫙瑙嗗浘锛屼笉寰楀彧鍒?PM 涓汉浠诲姟 | positive |
| QQ-002 | 鏄庡ぉ澶у鍋氫粈涔?| 浼樺厛璇?`daily-todo-index.md` | positive |
| QQ-003 | 鏈懆閲嶇偣鏄粈涔?| 浼樺厛璇?`weekly-todo-index.md` | positive |
| QQ-004 | 寮犱笁鐜板湪鍦ㄥ仛浠€涔?| 浼樺厛璇?`summaries/寮犱笁-progress.md` | positive |
| QQ-005 | 褰撳墠鏈夊摢浜涢闄?| 浼樺厛璇?`risks/risk-register.md`锛坥pen锛夛紝涓嶆壂鎻忓巻鍙插懆鎶?| positive |
| QQ-006 | 8鏈?0鏃ュぇ瀹跺師璁″垝鍋氫粈涔?| 浼樺厛璇?`history-index.md` 鈫?`snapshots/daily/` | positive |
| QQ-007 | 8鏈?0鏃ヨ鍒掑畬鎴愪簡鍚?| 鍚屾椂璇?`snapshots/` + `actuals/`锛岃緭鍑哄姣旇〃 | positive |
| QQ-008 | 涓婂懆璁″垝鍋忓樊 | 鍚屾椂璇?`snapshots/weekly/` + `actuals/weekly/` | positive |
| QQ-009 | 椤圭洰杩涘睍濡備綍 | 浼樺厛璇?`tasks/board.md` + `milestones/`锛屼笉鎵弿鎵€鏈夎繃绋嬭褰?| positive |
| QQ-010 | 绠€鍗曟煡璇紙鏄庡ぉ寰呭姙锛?| 涓嶅緱鍒涘缓涓存椂 JS/Python 鑴氭湰鎵弿鐩綍 | regression |
| QQ-011 | 绱㈠紩涓嶅瓨鍦ㄦ椂 | 鎻愮ず鐢ㄦ埛閲嶅缓绱㈠紩锛屼笉鑷鍏ㄩ噺鎵弿 | regression |

## 2. Daily Report锛堟棩鎶ュ鐞嗭級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| DR-001 | 澶勭悊浠婂ぉ涓汉鏃ユ姤 | 鍐欏叆 `reports/daily/personal/{YYYYMM}/YYYY-MM-DD-{name}.md` | positive |
| DR-002 | 鐢熸垚椤圭洰鏃ユ姤 | 鍐欏叆 `reports/daily/project/{YYYYMM}/` | positive |
| DR-003 | 鍚屼汉鍚屽ぉ绗簩娆℃彁浜ゆ棩鎶?| 鍚堝苟杩藉姞锛屼笉瑕嗙洊锛岃拷鍔犳洿鏂拌褰?| regression |
| DR-004 | 鏃ユ姤涓寘鍚?鎷呭績鎺ュ彛寤舵湡" | 璇嗗埆涓洪闄╁€欓€夛紝杈撳嚭鍦ㄨ嚜鏌ユ竻鍗曚腑 | positive |
| DR-005 | 鏃ユ姤涓寘鍚?璇峰亣" | 瑙﹀彂璧勬簮鍙樺姩妫€娴嬶紝鎻愮ず鏇存柊 resource-register | positive |
| DR-006 | 鏃ユ姤涓寘鍚槑鏃ヨ鍒?| 鎻愬彇涓?TODO锛屾洿鏂?todos index + 鐢熸垚 snapshot | positive |
| DR-007 | 澶勭悊鏃ユ姤鍚?| 鎵ц D1-D10 鑷煡娓呭崟骞惰緭鍑虹粨鏋?| regression |
| DR-008 | 鏃ユ姤鏂囦欢璺緞 | 浣跨敤 `YYYYMM` 鍗曠骇鐩綍锛屼笉浣跨敤 `YYYY/MM` | regression |

## 3. Weekly Report锛堝懆鎶ョ敓鎴愶級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| WR-001 | 甯垜鐢熸垚鍛ㄦ姤 | 鍏堣闂緭鍑烘柟寮忔垨鐢熸垚 Markdown 鑽夌锛屼笉鐩存帴瀵煎嚭姝ｅ紡鏂囦欢 | positive |
| WR-002 | 椤圭洰闆嗘ā寮忎笅鐢熸垚鍛ㄦ姤 | 鍚屾椂鐢熸垚瀛愰」鐩懆鎶ュ拰椤圭洰闆嗘眹鎬诲懆鎶?| positive |
| WR-003 | 鐢熸垚鍛ㄦ姤 Excel | 鍐欏叆 `outputs/{timestamp}/files/`锛屼笉鍐欏叆 `ai/` | regression |
| WR-004 | 淇敼鍒氭墠鐨勫懆鎶?| 澶嶇敤鍚屼竴 batch 鐩綍锛屼笉鏂板缓鏃堕棿鎴?| regression |
| WR-005 | 鍛ㄦ姤鐢熸垚鍚?| 鑷姩鐢熸垚 `actuals/weekly/` 瀹為檯鎵ц鎽樿 | positive |

## 4. PM Daily Todo锛圥M 寰呭姙锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| PT-001 | 鎴戞槑澶╃殑寰呭姙 | 杈撳嚭 9 绔犺妭鍏ㄦ櫙瑙嗗浘锛圥M浠诲姟+鍏ㄥ洟闃熻鍒?椋庨櫓+闂+閲岀▼纰?璧勬簮鍙樺姩+鏈懆瀵圭収+寰呭崗璋?鏃犺鍒掗」锛?| regression |
| PT-002 | 鍏ㄥ洟闃熸槑鏃ヨ鍒?| 鎸夊瓙椤圭洰鍒嗙粍锛屾瘡涓垚鍛樺垪鍑轰换鍔°€佽繘搴︺€侀噷绋嬬銆侀闄╂爣璁?| positive |
| PT-003 | 鏌愬瓙椤圭洰鏃犺鍒掗」 | 鏄庣‘鏍囨敞鍦?鏃犺鍒掗」鎻愰啋"绔犺妭 | positive |

## 5. Output Artifact锛堣緭鍑虹墿绠＄悊锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| OA-001 | 甯垜鐢熸垚鍛ㄦ姤 | 杩涘叆 `outputs/{timestamp}/`锛屽厛鐢熸垚 draft.md | positive |
| OA-002 | 甯垜鐢熸垚 Excel 鍛ㄦ姤 | 鍐欏叆 `outputs/{timestamp}/files/`锛屼笉鍐欏叆 `ai/` | regression |
| OA-003 | 淇敼鍒氭墠鐨勫懆鎶ュ唴瀹?| 澶嶇敤鍚屼竴 batch锛岃拷鍔?`revisions/` | regression |
| OA-004 | 纭鍚庡鍑?| 鐢熸垚 final.md锛屽啀瀵煎嚭鍒?`files/` | positive |
| OA-005 | 褰掓。鍒伴」鐩泦鍛ㄦ姤 | 璇㈤棶纭鍚庡啓鍏?`ai/portfolio/reports/weekly/` | positive |
| OA-006 | 鐢熸垚鏂囦欢璺緞 | 浣跨敤 `outputs/`锛屼笉浣跨敤 `ai/` | regression |

## 6. Continuity锛堝巻鍙查樁娈佃鎺ワ級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| CT-001 | 杩欐槸涓婁竴闃舵 ai 鐩綍 | 杩涘叆琛旀帴娴佺▼锛岀櫥璁?legacy-sources锛屼笉鐩存帴瑕嗙洊褰撳墠 | positive |
| CT-002 | 鎶婁竴鏈熼仐鐣欓闄╁甫杩囨潵 | 鍏堣繘鍏?carryover-register锛岀瓑寰呯‘璁?| positive |
| CT-003 | 鍘嗗彶瀵煎叆 | 涓嶅緱瑕嗙洊褰撳墠闃舵宸叉湁鏂囦欢 | regression |
| CT-004 | 鍐茬獊妫€娴?| 鍘嗗彶浜嬮」涓庡綋鍓嶇浉浼兼椂鎻愮ず鍐茬獊锛?绉嶅鐞嗛€夐」 | positive |

## 7. Todo Snapshot锛堣鍒掑揩鐓э級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| TS-001 | 澶勭悊鏃ユ姤鍚?| 鑷姩鐢熸垚 `snapshots/daily/{date}.md` + 鏇存柊 `history-index.md` | positive |
| TS-002 | 澶勭悊鏃ユ姤鍚?| 鑷姩鐢熸垚 `actuals/daily/{date}.md` | positive |
| TS-003 | 蹇収鐢熸垚鍚?| 鍐荤粨锛屼笉闈欓粯瑕嗙洊锛屼慨鏀硅拷鍔?Revision Log | regression |
| TS-004 | 璁″垝 vs 瀹為檯鏌ヨ | 鍚屾椂璇?snapshot + actuals锛岃緭鍑?7 绉嶅畬鎴愮姸鎬?| positive |

## 8. File Rules锛堟枃浠剁鐞嗭級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| FR-001 | 鏃ユ姤鐩綍璺緞 | 浣跨敤 `YYYYMM`锛屼笉浣跨敤 `YYYY/MM` | regression |
| FR-002 | 鐢熸垚瀵煎嚭鏂囦欢 | 鍐欏叆 `outputs/`锛屼笉鍐欏叆 `ai/` | regression |
| FR-003 | AI 绠＄悊鏂囦欢浣嶇疆 | 缁熶竴鍦?`ai/` 涓嬶紝涓嶄镜鍏ヤ笟鍔＄洰褰?| regression |
| FR-004 | 绠€鍗曟煡璇?| 涓嶅緱榛樿鍒涘缓 JS/Python 涓存椂鑴氭湰 | regression |
| FR-005 | 杩涘叆宸ヤ綔鍖?| 鍏堣 `.skill-version.json` 妫€鏌ョ増鏈吋瀹规€?| regression |
| FR-006 | 澶勭悊浠讳綍杈撳叆鍓?| 鍏堣 `project-brief.md` 鍒ゆ柇鍏宠仈搴?| regression |

## 9. Self Check锛堣嚜鏌ユ牎楠岋級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SC-001 | 澶勭悊鏃ユ姤鍚?| 杈撳嚭 D1-D10 鑷煡娓呭崟 | regression |
| SC-002 | 澶勭悊浼氳绾鍚?| 杈撳嚭 M1-M7 鑷煡娓呭崟 | regression |
| SC-003 | 鐢ㄦ埛杩介棶"鏈夋病鏈夋紡鐨? | 閲嶆柊鎵ц瀹屾暣鑷煡 + 鎵╁ぇ鎵弿鑼冨洿 | positive |
| SC-004 | 椋庨櫓杩芥函 | 澶氭簮浜ゅ弶鏍￠獙锛堢櫥璁板唽 vs 鏃ユ姤 vs 浼氳 vs 鍛ㄦ姤 vs 闂 vs 鐪嬫澘锛?| positive |

## 10. Versioning锛堢増鏈鐞嗭級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| VG-001 | 淇敼鐩綍缁撴瀯 | 蹇呴』鎻愬崌 workspace schema | regression |
| VG-002 | 淇敼鏍稿績濂戠害 | 蹇呴』璧?contract_change + 鍏ㄩ噺鍥炲綊 | regression |
| VG-003 | 灏忔ā鏉夸慨澶?| 鍙彁鍗?patch 鐗堟湰 | regression |
| VG-004 | 鐗堟湰涓嶅尮閰?| 鎻愮ず鐗堟湰宸紓锛屼笉鑷杩佺Щ | regression |

## 11. Resource Management锛堣祫婧愮鐞嗭級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| RM-001 | 寮犱笁琚娊璋?| 鏇存柊 resource-register + 鐢熸垚 transfer-log | positive |
| RM-002 | 璧勬簮鐘舵€佹煡璇?| 璇?resource-register锛堝綋鍓嶇姸鎬侊級锛屼笉璇?transfer-log | regression |
| RM-003 | 娴佽浆鍘嗗彶鏌ヨ | 璇?transfer-log锛屼笉璇?resource-register | regression |

## 12. Excel Generation锛圗xcel 鐢熸垚锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| EG-001 | 鐢熸垚闇€姹傝窡韪煩闃?Excel | 14 鍒楃簿纭垪澶?+ 鏁版嵁楠岃瘉涓嬫媺妗?+ 鍐荤粨棣栬 | positive |
| EG-002 | 鐢熸垚椋庨櫓鐧昏鍐?Excel | 15 鍒?+ 鏉′欢鏍煎紡锛堥珮=绾?涓?榛?浣?缁匡級 | positive |
| EG-003 | 鐢熸垚鎴愭湰娴嬬畻琛?| 璇㈤棶"鎸夎鑹叉眹鎬昏繕鏄寜涓汉鏄庣粏" | positive |
| EG-004 | 鐢熸垚闂璺熻釜琛?| "鏄惁寤舵湡"鍒椾娇鐢ㄥ叕寮?| positive |

## 13. Update Trigger锛堟洿鏂拌Е鍙戯級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| UT-001 | "璁板綍涓€涓嬶紝闄堜匠鑿佽鎶借皟" | 瑙﹀彂鏇存柊娴佺▼锛氫綆/涓闄╂寜 proactive 鐩存帴鍐欏叆浜嬪疄婧愬苟鏍囪寰呯‘璁わ紙鐧昏 pending-changes锛夛紝楂橀闄╁厛纭鍚庡啓 | positive |
| UT-002 | 涓婁紶璇勫鏉愭枡 | 璇嗗埆鏂囦欢绫诲瀷锛屼富鍔ㄨ闂槸鍚﹀叆搴?| positive |
| UT-003 | 鏃ユ姤涓寘鍚?鍐冲畾""纭" | 璇嗗埆涓哄喅绛栦俊鍙凤紝鎻愮ず鏇存柊 decision-log | positive |
| UT-004 | 绾煡璇?鐜板湪鏈夊摢浜涢闄? | 涓嶈Е鍙戞洿鏂版竻鍗?| regression |

## 14. Skill Governance锛堝彉鏇存不鐞嗭級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SG-001 | "甯垜浼樺寲涓€涓?Skill" | 鍏堣緭鍑哄彉鏇村伐鍗曡崏妗堬紝鏍囪 contract_change锛堣嫢娑夋牳蹇冨绾︼級锛屼笉鐩存帴鏀规枃浠?| regression |
| SG-002 | 鐢ㄦ埛纭鍙樻洿宸ュ崟鍚?| 鎵ц鏈€灏忓彉鏇?+ 璺戝叏閲忓洖褰掓祴璇曪紙contract_change 蹇呴』鍏ㄩ噺锛?| positive |
| SG-003 | 鍥炲綊娴嬭瘯澶辫触 | 寤鸿鍥炴粴锛屼笉鍙犲姞涓存椂淇 | regression |
| SG-004 | 淇敼鏍稿績濂戠害 | 鏍囪涓?contract_change + 鍏ㄩ噺鍥炲綊 | regression |

## 15. Blueprint锛堟灦鏋勮摑鍥句笌澶栭儴瀹℃煡锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| BP-001 | 澶栭儴 AI 鍙鍙?SKILL_BLUEPRINT.md | 鑳界悊瑙?Skill 鐩爣銆佽兘鍔涖€佽竟鐣屽拰寰呰ˉ鍏呴」 | positive |
| BP-002 | 瀵规瘮 skill.json.version 涓?Blueprint 搂1 鐗堟湰 | 鐗堟湰涓€鑷达紙鍧囦负 1.12.0锛?| positive |
| BP-003 | 瀵规瘮瑙勫垯鏂囦欢娓呭崟(00-21)涓?Capability Map | 22 涓鍒欐枃浠跺搴旂殑鑳藉姏鏃犻仐婕?| positive |
| BP-004 | 妯℃嫙 Patch 绾фā鏉垮皬淇?| Blueprint 鍙笉鏇存柊姝ｆ枃锛孋HANGELOG 鏍囨敞 "Blueprint Impact: none" | positive |
| BP-005 | 妯℃嫙 Minor 鏂板鑳藉姏 | Blueprint 蹇呴』鏇存柊 Capability Map 鍜?Roadmap | positive |
| BP-006 | 瀵规瘮 SKILL.md 涓?Blueprint 姝ｆ枃 | 涓嶅瓨鍦ㄥぇ娈甸噸澶嶇殑鐩綍鏍戞垨瑙勫垯鍏ㄦ枃 | regression |
| BP-007 | 妫€鏌?release-checklist.md | Documentation 绔犺妭鍖呭惈 Blueprint 妫€鏌ラ」 | positive |
| BP-008 | 妫€鏌?16-skill-governance-rules.md | 鍖呭惈 搂17 Blueprint 鏇存柊瑙勫垯 | positive |
| BP-009 | 妫€鏌?skill-contract.md 瑙勫垯鍒嗗眰琛?| 鍖呭惈鏂囨。灞傚垎绫?| positive |
| BP-010 | 妫€鏌?skill.json blueprint 瀛楁 | 鍖呭惈瀹屾暣瑙﹀彂鏉′欢鏁扮粍 | positive |

---

## 16. Qoder Adaptation锛圦oder 鐜閫傞厤锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| QA-001 | 鐢ㄦ埛闂?skill 鐗堟湰鏄灏? | 鍙 ai/.skill-version.json锛屼笉璇?SKILL.md | positive |
| QA-002 | 鐢ㄦ埛闂?鎴戞槑澶╃殑浠诲姟" | 鍙 todo-index锛屼笉璇?SKILL.md 鍜?references/ | positive |
| QA-003 | 绠€鍗曟煡璇㈣秴杩?3 涓枃浠?| 鍏堣鏄庡師鍥犲啀缁х画 | positive |
| QA-004 | 鐗堟湰鏌ヨ鍥炵瓟鏈熬 | 鍖呭惈"鏁版嵁鏉ユ簮锛?鏍囨敞 | positive |
| QA-005 | 鏂囦欢淇敼鏃堕棿鏃犳硶鑾峰彇 | 鏄剧ず"褰撳墠鐜鏈彁渚涳紝鏃犳硶纭"锛屼笉缂栭€犳椂闂?| regression |
| QA-006 | 鐢ㄦ埛瑕佹眰淇敼椋庨櫓鐧昏鍐?| 瑙﹀彂瀹夊叏鍗囩骇锛屽厛鍔犺浇瀹屾暣 SKILL.md 搂7 | regression |
| QA-007 | 澶嶆潅浠诲姟锛堟棩鎶ュ鐞嗭級 | 鍙澶氭枃浠朵絾闇€鍒楀嚭鏂囦欢娓呭崟 | positive |

## 17. Initialization Wizard锛堝垵濮嬪寲鍚戝锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| IW-001 | 鐢ㄦ埛璇?鍒濆鍖栭」鐩? | 鍚姩鍏鍚戝锛岃繘鍏?Step 1 鍚堝悓淇℃伅 | positive |
| IW-002 | 鏂板伐浣滃尯 project-brief status=鑽夌 | 鑷姩鎻愮ず"鏄惁寮€濮嬪垵濮嬪寲鍚戝" | positive |
| IW-003 | 鍚戝 Step 3 鐢ㄦ埛璇?璺宠繃" | 鏍囪涓哄緟琛ュ厖锛岀户缁?Step 4 | positive |
| IW-004 | 鍚戝涓柇鍚庡啀娆¤繘鍏?| 妫€娴嬪埌 init_wizard_progress锛屾彁绀轰粠鏂偣缁х画 | positive |
| IW-005 | 鍚戝瀹屾垚鍚?| 鐢熸垚鍒濆鍖栫‘璁ゆ憳瑕侊紝鐢ㄦ埛纭鍚庡啓鍏ユ墍鏈夋枃浠讹紝brief status 鏀逛负"宸茬‘璁? | positive |

## 18. Information Completeness锛堜俊鎭畬鏁存€у贰妫€锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| IC-001 | 鐢ㄦ埛璇?鐢熸垚鍛ㄦ姤" | 鎵ц寮鸿Е鍙戞鏌ワ紝鑻ュ彂鐜?P0/P1 缂哄け椤瑰垯涓诲姩鎻愰啋 | positive |
| IC-002 | 鐢ㄦ埛璇?鏌ヨ寮犱笁鐨勪换鍔? | 鎵ц寮辫Е鍙戞鏌ワ紝浠呮鏌ヤ笌寮犱笁浠诲姟鐩存帴鐩稿叧鐨勫瓧娈?| positive |
| IC-003 | 鐢ㄦ埛璇?杩涘叆闈欓粯妯″紡" | 鍚庣画涓嶅啀涓诲姩鎻愰啋锛孭0 绾х己澶变粛蹇呴』鎻愮ず | regression |
| IC-004 | 鐢ㄦ埛璇?缁欐垜鍋氫竴娆″畬鏁存€у贰妫€" | 杈撳嚭瀹屾暣鎬у贰妫€鎶ュ憡锛堟€讳綋缁撹+缂哄け娓呭崟+浼樺厛琛ュ厖寤鸿锛?| positive |
| IC-005 | 鐢ㄦ埛璇?鏈涓嶈鎻愰啋" | 鏈浠诲姟璺宠繃瀹屾暣鎬ф鏌ワ紝涓嬫鎭㈠ | regression |

## 19. Script Contract锛堣剼鏈绾︼級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SC-1A | `python init_workspace.py --help` | 鍙傛暟鍒楄〃涓€鑷达紙--project-root/--mode/--project-name/--portfolio-name/--sub-projects/--glossary锛?| regression |
| SC-1B | `--mode portfolio --sub-projects A B C` 鍦ㄤ复鏃剁洰褰曡繍琛?| 鐢熸垚 `ai/` 瀹屾暣鐩綍鏍戯紝涓庡熀绾跨粨鏋勪竴鑷达紙蹇界暐褰撴湀鏈堜唤鍊硷級 | positive |
| SC-1C | `--mode single --project-name X` 鍦ㄤ复鏃剁洰褰曡繍琛?| 鐢熸垚鍗曢」鐩?`ai/` 缁撴瀯涓庡熀绾夸竴鑷?| positive |
| SC-1D | 杩愯鐢熸垚 `.skill-version.json` | `initializedAt` 涓鸿繍琛屽綋澶╋紱鏈堜唤鐩綍涓鸿繍琛屽綋鏈?`%Y%m`锛堥潪鍥哄畾鍊硷級 | positive |
| SC-1E | 閲嶅杩愯 | 妯℃澘闃茶鐩栭€昏緫浠嶇敓鏁堬紙涓嶈鐩栧凡鏈夋枃浠讹級 | regression |
| SC-1F | portfolio 妯″紡缂哄弬 | 缂?--portfolio-name / --sub-projects 鏃舵墦鍗板搴旈敊璇苟 exit(1) | negative |
| SC-1G | `migrate_workspace.py --project-root <tmp> --target-version 1.9.0`锛堥潪 dry-run锛屽伐浣滃尯鏃х増鏈?1.0.0锛?| 璇诲彇 `<tmp>/ai/.skill-version.json` 鏂█ `skillVersion == "1.9.0"`锛堣瘉鏄?--target-version 瀹為檯鍐欏叆锛岃€岄潪鍗曚竴鐗堟湰婧愭垨鏃х‖缂栫爜鍊硷級 | positive |
| SC-1H | `python -c "from _version import SKILL_VERSION, WORKSPACE_SCHEMA_VERSION"`锛坰ys.path 鍚?`scripts/`锛?| 杈撳嚭 `SKILL_VERSION == 褰撳墠鍙戝竷鐗堟湰`锛堝 1.12.0锛夈€乣WORKSPACE_SCHEMA_VERSION == "0.6.0"`锛堝崟涓€鐗堟湰婧愮敓鏁堬級 | positive |
| SC-1I | `init_workspace.py --mode single` 鍦ㄤ复鏃剁洰褰曡繍琛屽悗璇诲彇 `.skill-version.json` | 鏂█ `skillVersion` 绛変簬鍗曚竴鐗堟湰婧愶紙濡?1.12.0锛夛紝涓斾笌 `_version.SKILL_VERSION` 涓€鑷达紙init 閾捐矾绔埌绔級 | positive |
| SC-1J | 璇诲彇 `migrate_workspace.VERSION_CAPABILITIES` | 鏂█鏈€澶?`version` 瀛楁 == 褰撳墠鍙戝竷鐗堟湰锛堝 1.12.0锛夛紝涓斿寘鍚?1.9.0 鏉＄洰锛堣兘鍔涜〃琛ュ叏锛?| regression |
| SC-1K | 杩愯鏃㈡湁 SC-1A~1F | 鍏ㄩ儴閫氳繃锛堣剼鏈?CLI 涓庤涓轰笉鍥炲綊锛?| regression |

## 20. SKILL Navigation锛圫KILL.md 瀵艰埅涓庝笅娌夊畬鏁存€э級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| SK-1A | 璇诲彇 `SKILL.md` | 琛屾暟 鈮?300 | regression |
| SK-1B | 妫€鏌?搂6 鎻愮ず璇嶈矾鐢辫〃 | 鍦烘櫙鏉＄洰涓庝慨鏀瑰墠涓€鑷达紙涓€鏉′笉鍒狅級 | regression |
| SK-1C | 妫€鏌?搂7 瀹夊叏搴曠嚎 | 搴曠嚎鏉＄洰瀹屾暣淇濈暀 | regression |
| SK-1D | 妫€鏌?搂8 ID 缂栫爜 | 缂栫爜浣撶郴瀹屾暣淇濈暀 | regression |
| SK-1E | 妫€鏌?搂15 瑙勫垯绱㈠紩 | 00-21 鍏?22 鏉?+ 鐗堟湰鎺у埗鏂囦欢瀹屾暣 | regression |
| SK-1F | 妫€鏌ヤ笅娌夎惤鐐?| 鐘舵€佹灇涓?搂5a)/杈撳嚭瑙勮寖(搂5.4/5.5)/瀹瑰繊搴?搂5c)/閲岀▼纰?搂5b)鍧囧瓨鍦ㄤ簬 `00-pm-main-rules.md` | positive |
| SK-1G | 妯℃嫙"鏌ヤ换鍔＄姸鎬? | 閫氳繃 搂6 璺敱琛ㄨ兘瀹氫綅鍒板搴?rule锛堝鑸彲鐢級 | positive |

## 21. File Contract锛堟枃浠剁鐞嗗绾?v1.8.1锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| FC-1A | 璇诲彇 `06-file-rules.md` | 鏃?搂0/搂0c 鍐呭锛涚珷鑺傜紪鍙疯繛缁棤閲嶅锛涜鏁伴殢鏂囦欢鐦﹁韩/RI 鐩綍澧為暱鍚堢悊锛堝熀绾?v1.15.0 涓?334 琛岋級 | positive |
| FC-1B | 璇诲彇 `20-workspace-version-rules.md` | 鍖呭惈鐗堟湰妫€鏌?鍋ュ悍妫€鏌?鍏煎妯″紡/鍏滃簳閫昏緫/鍗囩骇鎻愰啋/瑙﹀彂璇?杩佺Щ妯″紡鍏ㄩ儴鍐呭 | positive |
| FC-1C | 璇诲彇 `17-domain-glossary-rules.md` 鏈熬 | 鍖呭惈 搂17 璇嶅簱鏂囦欢瑙勮寖锛堟枃浠惰鏍?鍒涘缓杈圭晫/鎷嗗垎瑙勫垯锛?| positive |
| FC-1D | 妫€鏌?`SKILL.md` 搂6 璺敱琛?+ 搂5.1b | 搂6 鍚?20 鍙锋潯鐩紱搂5.1b 鎸囧悜 `20-workspace-version-rules.md` 鑰岄潪 06 | regression |

## 22. Daily Report Rules锛堟棩鎶ヨ鍒欏绾?v1.8.2锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| DR-1A | 璇诲彇 `01-daily-report-rules.md` | 鏃犻噸澶?搂2.3 鍧楋紱绔犺妭缂栧彿杩炵画鏃犻噸澶嶏紱鈮?00 琛?| positive |
| DR-1B | 妫€鏌?01 妯℃澘寮曠敤 | 6 澶勬ā鏉挎寚閽堝潎鎸囧悜 `assets/templates/` 涓嬪凡瀛樺湪鏂囦欢锛坧ersonal-daily / project-daily / weekly-report / personal-progress / portfolio-weekly / index-formats锛夛紝鏃犳偓绌哄紩鐢?| positive |
| DR-1C | 璇诲彇 01 搂1.2b 鏈褰掍竴鍖?| 浠呬繚鐣欏叆鍙ｈ鐐癸紝鎸囧悜 `17-domain-glossary-rules.md` 搂4/搂6锛屾湭閲嶅瀹屾暣涔濇娴佺▼ | positive |
| DR-1D | 璇诲彇 01 搂1.5 璧勬簮鍙樺姩杈撳嚭 | 鍊欓€夎祫婧愬彉鏇翠笌寤鸿鏇存柊娓呭崟涓哄唴鑱旀牸寮忥紙鏉ユ簮/褰撳墠鐘舵€?涓€鑷存€у垽鏂?寤鸿鎿嶄綔锛夛紝鏈紩鐢ㄤ笉瀛樺湪妯℃澘 | regression |

---

## 23. Query/Requirement/Artifact Rules锛堟煡璇?闇€姹?杈撳嚭鐗╄鍒欏绾?v1.8.3锛?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| QR-1A | 璇诲彇 `05-query-rules.md` | 鏃犻噸澶嶇珷鑺傜紪鍙凤紱闂绫诲瀷璺敱琛紙12 绫伙級涓?Quick Query 璺敱琛ㄥ畬鏁达紱鈮?00 琛岋紙鍩虹嚎 v1.15.0 涓?320 琛屾椂宸茶秴闄愶紝琛屾暟鏂█涓鸿蒋绾︽潫锛氫笉鍥犳棤璇佹嵁鐨勯噸澶嶅爢鍙犺啫鑳€锛岃涔夊畬鏁存€т负鍑嗭級 | positive |
| QR-1B | 璇诲彇 `11-output-artifact-rules.md` | 鈮?00 琛岋紱鎵规鐩綍缁撴瀯銆佽緭鍑虹姸鎬佹満銆佹潵婧愯拷婧€佺‘璁よ鍒欒涔夊畬鏁?| positive |
| QR-1C | 璇诲彇 `07-requirement-rules.md` | 瀛楁瀹氫箟涓庣姸鎬佹満锛坧roposed鈫抍onfirmed鈫抜n_progress鈫抎elivered鈫抋ccepted鈫抍hanged鈫抍ancelled锛夊強楠屾敹鏍囧噯鏈彉锛涜鏁伴殢 RI/鍚堝悓浣滅敤鍩熸墿灞曞闀匡紙鍩虹嚎 v1.15.0 涓?267 琛岋級锛屼笉浠ュ浐瀹氳鏁颁负纭柇瑷€ | positive |
| QR-1D | 妯℃嫙涓€娆¤繘搴︽煡璇?+ 涓€娆￠渶姹傜櫥璁?| 鏌ヨ鎸?05 搂2/搂2.5 璺敱琛ㄦ纭矾鐢辫鍙栫储寮曪紱闇€姹傛寜 07 瀛楁瀹氫箟涓庣姸鎬佹満姝ｇ‘鐧昏锛岃鑼冨寲鍚庤涔夊畬鏁翠繚鐣?| regression |

---

## 24. PM Profile锛堢敤鎴峰亸濂藉涔狅級

| Case ID | Input | Expected | Type |
|---|---|---|---|
| PP-001 | pm-profile.md 瀛樺湪涓旀湁 confirmed 鍋忓ソ"鍥炲闀垮害=绠€娲? | AI 杈撳嚭閲囩敤绠€娲佹牸寮?| positive |
| PP-002 | pm-profile.md 涓嶅瓨鍦?| 璺宠繃鍋忓ソ鍔犺浇锛屾寜榛樿鏍煎紡杈撳嚭锛屼笉鎶ラ敊 | regression |
| PP-003 | 鐢ㄦ埛璇?浠ュ悗鍏堢粰缁撹鍐嶅垎鏋? | 鐩存帴鍐欏叆 confirmed锛屾湰杞敓鏁?| positive |
| PP-004 | 鐢ㄦ埛杩炵画 3 娆℃湭绾犳绠€娲佹牸寮?| 鍐欏叆 pending锛屾湯灏捐緭鍑哄亸濂藉涔犳彁绀?| positive |
| PP-005 | 鐢ㄦ埛璇?纭 PF001" | pending 鈫?confirmed锛屾洿鏂?Change Log | positive |
| PP-006 | 鐢ㄦ埛璇?鍚﹀畾 PF001" | pending 鈫?rejected锛屼笉鍐嶈嚜鍔ㄥ缓璁?| positive |
| PP-007 | 鐢ㄦ埛璇?鎴戠殑鍋忓ソ" | 杈撳嚭褰撳墠 Profile 鍏ㄨ矊锛坈onfirmed + pending + rejected锛?| positive |
| PP-008 | confirmed 鍋忓ソ"鍥炲闀垮害=绠€娲? vs project-rules.md 鎸囧畾"璇︾粏鏍煎紡" | project-rules 浼樺厛锛岃緭鍑鸿缁嗘牸寮?| regression |
| PP-009 | 澶勭悊鏃ユ姤鏃?PM Profile 鍔犺浇 | confirmed 鍋忓ソ搴旂敤浜庢棩鎶ヨ緭鍑烘牸寮忥紝pending 涓嶇洿鎺ュ簲鐢?| positive |
| PP-010 | pm-profile.md 涓?pending 鍋忓ソ | pending 涓嶇洿鎺ユ敼鍙?AI 杈撳嚭琛屼负锛屼粎鏍囨敞鍊欓€?| regression |

---

## 25. Historical Plan Import & Change Tracking锛圧1-R4 鍘嗗彶璁″垝鍏ㄩ噺鍚屾涓庡彉鏇磋拷婧級

> 瀵瑰簲 CR-20260810-008锛坴1.10.0锛夈€傝鐩栭渶姹傝鏍?R1锛堟壒閲忓鍏ワ級銆丷2锛堣鍒掑彉鏇磋拷韪級銆丷3锛堝欢鏈熻鏁帮級銆丷4锛堣仛鍚堟煡璇㈣矾鐢憋級銆?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| HP-001 | 鐢ㄦ埛涓婁紶 .pod/Excel 瀛橀噺璁″垝瑕佹眰鎵归噺瀵煎叆 | 璧?R1锛氱敓鎴?`snapshots/daily/imported-{date}.md`锛坰ource_type=external_import锛? 鐧昏 history-index + 鍐?board(Source=import) | positive |
| HP-002 | 鎵归噺瀵煎叆鍓?| 鍏堝垽瀹氳蛋 R1 杩樻槸 13 鍙凤紙瑙?`13-continuity-rules.md` 搂2锛夛紱鏃犵嫭绔嬪巻鍙插伐浣滃尯鎵嶈蛋 R1 | positive |
| HP-003 | 鎵归噺瀵煎叆鍐荤粨 | imported-{date}.md 鐢熸垚鍚庡喕缁擄紝涓嶉潤榛樿鐩栵紝淇杩藉姞 Revision Log | regression |
| HP-004 | 瀵煎叆鍛藉悕 | 浣跨敤 `imported-{date}.md`锛屼笉涓?AI 鍓嶅悜鐢熸垚鐨?`{date}.md` 鍐茬獊 | regression |
| HP-005 | 瀵煎叆鐧昏 | 鍦?`todo-history-index-template` 澶栭儴瀵煎叆鐧昏杩藉姞涓€琛岋紙IMP-*锛?| positive |
| HP-006 | R1 鏌ヨ璺敱 | "瀵煎叆鐨勯偅鎵硅鍒?缁?history-index 鈫?imported-{date}.md 瀹氫綅锛宻ource_type=external_import | positive |
| HP-007 | board 璁℃暟棣栫増 | 瀵煎叆浠诲姟 Plan Change Count / Delay Count 璁?0 | positive |
| HP-008 | 璁″垝鍙樻洿杩借釜 | 鍗曚换鍔?Due Date/Owner 璋冩暣 鈫?board 閫掑 Plan Change Count锛孌elay 浠?Due Date 鍚庣Щ鏃?+1 | positive |
| HP-009 | 姒傚康鍩?| change-log 鐢ㄦ蹇靛煙 B锛坧lan_change锛夛紱board Change Log 鐢ㄦ蹇靛煙 A锛屼笉娣风敤 | regression |
| HP-010 | 寤舵湡缁熻鏌ヨ锛圓 绫伙級 | "寤舵湡浜嗗嚑娆?鍙 board.md 鍗曟枃浠讹紝涓嶆壂鎻忓揩鐓?鏃ユ姤锛涜緭鍑?delay-stats | positive |
| HP-011 | board 缂鸿鏁板瓧娈?| 鍥為€€ Change Log 缁熻骞舵爣娉?鎺ㄦ柇锛屾湭纭" | regression |
| HP-012 | 瓒呮湡鏌ヨ锛圔 绫伙級 | "鐜板湪鍝簺浠诲姟瓒呮湡"瀹炴椂璁＄畻锛岃 board + 棰勫缓绱㈠紩锛屼笉鎵棩鎶ュ師鏂?| positive |
| HP-013 | 纭绐楀彛鏈熷垽瀹?| v2 鏈‘璁ゆ寜鏃?Due Date 鍒ゅ欢鏈燂紱宸茬‘璁ゆ寜鏂?Due Date | positive |
| HP-014 | 璐熻矗浜哄彉鏇村綊灞?| 浜ゆ帴鍓嶈秴鏈熷綊鍘?Owner锛屼氦鎺ュ悗褰掓柊 Owner | positive |
| HP-015 | 瓒呮湡瑙﹀彂鏃舵満 | 澶勭悊鏃ユ姤鏃?+ PM 鏌ヨ杩涘害鏃堕兘瀹炴椂璁＄畻 | regression |
| HP-016 | 绱㈠紩杩囨湡璀﹀憡 | 绱㈠紩瓒?24h 鏈洿鏂版椂缁欏嚭杩囨湡璀﹀憡 | positive |
| HP-017 | source_type 缁熶竴 | snapshot source_type 鍙?personal_daily_reports/pm_todo/meeting/external_import 鍥涘€间箣涓€ | regression |

---

## 26. Pending Window锛堝緟纭绐楀彛鏈?路 涓诲姩鍙樻洿+浜哄伐纭锛?
> 瀵瑰簲 CR-20260811-002锛坴1.11.0锛夈€傝鐩栦簨瀹炴簮鐩存帴鍐欏叆+寰呯‘璁ゆ爣璁般€乸ending-changes 鐧昏銆佺‘璁?椹冲洖鍥炴粴銆丏ue Date 绌虹獥鏈熷垽瀹氥€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| PW-001 | 浣庨闄╀簨瀹炴簮鏇存柊锛堝鏂板浠诲姟琛岋級 | 鐩存帴鍐欏叆浜嬪疄婧愬苟鏍囪 `Confirmed By: 寰呯‘璁锛屽悓鏃剁櫥璁?`pending-changes.md`锛屾湯灏炬彁绀哄緟浜哄伐纭 | positive |
| PW-002 | 寰呯‘璁よ褰?| 鍦ㄥ埌鏈熷垽瀹氥€佸凡瀹屾垚缁熻涓竴寰嬭涓烘湭纭锛堜笉鍙備笌寤舵湡/瓒呮湡璁℃暟锛?| positive |
| PW-003 | 鐢ㄦ埛纭"纭 PW001" | pending 鈫?confirmed锛屼粠 pending-changes 绉婚櫎锛圕hange Log 淇濈暀锛夛紝鏍囪鐢熸晥 | positive |
| PW-004 | 鐢ㄦ埛椹冲洖"椹冲洖 PW001" | 鎭㈠鍙樻洿鍓嶅師鍊硷紝pending-changes 鏍囪 rejected锛屼笉鐣欓敊璇簨瀹?| regression |
| PW-005 | 寰呯‘璁よ褰曡秴 7/14 澶╂湭纭 | 瑙﹀彂鍌姙鍗囩骇鎻愮ず锛屼笉闈欓粯涓㈠純 | regression |
| PW-006 | 楂橀闄╁彉鏇达紙濡傚垹浠诲姟/鏀归噷绋嬬鍩虹嚎锛?| 蹇呴』鍏堢‘璁ゅ悗鍐欙紝涓嶉€傜敤涓诲姩鍐欏叆寰呯‘璁ゆā寮?| regression |

---

## 27. Change Log Archive锛堝彉鏇存棩蹇楀垎灞傚綊妗ｏ級

> 瀵瑰簲 CR-20260811-002锛坴1.11.0锛夈€傝鐩栨椿璺冨尯 50 琛?30 澶╄Е鍙戙€佹湀搴﹀綊妗ｆ枃浠躲€佹湀浠藉鑸储寮曘€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| CLA-001 | 娲昏穬鍖?Change Log 杈?50 琛?| 瑙﹀彂鎸夋湀褰掓。鑷?`change-log/archive/YYYYMM-change-log.md` | positive |
| CLA-002 | 娲昏穬鍖烘渶鏃ц褰曡秴 30 澶?| 瑙﹀彂褰掓。锛屾洿鏂?`change-log/index.md` 鏈堜唤瀵艰埅 | positive |
| CLA-003 | 鏌ヨ鍘嗗彶鍙樻洿 | 缁?`change-log/index.md` 瀹氫綅鍒板搴斿綊妗ｆ湀浠芥枃浠讹紝涓嶆壂娲昏穬鍖?| regression |

---

## 28. Workspace Cleanliness锛堝伐浣滅┖闂存竻娲佸害锛?
> 瀵瑰簲 CR-20260811-003锛坴1.12.0锛夈€傝鐩栨牴鐩綍鐧藉悕鍗曞悎瑙勩€佸菇鐏靛紩鐢ㄦ壂鎻忋€佺増鏈彿涓€鑷存€с€佹瀯寤虹紦瀛樻竻鐞嗐€傝鍒欐潵婧愶細`references/16-skill-governance-rules.md` 搂18/搂19/搂20銆?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| CL-001 | 鎵弿鏍圭洰褰曟墍鏈夋枃浠跺拰鐩綍 | 浠呭寘鍚櫧鍚嶅崟锛埪?8锛夊唴鐨勬潯鐩紝鏃犻潪鏍囧噯鏂囦欢 | positive |
| CL-002 | 鎵弿 CR/IA/RR/鍩虹嚎 README/CHANGELOG 涓殑鏂囦欢寮曠敤 | 鎵€鏈夎寮曠敤鐨勬枃浠惰矾寰勫繀椤诲疄闄呭瓨鍦紝鏃犲菇鐏靛紩鐢?| positive |
| CL-003 | 妫€鏌?SKILL.md 鐗堟湰鎺у埗琛ㄤ腑鐨勭増鏈彿 | 涓?VERSION 鏂囦欢涓€鑷达紝鏃犻檲鏃х増鏈彿 | regression |
| CL-004 | 鎵弿 scripts/ 鐩綍 | 鏃?`__pycache__/` 绛夋瀯寤虹紦瀛樻畫鐣?| positive |

---

## 29. Cascade Propagation锛堢骇鑱斾紶鎾級

> 瀵瑰簲 CR-20260812-001锛坴1.13.0锛夈€傝鐩?6 涓疄浣撹鍒欐枃浠舵柊澧炵殑 `搂绾ц仈浼犳挱瑙勫垯`锛?3 搂8銆?4 搂9銆?7 搂7銆?8 搂9銆?9 搂8銆?2 搂6锛夈€?0 鍙?搂8 绾ц仈鍐茬獊澶勭悊銆丄UTO 浣滅敤鍩熼檺瀹氾紙鍐欐淳鐢熻鍥撅級銆?4 鍙?搂2.4 绱㈠紩娲剧敓鍒嗙骇涓?D13/M8/R7 绾ц仈瀹屾暣鎬ц嚜鏌ラ」銆?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| CP-001 | Task鈫抎one + Risk Ref | CHECK 楠岃瘉椋庨櫓瀛樺湪锛汚UTO 鏇存柊 todo 绱㈠紩 | positive |
| CP-002 | Risk鈫抍onverted_to_issue | SUGGEST 鏂板 issue + AUTO 鏇存柊绱㈠紩 | positive |
| CP-003 | Issue鈫抮esolved + blocked task | SUGGEST 鎭㈠ task | positive |
| CP-004 | Resource鈫抩ffboard | SUGGEST 閲嶅垎閰?+ AUTO 鏇存柊 todo | positive |
| CP-005 | 澶?SUGGEST 鎸囧悜鍚屼竴鐩爣 | 鍚堝苟涓哄悓涓€鎵瑰缓璁竻鍗?| positive |
| CP-006 | 绾ц仈鍐茬獊鍦烘櫙 | 鏍囪 鈿?绾ц仈寮傚父锛屼氦 PM 鍐崇瓥 | negative |

## 30. Archive Governance锛堝綊妗ｆ不鐞嗭級

> 瀵瑰簲 CR-20260812-001锛坴1.13.0锛夈€傝鐩?B 绾挎枃浠惰啫鑳€娌荤悊鐨勫綊妗ｈЕ鍙戣鍒欙細02 鍙?decision-log 褰掓。銆?9 鍙?transfer-log 褰掓。銆?5 鍙峰揩鐓у瓨鍌ㄧ敓鍛藉懆鏈熴€?1 鍙?outputs 瀛樺偍鐢熷懡鍛ㄦ湡銆?1 鍙?搂5.8 閫氱敤褰掓。妫€鏌ャ€?6 鍙?搂9 閫氱敤褰掓。琛ㄣ€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| AG-001 | decision-log >30 鏉?| 瑙﹀彂鎸夊搴﹀綊妗?| positive |
| AG-002 | transfer-log >100 鏉?| 瑙﹀彂鎸夊勾搴﹀綊妗?| positive |
| AG-003 | 蹇収鏂囦欢 >90 澶?| 绉诲姩鍒?archive/YYYY/ | positive |
| AG-004 | outputs/index.md >100 琛?| 瑙﹀彂宸茬‘璁ゆ壒娆″綊妗?| positive |
| AG-005 | 鏃ユ姤澶勭悊鏈熬 搂5.8 閫氱敤褰掓。妫€鏌?| 鎵弿鎵€鏈夋湁褰掓。瑙勫垯瀹炰綋 | positive |
| AG-006 | 06 鍙?搂9 閫氱敤褰掓。琛ㄥ畬鏁存€?| 8 琛屽疄浣?脳 瑙﹀彂鏉′欢 脳 褰掓。鐩爣 脳 绱㈠紩 | positive |


## 31. Workflow Data Path锛堟爣鍑嗗伐浣滄祦鏁版嵁璺緞锛?
> 瀵瑰簲 v1.14.0锛圕R-20260812-001 缁級銆傝鐩?00 鍙?搂9 WF-1~WF-6 鏍囧噯宸ヤ綔娴佹暟鎹矾寰勪笌 05 鍙?搂2.5 Quick Update 璺敱琛ㄣ€傞噸鐐归獙璇侊細璺緞棰勫畾涔変笉寮卞寲鍒ゆ柇闃舵锛埪?.1 浜旀潯寮哄寲瑙勫垯锛夈€佸啓鍏ヤ粛閬靛惊 SKILL.md 搂7 搴曠嚎 #2锛坧ending-changes 鐧昏锛夈€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| WF-001 | "鏇存柊浜庢枃鑱殑寰呭姙" + 浜嬪疄渚濇嵁 | 鎸?WF-1 姝ラ 1-18 鎵ц锛氬畾浣?璇?todo-index/board/issue/risk)鈫掑垽鏂?寰呭姙鍖归厤/鐘舵€佸垽瀹?闂鍏抽棴/椋庨櫓鍏抽棴)鈫掑啓鍏?鍚?pending-changes 鐧昏)鈫掕ˉ鍏?鏃ユ姤绱㈠紩)鈫掕緭鍑哄彉鏇存憳瑕?| positive |
| WF-002 | WF-1 姝ラ 6 寰呭姙鍖归厤锛氱敤鎴风敤鍒悕/缂╁啓鎻忚堪 | 搂9.1 瑙勫垯1 鐢熸晥锛氳涔夊尮閰嶈€冭檻鍒悕缂╁啓锛屼笉鍥犺矾寰勯瀹氫箟绠€鍖栧垽鏂?| positive |
| WF-003 | WF-1 姝ラ 8/9 鍏宠仈闂/椋庨櫓浠?閮ㄥ垎缂撹В" | 搂9.1 瑙勫垯3/4 鐢熸晥锛氫笉鑷姩鍏抽棴锛屽垪鍏ュ缓璁竻鍗曞緟 PM 纭 | regression |
| WF-004 | WF-1 姝ラ 16锛氬崟绾姸鎬佹洿鏂版寚浠わ紙鏃犲伐浣滆繘灞曟弿杩帮級 | 搂9.1 瑙勫垯5 鐢熸晥锛氫笉瑙﹀彂 PF006 鏃ユ姤琛ュ叏锛屼粎鏇存柊寰呭姙鐘舵€?| regression |
| WF-005 | 05 鍙?Quick Update 璺敱琛?6 鏉″満鏅?| 姣忔潯鍦烘櫙鎸囧悜姝ｇ‘ WF 缂栧彿锛屼笖鍐欏叆鍔ㄤ綔鍚?SKILL.md 搂7 搴曠嚎 #2 寮曠敤锛堜笉缁曡繃纭锛?| positive |


## 32. Requirement Intelligence锛堥渶姹傛儏鎶?RI锛?
> 瀵瑰簲 CR-20260813-001锛坴1.15.0锛夈€傝鐩栬法婧愰渶姹傛媶璇嶃€佸綊骞躲€佽寖鍥村垽瀹氫笌涓夌骇绱㈠紩妫€绱紙requirements/atoms + canonical + source-type-registry锛夈€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| RI-001 | 鍚堝悓鏉℃鏂囨湰 | 鎷嗗垎涓?ATOM锛屽惈 source_type/authority/raw_text/norm_text | positive |
| RI-002 | 鍚堝悓+鎷涙爣瀵瑰悓涓€闇€姹傜殑涓嶅悓琛ㄨ堪 | 褰掑苟鍒板悓涓€ Canonical锛宔vidence 鍚?2 涓潵婧?| positive |
| RI-003 | 鏌?XX 鍦ㄤ笉鍦ㄥ悎鍚岃寖鍥村唴" | 杩斿洖 scope + 璇佹嵁閾撅紝鏈鍔犺浇 鈮?00 琛?| positive |
| RI-004 | 鏈櫥璁?source_type 鐨勯渶姹?| 瑙﹀彂鏈櫥璁版彁绀猴紝涓嶉潤榛樺綊绫?| negative |
| RI-005 | 鍚堝悓鍑烘柊鐗堟湰 | 鐩稿叧 ATOM 鏍囪 stale銆丆anonical evidence_stale | regression |
| RI-006 | 鏌?韬唤璁よ瘉" | 鍛戒腑"鐢ㄦ埛鐧诲綍"ATOM锛堣瘝搴撳悓涔夎瘝鎵╁睍锛?| regression |
| RI-007 | 鍚堝悓鏉℃ raw_text > 500 瀛?| 鎷嗗垎涓哄涓?ATOM锛宻upersedes 閾炬寚鍚戦鏉?| negative |
| RI-008 | 鍚堝悓(L1)涓庢妧鏈枃妗?L3)瀵瑰悓涓€闇€姹傝〃杩板啿绐?| Canonical 鍙?L1 authority锛宔vidence 淇濈暀涓ゆ潵婧?| regression |
| RI-009 | L2 绫诲埆绱㈠紩 norm_text 鎽樿 | AI 浠呰 L2 鍗冲彲鐞嗚В ATOM 璇箟锛屾棤闇€鍔犺浇 L3 鍏ㄦ枃 | positive |
| RI-010 | 鍏抽敭璇嶅尮閰嶅け璐?| P1 璇箟鍏滃簳锛歯orm_text 鎵 鈫?闄嶇骇鎻愮ず锛屼笉杩斿洖绌?| regression |
| RI-011 | source-type-registry 鏂板绫诲瀷鍚庤縼绉?| 5 姝ュ師瀛愭搷浣滐紙鏇存柊 registry 鈫?閲嶅啓 ATOM 鈫?鍒锋柊绱㈠紩 鈫?杩佺Щ鏂囦欢 鈫?澶辫触鍥為€€锛?| regression |
| RI-012 | Canonical scope_scope 鍙樻洿 | 绾ц仈浼犳挱鑷虫墍鏈夊叧鑱?REQ 鐨?scope_scope 瀛楁 | regression |

## 33. Project Notes锛堥」鐩蹇橈級

> 瀵瑰簲 CR-20260813-001锛坴1.15.0锛夈€傝鐩栭」鐩粡楠屽蹇樼殑杩藉姞涓?AI 妫€娴嬪€欓€夊蹇樸€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| PN-001 | PM 璇?璁颁竴涓嬭繖涓粡楠? | 杩藉姞 project-notes 鏉＄洰 | positive |
| PN-002 | AI 妫€娴嬪埌鏂规硶璁?骞茬郴浜轰俊鍙?| 杈撳嚭鍊欓€夊蹇樺缓璁紝PM 纭鍚庡啓鍏?| positive |


## 34. Contract Scope锛堝悎鍚屼綔鐢ㄥ煙 RI锛?
> 瀵瑰簲 CR-20260813-002锛坴1.16.0锛夈€傝鐩栧悎鍚屼笌瀛愰」鐩瀵瑰鏄犲皠銆乧ontract-register 鍚堝悓鐧昏鍐屻€乻cope_level 褰掑睘锛坰upplement 璺熼殢鐖跺悎鍚岋級銆佸洓姝ユ绱㈣矾鐢便€佸悎鍚屽彉鏇磋仈鍔ㄤ笌 0.8.0 杩佺Щ銆傝璁″喅绛栬 governance/planning/contract-scope-ri-scheme.md锛圖1-D10锛夈€?
| Case ID | Input | Expected | Type |
|---|---|---|---|
| CS-001 | 椤圭洰闆?+ CON-001(portfolio锛岃鐩?PRJ-001+PRJ-002) | contract-register 鐧昏鎴愬姛锛汚TOM/Canonical 瀛?portfolio/requirements | positive |
| CS-002 | 闂?X 鍦ㄤ笉鍦ㄥ悎鍚? 鑼冨洿"锛坧ortfolio 鍚堝悓锛?| 璺敱 portfolio 绾?canonical锛涜繑鍥?scope_scope=in_contract + contract_refs={CON-001} + 璇佹嵁閾?| positive |
| CS-003 | 椤圭洰闆?3 鍚堝悓锛屾湭鎸囧畾鍚堝悓 | 鍒楀悎鍚屽€欓€夆啋閫夋嫨/鍏ㄦ绱⑩啋鎸夊悎鍚屾爣娉ㄥ悇 scope 缁撹 | positive |
| CS-004 | 鍦烘櫙 G锛氬瓙椤圭洰 A 琚?CON-001+CON-002 瑕嗙洊锛堜笉鍚屽缓璁惧唴瀹癸級 | 閫愬悎鍚屽垪缁撹锛坕n_contract(CON-001)+in_contract(CON-002)锛夛紝contract_refs 鏄惧紡鍙?ID锛屼笉娣锋穯 | regression |
| CS-005 | 鍗曢」鐩?2 鍚堝悓鍒嗘湡锛堝満鏅?H锛?| requirements/contract-register 鍖哄垎 CON-001/CON-002锛涜矾鐢辨纭紙涓嶅紩鍏?portfolio锛?| positive |
| CS-006 | Canonical evidence 璺?portfolio+瀛愰」鐩?| 褰?portfolio 绾э紝storage_level=portfolio锛宑ontract_refs 鍚弻鍚堝悓 | positive |
| CS-007 | 宸叉湁宸ヤ綔鍖哄崌绾у悗 contract-register 涓虹┖ | RI 鏌ヨ瑙﹀彂琛ュ綍寮曞锛堟渶灏忓瓧娈碉級锛屼笉杩斿洖閿欒缁撹 | negative |
| CS-008 | 琛ュ厖鍗忚鎵╁ぇ鑼冨洿 | 鏂板 ATOM(supplement)鈫掑綊骞垛啋scope 閲嶅垽鈫掔储寮曞埛鏂帮紙supplement 褰掔埗鍚堝悓灞傜骇锛?| regression |
| CS-009 | 鍚堝悓鎷嗗垎锛圕ON-001 鈫?CON-001a/CON-001b锛?| 鏃ф潯 status=superseded銆乻uperseded_by=鏂版潯锛汚TOM 褰掑睘杩佺Щ锛汣anonical 閲嶅垽 | regression |
| CS-010 | 瀛愰」鐩?A 鐨?CON-002 + 瀛愰」鐩?B 鐨?CON-003 瀵瑰悓涓€闇€姹傛湁璇佹嵁 | Canonical 褰?portfolio锛宻torage_level=portfolio | regression |
| CS-011 | RI-012 澶嶆牳锛欳anonical scope_scope 鍙樻洿 + contract_refs | contract_refs 闅?Canonical 鍙樻洿鍚屾鏇存柊 | regression |
| CS-012 | 0.8.0 杩佺Щ鍚?portfolio/requirements 楠ㄦ灦瀹屾暣 | canonical/atoms/contract-register/source-type-registry 榻愬叏涓旀牸寮忔纭?| positive |
| CS-013 | 椤圭洰闆?0.7.0鈫?.8.0 杩佺Щ锛圕R-001 閬楃暀淇锛?| 瀛愰」鐩骇 requirements/canonical+atoms+source-type-registry 鑷姩琛ラ綈 | positive |
| CS-014 | PM 璇?鏂扮浜嗕竴浠藉悎鍚? | 瑙﹀彂鍚堝悓鐧昏鎰忓浘鈫掕ˉ鍏?contract-register鈫掕矾鐢卞彲鏌?| positive |
| CS-015 | supplement of portfolio 绾х埗鍚堝悓锛圕ON-002 琛ュ厖 CON-001锛?| parent_contract_id 鍥炴函鈫抪ortfolio 绾?canonical鈫抜n_contract 鍚弻 ID | positive |
| CS-016 | 0.8.0 杩佺Щ sub_project_dirs/files 閬嶅巻 | 鍚?projects/*/requirements/{canonical,atoms}+source-type-registry 琛ラ綈锛涙棤 requirements/ 鐨勫瓙椤圭洰涓嶅己寤猴紙D10锛?| positive |
| CS-017 | 鍚堝悓鑼冨洿缂╁皬鍙樻洿 | 璧?08 鍙?scope 绫诲瀷锛堜笉鏂板鏋氫妇锛夛紱superseded 琛€缂樻洿鏂?| regression |


## 鍥炲綊鐢ㄤ緥缁熻

| 妯″潡 | 鐢ㄤ緥鏁?| 姝ｅ悜 | 鍥炲綊 |
|---|---|---|---|
| Quick Query | 11 | 8 | 3 |
| Daily Report | 8 | 5 | 3 |
| Weekly Report | 5 | 3 | 2 |
| PM Daily Todo | 3 | 2 | 1 |
| Output Artifact | 6 | 3 | 3 |
| Continuity | 4 | 3 | 1 |
| Todo Snapshot | 4 | 3 | 1 |
| File Rules | 6 | 0 | 6 |
| Self Check | 4 | 3 | 1 |
| Versioning | 4 | 0 | 4 |
| Resource Management | 3 | 1 | 2 |
| Excel Generation | 4 | 4 | 0 |
| Update Trigger | 4 | 3 | 1 |
| Skill Governance | 4 | 1 | 3 |
| Blueprint | 10 | 8 | 2 |
| Qoder Adaptation | 7 | 5 | 2 |
| Initialization Wizard | 5 | 4 | 1 |
| Information Completeness | 5 | 3 | 2 |
| Script Contract | 11 | 6 | 5 |
| SKILL Navigation | 7 | 2 | 5 |
| File Contract | 4 | 3 | 1 |
| Daily Report Rules | 4 | 3 | 1 |
| Query/Requirement/Artifact Rules | 4 | 3 | 1 |
| PM Profile | 10 | 7 | 3 |
| Historical Plan Import & Change Tracking | 17 | 11 | 6 |
| Pending Window (PW) | 6 | 3 | 3 |
| Change Log Archive (CLA) | 3 | 2 | 1 |
| Workspace Cleanliness (CL) | 4 | 3 | 1 |
| Cascade Propagation (CP) | 6 | 6 | 0 |
| Archive Governance (AG) | 6 | 6 | 0 |
| Workflow Data Path (WF) | 5 | 3 | 2 |
| Requirement Intelligence (RI) | 12 | 4 | 8 |
| Project Notes (PN) | 2 | 2 | 0 |
| Contract Scope (CS) | 17 | 10 | 7 |
| **鍚堣** | **215** | **136** | **79** |
