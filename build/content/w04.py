# 4주차 · 분류와 회귀 — 데이터에 말 걸기
import os
_H = os.path.dirname(__file__)
_DATA = open(os.path.join(_H, '..', 'data_w04.js'), encoding='utf-8').read() + open(os.path.join(_H, '..', 'data_ai4i.js'), encoding='utf-8').read()

COLAB = '''#1. 분석 환경 : colab
#2. 파일 업로드 방식 : Colab으로 csv파일 업로드
#3. 분석모델 : 분류모델(이상탐지 모델)
#4. 변수
타겟변수 : nomal_abnormal
Input변수 : with_mm, surface_roughness_um, UT_dB, oven_temp_c
#5 훈련데이터 80% 테스트데이터 20%
#6 훈련데이터, 테스트데이터의 target 변수의 비율을 일치
#7 교차검증(5개)
#8 알고리즘은 분류모델로 4개이상
#9 출력
1. Confusion Matrix
2. 모델별 정확도 테이블'''

CLS = '''당신은 같은 품질 분석가로 일한다. 입력은 한 부품의 다섯 환경 측정값이다.
아래 출력 형식을 따른다.

[입력 — 다섯 개]
- air_temp_k (공기 온도, K)
- process_temp_k (공정 온도, K)
- rotational_speed_rpm (회전수, rpm)
- torque_nm (토크, Nm)
- tool_wear_min (도구 누적 가동 시간, 분)

[출력 — JSON 한 줄]
{"machine_failure": 0 또는 1, "predicted_failure_mode": "twf" | "hdf" | "pwf" | "osf" | "rnf" | null, "confidence": 0.0 ~ 1.0, "rationale": "한 줄 이유 (한국어)"}

rules:
- machine_failure가 0이면 predicted_failure_mode는 null이다.
- machine_failure가 1이면 predicted_failure_mode는 정확히 하나다.
- confidence는 모델 자신의 확신 정도다 (0.0~1.0).
- rationale은 한 줄, 30자 내외.

[예시 01 — 정상]
air 300.1 · process 309.5 · rotation 1520 · torque 36.0 · wear 130
→ {"machine_failure": 0, "predicted_failure_mode": null, "confidence": 0.91, "rationale": "다섯 입력 모두 정상 부근"}

[예시 02 — 이상 (도구 마모)]
air 300.4 · process 310.0 · rotation 1530 · torque 39.0 · wear 232
→ {"machine_failure": 1, "predicted_failure_mode": "twf", "confidence": 0.86, "rationale": "마모 232분 — 임계 초과"}'''

REG = '''당신은 같은 마모 추정가로 일한다. 입력은 한 부품의 다섯 환경 측정값이다.
아래 출력 형식을 따른다.

[출력 — JSON 한 줄]
{"estimated_wear": 0.0 ~ 1.0, "rationale": "한 줄 이유 (한국어)"}

rules:
- estimated_wear는 0.0~1.0 사이의 숫자다.
- rationale은 한 줄, 30자 내외.

좋은 분리는 두 구간이다 —
- 정상 부근 (0.0~0.40)
- 위험 부근 (0.70~1.00)

[예시 01 — 정상 부근]
air 300.1 · process 309.5 · rotation 1520 · torque 36.0 · wear 80
→ {"estimated_wear": 0.21, "rationale": "마모 80분 — 정상 부근"}

[예시 02 — 위험 부근]
air 304.0 · process 312.1 · rotation 1620 · torque 40.0 · wear 220
→ {"estimated_wear": 0.78, "rationale": "마모 220분 — 위험 임계"}'''

CH = {
 'slug': 'w04', 'num': '04',
 'title': '분류와 회귀 — 데이터에 말 걸기',
 'eyebrow': '4주차 · SECTION 2 · 데이터 · 금속 판재 경화·검사 라인',
 'desc': '스마트 제조 4주차 — 정상인가(분류)와 얼마나 더 쓰나(회귀)를 비유로 익히고, AI4I 2024 데이터로 QWEN 프롬프트 카드를 만들며, 불량품 판정 데이터 1,000개로 판정 기준을 직접 찾습니다.',
 'q': '"이 부품은 정상인가?"와 "얼마나 더 쓸 수 있나?"는 왜 다른 모델이 답할까?',
 'lead': '공장은 매일 두 가지를 묻습니다. 정상인가 아닌가(라벨), 그리고 얼마나 더 쓸 수 있나(숫자). 질문의 모양이 모델을 정합니다. 오늘은 판재 검사 라인과 CNC 데이터로 두 질문에 말을 겁니다.',
 'scene_alt': '금속 판재 경화·재단·검사 라인 3D. 경화 오븐, 폭 300mm 재단기, 표면 거칠기·초음파·폭 측정 게이트를 지난 판재가 정상 상자와 불량 상자로 갈라진다. 버튼으로 판정 기준을 하나만 켤 수 있다.',
 'scene_hud': '3D · 판재 검사 라인 — 오른쪽 아래 버튼으로 판정 기준을 바꿔 보세요',
 'scene_opts': {'cam': [3, 14, 24], 'target': [0, 1.5, 0]},
 'kpis': [('2가지', '질문의 모양: 라벨(분류) · 숫자(회귀)', 'm'), ('1,000개', '불량품 판정 데이터 (불량 100)', 'a'), ('3개', '데이터가 알려 준 판정 기준', 'g'), ('90%', '"모두 정상"이라고만 해도 나오는 정확도', 'r')],
 'hero_talk': [
   ('doc', 'e07', '오늘은 판재 검사 라인입니다. 네 가지 센서 값으로 불량을 가릅니다. 그런데 무슨 기준으로 가르는지, 아무도 적어 두지 않았습니다.'),
   ('robo', 'e16', 'AI에게 맡기면 정확도 97%! 끝!'),
   ('fly', 'e09', '어떤 기준으로 골랐는지 모르면 현장에서 못 써. 기준을 데이터에서 꺼내 보자.'),
   ('sia', 'e07', '두 질문을 먼저 나누는 것부터 순서대로 하겠습니다.'),
 ],
 'three': ['"정상인가"에는 분류가, "얼마나 더 쓰나"에는 회귀가 답합니다. 같은 데이터에서도 질문 모양에 따라 모델과 출력이 바뀝니다.',
           '분류는 정확도 하나로 보면 속습니다. 놓친 불량(FN)과 과잉 경보(FP)의 비용이 다르기 때문입니다.',
           'QWEN에 보낼 분류·회귀 프롬프트 카드와, 판정 기준을 데이터에서 뽑아내는 Colab 프롬프트를 만듭니다.'],
 'abbr': [('TP/TN', 'True Positive / True Negative', '참 양성(이상을 이상으로) / 참 음성(정상을 정상으로)'), ('FP/FN', 'False Positive / False Negative', '거짓 양성(과잉 경보) / 거짓 음성(놓침)'),
          ('UT', 'Ultrasonic Testing', '초음파 탐상 — 내부 결함을 소리 반사로 본다'), ('AI4I', 'AI4I 2020/2024 Predictive Maintenance', 'UCI 예지보전 공개 데이터 — 가공기 고장 예측'),
          ('JSON', 'JavaScript Object Notation', '{"키": 값} 모양의 기계가 읽기 쉬운 출력 형식'), ('CV', 'Cross Validation', '교차검증 — 학습 데이터를 여러 번 나눠 돌려 평가')],
 'why': [('질문 모양이 모델을 정한다', '정상/이상 같은 라벨은 분류, 마모량·수명 같은 숫자는 회귀입니다. 이걸 섞으면 "68.4"라는 답이 정상인지 아닌지 알 수 없습니다.'),
         ('기준이 보여야 쓴다', 'AI가 불량을 잘 골라도 기준을 모르면 작업자가 따를 수 없고, 고객에게 설명할 수 없습니다.'),
         ('정확도의 함정', '불량이 10%뿐인 데이터에서 "모두 정상"은 정확도 90%입니다. 놓친 불량 비용을 같이 봐야 합니다.')],
 'big_lead': '이번 주는 네 단계로 갑니다.',
 'big': [('① 비유', '의사결정 나무(분류) · 안전벨트(회귀) · 건강검진의 두 종류'), ('② 라우팅', '라벨인가 숫자인가 → 분류인가 회귀인가'),
         ('③ 프롬프트 카드', 'AI4I 2024 · 역할 · 출력 형식(JSON) · few-shot 예시'), ('④ 기준 도출', '불량품 판정 데이터 → Colab 분류 모델 → 판정 기준표')],
 'glossary': {
   '분류': ['분류', '모델', '입력을 보고 정해진 라벨(정상/이상, 등급) 중 하나를 고르는 모델입니다.'],
   '회귀': ['회귀', '모델', '입력을 보고 숫자(마모량, 수명, 온도)를 추정하는 모델입니다.'],
   '결정 경계': ['결정 경계', '개념', '분류 모델이 정상 영역과 이상 영역을 가르는 선입니다.'],
   '잔차': ['잔차', '개념', '실제 값 − 회귀가 추정한 값입니다. 회귀는 잔차를 작게 만드는 선을 찾습니다.'],
   '재현율': ['재현율', '지표', '실제 불량 중 모델이 잡아낸 비율입니다. 놓침(FN)이 비싼 곳에서 중요합니다.'],
   '정밀도': ['정밀도', '지표', '모델이 불량이라고 한 것 중 진짜 불량의 비율입니다. 과잉 경보(FP)가 비싼 곳에서 중요합니다.'],
   '층화': ['층화(stratify)', '방법', '학습·테스트로 나눌 때 정상/불량 비율을 똑같이 맞추는 것입니다.'],
   '교차검증': ['교차검증', '방법', '학습 데이터를 다섯 묶음으로 나눠 번갈아 검증하고 평균을 내는 방법입니다.'],
 },
 'subs': [
  {'id': 'sec-4-1', 'title': '공장이 AI에게 묻는 두 가지 질문', 'tags': ['라우팅: 라벨 · 숫자', '현장: 매일 두 번'],
   'pair': ('일상으로 치면', '건강검진표에는 "정상/경계/이상" 칸(라벨)과 "콜레스테롤 187mg/dL" 칸(숫자)이 함께 있다.',
            '공장에서는', '"이 부품은 정상인가?"에는 분류가, "이 공구는 앞으로 얼마나 더 쓸 수 있나?"에는 회귀가 답한다. 같은 센서 값에서 출발해도 출력 모양이 다르다.'),
   'body': ['분류의 출력은 라벨이고, 회귀의 출력은 숫자입니다. 이 구분 하나가 2·3·4회차의 모든 프롬프트와 작업지시서를 가릅니다.'],
   'talk': [('asst', 'e09', '"A/B/C 등급 중 어디?"는요? 숫자 같기도 한데요.'), ('fly', 'e10', '등급은 이름이 붙은 칸이야. 라벨이 셋 이상인 분류지.'), ('robo', 'e07', '그럼 "불량률은 몇 %?"는 회귀겠군요!')],
   'widget': ('w4-route', '<div class="ptitle">라우팅 게임 · 이 질문은 분류? 회귀?</div><div class="eq" id="rt-q"></div><div class="ctrl"><button class="bt" data-a="0" type="button">분류 (라벨)</button><button class="bt" data-a="1" type="button">회귀 (숫자)</button></div><div class="eq" id="rt-out" aria-live="polite"></div>'),
   'limit': '현실 질문은 둘을 섞기도 합니다. "마모가 0.78이면 정상인가?"는 회귀 숫자를 분류 규칙(임계값)으로 다시 가르는 것입니다(5주차).',
   'quiz': [{'q': '"이 공구의 남은 수명은 몇 시간인가?"에 답하는 모델은?', 'o': ['분류', '회귀'], 'a': 1, 'why': '답이 숫자이므로 회귀입니다.'}]},

  {'id': 'sec-4-2', 'title': '분류의 비유 — 의사결정 나무', 'tags': ['비유: 갈림길', '데이터: 판재 1,000개'],
   'pair': ('일상으로 치면', '"비가 오나? → 우산. 아니면 기온이 30도 넘나? → 반팔." 갈림길을 따라가면 마지막에 하나의 결론에 닿는다.',
            '분류 모델에서는', '"폭이 302.1mm 이하인가? → 거칠기가 4.9μm 이하인가? → 초음파가 27.5dB 이하인가? → 정상". 갈래를 따라가면 끝은 라벨이다.'),
   'body': ['아래 나무는 판재 데이터 1,000개로 직접 키운 깊이 3의 결정나무를 단순하게 옮긴 것입니다. 측정값을 바꿔 보면 판재가 어느 잎에 떨어지는지 보입니다.',
            '기준의 모양은 다양하지만 끝의 모양은 라벨입니다. 그래서 나무는 "왜 불량인가"를 갈림길 순서로 설명할 수 있습니다.'],
   'talk': [('robo', 'e19', '폭 302.2mm, 거칠기 3.0, 초음파 20! 정상입니다!'), ('fly', 'e09', '폭이 302.1을 넘었잖아. 첫 갈림길부터 다시 가 봐.'), ('moa', 'e01', '슬라이더로 판재를 하나씩 넣어 볼게요!')],
   'widget': ('w4-tree', '<div class="ptitle">실험 · 판재 하나를 나무에 넣어 보기</div><div class="ctrl"><div class="group"><span class="glabel">폭(mm)</span><input type="range" min="297" max="305" step="0.1" value="300" id="tr-w"><span class="val" id="tr-vw"></span></div><div class="group"><span class="glabel">거칠기(μm)</span><input type="range" min="1.5" max="8" step="0.1" value="3.2" id="tr-r"><span class="val" id="tr-vr"></span></div><div class="group"><span class="glabel">초음파(dB)</span><input type="range" min="11" max="40" step="0.5" value="20" id="tr-u"><span class="val" id="tr-vu"></span></div></div><div class="eq" id="tr-out" aria-live="polite"></div>'),
   'code': [('DecisionTreeClassifier(max_depth=3)', '깊이 3짜리 결정나무'), ('export_text(tree)', '갈림길을 글로 꺼내 보기')],
   'limit': '데이터로 키운 나무에는 "302.12 < 폭 ≤ 302.20이면 불량, 302.20 < 폭 ≤ 302.47이면 정상" 같은 우연한 갈래도 생깁니다. 이 페이지는 그런 갈래를 빼고 단순하게 옮겼습니다.',
   'quiz': [{'q': '의사결정 나무의 끝(잎)에 있는 것은?', 'o': ['숫자', '라벨', '확률만'], 'a': 1, 'why': '분류 나무는 갈래를 따라가 라벨로 끝납니다.'}]},

  {'id': 'sec-4-3', 'title': '회귀의 비유 — 안전벨트와 마모', 'tags': ['비유: 닳아 가는 벨트', '데이터: AI4I 마모'],
   'pair': ('일상으로 치면', '안전벨트는 쓸수록 조금씩 닳는다. "몇 번 더 써도 되나"는 정상/이상이 아니라 숫자로 답한다.',
            '회귀 모델에서는', '도구 누적 가동 시간(tool_wear_min)이 길수록 마모 지표(wear_proxy)가 커진다. 회귀는 이 숫자를 읽어 "앞으로 더 쓸 수 있는 분량"을 추정한다.'),
   'body': ['AI4I 미니 데이터 100행에서 wear_proxy는 tool_wear_min을 약 253으로 나눈 값과 거의 같습니다. 238분이면 0.94, 42분이면 0.17입니다.',
            '회귀의 약속은 셋입니다. ① 출력은 숫자 ② 측정한 점들을 지나는 선(직선 또는 곡선) ③ 임계선을 넘으면 경고. 세 번째에서 회귀 숫자가 다시 분류의 판단으로 넘어갑니다.'],
   'talk': [('asst', 'e07', '임계선을 0.70으로 두면, 몇 분부터 위험이에요?'), ('robo', 'e07', '0.70 × 253 = 약 177분입니다!'), ('fly', 'e10', '이번엔 계산이 맞네. 아래 그래프에서 확인해.')],
   'widget': ('w4-wear', '<div class="ptitle">실험 · 가동 시간과 마모 (AI4I 미니 100행)</div><div class="ctrl"><div class="group"><span class="glabel">임계 마모</span><input type="range" min="0.4" max="0.9" step="0.05" value="0.7" id="we-t"><span class="val" id="we-vt"></span></div></div><div class="cwrap"><svg id="we-svg"></svg></div><div class="eq" id="we-out" aria-live="polite"></div>'),
   'limit': '이 미니 데이터의 wear_proxy는 수업용으로 만든 파생 열입니다. 실제 공구 마모는 재질·절삭 조건에 따라 곡선으로 가속되는 일이 많습니다.',
   'quiz': [{'q': '회귀가 답하지 못하는 질문은?', 'o': ['마모가 얼마인가', '이 부품은 정상인가'], 'a': 1, 'why': '정상/이상은 라벨입니다. 회귀는 숫자만 냅니다.'}]},

  {'id': 'sec-4-4', 'title': '결정 경계 — 정상과 이상을 가르는 선', 'tags': ['개념: 결정 경계', '데이터: 거칠기 × 초음파'],
   'why': {'problem': '측정값 두 개(거칠기, 초음파)로 판재 1,000개를 찍으면 정상 점과 불량 점이 섞여 있습니다.',
           'limit': '변수 하나만 보고 자르면 다른 변수로만 드러나는 불량을 놓칩니다. 너무 복잡하게 그으면 우연까지 외웁니다.',
           'solve': '결정 경계는 평면을 둘로 가르는 선입니다. 단순한 선은 설명이 쉽고, 복잡한 선은 데이터에 더 붙습니다. 모양은 데이터가 정합니다.',
           'easy': '운동장에 분필로 선을 긋고 "이 선 밖은 불량"이라고 정하는 일.'},
   'body': ['아래 산점도는 실제 판재 1,000개입니다. 두 기준선을 움직여 정상 영역(왼쪽 아래 사각형)을 정해 보세요. 표는 네 가지 결과(TP·TN·FP·FN)를 바로 셉니다.'],
   'talk': [('fly', 'e09', '빨간 점 중 사각형 안에 남는 것들이 보여? 거칠기·초음파로는 안 잡히는 불량이야.'), ('asst', 'e04', '폭 때문에 불량인 판재들이겠네요!'), ('x2', 'e09', '(…끄덕)')],
   'widget': ('w4-bound', '<div class="ptitle">실험 · 기준선 두 개로 1,000개 가르기 (실제 수업 데이터)</div><div class="ctrl"><div class="group"><span class="glabel">거칠기 기준(μm)</span><input type="range" min="3" max="7" step="0.1" value="4.9" id="bd-r"><span class="val" id="bd-vr"></span></div><div class="group"><span class="glabel">초음파 기준(dB)</span><input type="range" min="20" max="35" step="0.5" value="27.5" id="bd-u"><span class="val" id="bd-vu"></span></div></div><div class="cwrap"><svg id="bd-svg" viewBox="0 0 600 340"></svg></div><div class="kpis" id="bd-k"></div>'),
   'limit': '두 변수만 그렸으므로 폭 불량은 이 그림에서 보이지 않습니다. 결정 경계는 변수 수만큼의 차원에 그어집니다.',
   'quiz': [{'q': '기준선을 아주 낮게 내리면 늘어나는 것은?', 'o': ['놓침(FN)', '과잉 경보(FP)'], 'a': 1, 'why': '정상까지 불량으로 부르게 되어 FP가 늘어납니다.'}]},

  {'id': 'sec-4-5', 'title': '네 가지 결과 — TP · TN · FP · FN', 'tags': ['지표: 정확도 · 재현율 · 정밀도', '현장: 비용의 무게'],
   'fx': {'q': '정확도 하나만 보면 안 돼요? 다른 건 왜 필요해요?',
          'school': '비율과 조건부 확률(고등 수학 확률과 통계)',
          'eq': '정확도 = (TP+TN) ÷ 전체 · <b>재현율</b> = TP ÷ (TP+FN) · <em>정밀도</em> = TP ÷ (TP+FP)',
          'rows': [('TP', '불량을 불량이라 함 (잘 찾음)'), ('TN', '정상을 정상이라 함'), ('FP', '정상을 불량이라 함 — 과잉 경보 · 점검·멈춤 비용'), ('FN', '불량을 정상이라 함 — 놓침 · 고객 클레임·시정 비용')],
          'calc': '세 기준(거칠기 4.9 · 초음파 27.5 · 폭 302.5)으로 1,000개를 가르면 TP 77, FN 23, FP 1, TN 899입니다. 정확도 97.6%, 재현율 77%, 정밀도 98.7%입니다.',
          'comment': '정확도는 97.6%로 높은데, 불량 4개 중 1개는 놓치고 있었네요!'},
   'body': ['어떤 비용이 더 무거운가는 현장의 책임이 정합니다. 자동차 안전 부품처럼 놓침이 치명적이면 재현율을, 정상품을 멈추는 비용이 크면 정밀도를 봅니다.'],
   'talk': [('robo', 'e16', '정확도 97.6%면 합격입니다!'), ('fly', 'e03', '불량 100개 중 23개가 고객한테 갔어. 그게 합격이야?'), ('doc', 'e10', '그래서 이 과목은 재현율을 함께 적게 합니다. 아래에서 비용을 넣어 보세요.')],
   'widget': ('w4-cost', '<div class="ptitle">계산기 · 오류 비용으로 보는 같은 결과 (TP 77 · FN 23 · FP 1 · TN 899)</div><div class="ctrl"><div class="group"><span class="glabel">놓침 1건 비용(만원)</span><input type="range" min="1" max="500" value="100" id="cs-n"><span class="val" id="cs-vn"></span></div><div class="group"><span class="glabel">과잉 경보 1건 비용(만원)</span><input type="range" min="1" max="100" value="5" id="cs-p"><span class="val" id="cs-vp"></span></div></div><div class="eq" id="cs-out" aria-live="polite"></div>'),
   'limit': '비용 숫자는 예시값입니다. 실제로는 클레임·리콜·라인 정지 비용을 회사 기준으로 넣어야 합니다.',
   'quiz': [{'q': '놓침(FN)이 치명적인 공정에서 가장 먼저 볼 지표는?', 'o': ['정확도', '재현율', '정밀도'], 'a': 1, 'why': '재현율은 실제 불량 중 잡아낸 비율입니다.'}]},

  {'id': 'sec-4-6', 'title': '회귀의 자기 점검 — 잔차', 'tags': ['개념: 잔차', '방법: 최소제곱'],
   'fx': {'q': '선이 점들에 "가깝다"는 걸 어떻게 숫자로 재요?',
          'school': '일차함수 y = ax + b, 제곱과 합',
          'eq': '잔차 e = 실제 − 추정 · 회귀가 작게 만드는 것 = <b>Σ e²</b>',
          'rows': [('a (기울기)', '가동 1분당 마모가 얼마나 느나'), ('b (절편)', '0분일 때 마모'), ('e > 0', '모델이 과소평가'), ('e < 0', '모델이 과대평가')],
          'calc': 'AI4I 미니 100행에 직선을 맞추면 기울기 0.00396, 절편 0.0006입니다. 238분이면 0.0006 + 0.00396 × 238 ≈ 0.94로, 실제 0.94와 같습니다.',
          'comment': '이 데이터는 거의 직선이라 잔차가 아주 작네요. 실제 공장은 이렇게 깔끔하지 않겠죠?'},
   'body': ['잔차가 한쪽으로 몰리면(예: 큰 값에서만 늘 위로) 직선이 부족하다는 신호입니다. 마모·열·누유 같은 누적형 데이터는 처음엔 천천히, 나중엔 가파르게 변하는 곡선이 어울립니다.'],
   'talk': [('asst', 'e07', '잔차가 작다는 게 "충분하다"는 뜻이에요?'), ('fly', 'e09', '학습 데이터에서만 작은지, 처음 보는 공구에서도 작은지는 달라.'), ('sia', 'e10', '5주차 회귀 앱에서 MAE·RMSE로 다시 확인하겠습니다.')],
   'widget': ('w4-res', '<div class="ptitle">실험 · 내가 그은 직선의 잔차 (AI4I 미니)</div><div class="ctrl"><div class="group"><span class="glabel">기울기 ×1000</span><input type="range" min="2" max="6" step="0.05" value="3" id="rs-a"><span class="val" id="rs-va"></span></div><button class="bt" id="rs-fit" type="button">최소제곱 직선으로</button></div><div class="cwrap"><svg id="rs-svg"></svg></div><div class="eq" id="rs-out" aria-live="polite"></div>'),
   'limit': '이 실험은 절편을 0.0006으로 고정하고 기울기만 바꿉니다.',
   'quiz': [{'q': '회귀가 최소로 만드는 것은?', 'o': ['잔차의 합', '잔차 제곱의 합', '점의 개수'], 'a': 1, 'why': '부호가 상쇄되지 않게 제곱해서 더합니다.'}]},

  {'id': 'sec-4-7', 'title': 'AI4I 2024 데이터 맛보기 — 14개 컬럼', 'tags': ['데이터: AI4I 2024', '분포: 정상 대다수'],
   'body': ['AI4I는 UCI 머신러닝 저장소의 예지보전 데이터로, 가공기의 공정 환경과 고장을 기록합니다. 수업에서는 100행짜리 미니판(ai4i_2024_mini.csv)을 씁니다.',
            '<div class="tw"><table class="tb"><tr><th>#</th><th>컬럼</th><th>뜻</th><th>분류에서</th><th>회귀에서</th></tr>'
            '<tr><td>1</td><td>UID</td><td>행 번호</td><td>—</td><td>—</td></tr>'
            '<tr><td>2~6</td><td>air_temp_k · process_temp_k · rotational_speed_rpm · torque_nm · tool_wear_min</td><td>공기 온도·공정 온도(K), 회전수, 토크, 도구 누적 가동 시간</td><td>입력</td><td>입력</td></tr>'
            '<tr><td>7</td><td>machine_failure</td><td>고장 여부 0/1</td><td><b>정답 라벨</b></td><td>—</td></tr>'
            '<tr><td>8~12</td><td>twf · hdf · pwf · osf · rnf</td><td>고장 원인 5종: 공구 마모 · 열 방산 · 전력 · 과부하 · 무작위</td><td>보조 라벨</td><td>—</td></tr>'
            '<tr><td>13</td><td>wear_proxy</td><td>마모 지표 0~1 (파생)</td><td>—</td><td><b>정답 숫자</b></td></tr>'
            '<tr><td>14</td><td>temp_diff</td><td>공정 − 공기 온도 차 (파생)</td><td>보강 입력</td><td>보강 입력</td></tr></table></div>',
            '원본 AI4I는 정상 96.55% · 이상 3.45%로 매우 기울어 있습니다. 미니판 100행은 정상 94 · 고장 6, 고장 원인 표시는 twf 2 · hdf 3 · pwf 1 · osf 1 · rnf 1입니다.'],
   'talk': [('robo', 'e04', '고장 6건인데 원인 표시는 8개? 숫자가 안 맞습니다!'), ('fly', 'e10', '좋은 의심이야. A0094는 twf·hdf 둘 다 1이고, A0096은 rnf=1인데 machine_failure는 0이야.'), ('moa', 'e09', '라벨끼리도 검수가 필요하네요.')],
   'widget': ('w4-ai4i', '<div class="ptitle">데이터 · AI4I 미니에서 고장·원인 표시가 있는 행</div><div class="tw" id="ai-tb"></div><div class="eq" id="ai-out" aria-live="polite"></div>'),
   'limit': '원자료 1회차 교안의 컬럼 표에서 twf를 "열에 의한 실패"로 적은 부분은, AI4I 원본 정의(tool wear failure, 공구 마모 고장)에 맞춰 이 페이지에서는 "공구 마모"로 바꿉니다.',
   'quiz': [{'q': 'AI4I에서 분류의 정답 라벨은?', 'o': ['wear_proxy', 'machine_failure', 'tool_wear_min'], 'a': 1, 'why': '고장 여부 0/1이 분류의 정답입니다.'}]},

  {'id': 'sec-4-8', 'title': '분류 프롬프트 카드 — 역할 · 출력 형식 · few-shot', 'tags': ['카드: 분류', 'QWEN: JSON 한 줄'],
   'body': ['2주차 5원칙이 카드 세 장으로 바뀝니다. ① 시스템 역할 — 품질 분석가 ② 출력 형식 — JSON 한 줄(machine_failure, predicted_failure_mode, confidence, rationale) ③ few-shot 예시 2개 — 정상 하나, 이상 하나.',
            'JSON으로 받는 이유는 5주차 앱이 그 결과를 사람 손 없이 카드로 옮기기 위해서입니다. 출력을 사람이 다시 정리하고 있다면 형식 카드가 약한 것입니다.',
            '<div class="prompt" data-raw="' + CLS.replace('"', '&quot;') + '">' + CLS.replace('<', '&lt;') + '</div>'],
   'talk': [('asst', 'e07', '마지막에 [대상 입력] 다섯 줄만 바꿔서 QWEN에 보내면 JSON 한 줄이 돌아와요.'), ('robo', 'e19', 'confidence는 빼도 됩니다. 저는 늘 확신하니까요!'), ('fly', 'e03', 'confidence 없이 prediction만 받으면, 애매한 판재를 구분할 수가 없어.')],
   'widget': ('w4-cls', '<div class="ptitle">조립 · AI4I 한 행을 골라 [대상 입력] 만들기</div><div class="ctrl"><label class="glabel" for="cl-s">행 고르기</label><select id="cl-s" style="background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:8px;padding:6px"></select></div><div class="prompt" id="cl-p"></div><div class="eq" id="cl-out" aria-live="polite"></div>'),
   'limit': 'QWEN의 답은 데이터에서 학습한 모델이 아니라 언어 모델의 추론입니다. few-shot 예시가 둘뿐이라, 열 방산(hdf)·과부하(osf) 같은 유형은 엇갈리기 쉽습니다. 그래서 다음 절들에서 데이터로 기준을 찾습니다.',
   'quiz': [{'q': 'machine_failure가 0일 때 predicted_failure_mode는?', 'o': ['twf', 'null', '아무거나'], 'a': 1, 'why': '카드 규칙: 정상이면 null입니다.'}]},

  {'id': 'sec-4-9', 'title': '회귀 프롬프트 카드 — 두 구간과 주의 부근', 'tags': ['카드: 회귀', '구간: 0.40 · 0.70'],
   'body': ['회귀 카드는 입력은 같고 출력만 다릅니다. estimated_wear(0.0~1.0)와 rationale 한 줄입니다.',
            '좋은 분리는 두 구간입니다. 정상 부근(0.0~0.40)과 위험 부근(0.70~1.00). 0.40과 0.70 사이는 정상·위험 어느 쪽도 강하지 않은 주의 부근입니다.',
            '<div class="prompt" data-raw="' + REG.replace('"', '&quot;') + '">' + REG.replace('<', '&lt;') + '</div>'],
   'talk': [('moa', 'e09', '임계값을 카드 안에 적지 말고 현장 규칙으로 두라고 교안에 있었어요.'), ('doc', 'e10', '맞습니다. 0.40·0.70은 5주차 작업지시서의 분기 기준이 됩니다.')],
   'widget': ('w4-zone', '<div class="ptitle">실험 · 마모 추정값은 어느 구간에 들어가나</div><div class="ctrl"><div class="group"><span class="glabel">estimated_wear</span><input type="range" min="0" max="1" step="0.01" value="0.52" id="zn-v"><span class="val" id="zn-vv"></span></div></div><div class="eq" id="zn-out" aria-live="polite"></div>'),
   'limit': '0.40·0.70은 교안이 정한 수업용 경계입니다. 실제 경계는 고장 이력과 비용으로 정합니다.',
   'quiz': [{'q': 'estimated_wear 0.55는?', 'o': ['정상 부근', '주의 부근', '위험 부근'], 'a': 1, 'why': '0.40~0.70 사이는 주의 부근입니다.'}]},

  {'id': 'sec-4-10', 'title': '"무슨 기준으로 골랐는지" 안 보인다 — 데이터로 판정 기준 찾기', 'tags': ['데이터: 불량품 판정 1,000개', '방법: Colab 분류 모델'],
   'why': {'problem': '프롬프트 카드만으로는 AI가 어떤 기준으로 불량/정상을 갈랐는지 알 수 없습니다.',
           'limit': '기준이 안 보이면 작업자는 따를 수 없고, 고객에게 설명할 수 없으며, 기준이 틀려도 고칠 수 없습니다.',
           'solve': '그래서 데이터를 주고, 분류 모델을 여러 개 학습시켜 판정 기준을 도출하게 합니다. 아래 프롬프트를 Colab 생성 AI(또는 QWEN)에 넣으면 코드와 결과가 나옵니다.',
           'easy': '숙련 검사원 옆에서 1,000개 판정을 지켜본 뒤 "이분은 이걸 보고 고르시는구나"를 적어 내는 일.'},
   'body': ['<div class="prompt" data-raw="' + COLAB.replace('"', '&quot;') + '">' + COLAB.replace('<', '&lt;') + '</div>',
            '데이터: 불량품_판정_데이터.csv — sample_id, with_mm(폭, 원자료 철자 그대로), surface_roughness_um(표면 거칠기), UT_dB(초음파), oven_temp_c(경화 오븐 온도), nomal_abnormal(0 정상 · 1 불량, 원자료 철자 그대로). 1,000개 중 불량 100개입니다.',
            '이 페이지가 같은 조건(8:2 층화 분할, 5겹 교차검증, 6개 알고리즘)으로 직접 돌린 결과는 실습 리포트에 있습니다. 결론만 먼저 말하면, 판정 기준은 세 가지였고 오븐 온도는 거의 상관이 없었습니다.'],
   'talk': [('robo', 'e16', '모델을 여섯 개나 돌렸습니다! 제일 높은 정확도를 고르면 끝!'), ('fly', 'e09', '정확도가 다 비슷하면? 기준을 읽을 수 있는 모델이 더 쓸모 있어.'), ('asst', 'e07', '아래에서 변수 하나씩 정상·불량 분포를 비교해 볼게요.'), ('x1', 'e01', '(반짝)')],
   'widget': ('w4-dist', '<div class="ptitle">탐색 · 변수별 정상(초록)과 불량(빨강) 분포 (실제 수업 데이터)</div><div class="ctrl" id="ds-bt"></div><div class="cwrap"><svg id="ds-svg"></svg></div><div class="eq" id="ds-out" aria-live="polite"></div>'),
   'limit': '원자료의 m1·m2 추가 데이터(판정샘플 40, 학습데이터 불량18/50/100 등)는 이번 업로드에 파일이 없어 이 페이지에서 다루지 않았습니다. 받으면 리포트에 더하겠습니다.',
   'quiz': [{'q': '분포를 비교했을 때 정상·불량이 거의 겹치는 변수는?', 'o': ['표면 거칠기', '오븐 온도', '초음파'], 'a': 1, 'why': '오븐 온도는 정상 평균 179.98, 불량 179.89로 거의 같습니다.'}]},

  {'id': 'sec-4-11', 'title': '층화 · 교차검증 · 정확도의 함정', 'tags': ['방법: 8:2 층화 분할', '함정: 기울어진 데이터'],
   'body': ['불량이 10%뿐이면 무작위로 나눈 테스트 세트에 불량이 7%만 들어갈 수도, 13% 들어갈 수도 있습니다. 그래서 학습·테스트의 불량 비율을 똑같이 맞춥니다(층화). 이번 분할은 둘 다 10.0%였습니다.',
            '교차검증은 학습 데이터 800개를 다섯 묶음으로 나눠, 한 묶음씩 번갈아 검증합니다. 한 번 운 좋게 나온 점수를 믿지 않으려는 장치입니다.',
            '그래도 정확도의 함정은 남습니다. "모두 정상"이라고만 답해도 정확도 90%입니다. 아래 대결에서 숫자로 봅니다.'],
   'talk': [('sia', 'e07', '층화, 교차검증, 재현율. 세 가지를 프롬프트 #6·#7과 결과 해석에 같이 적겠습니다.'), ('fly', 'e10', '좋아. 그리고 정확도 표 옆에 혼동행렬을 꼭 붙여.')],
   'widget': ('w4-strat', '<div class="ptitle">실험 · 무작위 분할을 20번 하면 테스트의 불량 비율은?</div><button class="bt primary" id="sf-run" type="button">20번 나눠 보기</button><div class="cwrap"><svg id="sf-svg"></svg></div><div class="eq" id="sf-out" aria-live="polite"></div>'),
   'limit': '교차검증 점수는 학습 데이터 안에서의 점수입니다. 최종 판단은 한 번도 안 쓴 테스트 세트와, 그 뒤의 새 생산 데이터로 합니다.',
   'quiz': [{'q': '불량 10% 데이터에서 "모두 정상" 모델의 재현율은?', 'o': ['90%', '10%', '0%'], 'a': 2, 'why': '불량을 하나도 잡지 못하므로 재현율 0%입니다.'}]},

  {'id': 'sec-4-12', 'title': '자주 하는 실수 다섯 가지', 'tags': ['점검: 프롬프트·결과', '정리'],
   'body': ['① 입력 다섯 개 중 일부만 적는다 — 카드에는 입력 다섯 개를 모두 적습니다. ② 출력 형식 없이 받는다 — 그러면 결과를 손으로 다시 정리하게 됩니다.',
            '③ confidence 없이 prediction만 받는다 — 애매한 행을 가려낼 수 없습니다. ④ rationale 없이 숫자만 받는다 — 작업지시서에 옮길 이유가 없습니다.',
            '⑤ 정확도 하나로 모델을 고른다 — 기울어진 데이터에서는 혼동행렬과 재현율을 함께 봅니다.'],
   'talk': [('robo', 'e14', '저는 다섯 개 다 했습니다…'), ('moa', 'e12', '괜찮아요! 체크리스트로 만들어 드릴게요.'), ('x3', 'e16', '(삐빅)')],
   'widget': ('w4-check', '<div class="ptitle">체크리스트 · 내 프롬프트와 결과 점검</div><div class="ctrl" id="ck4-bt"></div><div class="eq" id="ck4-out" aria-live="polite"></div>'),
   'limit': '체크리스트는 출발점입니다. 실제로 돌려 본 결과를 원본과 대조하는 ③ 검수는 따로 해야 합니다.',
   'quiz': [{'q': '결과를 사람이 손으로 다시 정리하고 있다면 약한 카드는?', 'o': ['역할 카드', '출력 형식 카드', '예시 카드'], 'a': 1, 'why': '출력 형식을 정하면 결과가 바로 다음 단계로 넘어갑니다.'}]},
 ],
 'duel': {
   'q': '불량 100개가 섞인 1,000개, 누가 더 잘 골랐나?',
   'intro': [('doc', 'e07', '주판봇은 "모두 정상"이라고 답하는 모델, 초파리 연구원은 데이터에서 찾은 기준 세 개(거칠기 4.9 · 초음파 27.5 · 폭 302.5)입니다.'), ('sia', 'e12', '판정 깃발 들겠습니다!')],
   'fly': '기준 세 개로 고른다. 정확도보다 놓친 불량 수를 봐.',
   'robo': '전부 정상! 정확도 90%가 보장됩니다!',
   'widget': 'w4-duel',
   'panel': '<div class="ptitle">채점 · 1,000개 전체 (실제 수업 데이터)</div><button class="bt primary" id="du4-run" type="button">채점하기</button><div class="kpis" id="du4-k"></div><div class="tw" id="du4-tb"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('moa', 'e01', '재현율 0%라니…'), ('x1', 'e04', '(헉)'), ('x2', 'e16', '(짝짝)')],
 },
 'summary': {
   'head': ['절', '한 줄', '다음 주로'],
   'rows': [['4.1~4.3', '라벨은 분류, 숫자는 회귀. 회귀 숫자는 임계선에서 다시 판단으로', '5주 점수형 분기'],
            ['4.4~4.5', '결정 경계와 네 가지 결과, 정확도 97.6%여도 재현율 77%', '5주 유형형 분기'],
            ['4.6', '잔차 제곱합을 줄이는 선, 잔차 패턴은 직선의 한계 신호', '5주 MAE·RMSE'],
            ['4.7~4.9', 'AI4I 14컬럼, 분류·회귀 카드(JSON, few-shot)', '5주 앱 입력폼'],
            ['4.10~4.12', '판정 기준 = 거칠기 4.9 · 초음파 27.5 · 폭 302.5, 오븐 온도는 무관', '실습 리포트']],
   'limits': ['3D 라인의 불량 판재 비율과 색은 장면용입니다. 실제 판정 결과는 대결과 실습 리포트의 숫자를 봅니다.',
              '의사결정 나무는 실제 학습 결과를 단순하게 옮긴 것입니다.',
              '오류 비용 계산기의 비용은 예시값입니다.'],
 },
 'outro': [('doc', 'e16', '같은 데이터도 질문 모양에 따라 분류와 회귀로 갈립니다. 그리고 기준이 보여야 현장에서 쓸 수 있습니다.'),
           ('asst', 'e01', '판정 기준 세 개, 실습 리포트에서 숫자로 확인할게요!'),
           ('fly', 'e10', '다음 주에는 그 숫자 한 줄을 작업자가 받아 움직이는 작업지시서로 바꿔.'),
           ('robo', 'e11', '"전부 정상" 모델은… 조용히 퇴근시키겠습니다.')],
 'sources': [('강의 교안', '코딩 없는 제조업의 AI 데이터 분석 1회차 「비유와 개념」 · 2회차 「데이터 셋에 어떤 말을 걸까」 — 안상선 · 불량품 판정 Colab 프롬프트 · 분류·회귀 결과 출력 프롬프트'),
             ('수업 데이터', '불량품_판정_데이터.csv (1,000행, 가상) · ai4i_2024_mini.csv (100행, AI4I 2020 Predictive Maintenance 데이터의 구성을 따른 수업용 미니판)'),
             ('공개 데이터', 'AI4I 2020 Predictive Maintenance Dataset, UCI Machine Learning Repository'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '오류 비용, 라우팅·체크리스트 문항, 3D 장면의 불량 비율은 설명용입니다. 판정 결과·분포·결정 경계·마모 직선은 수업 데이터로 계산했습니다.',
 'practice': ('practice.html', '불량품 판정 기준 세 개를 데이터에서 찾다'),
}

CH['js'] = _DATA + r'''
function cm(pred){var t={TP:0,TN:0,FP:0,FN:0};D4.y.forEach(function(y,i){var p=pred(i);if(y&&p)t.TP++;else if(!y&&!p)t.TN++;else if(!y&&p)t.FP++;else t.FN++;});return t;}
function sayDoc(mood,html){var v=document.getElementById('verdict');v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
W['w4-route']=function(b){var Q=[['이 판재는 불량인가?',0],['이 공구는 몇 분 더 쓸 수 있나?',1],['이 고장은 twf·hdf·pwf 중 무엇인가?',0],['다음 달 불량률은 몇 %인가?',1],['이 배치는 A·B·C 등급 중 어디인가?',0],['베어링 온도는 내일 몇 도까지 오르나?',1]],i=0,sc=0,q=b.querySelector('#rt-q'),o=b.querySelector('#rt-out');function sh(){q.textContent='('+(i+1)+'/6) '+Q[i][0];}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var ok=+x.dataset.a===Q[i][1];if(ok)sc++;o.innerHTML=(ok?'✔ ':'✘ 정답 <b>'+['분류','회귀'][Q[i][1]]+'</b> · ')+'점수 '+sc+'/'+(i+1);i=(i+1)%6;if(!i)sc=0;sh();};});sh();};
W['w4-tree']=function(b){var w=b.querySelector('#tr-w'),r=b.querySelector('#tr-r'),u=b.querySelector('#tr-u'),o=b.querySelector('#tr-out');function f(){var W_=+w.value,R=+r.value,U=+u.value;b.querySelector('#tr-vw').textContent=W_.toFixed(1);b.querySelector('#tr-vr').textContent=R.toFixed(1);b.querySelector('#tr-vu').textContent=U.toFixed(1);var path=[],res;if(W_>302.5){path.push('폭 '+W_.toFixed(1)+' > 302.5 → <em>예</em>');res=1;}else{path.push('폭 ≤ 302.5 → 아니오');if(R>4.9){path.push('거칠기 '+R.toFixed(1)+' > 4.9 → <em>예</em>');res=1;}else{path.push('거칠기 ≤ 4.9 → 아니오');if(U>27.5){path.push('초음파 '+U.toFixed(1)+' > 27.5 → <em>예</em>');res=1;}else{path.push('초음파 ≤ 27.5 → 아니오');res=0;}}}o.innerHTML=path.join(' ▸ ')+' ▸ 잎: <b style="color:'+(res?'var(--eye)':'var(--gfp)')+'">'+(res?'불량':'정상')+'</b>'+(W_>301&&W_<=302.5&&!res?' · <i>폭 301~302.5mm는 데이터에서 불량이 섞이는 회색 지대입니다</i>':'');}[w,r,u].forEach(function(e){e.oninput=f});f();};
W['w4-wear']=function(b){var t=b.querySelector('#we-t'),s=b.querySelector('#we-svg'),o=b.querySelector('#we-out');var idx=AI4I.tool_wear_min.map(function(v,i){return i}).sort(function(a,c){return AI4I.tool_wear_min[a]-AI4I.tool_wear_min[c]});function f(){var T=+t.value;b.querySelector('#we-vt').textContent=T.toFixed(2);Chart.line(s,{labels:idx.map(function(i){return AI4I.tool_wear_min[i]+'분'}),series:[{name:'wear_proxy',color:'#f1b646',values:idx.map(function(i){return AI4I.wear_proxy[i]}),dots:true,width:0.5}],ref:T,min:0,max:1,h:220,ticks:8});var m=Math.round((T-.0006)/.00396);var over=AI4I.wear_proxy.filter(function(v){return v>=T}).length;o.innerHTML='임계 '+T.toFixed(2)+' ↔ 가동 약 <b>'+m+'분</b> · 100개 중 <em>'+over+'개</em>가 임계 이상 · 노란 점선 = 임계';}t.oninput=f;f();};
W['w4-bound']=function(b){var R=b.querySelector('#bd-r'),U=b.querySelector('#bd-u'),s=b.querySelector('#bd-svg'),k=b.querySelector('#bd-k'),NS='http://www.w3.org/2000/svg';var X=function(v){return 50+(v-1.5)/(8-1.5)*530},Y=function(v){return 310-(v-10)/(40-10)*290};var g=document.createElementNS(NS,'g');s.appendChild(g);D4.r.forEach(function(r,i){var c=document.createElementNS(NS,'circle');c.setAttribute('cx',X(r));c.setAttribute('cy',Y(D4.u[i]));c.setAttribute('r',D4.y[i]?3.5:2.2);c.setAttribute('fill',D4.y[i]?'#f0604d':'rgba(94,227,156,.45)');g.appendChild(c);});var ax=document.createElementNS(NS,'text');ax.setAttribute('x',300);ax.setAttribute('y',335);ax.textContent='표면 거칠기(μm) →';s.appendChild(ax);var ay=document.createElementNS(NS,'text');ay.setAttribute('x',4);ay.setAttribute('y',14);ay.textContent='↑ 초음파(dB)';s.appendChild(ay);var rect=document.createElementNS(NS,'rect');rect.setAttribute('fill','none');rect.setAttribute('stroke','#f1b646');rect.setAttribute('stroke-width','2');rect.setAttribute('stroke-dasharray','6 4');s.appendChild(rect);function f(){var r=+R.value,u=+U.value;b.querySelector('#bd-vr').textContent=r.toFixed(1);b.querySelector('#bd-vu').textContent=u.toFixed(1);rect.setAttribute('x',X(1.5));rect.setAttribute('y',Y(u));rect.setAttribute('width',X(r)-X(1.5));rect.setAttribute('height',Y(10)-Y(u));var t=cm(function(i){return D4.r[i]>r||D4.u[i]>u});k.innerHTML='<div class="kpi g"><b>'+t.TP+'</b><span>TP 불량을 불량으로</span></div><div class="kpi r"><b>'+t.FN+'</b><span>FN 놓친 불량</span></div><div class="kpi a"><b>'+t.FP+'</b><span>FP 과잉 경보</span></div><div class="kpi m"><b>'+(t.TP/(t.TP+t.FN)*100).toFixed(0)+'%</b><span>재현율 (정확도 '+((t.TP+t.TN)/10).toFixed(1)+'%)</span></div>';}R.oninput=U.oninput=f;f();};
W['w4-cost']=function(b){var n=b.querySelector('#cs-n'),p=b.querySelector('#cs-p'),o=b.querySelector('#cs-out');function f(){var N=+n.value,P=+p.value;b.querySelector('#cs-vn').textContent=N;b.querySelector('#cs-vp').textContent=P;var c1=23*N+1*P,c0=100*N;o.innerHTML='기준 세 개의 오류 비용 = 23 × '+N+' + 1 × '+P+' = <b>'+c1.toLocaleString()+'만원</b> · "모두 정상"의 비용 = 100 × '+N+' = <em>'+c0.toLocaleString()+'만원</em> · 놓친 23건만 줄여도 비용이 가장 크게 줄어듭니다.';}n.oninput=p.oninput=f;f();};
W['w4-res']=function(b){var a=b.querySelector('#rs-a'),s=b.querySelector('#rs-svg'),o=b.querySelector('#rs-out');var idx=AI4I.tool_wear_min.map(function(v,i){return i}).sort(function(x,y){return AI4I.tool_wear_min[x]-AI4I.tool_wear_min[y]});function f(){var A=+a.value/1000;b.querySelector('#rs-va').textContent=(+a.value).toFixed(2);var sse=0,res=[];idx.forEach(function(i){var e=AI4I.wear_proxy[i]-(.0006+A*AI4I.tool_wear_min[i]);sse+=e*e;res.push(e);});Chart.line(s,{labels:idx.map(function(i){return AI4I.tool_wear_min[i]}),series:[{name:'실제',color:'#f1b646',values:idx.map(function(i){return AI4I.wear_proxy[i]}),dots:true,width:.5},{name:'내 직선',color:'#82b8ff',values:idx.map(function(i){return .0006+A*AI4I.tool_wear_min[i]})}],min:0,max:1.2,h:220,ticks:8});var pos=res.filter(function(e){return e>0}).length;o.innerHTML='잔차 제곱합 <b>'+sse.toFixed(4)+'</b> · 잔차가 양수인 점 '+pos+'/100 '+(pos>80?'→ <em>선이 점들보다 아래(과소평가)</em>':pos<20?'→ <em>선이 점들보다 위(과대평가)</em>':'→ 고르게 흩어짐');}b.querySelector('#rs-fit').onclick=function(){a.value=3.96;f();};a.oninput=f;f();};
W['w4-ai4i']=function(b){var C=['UID','tool_wear_min','torque_nm','rotational_speed_rpm','process_temp_k','machine_failure','twf','hdf','pwf','osf','rnf'];var rows=[];AI4I.UID.forEach(function(u,i){if(AI4I.machine_failure[i]||AI4I.twf[i]+AI4I.hdf[i]+AI4I.pwf[i]+AI4I.osf[i]+AI4I.rnf[i])rows.push(i)});b.querySelector('#ai-tb').innerHTML='<table class="tb"><tr>'+C.map(function(c){return '<th>'+c+'</th>'}).join('')+'</tr>'+rows.map(function(i){var flag=AI4I.twf[i]+AI4I.hdf[i]+AI4I.pwf[i]+AI4I.osf[i]+AI4I.rnf[i];var odd=flag>1||(!AI4I.machine_failure[i]&&flag);return '<tr'+(odd?' style="background:rgba(241,182,70,.12)"':'')+'>'+C.map(function(c){return '<td class="n">'+AI4I[c][i]+'</td>'}).join('')+'</tr>'}).join('')+'</table>';b.querySelector('#ai-out').innerHTML='노란 행: 원인 표시가 두 개(A0094 twf·hdf)이거나, 원인은 있는데 고장은 0(A0096 rnf). 무작위 고장(rnf)은 원본 AI4I에서도 고장으로 이어지지 않는 경우가 있습니다.';};
W['w4-cls']=function(b){var s=b.querySelector('#cl-s'),p=b.querySelector('#cl-p'),o=b.querySelector('#cl-out');AI4I.UID.forEach(function(u,i){var op=document.createElement('option');op.value=i;op.textContent=u+(AI4I.machine_failure[i]?' (고장)':'');s.appendChild(op);});s.value=91;function f(){var i=+s.value;var t='[대상 입력]\nair '+AI4I.air_temp_k[i]+'\nprocess '+AI4I.process_temp_k[i]+'\nrotation '+AI4I.rotational_speed_rpm[i]+'\ntorque '+AI4I.torque_nm[i]+'\nwear '+AI4I.tool_wear_min[i];p.textContent=t;p.setAttribute('data-raw',t);var c=document.createElement('button');c.className='bt copy';c.type='button';c.textContent='복사';c.onclick=function(){navigator.clipboard&&navigator.clipboard.writeText(t);c.textContent='복사됨';};p.appendChild(c);var m=['twf','hdf','pwf','osf','rnf'].filter(function(k){return AI4I[k][i]});o.innerHTML='이 행의 실제 정답: machine_failure <b>'+AI4I.machine_failure[i]+'</b>, 원인 '+(m.length?'<b>'+m.join('·')+'</b>':'null')+' · QWEN 답과 대조해 보세요(검수).';}s.onchange=f;f();};
W['w4-zone']=function(b){var v=b.querySelector('#zn-v'),o=b.querySelector('#zn-out');function f(){var x=+v.value;b.querySelector('#zn-vv').textContent=x.toFixed(2);var z=x<.4?['정상 부근','var(--gfp)','다음 점검 주기까지 정상 가동']:x<.7?['주의 부근','var(--amber)','점검 주기 절반으로 단축, 교체 일정 한 단계 앞당김']:['위험 부근','var(--eye)','즉시 교체 또는 가동 중단 — 1시간 내 결정'];o.innerHTML='<b style="color:'+z[1]+'">'+z[0]+'</b> → 5주차 작업지시서 행동: '+z[2];}v.oninput=f;f();};
W['w4-dist']=function(b){var V=[['w','폭(mm)',296,306],['r','거칠기(μm)',1.5,8],['u','초음파(dB)',10,40],['o','오븐 온도(℃)',176,184]],bt=b.querySelector('#ds-bt'),s=b.querySelector('#ds-svg'),o=b.querySelector('#ds-out');V.forEach(function(v,j){var x=document.createElement('button');x.className='bt';x.textContent=v[1];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.toggle('on',y===x)});var nb=20,h0=new Array(nb).fill(0),h1=new Array(nb).fill(0),L=[];for(var k=0;k<nb;k++)L.push((v[2]+(v[3]-v[2])*(k+.5)/nb).toFixed(1));D4[v[0]].forEach(function(val,i){var k=Math.max(0,Math.min(nb-1,Math.floor((val-v[2])/(v[3]-v[2])*nb)));(D4.y[i]?h1:h0)[k]++;});var n0=900,n1=100;Chart.bars(s,{labels:L,series:[{name:'정상(비율)',color:'#5ee39c',values:h0.map(function(c){return c/n0})},{name:'불량(비율)',color:'#f0604d',values:h1.map(function(c){return c/n1})}],min:0,h:220});var m0=0,m1=0;D4[v[0]].forEach(function(val,i){if(D4.y[i])m1+=val;else m0+=val;});o.innerHTML=v[1]+' 평균 · 정상 <b>'+(m0/n0).toFixed(2)+'</b> · 불량 <em>'+(m1/n1).toFixed(2)+'</em>'+(v[0]=='o'?' → 거의 같습니다. 판정에 쓰이지 않는 변수로 보입니다.':' → 불량 쪽 분포가 길게 퍼져 있습니다.');};bt.appendChild(x);});bt.firstChild.click();};
W['w4-strat']=function(b){b.querySelector('#sf-run').onclick=function(){var r=rng(Date.now()%100000),res=[];for(var t=0;t<20;t++){var idx=D4.y.map(function(_,i){return i});for(var i=idx.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var tmp=idx[i];idx[i]=idx[j];idx[j]=tmp;}var te=idx.slice(0,200),n=te.filter(function(i){return D4.y[i]}).length;res.push(n/200*100);}Chart.bars(b.querySelector('#sf-svg'),{labels:res.map(function(_,i){return i+1}),series:[{name:'테스트 불량 비율(%)',color:'#82b8ff',values:res}],ref:10,min:0,max:16,h:200});b.querySelector('#sf-out').innerHTML='무작위 분할 20번: 최소 <b>'+Math.min.apply(null,res).toFixed(1)+'%</b> ~ 최대 <b>'+Math.max.apply(null,res).toFixed(1)+'%</b> · 층화하면 늘 <em>10.0%</em>(노란 점선)입니다.';};};
W['w4-check']=function(b){var C=['입력 다섯 개를 모두 적었다','출력 형식(JSON)을 정했다','confidence를 받는다','rationale을 받는다','혼동행렬·재현율을 함께 본다'],on=C.map(function(){return 0}),bt=b.querySelector('#ck4-bt'),o=b.querySelector('#ck4-out');C.forEach(function(c,i){var x=document.createElement('button');x.className='bt';x.setAttribute('aria-pressed','false');x.textContent=(i+1)+'. '+c;x.onclick=function(){on[i]=1-on[i];x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var n=on.reduce(function(a,c){return a+c},0);o.innerHTML='점검 <b>'+n+'/5</b> '+(n==5?'— 5주차 앱으로 넘길 준비 완료':'— 남은 것: <i>'+C.filter(function(_,i){return !on[i]}).join(', ')+'</i>');}f();};
W['w4-duel']=function(b){b.querySelector('#du4-run').onclick=function(){var a=cm(function(){return false}),c=cm(function(i){return D4.w[i]>302.5||D4.r[i]>4.9||D4.u[i]>27.5});function row(n,t){return '<tr><td>'+n+'</td><td class="n">'+t.TP+'</td><td class="n">'+t.FN+'</td><td class="n">'+t.FP+'</td><td class="n">'+t.TN+'</td><td class="n">'+((t.TP+t.TN)/10).toFixed(1)+'%</td><td class="n">'+(t.TP/(t.TP+t.FN)*100).toFixed(0)+'%</td></tr>';}b.querySelector('#du4-tb').innerHTML='<table class="tb"><tr><th>모델</th><th>TP</th><th>FN</th><th>FP</th><th>TN</th><th>정확도</th><th>재현율</th></tr>'+row('주판봇: 모두 정상',a)+row('초파리: 기준 세 개',c)+'</table>';b.querySelector('#du4-k').innerHTML='<div class="kpi r"><b>90.0%</b><span>주판봇 정확도 · 재현율 0%</span></div><div class="kpi g"><b>'+((c.TP+c.TN)/10).toFixed(1)+'%</b><span>초파리 정확도 · 재현율 '+(c.TP)+'%</span></div><div class="kpi a"><b>'+c.FN+'</b><span>초파리도 놓친 불량</span></div><div class="kpi m"><b>'+c.FP+'</b><span>초파리의 과잉 경보</span></div>';sayDoc('e10','초파리 연구원 승. 정확도 차이는 7.6%p뿐이지만, 주판봇은 불량 100개를 하나도 잡지 못했습니다(재현율 0%). 초파리 기준도 23개를 놓칩니다. 그 23개는 폭 301~302.5mm 회색 지대에 몰려 있어, 실습 리포트에서 따로 봅니다.');};};
'''

RP = {
 'title': 'AI는 무슨 기준으로 불량을 골랐을까?',
 'eyebrow': '4주차 실습 리포트 · 분류 모델 · 불량품 판정 데이터 1,000개',
 'desc': '스마트 제조 4주차 실습 리포트 — 불량품 판정 데이터로 6개 분류 모델을 학습·비교하고, 판정 기준 세 개(거칠기·초음파·폭)와 폭의 회색 지대를 찾은 결과를 박사가 정리합니다.',
 'lead': 'QWEN 프롬프트 카드만으로는 AI가 어떤 기준으로 불량을 갈랐는지 보이지 않았습니다. 그래서 데이터를 주고 분류 모델을 직접 학습시켜 판정 기준을 꺼냈습니다. 기준은 세 개였고, 오븐 온도는 상관이 없었습니다.',
 'cover_mood': 'e07', 'back': ('index.html', '4주차 본문으로'), 'next': ('../w05/practice.html', '5주차 실습 리포트'),
 'summary': {
   'finding': '불량품 판정 데이터에서 불량은 "표면 거칠기 4.9μm 초과 · 초음파 27.5dB 초과 · 폭 302.5mm 초과" 세 기준으로 대부분 설명되었고(재현율 77%, 정밀도 98.7%), 오븐 온도는 판정과 거의 무관했습니다.',
   'evidence': ['<span class="fact">사실</span> 세 기준으로 1,000개를 가르면 TP 77 · FN 23 · FP 1 · TN 899입니다(<a href="#tab-r4-2">표 2</a>).',
                '<span class="fact">사실</span> 오븐 온도 평균은 정상 179.98℃, 불량 179.89℃로 거의 같습니다(<a href="#tab-r4-1">표 1</a>).',
                '<span class="fact">사실</span> 6개 모델의 5겹 교차검증 정확도는 94.4~97.1%로 비슷했고, 테스트 재현율은 55~80%로 크게 갈렸습니다(<a href="#tab-r4-3">표 3</a>).',
                '<span class="interp">해석</span> 놓친 23개는 폭 301~302.5mm 구간에 몰려 있습니다. 폭은 딱 자르는 선이 아니라 불량 확률이 서서히 오르는 회색 지대로 읽힙니다(<a href="#fig-r4-2">그림 2</a>).'],
   'fig': ('fig', {'id': 'fig-r4-1', 'cap': '[그림 1] 표면 거칠기 × 초음파 산점도와 두 기준선', 'w': 'r4-scatter', 'alt': '판재 1,000개 산점도. 가로 거칠기, 세로 초음파. 불량(빨강)은 거칠기 4.9 오른쪽과 초음파 27.5 위쪽에 몰려 있다', 'src': '출처: 불량품_판정_데이터.csv(가상, 1,000행), 저자 계산'}),
 },
 'sections': [
  {'id': 'sec-r4-1', 'nav': '들어가며', 'title': '들어가며 — 기준이 안 보이는 판정', 'blocks': [
    ('memo', 'e09', '여러분, "AI가 불량이라고 했어요"라는 말만으로 라인을 세울 수 있을까요? 저라면 못 세웁니다. 이유를 물어볼 거예요.'),
    ('p', '2회차 프롬프트 카드는 QWEN에게 한 행씩 판정을 받는 방식이었습니다. 문제는 어떤 기준으로 불량/정상을 갈랐는지 구분이 안 된다는 점이었습니다.'),
    ('p', '그래서 데이터를 주고 판정 기준을 도출하는 분류 모델을 만드는 프롬프트를 새로 썼습니다. 이 리포트가 답할 질문은 셋입니다. ① 판정 기준은 무엇인가 ② 어느 모델이 가장 쓸 만한가 ③ 기준으로 설명되지 않는 불량은 무엇인가.')]},
  {'id': 'sec-r4-2', 'nav': '배경', 'title': '배경 — 판재 라인의 네 측정값', 'blocks': [
    ('p', '판재는 경화 오븐(oven_temp_c)을 지나 폭 300mm로 재단(with_mm)되고, 표면 거칠기(surface_roughness_um)와 초음파(UT_dB) 검사를 받습니다. nomal_abnormal은 검사원의 최종 판정입니다(열 이름은 원자료 철자 그대로).'),
    ('p', '비유로 말하면, 숙련 검사원 옆에서 1,000번의 판정을 지켜본 뒤 "이분은 이걸 보고 고르시는구나"를 적어 내는 일입니다.'),
    ('memo', 'e07', '결정나무가 좋은 이유가 여기 있어요. 갈림길이 곧 기준표라서, 검사원 언어로 바로 옮길 수 있거든요.')]},
  {'id': 'sec-r4-3', 'nav': '방법', 'title': '방법 — 프롬프트 한 장, 모델 여섯 개', 'blocks': [
    ('prompt', COLAB),
    ('p', '같은 조건으로 이 리포트가 직접 돌렸습니다. 8:2 층화 분할(학습 800 · 테스트 200, 불량 비율 둘 다 10.0%), 학습 데이터 5겹 층화 교차검증, 알고리즘 6개(로지스틱 회귀 · 결정나무(깊이 4) · 랜덤 포레스트 · 그래디언트 부스팅 · KNN(5) · SVM), 난수 시드 42.'),
    ('p', '판정 기준은 전체 1,000개로 깊이 3 결정나무를 키워 갈림길을 읽고, 단순한 문턱 세 개로 정리했습니다. 계산 코드는 저장소 analysis/w04_classify.py에 있습니다.'),
    ('table', {'id': 'tab-r4-1', 'cap': '<표 1> 변수별 정상·불량 평균 (단위: mm, μm, dB, ℃)', 'head': ['변수', '정상 평균 (900)', '불량 평균 (100)', '정상 최대', '읽기'],
               'rows': [['폭 with_mm', '300.00', '301.40', '302.44', '불량이 넓다'], ['거칠기', '3.19', '4.14', '4.87', '불량 쪽으로 길게 퍼짐'], ['초음파 UT_dB', '19.97', '22.06', '28.38', '불량 쪽으로 길게 퍼짐'], ['오븐 온도', '179.98', '179.89', '182.75', '차이 없음']],
               'src': '출처: 불량품_판정_데이터.csv, 저자 계산'})]},
  {'id': 'sec-r4-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3 id="sec-r4-4-1">결과 1 · 판정 기준은 세 개</h3>'),
    ('table', {'id': 'tab-r4-2', 'cap': '<표 2> 세 기준으로 가른 1,000개 (단위: 개)', 'head': ['', '기준으로 정상', '기준으로 불량', '합계'],
               'rows': [['실제 정상', '899', '1', '900'], ['실제 불량', '23', '77', '100'], ['기준별 잡은 불량', '거칠기 4.9 초과 29 · 폭 302.5 초과 30 · 초음파 27.5 초과 18 (겹침 없음)', '', '']],
               'src': '출처: 불량품_판정_데이터.csv, 저자 계산 (정확도 97.6% · 재현율 77% · 정밀도 98.7%)'}),
    ('p', '<span class="fact">사실</span> 세 기준은 서로 다른 불량을 잡았습니다(29 + 30 + 18 = 77, 겹침 없음). 정상 900개 중 기준에 걸린 것은 1개뿐입니다.'),
    ('key', '판정 기준표: 거칠기 > 4.9μm 또는 초음파 > 27.5dB 또는 폭 > 302.5mm → 불량.'),
    ('p', '<span class="interp">해석</span> 정상 판재의 최대값(거칠기 4.87, 초음파 28.38, 폭 302.44) 바로 위에 문턱이 놓였습니다. 검사원이 실제로 쓰는 규격 한계와 가까울 것으로 읽습니다.'),
    ('html', '<h3 id="sec-r4-4-2">결과 2 · 모델 여섯 개는 정확도가 비슷하고 재현율이 다르다</h3>'),
    ('table', {'id': 'tab-r4-3', 'cap': '<표 3> 모델별 성능 (학습 800 교차검증 · 테스트 200)', 'head': ['모델', 'CV 정확도', '테스트 정확도', '재현율', '정밀도', '혼동행렬 [TN FP / FN TP]'],
               'rows': [['결정나무(깊이 4)', '97.0%', '96.0%', '80%', '80.0%', '176 4 / 4 16'], ['랜덤 포레스트', '97.1%', '95.5%', '80%', '76.2%', '175 5 / 4 16'], ['그래디언트 부스팅', '95.9%', '94.5%', '80%', '69.6%', '173 7 / 4 16'], ['KNN(5)', '97.1%', '96.0%', '70%', '87.5%', '178 2 / 6 14'], ['SVM', '97.1%', '95.0%', '70%', '77.8%', '176 4 / 6 14'], ['로지스틱 회귀', '94.4%', '93.0%', '55%', '68.8%', '175 5 / 9 11']],
               'src': '출처: 불량품_판정_데이터.csv, 8:2 층화 분할(시드 42), 5겹 층화 교차검증, 저자 계산'}),
    ('fig', {'id': 'fig-r4-3', 'cap': '[그림 3] 모델별 테스트 정확도와 재현율', 'w': 'r4-models', 'alt': '6개 모델의 테스트 정확도(93~96%)와 재현율(55~80%) 막대', 'src': '출처: 표 3과 같음'}),
    ('p', '<span class="fact">사실</span> 테스트 정확도는 93.0~96.0%로 3%p 안에 있지만, 재현율은 55~80%로 25%p 벌어졌습니다. 로지스틱 회귀는 불량 20개 중 9개를 놓쳤습니다.'),
    ('p', '<span class="interp">해석</span> 이 데이터의 기준은 "문턱"이라 직선 하나로 가르는 로지스틱 회귀보다, 문턱을 그대로 표현하는 결정나무가 잘 맞습니다. 정확도가 비슷하면 기준을 읽을 수 있는 결정나무를 고릅니다.'),
    ('html', '<h3 id="sec-r4-4-3">결과 3 · 놓친 23개는 폭의 회색 지대에 있다</h3>'),
    ('fig', {'id': 'fig-r4-2', 'cap': '[그림 2] 세 기준을 모두 통과한 판재의 폭 구간별 불량 비율', 'w': 'r4-gray', 'alt': '폭 구간별 불량 비율 막대. 300mm 이하 0%, 300~301 1.5%, 301~301.5 10%, 301.5~302 12.9%, 302~302.5 46.2%', 'src': '출처: 불량품_판정_데이터.csv 중 세 기준 통과 922개, 저자 계산'}),
    ('p', '<span class="fact">사실</span> 세 기준을 통과한 922개 중 불량 23개는 폭 300mm 이하에 0개, 300~301mm에 5개, 301~302.5mm에 18개입니다. 302~302.5mm 구간은 13개 중 6개(46%)가 불량입니다.'),
    ('p', '<span class="interp">해석</span> 폭은 302.5mm에서 딱 자르는 선이 아니라, 301mm부터 불량 확률이 서서히 오르는 회색 지대입니다. 측정 오차나 검사원의 판단 차이가 섞인 것으로 읽습니다.'),
    ('memo', 'e16', '이 23개가 오늘의 진짜 발견이에요. 기준을 더 낮추면 놓침은 줄지만 과잉 경보가 늘어요. 그 균형은 5주차 "보수형 분기"로 풉니다.')]},
  {'id': 'sec-r4-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 폭 불량은 "300mm에서 멀어진 정도"(양쪽)일 수 있다. 확인해 보니 폭이 좁은 쪽(298.5mm 미만 32개)에서는 불량이 없었습니다. 이 데이터에서는 넓은 쪽만 불량입니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 두 변수의 조합(예: 폭 301 + 거칠기 4.5)이 불량을 만들 수 있다. 깊이 4 나무와 앙상블도 재현율 80%에 머물러, 이 데이터에서는 강한 조합 효과가 보이지 않았습니다.'),
    ('p', '<span class="guess">추측</span> 놓친 23개 중 일부는 판정 라벨 자체의 흔들림(같은 판재를 다시 재면 정상으로 나올 가능성)일 수 있습니다. 재측정 데이터가 있으면 확인할 수 있습니다.')]},
  {'id': 'sec-r4-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 프롬프트 카드의 "판정"을 데이터에서 꺼낸 "기준표"로 바꿨습니다. 기준표는 작업자가 따를 수 있고, 고객에게 설명할 수 있고, 틀리면 고칠 수 있습니다.'),
    ('p', '한계: ① 가상 데이터 1,000개 ② 테스트 불량 20개라 불량 1개가 재현율을 5%p씩 움직임 ③ 원자료의 m1·m2 추가 데이터(판정샘플 40, 불량 18·50·100 학습 데이터)는 파일이 없어 다루지 못함 ④ 오븐 온도가 무관하다는 것은 180℃ 안팎의 좁은 범위 안에서의 결과입니다.'),
    ('memo', 'e08', '다음 주에는 이 기준표가 작업지시서의 "분기"가 됩니다. 숫자 한 줄이 행동 한 줄로 바뀌는 걸 보게 될 거예요.')]},
 ],
 'refs': ['안상선, 「코딩 없는 제조업의 AI 데이터 분석」 1회차·2회차 강의 교안, 2026', '안상선, 불량품 판정 분류 모델 Colab 프롬프트(수업 자료), 2026', 'Matzka, S. (2020). AI4I 2020 Predictive Maintenance Dataset. UCI Machine Learning Repository', '이 저장소 analysis/w04_classify.py — 저자 계산(scikit-learn)'],
 'sources': [('원자료', '불량품_판정_데이터.csv(가상) · 수업 프롬프트'), ('계산', '저자 계산 (analysis/w04_classify.py)')],
 'notes': '데이터는 수업용 가상 데이터입니다. 모델 성능은 시드 42의 한 번 분할 결과입니다.',
}
RP['js'] = _DATA + r'''
W['r4-scatter']=function(s){var NS='http://www.w3.org/2000/svg';s.setAttribute('viewBox','0 0 600 340');s.setAttribute('class','chart');var X=function(v){return 50+(v-1.5)/(8-1.5)*530},Y=function(v){return 310-(v-10)/(40-10)*290};D4.r.forEach(function(r,i){var c=document.createElementNS(NS,'circle');c.setAttribute('cx',X(r));c.setAttribute('cy',Y(D4.u[i]));c.setAttribute('r',D4.y[i]?3.5:2.2);c.setAttribute('fill',D4.y[i]?'#f0604d':'rgba(94,227,156,.45)');s.appendChild(c);});[[X(4.9),20,X(4.9),310],[50,Y(27.5),580,Y(27.5)]].forEach(function(l){var e=document.createElementNS(NS,'line');e.setAttribute('x1',l[0]);e.setAttribute('y1',l[1]);e.setAttribute('x2',l[2]);e.setAttribute('y2',l[3]);e.setAttribute('stroke','#f1b646');e.setAttribute('stroke-dasharray','6 4');e.setAttribute('stroke-width',2);s.appendChild(e);});var t=document.createElementNS(NS,'text');t.setAttribute('x',300);t.setAttribute('y',335);t.textContent='표면 거칠기(μm) → · 노란 점선: 4.9μm, 27.5dB';s.appendChild(t);var t2=document.createElementNS(NS,'text');t2.setAttribute('x',4);t2.setAttribute('y',14);t2.textContent='↑ 초음파(dB)';s.appendChild(t2);};
W['r4-models']=function(s){var M=['결정나무','랜덤포레스트','그래디언트','KNN','SVM','로지스틱'];Chart.bars(s,{labels:M,series:[{name:'테스트 정확도',color:'#82b8ff',values:[96,95.5,94.5,96,95,93]},{name:'재현율',color:'#f0604d',values:[80,80,80,70,70,55]}],min:0,max:100,values:true,fmt:function(v){return v+'%'},h:250});};
W['r4-gray']=function(s){Chart.bars(s,{labels:['~299','299~300','300~301','301~301.5','301.5~302','302~302.5'],series:[{name:'불량 비율(%)',color:'#f0604d',values:[0,0,1.5,10,12.9,46.2]}],min:0,max:55,values:true,fmt:function(v){return v+'%'},h:240});};
'''
