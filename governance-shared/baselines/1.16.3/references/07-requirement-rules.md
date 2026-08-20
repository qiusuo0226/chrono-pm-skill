# 闇€姹傜鐞嗙害鏉熻鍒?
鏈鍒欓€傜敤浜庨渶姹傜殑鏀堕泦銆佸垎绫汇€佹媶瑙ｃ€佽瘎瀹″拰杩借釜鐭╅樀缁存姢銆傞渶姹傚彉鏇寸鐞嗚 `08-change-control-rules.md`銆?
---

## 1. 闇€姹傚垎绫?
### 1.1 鎸夌被鍨嬪垎绫?
| 绫诲瀷 | 浠ｅ彿 | 璇存槑 |
|------|------|------|
| 鍔熻兘闇€姹?| FR | 绯荤粺蹇呴』瀹炵幇鐨勫姛鑳借涓?|
| 闈炲姛鑳介渶姹?| NFR | 鎬ц兘銆佸畨鍏ㄣ€佸彲鐢ㄦ€с€佸吋瀹规€х瓑 |
| 绾︽潫闇€姹?| CR | 鎶€鏈€夊瀷銆佸悎瑙勩€佹爣鍑嗙瓑寮哄埗绾︽潫 |
| 鎺ュ彛闇€姹?| IR | 涓庡閮ㄧ郴缁熺殑鎺ュ彛瀵规帴 |
| 鏁版嵁闇€姹?| DR | 鏁版嵁鏍煎紡銆佽縼绉汇€佹爣鍑?|

### 1.2 鎸変紭鍏堢骇鍒嗙被锛圡oSCoW锛?
| 浼樺厛绾?| 璇存槑 | 鍒ゅ畾鏍囧噯 |
|--------|------|----------|
| Must | 蹇呴』瀹炵幇 | 涓嶅疄鐜板垯绯荤粺鏃犳硶楠屾敹 |
| Should | 搴旇瀹炵幇 | 涓嶅疄鐜板奖鍝嶇敤鎴蜂綋楠?|
| Could | 鍙互瀹炵幇 | 鏈変环鍊间絾闈炴湰娆″繀椤?|
| Won't | 鏆備笉瀹炵幇 | 鏄庣‘鎺掗櫎鐨勮寖鍥?|

娉ㄦ剰锛氶渶姹備紭鍏堢骇锛圡oSCoW锛変唬琛ㄤ笟鍔′环鍊硷紝浠诲姟浼樺厛绾э紙P0-P3锛変唬琛ㄦ墽琛岀揣鎬ュ害锛屼袱鑰呬笉瀹屽叏绛夊悓銆備竴涓?Must 闇€姹傛媶鍑虹殑浠诲姟涓嶄竴瀹氶兘鏄?P0銆?
### 1.3 鎸夋潵婧愬垎绫?
| 鏉ユ簮 | 闇€瑕佺‘璁ょ殑浜嬮」 |
|------|----------------|
| 鍚堝悓/鎷涙爣鏂囦欢 | 閫愭潯鏍稿锛屼笉鍙仐婕忥紝鍏锋硶寰嬫晥鍔?|
| 闇€姹傝鏍艰鏄庝功 | 纭鏄惁宸茶瘎瀹￠€氳繃 |
| 鐢ㄦ埛鍙ｈ堪/浼氳 | 纭鏄惁鏈変功闈㈣褰曟垨绾 |
| 闅愬惈闇€姹?| 涓庡共绯讳汉纭鍚庣撼鍏?|

## 2. 闇€姹傜櫥璁板唽

`requirements/requirement-register.md` 鏄渶姹傜鐞嗙殑鏍稿績浜嬪疄婧愶紝鍚屾椂鎵胯浇闇€姹傛竻鍗曞拰杩借釜鐭╅樀銆?
### 2.1 瀛楁瀹氫箟

| 瀛楁 | 璇存槑 | 蹇呭～ |
|------|------|------|
| Req ID | REQ-[妯″潡浠ｅ彿]-NNN | 鏄?|
| 鏍囬 | 闇€姹傛爣棰?| 鏄?|
| 绫诲瀷 | FR / NFR / CR / IR / DR | 鏄?|
| 浼樺厛绾?| Must / Should / Could / Won't | 鏄?|
| 鏉ユ簮 | contract / document / meeting / implied | 鏄?|
| 鏉ユ簮寮曠敤 | 鍚堝悓鏉℃鍙锋垨鏂囨。绔犺妭 | 鏄?|
| 楠屾敹鏍囧噯 | 鍙獙璇佺殑楠屾敹鏉′欢 | 鏄?|
| 鍏宠仈浠诲姟 | Task ID 鍒楄〃 | 鍚︼紙鎷嗚В鍚庡～锛?|
| 鍏宠仈閲岀▼纰?| M-NN | 鍚?|
| 楠屾敹鐘舵€?| pending / in_progress / accepted / rejected | 鏄?|
| 鐘舵€?| proposed / confirmed / in_progress / delivered / accepted / changed / cancelled | 鏄?|
| 鍙樻洿璁板綍 | CR-YYYYMMDD-NNN | 鍚?|
| Source | 鏉ユ簮璇存槑 | 鏄?|

### 2.2 杩借釜鐭╅樀

杩借釜鐭╅樀鍐呭祵鍦ㄩ渶姹傜櫥璁板唽涓紝閫氳繃瀛楁鍏宠仈瀹炵幇鍏ㄩ摼璺拷婧細

```
鍚堝悓鏉℃ 鈫?闇€姹?REQ) 鈫?浠诲姟(T) 鈫?娴嬭瘯鐢ㄤ緥 鈫?楠屾敹
```

姣忔潯闇€姹傚繀椤昏兘杩芥函鍒版潵婧愶紙鍚堝悓鏉℃鎴栭渶姹傛枃妗ｏ級锛屽苟鑳藉悜涓嬭拷韪埌浠诲姟鍜岄獙鏀躲€?
## 3. 闇€姹傛媶瑙?
### 3.1 鎷嗚В灞傜骇

```
闇€姹傦紙Requirement锛?  鈹斺攢鈹€ Epic锛堜笟鍔″彶璇楋級
       鈹斺攢鈹€ Feature锛堝姛鑳界壒鎬э級
            鈹斺攢鈹€ Task锛堝紑鍙戜换鍔★級
```

### 3.2 鎷嗚В鍘熷垯

1. 姣忓眰鎷嗚В蹇呴』绗﹀悎 MECE 鍘熷垯锛堢浉浜掔嫭绔嬨€佸畬鍏ㄧ┓灏斤級銆?2. 鎷嗚В涓?Task 鏃跺繀椤绘弧瓒冲彲鍒嗛厤銆佸彲浼扮畻銆佸彲娴嬭瘯銆?3. 涓€涓渶姹傛媶瑙ｄ负澶氫釜浠诲姟鏃讹紝鎵€鏈変换鍔″繀椤诲叧鑱斿埌璇ラ渶姹?ID銆?4. 鎷嗚В鍚庡繀椤绘洿鏂伴渶姹傜櫥璁板唽鐨?鍏宠仈浠诲姟"瀛楁銆?
### 3.3 闇€姹傛弿杩拌鑼?
```markdown
### REQ-[妯″潡浠ｅ彿]-NNN锛歔闇€姹傛爣棰榏

**绫诲瀷**锛欶R
**浼樺厛绾?*锛歁ust
**鏉ユ簮**锛氬悎鍚岄檮浠? 绗?.1鏉?**楠屾敹鏍囧噯**锛?1. [鏉′欢1] 鏃讹紝绯荤粺搴?[琛屼负1]
2. [鏉′欢2] 鏃讹紝绯荤粺搴?[琛屼负2]
3. 寮傚父鎯呭喌锛歔寮傚父鍦烘櫙] 鏃讹紝绯荤粺搴?[寮傚父澶勭悊]

**鍏宠仈浠诲姟**锛?- T-YYYYMMDD-001
- T-YYYYMMDD-002

**鐘舵€?*锛歝onfirmed
```

## 4. 闇€姹傝瘎瀹?
### 4.1 璇勫妫€鏌ユ竻鍗?
| 妫€鏌ラ」 | 閫氳繃鏍囧噯 |
|--------|----------|
| 瀹屾暣鎬?| 瑙掕壊銆佸姛鑳姐€佺洰鐨勩€侀獙鏀舵爣鍑嗛綈鍏?|
| 娓呮櫚鎬?| 鏃犳涔夛紝鏃犱富瑙傚舰瀹硅瘝锛堝"蹇€?"鍙嬪ソ"锛?|
| 涓€鑷存€?| 涓庡叾浠栭渶姹傛棤鐭涚浘 |
| 鍙獙璇佹€?| 楠屾敹鏍囧噯鏄庣‘涓斿彲鎵ц |
| 鍙拷婧€?| 鍙拷婧埌鍚堝悓鏉℃鎴栭渶姹傛枃妗?|
| 鍙鎬?| 鏈夋妧鏈彲琛屾€у垎鏋?|
| 蹇呰鎬?| 涓庨」鐩洰鏍囩浉鍏筹紝闈為晙閲?|

### 4.2 璇勫缁撹

- **閫氳繃**锛氱撼鍏ュ熀绾匡紝鐘舵€佹敼涓?`confirmed`銆?- **鏈夋潯浠堕€氳繃**锛氬垪鍑哄緟琛ュ厖椤癸紝鐘舵€佷繚鎸?`proposed`銆?- **涓嶉€氳繃**锛氳鏄庡師鍥狅紝鐘舵€佹敼涓?`cancelled`銆?- **鏆傜紦**锛氳褰曞埌闇€姹傛睜锛岀姸鎬佷繚鎸?`proposed`锛屾爣娉ㄦ殏缂撳師鍥犮€?
## 5. 闇€姹備笌鍙樻洿鐨勮竟鐣?
1. 闇€姹傜櫥璁板唽鍙褰曞綋鍓嶆湁鏁堢殑闇€姹傜姸鎬併€?2. 浠讳綍鍙樻洿锛堟柊澧炪€佷慨鏀广€佸垹闄ゃ€佷紭鍏堢骇璋冩暣锛夊繀椤诲厛杩涘叆 `requirements/change-log.md`銆?3. 鍙樻洿鎵瑰噯鍚庢墠鑳芥洿鏂伴渶姹傜櫥璁板唽銆?4. 闇€姹傜櫥璁板唽涓殑"鍙樻洿璁板綍"瀛楁鍏宠仈鍒板搴旂殑 Change ID銆?
## 6. Change Log

闇€姹傜櫥璁板唽搴曢儴缁存姢 Change Log锛屾牸寮忓悓鍏朵粬浜嬪疄婧愩€侰hange Log 娲昏穬鍖轰笂闄?50 琛屾垨瓒呰繃 30 澶╂椂瑙﹀彂鎸夋湀褰掓。鍒?`change-log/archive/YYYYMM-change-log.md`锛屽苟缁存姢 `change-log/index.md` 鏈堜唤瀵艰埅锛堜笌 06/03 鍙峰綊妗ｈ鍒欎竴鑷达級銆?
## 7. 绾ц仈浼犳挱瑙勫垯

鏈疄浣擄紙Requirement锛夌姸鎬佸彉鏇存椂锛屾寜浠ヤ笅瑙勫垯瑙﹀彂涓嬫父鍔ㄤ綔銆傚姩浣滃垎涓夌被锛?- [AUTO] 鍐欐淳鐢熻鍥撅紙绱㈠紩锛夛紝浣庨闄╋紝鐩存帴鎵ц
- [CHECK] 鍙鏍￠獙锛屾鏌ュ叧鑱旀槸鍚﹀瓨鍦?涓€鑷?- [SUGGEST] 鍐欎簨瀹炴簮鎴栧奖鍝嶅叾浠栧疄浣擄紝鍔犲叆寤鸿鏇存柊娓呭崟寰?PM 纭

> **AUTO 浣滅敤鍩熷０鏄?*锛欰UTO 浠呬綔鐢ㄤ簬闈炰簨瀹炴簮鐨勬淳鐢熻鍥撅紝涓嶈Е纰颁换浣曚簨瀹炴簮鏂囦欢銆備簨瀹炴簮鍐欏叆锛堝惈 pending 鐧昏锛変竴寰嬪彈 `skill-contract.md` 绗?5 鏉＄害鏉熴€?
鎵ц椤哄簭锛氬厛 AUTO 鈫?鍐?CHECK 鈫?鏈€鍚?SUGGEST銆?鍚屼竴澶勭悊娴佺▼鍐咃紝绾ц仈鍔ㄤ綔鍙墽琛屼竴娆★紱澶氫釜 SUGGEST 姹囨€讳负鍚屼竴鎵瑰缓璁竻鍗曪紝娴佺▼鏈熬缁熶竴杈撳嚭銆?鎵ц瀹屾瘯鍚庯紝14 鍙疯嚜鏌ユ竻鍗曢獙璇佸畬鏁存€с€?
> **寮哄埗鎵ц瑕佹眰**锛堣 `00-pm-main-rules.md` 搂8a锛夛細浠ヤ笂 AUTO/CHECK/SUGGEST 鍔ㄤ綔涓嶅緱闈欓粯璺宠繃銆係UGGEST 蹇呴』鍛堢幇缁?PM 纭锛屼笉寰椾互"鐢ㄦ埛鏈姹?涓虹敱鐪佺暐銆傛祦绋嬫湯灏惧繀椤昏緭鍑?绾ц仈瀹屾暣鎬?缁撹銆?
Requirement 鐘舵€佸彉鏇?鈫?  [CHECK] 妫€鏌ュ叧鑱?task 鐨勭姸鎬佷竴鑷存€э紙杩借釜鐭╅樀锛?  [AUTO] 鏇存柊 requirement-register 琛嶇敓绱㈠紩

Requirement 浼樺厛绾у彉鏇?鈫?  [CHECK] 妫€鏌ュ叧鑱?task 鏄惁闇€瑕佽皟鏁翠紭鍏堢骇

## 8. 璺ㄦ簮闇€姹傚綊闆嗕笌鑼冨洿鍒ゅ畾锛圧I锛?CR-20260813-001)

褰撳悓涓€鎵归渶姹傚垎鏁ｅ湪**鍚堝悓銆佹嫑鎶曟爣銆佺珛椤广€佸瘑璇?绛変繚銆侀噷绋嬬**绛夊鏉ユ簮鏂囨。鏃讹紝鐢ㄤ笁灞傛暟鎹ā鍨嬫妸"闇€姹傚湪涓嶅湪鏌愯寖鍥?浠庢壇鐨彉鎴?*鍙彇璇?*銆傛湰鑳藉姏鍦?搂1.3 鏉ユ簮鍒嗙被涓?搂2 杩借釜鐭╅樀涔嬩笂鎵╁睍锛屼笉鏀瑰彉鏃㈡湁 REQ 灞傚瓧娈点€?
### 8.1 涓夊眰鏁版嵁妯″瀷

```
婧愭枃妗ｏ紙浠绘剰 source_type锛?  鈫?ATOM锛堣瘉鎹眰锛屽彧璇伙級鈫?Canonical锛堝綊骞跺眰锛夆啋 REQ锛堢鐞嗗眰锛岀櫥璁板唽锛?```

| 灞?| 瀹炰綋 | 璇存槑 |
|----|------|------|
| 璇佹嵁灞?| ATOM | 浠庢簮鏂囨。鏉℃鎻愬彇鐨勫師瀛愪簨瀹烇紝鍙涓嶅彲鏀瑰啓锛沗raw_text` 瀛樻潯娆惧師鏂囷紙鈮?00 瀛楋級锛屽師濮嬫枃妗ｄ笉鍏ュ簱鍙瓨鎸囬拡锛堟枃妗ｅ悕+鐗堟湰+鏉℃鍙凤級 |
| 褰掑苟灞?| Canonical | 璺ㄦ簮璇箟褰掑苟鍚庣殑瑙勮寖闇€姹傦紝鍚?evidence 璇佹嵁閾?+ scope_scope 鍒ゅ畾锛沗Canonical 1:N ATOM` |
| 绠＄悊灞?| REQ | 鐜版湁鐧昏鍐屾潯鐩紱榛樿 `REQ 1:1 Canonical`锛屽浜や粯闇€姹傛椂鍏佽澶?REQ 浠?`canonical_id` 鍥炴寚鍚屼竴 Canonical |

`Canonical 1:N ATOM`锛沗REQ 1:1 Canonical`锛堥粯璁わ級+ `Canonical 1:N REQ`锛坈anonical_id 鍥炴寚锛夈€俁EQ 鐨?`鏉ユ簮/Source` 瀛楁鍗囩骇涓烘寚鍚?Canonical ID 鐨勬寚閽堬紙鏃у伐浣滃尯浠嶄负鑷敱鏂囨湰锛屽悜鍚庡吋瀹癸級銆?
### 8.2 鍙屽眰鏉ユ簮鍒嗙被

| 灞?| 瀛楁 | 绮掑害 | 鍙栧€?|
|----|------|------|------|
| REQ锛堢幇鏈夛級 | `鏉ユ簮` | 绮?| contract / document / meeting / implied锛埪?.3锛屼笉鍙橈級 |
| ATOM锛堟柊澧烇級 | `source_type` | 缁?| 瑙?`requirements/source-type-registry.md` |

source_type 椤圭洰绾у彲鎵╁睍锛涙瘡鏉″繀椤诲綊鍏?`source_type鈫抯ource_category`锛坈ontractual/procurement/approval/compliance/technical/operational锛屽浐瀹?6 绫伙級锛岀户鎵块粯璁?authority銆傛湭鐭?source_type 瑙﹀彂"鏈櫥璁?鎻愮ず锛屼笉闈欓粯褰掔被銆?
### 8.3 鏉ユ簮鏉冨▉灞傜骇涓庨粯璁ゅ€?
| authority | 灞傜骇 | 鏉ユ簮绫诲埆榛樿 |
|---|---|---|
| L1 | 鍚堝悓/鍗忚 | contractual |
| L2 | 鎷涙姇鏍?鎶曟爣鎵胯 | procurement |
| L3 | 绔嬮」/鎶€鏈熀绾?| approval銆乼echnical锛堝熀绾垮寲鍚庯級 |
| L4 | 鍚堣寮哄埗 | compliance锛堝瘑璇?绛変繚锛?|
| L5 | 宸ユ湡/閲岀▼纰?| operational锛堝伐鏈?閲岀▼纰戞潯娆鹃粯璁?L5锛屽叾浣欓粯璁?L3锛?|

### 8.4 ATOM 瀛楁

```
ATOM_ID         : ATOM-<source_type>-NNN
kind            : requirement / requirement_directive / agreement / constraint
source_doc      : 鏂囨。鍚?source_version  : 婧愭枃妗ｇ増鏈彿锛坰tale 妫€娴嬪熀鍑嗭級
source_ref      : 鏉℃鍙?/ 绔犺妭 / 椤电爜
source_type     : registry 缁嗙矑搴︾被鍨?source_category : 6 绫讳箣涓€
authority       : L1~L5锛堢敱 source_category 榛樿鎺ㄦ柇锛屽彲瑕嗙洊锛?raw_text        : 鏉℃绾у師鏂囷紙鈮?00 瀛楋紝瓒呴暱鎷嗗垎涓哄鏉★紝鐢?supersedes 鏍囪琛€缂橈級
supersedes      : 闀挎潯娆炬媶鍒嗘椂鎸囧悜鍚屼竴鏉℃鎷嗗垎鍓?鍚?ATOM_ID锛堥敋瀹氭媶鍒嗚缂橈級
norm_text       : 璇箟褰掍竴鍚庣殑鏍囧噯琛ㄨ堪锛圓I 鐢熸垚锛宑onfidence 璁板綍锛屼汉宸ョ‘璁わ級
keywords        : 鎷嗚瘝鍥涘厓缁?[瀵硅薄][鍔ㄤ綔][绾︽潫][鎸囨爣]
confidence      : AI 褰掍竴/鍖归厤缃俊搴?milestone       : 鍏宠仈閲岀▼纰?M-NN锛堣嫢鏈夛級
hash            : 闃茬鏀规憳瑕?updated         : 鏃堕棿鎴?```

> scope_scope 鏄?*璺ㄦ簮鑱氬悎缁撹**锛屽彧灞?Canonical 灞傦紱鍗曚釜 ATOM 鐢?authority + source_category 琛ㄨ揪鍗曟潯璇佹嵁鏁堝姏锛屼笉璁?scope_scope銆?
### 8.5 Canonical 瀛楁

```
CAN_ID          : CAN-NNN
evidence        : ATOM_ID 璇佹嵁閾撅紙1:N锛? 鍚勮嚜 source_type/authority
scope_scope     : in_contract / in_bid_only / in_initiation_only / not_in_scope / conflict
consistency     : consistent / conflict锛堟潵婧愪簰鏂ヨ浆浜哄伐瑁佸喅锛屾部鐢?pending鈫抍onfirmed锛?milestone       : 鍏宠仈閲岀▼纰戙€佸悎瑙勯棬绂?status          : active / evidence_stale
```

**scope_scope 涓庝紭鍏堢骇瑙ｈ€?*锛歚scope_scope`锛堣寖鍥村綊灞烇級涓?搂1.2 `浼樺厛绾锛圡oSCoW锛夋槸**涓や釜鐙珛缁村害**銆備緥锛歚scope_scope=in_contract` + `浼樺厛绾?Won't`锛堝悎鍚屾湁浣嗗弻鏂瑰悓鎰忔殏涓嶅仛锛夛紱`scope_scope=in_initiation_only` + `浼樺厛绾?Must`锛堢珛椤硅姹備絾鍚堝悓鏈鐩栵紝闇€浼樺厛鎺ㄥ姩绾冲叆锛夈€傜櫥璁板唽涓綔涓轰袱鍒楃嫭绔嬪憟鐜般€?
### 8.6 鎻愬彇涓庡綊骞舵祦绋?
1. **瑙﹀彂**锛欰) PM 涓诲姩鎻愪緵婧愭枃妗ｅ苟瑕佹眰鎻愬彇/鎷嗚В锛汢) 鍒濆鍖栧悜瀵?Step1 鍚堝悓灞傚悓姝ユ彁鍙栵紱C) 婧愭枃妗ｅ嚭鏂扮増鏈紙琛ュ厖鍗忚/琛ラ仐锛夋椂澧為噺鎻愬彇 + 婧愮増鏈?stale 鍒ゅ畾銆?2. **鎷嗚瘝褰掍竴**锛氭寜 ES 鍒嗘瀽閾撅紝AI 鍘熷瓙鍖栧垏鍧?鈫?17 鍙疯涔夊綊涓€鐢熸垚 norm_text锛堟湳璇骇璧拌瘝搴撶姸鎬佹満锛屽彞瀛愮骇 confidence 璁颁簬 ATOM銆佷汉宸ョ‘璁わ級銆?3. **褰掑苟**锛氬熀浜?norm_text + keywords 鍙岃矾鍖归厤锛屽懡涓凡鏈?Canonical 鍒欒拷鍔?evidence锛涙湭鍛戒腑鍒欐柊寤?Canonical锛涘綊骞?鏂板缓缁撴灉椤?PM 纭銆?4. **鑼冨洿鍒ゅ畾**锛欳anonical 鑱氬悎 all evidence 鍒ゅ畾 scope_scope锛涙潵婧愪簰鏂ユ爣 conflict 杞汉宸ヨ鍐筹紱瀵嗚瘎绛?compliance 绫诲甫寮哄埗闂ㄧ锛堜笉杩囧瘑璇勪笉寰楄繘鍏ラ獙鏀讹級銆?5. **绱㈠紩**锛氭洿鏂板搴旂被鍒?L1/L2 绱㈠紩涓?ATOM 鍏ㄦ枃锛堣 05 鍙蜂笁绾х储寮曪級锛涗换浣曞け璐ユ暣浣撳洖閫€骞舵爣璁?stale銆?
### 8.7 绾ц仈浼犳挱瑙勫垯锛圧I 鎵╁睍锛?
ATOM 褰掑苟/鍙樻洿 鈫?  [AUTO] 鏇存柊 canonical evidence 閾?+ L1/L2 绱㈠紩锛堟淳鐢熻鍥撅級
  [CHECK] 鏍￠獙 source_version 涓庣储寮?last_source_version 涓€鑷存€?  [SUGGEST] 鏂?Canonical 鎴?scope 鍒ゅ畾缁撴灉 鈫?寰?PM 纭锛沞vidence 鍏?stale 鈫?鎻愮ず閲嶆柊璇勪及

### 8.8 Project Notes 闅忕瑪鍑嗗垯 (CR-20260813-001)

PM 鏂规硶璁恒€佸共绯讳汉娌熼€氬蹇樸€侀」鐩礊瀵熴€佷氦浠樼瓥鐣ョ瓑**浣庣粨鏋勫寲銆佽拷鍔犲紡**鍐呭锛岀粺涓€瀛樺叆 `ai/projects/{瀛愰」鐩畗/context/project-notes.md`锛堥」鐩泦涓?`ai/portfolio/context/project-notes.md`锛夈€?*鍙拷鍔?*锛屼笉淇敼鍘嗗彶鏉＄洰銆?
姣忔潯鏍煎紡锛歚- YYYY-MM-DD [#鏍囩] 鍐呭锛堟潵婧愶細PM涓诲姩/AI鎰熺煡-<淇″彿>锛塦

鏍囩锛歚#鏂规硶璁篳 `#骞茬郴浜篳 `#娲炲療` `#绛栫暐` `#椋庨櫓鐩磋`

**鍙屽叆鍙?*锛?1. PM 涓诲姩瑕佹眰锛?璁颁竴涓?澶囧繕/杩欎釜缁忛獙璁颁笅"锛夆啋 鐩存帴杩藉姞銆?2. AI 涓诲姩鎰熺煡锛堜豢 17 鍙?搂8.1 鑷姩鍙戠幇 + pending鈫抍onfirmed锛夛細瀵硅瘽鍛戒腑鏂规硶璁?骞茬郴浜?娲炲療/绛栫暐淇″彿 鈫?闄勫姞"馃挕 妫€娴嬪埌 N 鏉″€欓€夊蹇橈紝鏄惁璁板叆 project-notes锛? 鈫?PM 纭鍐欏叆銆佸惁瀹氫笉璁板綍銆佷笉闃诲涓讳綋浠诲姟銆?
**鏇存柊鏉冮檺**锛歱roject-notes 涓轰綆缁撴瀯鍖栬拷鍔犲紡璁板綍锛屽睘**浣?涓闄╂洿鏂?*锛坧roactive 妯″紡鍙洿鎺ヨ拷鍔犲苟鏍?`Confirmed By: 寰呯‘璁锛屼笌 AI 鎰熺煡"寤鸿淇濆瓨鈫掔‘璁?涓€鑷达級锛屼笉娑夊強浜嬪疄婧愮姸鎬佸彉鏇淬€?
**涓庢棦鏈夋枃浠惰竟鐣?*锛歚project-context`=缁撴瀯鍖栬儗鏅紱`decision-log`=姝ｅ紡鍐崇瓥锛沗lessons-learned`=澶嶇洏浜у嚭锛沗project-notes`=闈炴寮忛殢绗?澶囧繕銆?
**褰掓。**锛歱roject-notes 瓒呰繃 100 鏉℃垨 6 涓湀鏃讹紝鎸夊搴﹀綊妗ｅ埌 `context/project-notes-archive/`锛堟部鐢?06 鍙峰綊妗ｈ鍒欙級銆?
### 8.9 鍚堝悓浣滅敤鍩熶笌妫€绱㈣矾鐢憋紙CR-20260813-002锛?
RI 鑼冨洿鍒ゅ畾闅愬惈"鍚堝悓鈫斿瓙椤圭洰 1:1"鍋囪锛屼絾鐜板疄涓负**澶氬澶?*锛堣仈鍚堜綋鍚堝悓銆佽法瀛愰」鐩悎鍚屻€佷富鍚堝悓+澶氳ˉ鍏呭崗璁€佸悓涓€瀛愰」鐩澶氫唤鍚堝悓瑕嗙洊绛夛級銆傛湰灏忚妭琛ラ綈璇ョ己鍙ｏ細contract-register 浣滀负鍚堝悓浣滅敤鍩熸槧灏勪簨瀹炴簮锛屽畾涔?ATOM/Canonical 鐨勫瓨鍌ㄥ綊灞炪€佸甫鍚堝悓缁村害鐨?scope 鍒ゅ畾涓庢绱㈣矾鐢便€?
#### 8.9.1 contract-register.md 鍚堝悓鐧昏鍐岋紙鍞竴鏄犲皠浜嬪疄婧愶級

**浣嶇疆**锛氶」鐩泦妯″紡鍞竴鐧昏鍐屽湪 `portfolio/requirements/contract-register.md`锛圖4锛屽瓙椤圭洰涓嶅鍒讹級锛涘崟椤圭洰妯″紡鍦?`requirements/contract-register.md`锛圖3锛夈€傛墍鏈変富鍚堝悓涓庤ˉ鍏呭崗璁粺涓€鐧昏銆?
**瀛楁**锛?
| 瀛楁 | 蹇呭～ | 璇存槑 |
|---|---|---|
| Contract ID | 鏄?| CON-NNN |
| 鍚堝悓鍚嶇О | 鏄?| 鍚堝悓鍏ㄧО |
| 鍚堝悓绫诲瀷 | 鏄?| 涓诲悎鍚?/ 琛ュ厖鍗忚 / 鍒嗗寘鍚堝悓 绛?|
| scope_level | 鏄?| `portfolio`锛堣法瀛愰」鐩?鏁翠綋锛? `project`锛堝崟涓瓙椤圭洰鎴栧崟椤圭洰鏁翠綋锛? `supplement`锛堣ˉ鍏呭崗璁級 |
| parent_contract_id | 琛ュ厖鍗忚蹇呭～ | 鎸囧悜琚ˉ鍏呭悎鍚?CON-NNN锛圖7锛夛紱涓诲悎鍚屽～銆?銆?|
| coverage 瑕嗙洊瀵硅薄 | 鏄?| 鍙楁鍚堝悓绾︽潫鐨?PRJ-NNN 鍒楄〃锛堟垨鍗曢」鐩暣浣擄級 |
| 鍏宠仈鎷涙姇鏍?| 鍚?| 鎴愬鏂囨。绨囷細BID-NNN |
| 鍏宠仈绔嬮」 | 鍚?| INIT-NNN |
| 鍏宠仈瀵嗚瘎 | 鍚?| COMP-NNN |
| status | 鏄?| active / superseded |
| superseded_by | 鍚?| 鍚堝悓鎷嗗垎/鏇夸唬鏃剁殑琛€缂橈紙D8锛?|
| Source | 鏄?| 鏉ユ簮鍚堝悓/鏂囨。 |

> 鎾板啓閬靛惊 SKILL.md 搴曠嚎 #2锛堝緟纭 + pending-changes锛夛紱鍐欏叆璧颁富鍔ㄥ彉鏇存ā寮忔爣璁?`Confirmed By: 寰呯‘璁銆?
**鏂囨。绨囧叧鑱旓紙N5锛?*锛氭嫑鎶曟爣/绔嬮」/瀵嗚瘎绛夋枃妗ｄ笌鍚堝悓鎴愬鍑虹幇銆傞€氳繃 contract-register 鐨勫叧鑱斿瓧娈靛舰鎴愭枃妗ｇ皣锛歚CON-NNN锛堝悎鍚岋級鈫?BID-NNN锛堟嫑鏍囨枃浠讹級鈫?INIT-NNN锛堢珛椤规壒澶嶏級鈫?COMP-NNN锛堝瘑璇勬姤鍛婏級`銆傛绱?鏌?PDF 瑕佹眰 X 鍦ㄤ笉鍦ㄥ悎鍚岃寖鍥?鏃讹紝鍏堢粡鏂囨。绨囧畾浣嶅搴斿悎鍚岋紝鍐嶈蛋 搂8.9.3 璺敱銆?
#### 8.9.2 ATOM/Canonical 瀛樺偍褰掑睘锛圖2/D3/D7锛?
| 鍚堝悓 scope_level | ATOM 瀛樺湪鍝?| Canonical 瀛樺湪鍝?|
|---|---|---|
| `portfolio`锛堣法瀛愰」鐩級 | `portfolio/requirements/atoms/` | `portfolio/requirements/canonical/` |
| `project`锛堝崟瀛愰」鐩垨鍗曢」鐩級 | `projects/{瀛愰」鐩畗/requirements/atoms/`锛堝崟椤圭洰 `requirements/atoms/`锛?| `projects/{瀛愰」鐩畗/requirements/canonical/`锛堝崟椤圭洰 `requirements/canonical/`锛?|
| `supplement`锛堣ˉ鍏呭崗璁級 | **璺熼殢鐖跺悎鍚?scope_level**锛圖7锛?| **璺熼殢鐖跺悎鍚?scope_level**锛圖7锛?|

**Canonical storage_level 鍒ゅ畾锛圖2锛?*锛欳anonical 鏄法婧愬綊骞朵骇鐗╋紝鍏跺綊灞炵敱 evidence 鐨勫眰绾у喅瀹氾細
- evidence 鍏ㄩ儴鏉ヨ嚜鍚屽眰绾у悎鍚?鈫?褰掕灞傜骇锛?- evidence 璺?`portfolio`/`project` 鎴栧瀛愰」鐩?鈫?褰?portfolio 绾э紝`storage_level=portfolio`锛?- 鍗曢」鐩?multi-鍚堝悓锛堝満鏅?D/H锛変笉寮曞叆 portfolio 鐩綍锛孋anonical 褰?`requirements/canonical/`锛岀敤 `contract_refs` 鍖哄垎鍚堝悓銆?
**contract_refs 浼撮殢瀛楁锛圖1锛?*锛欳anonical 灞傛柊澧?`contract_refs`锛堝叧鑱斿悎鍚?ID 鍒楄〃锛夛紝琛ㄨ揪"鍦ㄥ摢浜涘悎鍚岃寖鍥村唴"銆俿cope_scope 淇濇寔鏃㈡湁 5 鍊兼灇涓句笉鍙橈紙鍚戝悗鍏煎锛夛紝`contract_refs` 涓轰即闅忓瓧娈点€傛棫 Canonical 鏃犺瀛楁 鈫?瑙嗕负"鏈叧鑱斿悎鍚?闄嶇骇鏍囨敞锛屼笉鎶ラ敊銆?
#### 8.9.3 妫€绱㈣矾鐢憋紙閰嶅悎 05 鍙?搂Quick Query锛?
```
Step 0  璇?contract-register锛堢┖ 鈫?瑙﹀彂琛ュ綍寮曞锛屾渶灏忓瓧娈碉細ID/鍚嶇О/scope_level/瑕嗙洊/status锛?Step 1  瑙ｆ瀽鍚堝悓鎸囧悜
        鈹溾攢 鎸囧畾鍚堝悓锛圕ON-XXX/鍚嶇О锛夆啋
        鈹?    scope_level=portfolio   鈫?鏌?portfolio/requirements/canonical
        鈹?    scope_level=project     鈫?鏌ュ搴斿瓙椤圭洰 canonical
        鈹?    scope_level=supplement  鈫?缁?parent_contract_id 鍥炴函鐖跺悎鍚?scope_level 鈫?鎸夌埗鍚堝悓灞傜骇璺敱锛圖7锛?        鈹溾攢 鏈寚瀹?鈫?鍒楀悎鍚屽€欓€変緵閫夋嫨锛涙垨"鍏ㄩ儴鑼冨洿"鈫?閫愬悎鍚屾绱㈠悎骞?        鈹斺攢 鐧昏鍐岀┖/鏃犲尮閰?鈫?鎻愮ず琛ュ綍锛屼笉鑷嗛€狅紙D5锛?Step 2  鐩爣 canonical 璧?L1鈫扡2鈫扡3 涓夌骇绱㈠紩锛堝崟娆?200-400 琛屾渶灏忚鍙栵紝05 鍙凤級
Step 3  杈撳嚭 scope_scope(result) + contract_refs + 璇佹嵁閾?        鍦烘櫙 G 澶氬悎鍚岃鐩?鈫?閫愬悎鍚屽垪缁撹
        scope_level=supplement 鈫?contract_refs 鍚?supplement 涓庣埗鍚堝悓鍙?ID
```

#### 8.9.4 鍚堝悓鍙樻洿涓夌骇鑱斿姩锛圢14锛孌8锛屽紩鐢?08 鍙凤級

| 绫诲埆 | ATOM | Canonical | contract-register | 08 鍙峰彉鏇寸被鍨?|
|---|---|---|---|---|
| 鍚堝悓鑼冨洿鎵╁ぇ锛堝惈琛ュ厖鍗忚锛?| 澧為噺鎻愬彇鏂板 ATOM(supplement) | 鏂?ATOM 褰掑苟锛宻cope 閲嶅垽 | 琛ュ厖鍗忚鐧昏锛坧arent_contract_id锛?| `scope` + `requirement` |
| 鍚堝悓鎷嗗垎涓轰袱浠?| 鍘?ATOM 鎸夋柊鍚堝悓褰掑睘杩佺Щ | 鐩稿叧 Canonical 閲嶅垽 | 鏃ф潯 status=superseded銆乻uperseded_by=鏂版潯锛涙柊澧?2 鏉?| `scope` + `cost` |
| 鍚堝悓鑼冨洿缂╁皬 | 鐩稿叧 ATOM 鏍?stale/鍓旈櫎 | 鍘?in_contract 鐨?Canonical 鍙兘鍙?not_in_scope | 缁存姢 status/琛€缂?| `scope` |

> 鍚堝悓鑼冨洿鍙樻洿**涓嶄慨鏀?08 鍙锋蹇靛煙 B 鏋氫妇**锛堜笉鏂板 `contract_scope`锛夛紝澶嶇敤鏃㈡湁 `scope`/`cost`/`requirement` 绫诲瀷锛圖8锛夈€傜骇鑱旀墽琛岄『搴忛伒寰?搂8.7锛圓UTO鈫扖HECK鈫扴UGGEST锛夛紝浜嬪疄婧愬啓鍏ュ緟 PM 纭銆?>
> **contract_refs 鍚屾锛圕S-011/RI-012 澶嶆牳鍙ｅ緞锛?*锛欳anonical 鐨?scope_scope 閲嶅垽鏃讹紝`contract_refs` 蹇呴』鍚屾鏇存柊鈥斺€斿悎鍚屾墿澶?琛ュ厖鍗忚鏃跺湪 contract_refs 杩藉姞锛堝惈 supplement 涓庣埗鍚堝悓鍙?ID锛夛紱鍚堝悓鎷嗗垎鏃舵棫 Canonical 鐨?contract_refs 鏀规寚鍚戞柊鍚堝悓銆佹棫鍚堝悓鏉＄洰杩涘叆琛€缂橈紱鍚堝悓缂╁皬绉婚櫎瀵瑰簲鍚堝悓 ID锛涙棫 Canonical 鏃?contract_refs 鏃舵寜"鏈叧鑱斿悎鍚?澶勭悊锛圖1锛夈€?
