# 5주차 · 작업지시서와 한 페이지 앱
import os, json
_H = os.path.dirname(__file__)
_AI = open(os.path.join(_H, '..', 'data_ai4i.js'), encoding='utf-8').read()
M5 = [
  {'id': 'A0091', 'label': 'CNC-1 · wear 0.94 · twf', 'zone': '위험', 'act': '즉시 공구 교체 · 폐기 후 신규 등록', 'who': '팀장 최씨 + 안전요원 김씨', 'due': '1시간 내'},
  {'id': 'A0092', 'label': 'CNC-2 · wear 0.43 · hdf', 'zone': '위험', 'act': '라인 정지 · 냉각 15분 후 재가동 판단', 'who': '라인 책임자 이씨', 'due': '15분 후 재판단'},
  {'id': 'A0093', 'label': 'CNC-3 · wear 0.55 · pwf', 'zone': '위험', 'act': '전원 점검 · UPS 가동 · 전기팀 호출', 'who': '전기팀 + 이씨', 'due': '즉시'},
  {'id': 'A0095', 'label': 'CNC-4 · wear 0.30 · osf', 'zone': '위험', 'act': '절삭 조건 낮춤 · 공구·고정구 점검', 'who': '라인 책임자 이씨', 'due': '1시간 내'},
  {'id': 'A0013', 'label': 'CNC-5 · wear 0.53 · 고장 없음', 'zone': '주의', 'act': '점검 주기 절반 단축 · 교체 일정 앞당김', 'who': '라인 책임자 이씨', 'due': '4시간 내'},
  {'id': 'A0005', 'label': 'CNC-6 · wear 0.05 · 고장 없음', 'zone': '정상', 'act': '정상 가동 기록 · 다음 점검 등록', 'who': '점검자 박씨', 'due': '당일 17:00'},
]

APP_PROMPT = '''#역할
너는 제조 현장용 한 페이지 HTML 앱을 만드는 도우미다.
#맥락
CNC 가공 셀의 점검 결과를 작업자가 받아 바로 움직이게 하는 "분기형 작업지시서" 앱이다. 코드는 작업자에게 보이지 않는다.
#조건
1) HTML 파일 하나(CSS·JS 포함), 외부 라이브러리 없음, 인터넷 없이 열린다.
2) 입력 폼: air_temp_k, process_temp_k, rotational_speed_rpm, torque_nm, tool_wear_min (숫자가 아니면 거부, 범위 밖이면 빨간 테두리, 기본값 채움)
   + 분류 결과(정상/twf/hdf/pwf/osf/rnf) 선택 + 회귀 결과 estimated_wear(0~1) 입력
3) 분기: 유형이 정상이 아니면 유형 분기 우선, 정상이면 점수 분기(0.40/0.70)
4) 결과 카드 다섯 칸: ① 결과 라인 ② 작업자 ③ 작업 항목(동사+사물) ④ 완료 시각 ⑤ 메모(보고 회선)
5) [인쇄] 버튼: A4 한 장, 글자 11pt 이상, 검정 잉크만
#형식
완성된 HTML 전체를 코드 블록 하나로.
#예시
estimated_wear 0.78, 분류 hdf → 위험 · 팀장 최씨 + 안전요원 김씨 · 라인 정지·냉각 · 1시간 내 · 품질팀·생산팀 보고'''

CH = {
 'slug': 'w05', 'num': '05',
 'title': '작업지시서와 한 페이지 앱',
 'eyebrow': '5주차 · SECTION 2 · 데이터 · CNC 밀링 가공 셀 (AI4I)',
 'desc': '스마트 제조 5주차 — 분류·회귀 숫자 한 줄을 작업자가 받아 움직이는 분기형 작업지시서로 옮기고, 입력 폼·결과 카드·인쇄가 있는 HTML 한 페이지 앱으로 마감합니다.',
 'q': '점검 결과 숫자 한 줄이 도착하면, 작업자는 무엇을 하는가?',
 'lead': '"wear_proxy 0.78" — 점검표는 여기서 끝납니다. 그다음 행동이 적혀야 작업지시서가 됩니다. 오늘은 CNC 가공 셀에서 숫자를 행동 카드로 옮기는 분기 규칙을 만들고, 그 규칙을 한 페이지 앱으로 돌립니다.',
 'scene_alt': 'CNC 밀링 가공 셀 3D. 가공기 여섯 대와 로딩 로봇이 있고, 설비마다 정상(초록)·주의(노랑)·위험(빨강 깜빡임) 램프가 켜져 있다. 설비를 누르면 벽 보드에 작업지시서 카드가 뜬다.',
 'scene_hud': '3D · CNC 가공 셀 — 설비나 램프를 누르면 작업지시서 카드가 뜹니다',
 'scene_opts': {'cam': [2, 16, 25], 'target': [-1, 1.5, 1]},
 'kpis': [('0.40 · 0.70', '점수 분기의 두 임계값', 'a'), ('6갈래', '유형 분기: 정상·twf·hdf·pwf·osf·rnf', 'm'), ('5칸', '결과·작업자·항목·시한·메모', 'g'), ('4/6', '점수만 쓰면 놓치는 고장 (AI4I 미니)', 'r')],
 'hero_talk': [
   ('doc', 'e07', 'CNC 가공 셀입니다. 램프가 빨간데, 작업자는 무엇을 해야 할까요? 숫자만 적힌 점검표로는 모릅니다.'),
   ('robo', 'e16', 'wear 0.78! 숫자를 크게 써 붙이면 다 알아봅니다!'),
   ('fly', 'e09', '그래서 누가, 뭘, 언제까지? 그 줄이 비어 있으면 작업자는 멈춰.'),
   ('moa', 'e07', '저는 정장 입고 작업지시서 결재 받으러 왔어요.'),
 ],
 'three': ['분류·회귀 결과(숫자·라벨)를 "누가 · 무엇을 · 언제까지"가 적힌 분기형 작업지시서 카드로 옮깁니다.',
           '숫자만 있는 점검표는 행동이 빠져 작업자를 멈추게 하고 책임을 흐리게 합니다. 분기 규칙이 있어야 같은 상황에서 누구나 같은 행동을 합니다.',
           '입력 폼 → 결과 카드 → 인쇄의 한 페이지 앱으로, 점검 결과가 바로 현장 행동이 됩니다.'],
 'abbr': [('twf', 'Tool Wear Failure', '공구 마모 고장'), ('hdf', 'Heat Dissipation Failure', '열 방산 고장'), ('pwf', 'Power Failure', '전력 고장'),
          ('osf', 'Overstrain Failure', '과부하 고장'), ('rnf', 'Random Failure', '무작위 고장'), ('UPS', 'Uninterruptible Power Supply', '무정전 전원 장치'),
          ('MAE', 'Mean Absolute Error', '평균 절대 오차'), ('RMSE', 'Root Mean Square Error', '제곱 평균 오차의 제곱근')],
 'why': [('결과만 — 행동 없음', 'wear 0.78, 그래서 무엇을? 작업자는 빠른 결정을 요구받다가 그 자리에서 멈춥니다.'),
         ('책임이 흐려진다', '모델의 답인지 사람 판단인지 문서가 답하지 않으면 책임이 흐립니다.'),
         ('한 장이 안 된다', '매뉴얼 17쪽, 양식 5종 — 지금 당장 어느 장을 펴야 할지 모릅니다.')],
 'big_lead': '네 섹션이 한 작업지시서를 만듭니다.',
 'big': [('3.1 왜', '점검표의 한계와 작업지시서의 세 약속(행동·책임·한 장)'), ('3.2 분기', '점수형(0.40/0.70)과 유형형(6갈래), 혼합형·보수형'),
         ('3.3 본문', '회의록·매뉴얼·점검표를 한 장으로, 빈칸 다섯 점검'), ('3.4 앱', '입력 폼 → 결과 카드 → 인쇄, 페이지 이동 없음')],
 'glossary': {
   '작업지시서': ['작업지시서', '문서', '결과 한 줄 + 행동 한 줄 + 책임 한 줄을 한 장에 담은 카드입니다.'],
   '분기': ['분기', '규칙', '결과에 따라 행동이 갈라지는 지점입니다. 기준이 명확해야 누구나 같은 행동을 합니다.'],
   '점수 분기': ['점수 분기', '규칙', '회귀 숫자(0~1)를 임계값 두 개로 정상·주의·위험 세 구간으로 가르는 것입니다.'],
   '유형 분기': ['유형 분기', '규칙', '분류 라벨(고장 유형)에 따라 행동을 가르는 것입니다.'],
   '보수형': ['보수형 분기', '규칙', '놓침 비용이 큰 곳에서 임계값을 낮춰(0.40 → 0.30) 더 일찍 행동하게 하는 것입니다.'],
 },
 'subs': [
  {'id': 'sec-5-1', 'title': '점검표에서 비어 있는 세 항목', 'tags': ['일상: 진단서만 받은 환자', '현장: wear 0.78'],
   'pair': ('일상으로 치면', '병원에서 "혈압 165"라고만 적힌 종이를 받았다. 약을 먹어야 하나, 다시 와야 하나, 누구에게 물어야 하나 적혀 있지 않다.',
            '공장에서는', '점검표에 "wear_proxy 0.78"만 있다. 교체할지, 누가 할지, 언제까지인지 비어 있다. 결과만 있고 행동·책임·한 장이 없다.'),
   'body': ['분류·회귀 모델이 좋은 숫자를 돌려줘도, 그다음 행동이 빈칸이면 작업자는 멈춥니다. 현장에서 흔들리는 것은 늘 이 부분입니다.'],
   'talk': [('asst', 'e09', '그럼 숫자 옆에 "교체하세요"만 붙이면 되나요?'), ('fly', 'e09', '누가? 언제까지? 교체 말고 다른 고장이면?'), ('sia', 'e07', '세 항목을 하나씩 채워 보겠습니다.')],
   'widget': ('w5-blank', '<div class="ptitle">비교 · 점검표 한 줄 vs 작업지시서 한 장</div><div class="ctrl"><button class="bt on" data-m="0" type="button">점검표</button><button class="bt" data-m="1" type="button">작업지시서</button></div><div id="bl-out"></div>'),
   'limit': '모든 결과가 작업지시서가 필요한 것은 아닙니다. 일상 점검처럼 한 가지 작업이면 책임과 시한만 적은 단순 카드로 충분합니다(5.2).',
   'quiz': [{'q': '점검표의 세 한계가 아닌 것은?', 'o': ['행동이 없다', '책임이 흐리다', '숫자가 틀리다'], 'a': 2, 'why': '숫자가 맞아도 행동·책임·한 장이 비면 작업자가 멈춥니다.'}]},

  {'id': 'sec-5-2', 'title': '세 문서를 한 장으로 — 점검표 + 회의록 + 매뉴얼', 'tags': ['구성: 다섯 칸', '단순 카드와 분기 카드'],
   'body': ['점검표는 결과만, 회의록은 결정만, 매뉴얼은 방법만 갖고 있습니다. 세 가지가 한 장에 닿으면 비로소 행동이 시작됩니다.',
            '<div class="tw"><table class="tb"><tr><th>카드 칸</th><th>어디서 오나</th><th>예</th></tr>'
            '<tr><td>① 결과 라인</td><td>점검표</td><td>wear_proxy 0.78 → 위험</td></tr>'
            '<tr><td>② 작업자</td><td>회의록(누가 맡기로 했나)</td><td>팀장 최씨 + 안전요원 김씨</td></tr>'
            '<tr><td>③ 작업 항목</td><td>매뉴얼(절차)</td><td>① 안전 점검 ② 전원 차단 ③ 교체 ④ 기록 ⑤ 보고 — 평균 15분</td></tr>'
            '<tr><td>④ 완료 시각</td><td>회의록(기한)</td><td>1시간 내 결정</td></tr>'
            '<tr><td>⑤ 메모</td><td>회의록(보고·갱신)</td><td>품질팀·생산팀 보고, 30분 단위 갱신</td></tr></table></div>',
            '결과에 따라 행동이 갈라지지 않는 일(일상 점검표 회수 등)은 분기 없이 작업자·항목·시한만 적은 단순 카드면 됩니다.'],
   'talk': [('moa', 'e12', '회의록 담당이 저라서, ②④⑤칸은 제가 채울게요!'), ('robo', 'e07', '저는 ①칸 숫자를 맡겠습니다.'), ('x2', 'e09', '(…끄적)')],
   'widget': ('w5-merge', '<div class="ptitle">조립 · 세 문서에서 한 칸씩 가져오기</div><div class="ctrl" id="mg-bt"></div><div id="mg-out"></div>'),
   'limit': '회의록·매뉴얼이 없는 공장도 많습니다. 그럴 때는 숙련자 인터뷰가 먼저입니다(14주차, 빈 슬롯).',
   'quiz': [{'q': '"평균 15분, ① 안전 점검 ② 전원 차단…"은 어느 문서에서 오나?', 'o': ['점검표', '회의록', '매뉴얼'], 'a': 2, 'why': '작업 절차는 매뉴얼의 몫입니다.'}]},

  {'id': 'sec-5-3', 'title': '같은 숫자, 다른 구간, 다른 행동 — 분기형', 'tags': ['원리: 분기', '구간 → 행동'],
   'pair': ('일상으로 치면', '체온 37.2도는 "지켜보기", 38.5도는 "해열제", 40도는 "응급실". 숫자를 외울 필요 없이 구간만 보면 행동이 적혀 있다.',
            '작업지시서에서는', '점검 결과(0.0~1.0)가 ≤0.40이면 정상, 0.40~0.70이면 주의, ≥0.70이면 위험. 작업자는 0.78인지 0.52인지 기억할 필요 없이 구간만 본다.'),
   'body': ['분기가 없는 작업지시서는 한 장의 줄글이 됩니다. 분기는 그 글 안에 갈래를 만듭니다. 기준이 명확해야 작업자도 같은 행동을 합니다.'],
   'talk': [('asst', 'e07', '그래서 구간 이름(정상·주의·위험)이 숫자보다 먼저 보이게 카드를 만드는 거군요.'), ('fly', 'e10', '맞아. 숫자는 근거로, 구간은 행동으로.')],
   'widget': ('w5-score', '<div class="ptitle">실험 · 점수 하나 → 구간 → 카드</div><div class="ctrl"><div class="group"><span class="glabel">wear_proxy</span><input type="range" min="0" max="1" step="0.01" value="0.78" id="sc-v"><span class="val" id="sc-vv"></span></div></div><div id="sc-out"></div>'),
   'limit': '0.40·0.70은 수업용 경계입니다. 실제 경계는 고장 이력, 교체 비용, 놓침 비용으로 정합니다.',
   'quiz': [{'q': '분기형 작업지시서에서 작업자가 먼저 보는 것은?', 'o': ['숫자 0.78', '구간 이름(위험)과 그 행동'], 'a': 1, 'why': '구간만 보면 행동이 적혀 있게 만드는 것이 분기형입니다.'}]},

  {'id': 'sec-5-4', 'title': '점수 분기 — 임계값 두 개로 셋', 'tags': ['회귀 결과용', '0.21 · 0.52 · 0.78 · 0.95'],
   'body': ['<div class="tw"><table class="tb"><tr><th>점수</th><th>구간</th><th>행동</th><th>작업자</th><th>시한</th></tr>'
            '<tr><td>0.21</td><td>정상</td><td>가동 유지, 다음 점검 주기 등록</td><td>점검자 박씨</td><td>당일 17:00</td></tr>'
            '<tr><td>0.52</td><td>주의</td><td>점검 주기 절반 단축, 교체 일정 한 단계 앞당김</td><td>라인 책임자 이씨</td><td>4시간 내</td></tr>'
            '<tr><td>0.78</td><td>위험</td><td>즉시 교체 또는 가동 중단</td><td>팀장 최씨 + 안전요원</td><td>1시간 내</td></tr>'
            '<tr><td>0.95</td><td>이미 늦음</td><td>라인 정지, 보고 기록 — 다음 점검은 의미 없음</td><td>팀장 최씨</td><td>즉시</td></tr></table></div>',
            '점수 분기는 회귀 결과(마모량 같은 숫자)에 어울립니다. 4주차 회귀 카드의 estimated_wear가 바로 이 표에 들어갑니다.'],
   'talk': [('robo', 'e19', '0.69는 주의, 0.70은 위험! 깔끔합니다!'), ('fly', 'e09', '0.69와 0.70이 정말 그렇게 다를까? 경계 근처는 어떻게 할 건데?'), ('doc', 'e10', '그 질문이 5.6 보수형 분기로 이어집니다.')],
   'widget': ('w5-day', '<div class="ptitle">시나리오 · 더미 공장 A라인의 하루 (교안)</div><div class="ctrl" id="dy-bt"></div><div id="dy-out"></div>'),
   'limit': '하루 시나리오의 시각·점수는 교안의 예시입니다.',
   'quiz': [{'q': 'wear 0.52의 시한은?', 'o': ['1시간 내', '4시간 내', '당일 17:00'], 'a': 1, 'why': '주의 구간은 4시간 내 점검 주기 단축입니다.'}]},

  {'id': 'sec-5-5', 'title': '유형 분기 — 고장 유형마다 다른 점검', 'tags': ['분류 결과용', '여섯 갈래'],
   'body': ['같은 machine_failure = 1이라도 twf(공구 마모)와 hdf(열 방산)는 다른 점검으로 이어집니다. 유형 분기는 분류 라벨의 이름이 갈래입니다.',
            '<div class="tw"><table class="tb"><tr><th>라벨</th><th>뜻</th><th>행동</th></tr>'
            '<tr><td>정상</td><td>machine_failure = 0</td><td>가동 유지, 다음 점검까지 유예</td></tr>'
            '<tr><td>twf</td><td>공구 마모</td><td>즉시 교체 — 해당 공구 폐기 후 신규 등록</td></tr>'
            '<tr><td>hdf</td><td>열 방산</td><td>라인 정지 · 냉각 — 15분 후 재가동 판단</td></tr>'
            '<tr><td>pwf</td><td>전력</td><td>전원 점검 — UPS 가동 · 전기팀 호출</td></tr>'
            '<tr><td>osf</td><td>과부하</td><td>절삭 조건(토크·이송) 낮춤 · 공구·고정구 점검 <span class="stamp">이 페이지 예시</span></td></tr>'
            '<tr><td>rnf</td><td>무작위</td><td>재측정 · 관찰 기록 · 원인 미상 보고 <span class="stamp">이 페이지 예시</span></td></tr></table></div>',
            '교안은 여섯 갈래 중 네 갈래(정상·twf·hdf·pwf)의 행동을 적었습니다. osf·rnf 행동은 이 페이지가 채운 예시이니, 실제로는 회의록으로 정합니다.'],
   'talk': [('asst', 'e04', 'hdf인데 마모는 0.43이면, 점수로는 주의인데요?'), ('fly', 'e10', '그래서 유형 분기가 따로 있어야 해. 열 문제를 공구 교체로 풀 순 없잖아.'), ('x3', 'e04', '(삐빅?)')],
   'widget': ('w5-type', '<div class="ptitle">실험 · 고장 유형을 골라 카드 보기</div><div class="ctrl" id="ty-bt"></div><div id="ty-out"></div>'),
   'limit': 'AI4I 미니 데이터에는 한 행에 유형이 둘(twf·hdf)인 경우가 있습니다. 그럴 때는 더 위험한 쪽(라인 정지)을 먼저 하고 둘 다 적습니다.',
   'quiz': [{'q': 'pwf 카드의 행동은?', 'o': ['공구 교체', '전원 점검·UPS·전기팀 호출', '냉각'], 'a': 1, 'why': '전력 고장은 전원부터 봅니다.'}]},

  {'id': 'sec-5-6', 'title': '분기 기준 네 가지 — 점수형 · 유형형 · 혼합형 · 보수형', 'tags': ['설계: 분기 기준', 'AI4I 미니 100행'],
   'body': ['① 점수형 — 숫자 구간이 갈래(회귀 결과). ② 유형형 — 라벨 이름이 갈래(분류 결과). ③ 혼합형 — 점수로 구간을 가른 뒤 유형으로 행동을 가른다. ④ 보수형 — 놓침 비용이 큰 곳에서 경계를 낮춘다(0.40 → 0.30).',
            'AI4I 미니 100행에 점수형만 쓰면 위험 카드 13장 중 실제 고장은 2장뿐이고, 고장 6건 중 4건은 정상·주의 카드로 나갑니다. 특히 과부하 고장 A0095는 마모 0.30이라 정상 카드를 받습니다.'],
   'talk': [('robo', 'e24', '과부하로 멈춘 설비에 "정상 가동" 카드가 나갔다고요?'), ('fly', 'e10', '마모 숫자 하나로 모든 고장을 보려 해서 그래. 혼합형이 필요해.'), ('sia', 'e10', '아래에서 네 기준을 바꿔 가며 카드 분포를 보겠습니다.')],
   'widget': ('w5-mix', '<div class="ptitle">실험 · AI4I 미니 100행에 분기 기준 적용 (실제 수업 데이터)</div><div class="ctrl" id="mx-bt"></div><div class="kpis" id="mx-k"></div><div class="eq" id="mx-out" aria-live="polite"></div>'),
   'limit': '혼합형에서 유형은 데이터의 정답 라벨을 그대로 썼습니다. 실제로는 분류 모델(또는 QWEN)의 답이 들어가므로 그만큼 틀릴 수 있습니다.',
   'quiz': [{'q': '마모는 낮은데 과부하 고장이 난 설비를 잡는 기준은?', 'o': ['점수형', '유형형·혼합형'], 'a': 1, 'why': '고장 유형이 행동을 정해야 합니다.'}]},

  {'id': 'sec-5-7', 'title': '행동 매핑 — 누가 · 무엇을 · 언제까지', 'tags': ['구성: 책임의 위치', '현장: 박씨·이씨·최씨'],
   'body': ['분기가 구간을 알려 준다면, 행동 매핑은 그 구간에 누가·무엇을·언제까지를 붙입니다. 정상은 점검자 박씨가 당일 17:00까지, 주의는 라인 책임자 이씨가 4시간 내, 위험은 팀장 최씨와 안전요원이 1시간 내입니다.',
            '구간이 위로 갈수록 책임자 직급이 오르고 시한이 짧아집니다. 위험 구간에는 보고 회선(품질팀·생산팀)이 꼭 붙습니다.'],
   'talk': [('moa', 'e12', '이름을 다 적으니 누구한테 전화할지 바로 보여요.'), ('asst', 'e07', '아래에서 우리 공장 이름으로 바꿔 볼게요.')],
   'widget': ('w5-map', '<div class="ptitle">편집 · 우리 공장 행동 매핑표</div><div class="tw" id="mp-tb"></div><div class="eq" id="mp-out" aria-live="polite"></div>'),
   'limit': '편집한 내용은 저장되지 않습니다. 인쇄하거나 복사해 두세요.',
   'quiz': [{'q': '위험 구간에 반드시 붙어야 하는 것은?', 'o': ['장식 그림', '보고 회선(품질팀·생산팀)', '긴 설명'], 'a': 1, 'why': '보고 회선이 없으면 위험 구간에서 책임이 사라집니다.'}]},

  {'id': 'sec-5-8', 'title': '자주 빠지는 빈칸 다섯 가지', 'tags': ['점검: 다섯 빈칸', '방법: 자가 점검'],
   'body': ['① 책임자 이름이 구체적이지 않다 — 성 하나·직함 하나라도 적습니다. ② 임계값이 숫자로 적혀 있지 않다 — 0.40과 0.70, 두 숫자가 있어야 구간이 정의됩니다.',
            '③ 완료 시한이 "곧", "ASAP", "검토 후" — 사실상 없는 것입니다. "1시간 내", "당일 17:00"처럼 시간 단위로 씁니다. ④ 작업 항목이 "검토", "판단"뿐 — 동사 + 사물(전원 차단, 공구 교체)이 있어야 행동이 시작됩니다.',
            '⑤ 보고 회선이 없다 — 위험 부근에서 책임이 사라집니다.'],
   'talk': [('robo', 'e07', '제 카드: "담당: 관련 부서, 항목: 검토, 시한: ASAP". 완벽합니다!'), ('fly', 'e03', '빈칸 다섯 개를 다 채웠네, 반대로.'), ('asst', 'e15', '아래 검사기에 넣어 볼게요…')],
   'widget': ('w5-lint', '<div class="ptitle">검사기 · 작업지시서 문장의 빈칸 찾기</div><textarea id="ln5" rows="5" style="width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:8px;padding:8px;font:inherit">결과: wear_proxy 0.78\n담당: 관련 부서\n항목: 검토\n시한: ASAP\n메모: -</textarea><div class="ctrl"><button class="bt primary" id="ln5-bt" type="button">빈칸 검사</button><button class="bt" id="ln5-ok" type="button">좋은 예 넣기</button></div><div class="insight" id="ln5-out" aria-live="polite"></div>'),
   'limit': '검사기는 단어 규칙으로만 봅니다. 내용이 맞는지(그 사람이 그 일을 할 수 있는지)는 사람이 확인합니다.',
   'quiz': [{'q': '"시한: 검토 후"는 몇 번 빈칸인가?', 'o': ['①', '③', '⑤'], 'a': 1, 'why': '모호한 시한은 사실상 시한이 없는 것입니다.'}]},

  {'id': 'sec-5-9', 'title': 'HTML 한 페이지 앱 — 입력 폼 · 결과 카드 · 인쇄', 'tags': ['앱: 실제로 작동', '약속: 페이지 이동 없음'],
   'body': ['한 페이지 앱의 약속은 넷입니다. ① 입력 영역이 있다 ② 분기 결과 카드가 있다 ③ 인쇄 버튼이 있다 ④ 페이지 이동이 없다.',
            '입력 폼은 숫자가 아닌 값은 거부하고, 범위 밖은 빨간 테두리로 표시하고, 기본값으로 바로 시작하게 합니다. 결과 카드는 다섯 칸이 동시에 채워집니다. 인쇄는 A4 한 장, 글자 11pt 이상, 검정 잉크만입니다.',
            '아래 앱은 이 페이지에서 실제로 작동합니다. 분류 결과와 회귀 결과 칸에는 QWEN이 돌려준 JSON 값을 옮겨 넣으면 됩니다.'],
   'talk': [('doc', 'e08', '작업자는 이 화면 하나만 보면 됩니다. 화면을 닫아도 카드는 인쇄되어 손에 남습니다.'), ('x1', 'e01', '(반짝)')],
   'widget': ('w5-app', '<div class="ptitle">한 페이지 앱 · 분기형 작업지시서 (실제 작동)</div><div class="ctrl" style="align-items:flex-end" id="ap-form"></div><div class="ctrl"><button class="bt primary" id="ap-run" type="button">카드 만들기</button><button class="bt" id="ap-print" type="button">인쇄 (A4 한 장)</button></div><div id="ap-card" aria-live="polite"></div>'),
   'code': [('input type="number" min max', '숫자만, 범위 밖이면 표시'), ('if (type !== "정상") … else if (wear >= 0.7)', '유형 분기 우선, 그다음 점수 분기'), ('window.print()', '인쇄 버튼')],
   'limit': '이 앱은 QWEN을 직접 부르지 않습니다. 분류·회귀 답은 사람이 옮겨 넣습니다. 자동 연결은 15주차 자동화 흐름(빈 슬롯)에서 다룹니다.',
   'quiz': [{'q': '한 페이지 앱의 약속이 아닌 것은?', 'o': ['입력 영역', '결과 카드', '여러 페이지로 이동'], 'a': 2, 'why': '페이지 이동 없이 한 화면에서 끝나는 것이 약속입니다.'}]},

  {'id': 'sec-5-10', 'title': 'QWEN으로 앱 만들기 — 분류 앱 · 회귀 앱 · 지시서 앱', 'tags': ['프롬프트: 앱 생성', '자료: 03·04·05 md'],
   'body': ['수업 자료의 03-classification-app.md, 04-regression-app.md, 05-instruction-app.md는 QWEN에게 각각 분류 앱·회귀 앱·작업지시서 앱을 HTML로 만들게 하는 지시서입니다. 이 페이지에는 그 파일 원문이 없어, 같은 목적의 프롬프트를 5원칙으로 다시 썼습니다.',
            '<div class="prompt" data-raw="' + APP_PROMPT.replace('"', '&quot;') + '">' + APP_PROMPT.replace('<', '&lt;') + '</div>',
            'QWEN이 만든 HTML은 바로 열어 보기 전에 다섯 가지를 확인합니다. ① 외부 주소를 부르지 않는가 ② 숫자가 아닌 값을 막는가 ③ 0.40·0.70이 코드에 그대로 있는가 ④ 카드 다섯 칸이 다 있는가 ⑤ 인쇄가 한 장에 들어가는가.'],
   'talk': [('robo', 'e19', 'QWEN이 만든 앱, 화려합니다! 애니메이션도 있습니다!'), ('fly', 'e09', '화려한 것보다 0.70이 0.7로 제대로 들어갔는지부터 봐.'), ('moa', 'e10', '확인 다섯 개를 체크리스트로 붙여 둘게요.')],
   'widget': ('w5-qa', '<div class="ptitle">점검 · QWEN이 만든 앱 받기 전 다섯 확인</div><div class="ctrl" id="qa-bt"></div><div class="eq" id="qa-out" aria-live="polite"></div>'),
   'limit': '같은 프롬프트라도 QWEN이 만든 HTML은 매번 다릅니다. 마음에 드는 결과가 나오면 파일로 보관하고, 프롬프트도 함께 기록합니다(OT의 "프롬프트를 기록해 재사용").',
   'quiz': [{'q': 'QWEN이 만든 앱에서 가장 먼저 확인할 것은?', 'o': ['색상', '분기 임계값과 다섯 칸이 맞는가', '글꼴'], 'a': 1, 'why': '보기 좋은 것보다 규칙이 맞는 것이 먼저입니다.'}]},

  {'id': 'sec-5-11', 'title': '회귀 앱 점검 — MAE와 RMSE', 'tags': ['지표: MAE · RMSE', '발견: few-shot 예시값'],
   'fx': {'q': 'MAE랑 RMSE는 뭐가 달라요? 둘 다 "평균 오차" 아니에요?',
          'school': '절댓값, 제곱과 제곱근, 평균',
          'eq': 'MAE = 평균 |실제 − 추정| · RMSE = √(평균 (실제 − 추정)²) · <b>RMSE ≥ MAE</b>',
          'rows': [('MAE', '평균적으로 얼마나 빗나가나'), ('RMSE', '큰 오차에 더 무겁게 벌점'), ('차이가 크다', '몇 개가 크게 빗나갔다는 신호')],
          'calc': '회귀 카드의 few-shot 예시는 wear 80분 → 0.21, 220분 → 0.78입니다. 데이터의 마모 정의(가동 시간 ÷ 약 253)로는 0.32, 0.87입니다. 두 점의 MAE는 0.10, RMSE도 약 0.10입니다.',
          'comment': '예시가 0.1쯤 낮으니까, 앱이 마모를 늘 낮게 볼 수도 있겠네요!'},
   'body': ['교안 자료의 회귀 앱 결과표에는 MAE·RMSE 칸이 비어 있습니다. 여러분이 QWEN 답을 실제 값과 비교해 채울 곳입니다.',
            '이 페이지가 찾은 점은, few-shot 예시값이 데이터의 마모 정의보다 약 0.1 낮다는 것입니다. 예시를 따라 답하면 위험 경계 0.70에 닿는 시점이 실제보다 늦어질 수 있습니다(실습 리포트).'],
   'talk': [('fly', 'e10', '예시를 데이터에서 직접 뽑아 넣으면 이 문제가 줄어.'), ('asst', 'e07', '아래 표에 QWEN 답을 넣고 MAE·RMSE를 바로 계산해 볼게요.')],
   'widget': ('w5-mae', '<div class="ptitle">계산기 · QWEN 회귀 답 채점 (AI4I 미니 5행)</div><div class="tw" id="ma-tb"></div><div class="eq" id="ma-out" aria-live="polite"></div>'),
   'limit': '5행으로 낸 MAE·RMSE는 흔들림이 큽니다. 최소 20~30행으로 채점하는 것이 좋습니다.',
   'quiz': [{'q': 'MAE 0.05, RMSE 0.15라면?', 'o': ['고르게 조금씩 빗나감', '몇 개가 크게 빗나감'], 'a': 1, 'why': 'RMSE가 MAE보다 훨씬 크면 큰 오차가 섞여 있다는 뜻입니다.'}]},

  {'id': 'sec-5-12', 'title': '자주 묻는 다섯 가지와 정리', 'tags': ['FAQ', '다음: REVIEW'],
   'body': ['Q1 같은 입력에 답이 달라요 → few-shot 예시를 정상·임계 두 구간으로 고정하고 다시 받습니다. Q2 추정값이 0~1 밖이에요 → "0.0~1.0 사이, 그 외는 무효"를 출력 형식에 적습니다.',
            'Q3 카드에 완료 시각이 없어요 → 시한이 없으면 작업지시서가 아닙니다. 다시 씁니다. Q4 분류·회귀 답이 둘 다 마음에 안 들어요 → 보수형 분기로 임계값을 낮추고 자가 점검합니다.',
            'Q5 작업자가 카드를 거부해요 → 카드 다섯 칸을 다시 묻습니다. 빈칸이 있으면 이유가 있습니다.'],
   'talk': [('doc', 'e16', '카드 한 장이 작업자 손에 닿으면 그것이 작업지시서입니다. 다음 주는 1~5주를 다시 보는 REVIEW입니다.'), ('sia', 'e07', '6주에는 면류 공장으로 다섯 주를 한 번에 엮겠습니다.')],
   'widget': ('w5-faq', '<div class="ptitle">퀴즈 · 이 상황엔 몇 번 답?</div><div class="eq" id="fq-q"></div><div class="ctrl"><button class="bt" data-a="1" type="button">Q1</button><button class="bt" data-a="2" type="button">Q2</button><button class="bt" data-a="3" type="button">Q3</button><button class="bt" data-a="4" type="button">Q4</button><button class="bt" data-a="5" type="button">Q5</button></div><div class="eq" id="fq-out" aria-live="polite"></div>'),
   'limit': 'FAQ의 답은 출발점입니다. 반복되는 문제는 회의록에 남겨 분기 규칙 자체를 고칩니다.',
   'quiz': [{'q': 'QWEN이 estimated_wear 1.3을 돌려줬다. 고칠 카드는?', 'o': ['역할 카드', '출력 형식 카드', '인쇄 설정'], 'a': 1, 'why': '범위를 출력 형식에 명시합니다(Q2).'}]},
 ],
 'duel': {
   'q': 'AI4I 미니 100대, 점수형으로 충분할까?',
   'intro': [('doc', 'e07', '주판봇은 마모 점수 하나로 가르는 점수형, 초파리 연구원은 유형 분기를 먼저 보는 혼합형입니다. 실제 고장 6건이 어떤 카드를 받는지 봅니다.'), ('sia', 'e12', '판정 시작합니다!')],
   'fly': '혼합형. 고장 유형이 있으면 그 유형의 카드를 먼저 낸다.',
   'robo': '점수형! 숫자 하나로 다 됩니다. 규칙이 단순해야 현장이 따릅니다!',
   'widget': 'w5-duel',
   'panel': '<div class="ptitle">채점 · 고장 6건이 받은 카드 (실제 수업 데이터)</div><button class="bt primary" id="du5-run" type="button">카드 나눠 주기</button><div class="tw" id="du5-tb"></div><div class="kpis" id="du5-k"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('moa', 'e12', '정장 입고 응원합니다!'), ('x2', 'e01', '(짝짝)'), ('x3', 'e16', '(삐빅)')],
 },
 'summary': {
   'head': ['절', '한 줄', '쓰는 곳'],
   'rows': [['5.1~5.2', '점검표 + 회의록 + 매뉴얼 = 작업지시서 다섯 칸', '단순 카드 / 분기 카드'],
            ['5.3~5.6', '점수형(0.40/0.70) · 유형형(6갈래) · 혼합형 · 보수형', '고장 6건 중 4건은 점수형만으로 놓침'],
            ['5.7~5.8', '누가·무엇을·언제까지 + 빈칸 다섯', '카드 검사기'],
            ['5.9~5.11', '입력 폼 → 결과 카드 → 인쇄, QWEN 앱 점검, MAE·RMSE', '한 페이지 앱']],
   'limits': ['3D 가공 셀의 설비·램프 상태는 AI4I 미니의 여섯 행을 장면으로 옮긴 것입니다.',
              'osf·rnf 행동과 이름(박씨·이씨·최씨)은 예시입니다. 실제 행동과 책임자는 회의록으로 정합니다.',
              '한 페이지 앱은 QWEN을 부르지 않으며, 분류·회귀 답은 사람이 옮겨 넣습니다.'],
 },
 'outro': [('doc', 'e16', '분류는 라벨, 회귀는 숫자. 분기형 작업지시서가 그 숫자를 행동으로 옮깁니다. 카드 한 장이 작업자 손에 닿으면 완성입니다.'),
           ('asst', 'e01', '한 페이지 앱으로 우리 라인 카드를 인쇄해 볼게요!'),
           ('fly', 'e10', '다음 주 REVIEW에서는 다섯 주를 하나의 공장 문제로 다시 엮어.'),
           ('robo', 'e12', '점수형만 고집하지 않겠습니다. 혼합형 만세!')],
 'sources': [('강의 교안', '코딩 없는 제조업의 AI 데이터 분석 3·4회차 「오류를 잡는 작업지시서」 — 안상선 · 수업 자료 01~05 프롬프트 md 목록'),
             ('수업 데이터', 'ai4i_2024_mini.csv (100행)'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': 'osf·rnf 행동, 행동 매핑의 이름, 앱 프롬프트(03~05 md 원문 대신 재작성)는 예시입니다. 분기 결과·MAE는 수업 데이터로 계산했습니다.',
 'practice': ('practice.html', 'AI4I 100대에 분기 규칙을 돌려 보다'),
}

CH['js'] = _AI + 'window.M5=' + json.dumps(M5, ensure_ascii=False) + ';' + r'''
var ZC={정상:'#2e8b57',주의:'#b8860b',위험:'#c0392b','이미 늦음':'#7b1d1d'};
var ACT={정상:['점검자 박씨','정상 가동 기록 · 다음 점검 주기 등록','당일 17:00','가동 계속'],주의:['라인 책임자 이씨','점검 주기 절반 단축 · 교체 일정 한 단계 앞당김','4시간 내','30분 단위 갱신'],위험:['팀장 최씨 + 안전요원 김씨','① 안전 점검 ② 전원 차단 ③ 공구 교체 ④ 기록 ⑤ 보고','1시간 내','품질팀·생산팀 즉시 보고'],'이미 늦음':['팀장 최씨','라인 정지 · 보고 기록','즉시','다음 점검은 의미 없음 · 원인 보고']};
var TYP={twf:['공구 마모','팀장 최씨 + 안전요원 김씨','즉시 공구 교체 · 해당 공구 폐기 후 신규 등록','1시간 내'],hdf:['열 방산','라인 책임자 이씨','라인 정지 · 냉각 15분 후 재가동 판단','15분 후 재판단'],pwf:['전력','전기팀 + 이씨','전원 점검 · UPS 가동 · 전기팀 호출','즉시'],osf:['과부하','라인 책임자 이씨','절삭 조건(토크·이송) 낮춤 · 공구·고정구 점검','1시간 내'],rnf:['무작위','점검자 박씨','재측정 · 관찰 기록 · 원인 미상 보고','당일 17:00']};
function zone(w,lo,hi){lo=lo||.4;hi=hi||.7;return w>=.95?'이미 늦음':w>=hi?'위험':w>=lo?'주의':'정상';}
function card(t){return '<div class="wo"><h4>작업지시서 · '+t.id+' <span class="lv" style="background:'+(ZC[t.zone]||'#555')+'">'+t.zone+'</span></h4><table><tr><td>① 결과</td><td>'+t.res+'</td></tr><tr><td>② 작업자</td><td>'+t.who+'</td></tr><tr><td>③ 작업 항목</td><td>'+t.act+'</td></tr><tr><td>④ 완료 시각</td><td>'+t.due+'</td></tr><tr><td>⑤ 메모</td><td>'+t.memo+'</td></tr></table></div>';}
function mk(id,w,typ){if(typ&&typ!=='정상'&&TYP[typ]){var T=TYP[typ];return {id:id,zone:'위험',res:'machine_failure=1, '+typ+'('+T[0]+'), wear_proxy '+w.toFixed(2),who:T[1],act:T[2],due:T[3],memo:'유형 분기 우선 · 품질팀·생산팀 보고'};}var z=zone(w),A=ACT[z];return {id:id,zone:z,res:'wear_proxy '+w.toFixed(2)+' → '+z,who:A[0],act:A[1],due:A[2],memo:A[3]};}
function sayDoc(mood,html){var v=document.getElementById('verdict');v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
W['w5-blank']=function(b){var o=b.querySelector('#bl-out');function f(m){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',+x.dataset.m===m)});o.innerHTML=m?card(mk('CNC-1',.78,'')):'<div class="wo"><h4>점검표</h4><table><tr><td>CNC-1</td><td>wear_proxy 0.78</td></tr><tr><td>작업자</td><td style="color:#c0392b">(비어 있음)</td></tr><tr><td>항목</td><td style="color:#c0392b">(비어 있음)</td></tr><tr><td>시한</td><td style="color:#c0392b">(비어 있음)</td></tr></table></div>';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(+x.dataset.m)}});f(0);};
W['w5-merge']=function(b){var S=[['점검표','① 결과 라인','wear_proxy 0.78 → 위험'],['회의록','② 작업자','팀장 최씨 + 안전요원 김씨'],['매뉴얼','③ 작업 항목','① 안전 점검 ② 전원 차단 ③ 교체 ④ 기록 ⑤ 보고'],['회의록','④ 완료 시각','1시간 내 결정'],['회의록','⑤ 메모','품질팀·생산팀 보고 · 30분 단위 갱신']],on=S.map(function(){return 0}),bt=b.querySelector('#mg-bt'),o=b.querySelector('#mg-out');S.forEach(function(s,i){var x=document.createElement('button');x.className='bt';x.setAttribute('aria-pressed','false');x.textContent=s[0]+' → '+s[1];x.onclick=function(){on[i]=1;x.setAttribute('aria-pressed','true');f();};bt.appendChild(x);});function f(){o.innerHTML='<div class="wo"><h4>작업지시서 조립 '+on.reduce(function(a,c){return a+c},0)+'/5</h4><table>'+S.map(function(s,i){return '<tr><td>'+s[1]+'</td><td>'+(on[i]?s[2]:'<span style="color:#999">( '+s[0]+'에서 가져오세요 )</span>')+'</td></tr>'}).join('')+'</table></div>';}f();};
W['w5-score']=function(b){var v=b.querySelector('#sc-v'),o=b.querySelector('#sc-out');function f(){var x=+v.value;b.querySelector('#sc-vv').textContent=x.toFixed(2);o.innerHTML=card(mk('CNC-1',x,''));}v.oninput=f;f();};
W['w5-day']=function(b){var D=[['09:00','아침 점검',.18,''],['11:30','마모 상승',.52,''],['13:15','위험 도달 + hdf',.78,'hdf'],['15:00','교체 후 복귀',.09,'']],bt=b.querySelector('#dy-bt'),o=b.querySelector('#dy-out');D.forEach(function(d,i){var x=document.createElement('button');x.className='bt';x.textContent=d[0]+' '+d[1];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.toggle('on',y===x)});var c=mk('A라인 '+d[0],d[2],d[3]);o.innerHTML=card(c);};bt.appendChild(x);});bt.firstChild.click();};
W['w5-type']=function(b){var T=['정상','twf','hdf','pwf','osf','rnf'],bt=b.querySelector('#ty-bt'),o=b.querySelector('#ty-out');T.forEach(function(t){var x=document.createElement('button');x.className='bt';x.textContent=t;x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.toggle('on',y===x)});o.innerHTML=card(mk('CNC-2',.43,t));};bt.appendChild(x);});bt.children[2].click();};
W['w5-mix']=function(b){var M=[['점수형 (0.40/0.70)',0],['유형형',1],['혼합형',2],['보수형 (0.30/0.60) + 혼합',3]],bt=b.querySelector('#mx-bt'),k=b.querySelector('#mx-k'),o=b.querySelector('#mx-out');function typ(i){var t=['twf','hdf','pwf','osf','rnf'].filter(function(c){return AI4I[c][i]});return AI4I.machine_failure[i]&&t.length?t[0]:'';}M.forEach(function(m){var x=document.createElement('button');x.className='bt';x.textContent=m[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.toggle('on',y===x)});var cnt={정상:0,주의:0,위험:0},miss=[],dang=0,dangFail=0;AI4I.UID.forEach(function(u,i){var w=AI4I.wear_proxy[i],t=typ(i),z;if(m[1]==0)z=zone(w)=='이미 늦음'?'위험':zone(w);else if(m[1]==1)z=t?'위험':'정상';else if(m[1]==2)z=t?'위험':(zone(w)=='이미 늦음'?'위험':zone(w));else z=t?'위험':(w>=.6?'위험':w>=.3?'주의':'정상');cnt[z]++;if(z=='위험'){dang++;if(AI4I.machine_failure[i])dangFail++;}if(AI4I.machine_failure[i]&&z!=='위험')miss.push(u+'('+z+')');});k.innerHTML='<div class="kpi g"><b>'+cnt.정상+'</b><span>정상 카드</span></div><div class="kpi a"><b>'+cnt.주의+'</b><span>주의 카드</span></div><div class="kpi r"><b>'+cnt.위험+'</b><span>위험 카드 (그중 실제 고장 '+dangFail+')</span></div><div class="kpi m"><b>'+miss.length+'/6</b><span>위험 카드를 못 받은 고장</span></div>';o.innerHTML=miss.length?'위험 카드를 못 받은 고장: <em>'+miss.join(', ')+'</em>':'고장 6건 모두 위험 카드를 받았습니다.'+(m[1]==1?' 다만 유형형만 쓰면 마모가 높은 설비(주의 구간)가 모두 정상 카드를 받습니다.':'');};bt.appendChild(x);});bt.firstChild.click();};
W['w5-map']=function(b){var R=[['정상','점검자 박씨','당일 17:00'],['주의','라인 책임자 이씨','4시간 내'],['위험','팀장 최씨 + 안전요원 김씨','1시간 내']],tb=b.querySelector('#mp-tb'),o=b.querySelector('#mp-out');tb.innerHTML='<table class="tb"><tr><th>구간</th><th>작업자 (고쳐 쓰세요)</th><th>시한</th></tr>'+R.map(function(r,i){return '<tr><td>'+r[0]+'</td><td><input data-i="'+i+'" value="'+r[1]+'" style="width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:6px;padding:4px"></td><td><input data-j="'+i+'" value="'+r[2]+'" style="width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:6px;padding:4px"></td></tr>'}).join('')+'</table>';function f(){var bad=[];tb.querySelectorAll('input').forEach(function(x){var v=x.value.trim();if(!v||/관련|담당 부서|ASAP|곧|검토 후/.test(v))bad.push(v||'(빈칸)');x.style.borderColor=(!v||/관련|ASAP|곧|검토 후/.test(v))?'var(--eye)':'var(--rule)';});o.innerHTML=bad.length?'<em>모호한 칸: '+bad.join(', ')+'</em>':'모든 칸에 구체적인 이름과 시간이 있습니다.';}tb.querySelectorAll('input').forEach(function(x){x.oninput=f});f();};
W['w5-lint']=function(b){var t=b.querySelector('#ln5'),o=b.querySelector('#ln5-out');function f(){var s=t.value,P=[];if(!/(씨|팀장|반장|책임자|[가-힣]{2,3}\s?(대리|과장|주임))/.test(s)||/관련 부서/.test(s))P.push('① 책임자 이름이 구체적이지 않습니다');if(!/0\.\d/.test(s))P.push('② 임계값·점수 숫자가 없습니다');if(/ASAP|곧|검토 후/.test(s)||!/(\d+\s?(시간|분)|\d{1,2}:\d{2})/.test(s))P.push('③ 완료 시한이 시간 단위가 아닙니다');if(/항목:\s*(검토|판단)\s*$/m.test(s)||!/(교체|차단|정지|점검|냉각|등록|호출)/.test(s))P.push('④ 작업 항목에 동사 + 사물이 없습니다');if(!/(보고|팀)/.test(s.split('메모')[1]||''))P.push('⑤ 보고 회선이 없습니다');o.innerHTML=P.length?P.map(function(p){return '<p class="r">'+p+'</p>'}).join(''):'<p class="g">빈칸 다섯이 모두 채워졌습니다.</p>';}b.querySelector('#ln5-bt').onclick=f;b.querySelector('#ln5-ok').onclick=function(){t.value='결과: wear_proxy 0.78 → 위험\n담당: 팀장 최씨 + 안전요원 김씨\n항목: ① 안전 점검 ② 전원 차단 ③ 공구 교체 ④ 기록 ⑤ 보고\n시한: 1시간 내\n메모: 품질팀·생산팀 즉시 보고';f();};f();};
W['w5-app']=function(b){var F=[['air_temp_k','공기 온도(K)',295,306,300.2],['process_temp_k','공정 온도(K)',305,316,310.2],['rotational_speed_rpm','회전수(rpm)',1100,2900,1519],['torque_nm','토크(Nm)',3,80,38.8],['tool_wear_min','공구 가동(분)',0,260,238]],fm=b.querySelector('#ap-form');var st='background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:8px;padding:6px;width:110px';fm.innerHTML=F.map(function(f){return '<label class="group" style="flex-direction:column;align-items:flex-start"><span class="glabel">'+f[1]+'</span><input type="number" step="any" data-k="'+f[0]+'" min="'+f[2]+'" max="'+f[3]+'" value="'+f[4]+'" style="'+st+'"></label>'}).join('')+'<label class="group" style="flex-direction:column;align-items:flex-start"><span class="glabel">분류 결과(QWEN)</span><select id="ap-t" style="'+st+'"><option>정상</option><option selected>twf</option><option>hdf</option><option>pwf</option><option>osf</option><option>rnf</option></select></label><label class="group" style="flex-direction:column;align-items:flex-start"><span class="glabel">회귀 결과 estimated_wear</span><input type="number" id="ap-w" step="0.01" min="0" max="1" value="0.94" style="'+st+'"></label>';var c=b.querySelector('#ap-card');function run(){var ok=true;fm.querySelectorAll('input').forEach(function(x){var v=parseFloat(x.value),bad=isNaN(v)||v<+x.min||v>+x.max;x.style.borderColor=bad?'#f0604d':'var(--rule)';x.style.borderWidth=bad?'2px':'1px';if(bad)ok=false;});if(!ok){c.innerHTML='<p class="lim">빨간 칸을 고쳐 주세요. 숫자가 아니거나 범위 밖입니다.</p>';return;}var w=parseFloat(b.querySelector('#ap-w').value),t=b.querySelector('#ap-t').value;var d=new Date();c.innerHTML='<div id="wo-print">'+card(mk('CNC 셀 · '+d.getHours()+':'+String(d.getMinutes()).padStart(2,'0'),w,t))+'</div>';}b.querySelector('#ap-run').onclick=run;b.querySelector('#ap-print').onclick=function(){run();var s=document.createElement('style');s.id='ps';s.textContent='@media print{body *{visibility:hidden}#wo-print,#wo-print *{visibility:visible}#wo-print{position:absolute;left:0;top:0;width:100%}#wo-print .wo{font-size:12pt;color:#000;background:#fff}#wo-print .lv{color:#000;border:1px solid #000;background:#fff!important}}';document.head.appendChild(s);window.print();setTimeout(function(){s.remove()},500);};run();};
W['w5-qa']=function(b){var C=['외부 주소를 부르지 않는다','숫자가 아닌 값을 막는다','0.40·0.70이 코드에 그대로 있다','카드 다섯 칸이 다 있다','인쇄가 A4 한 장에 들어간다'],on=C.map(function(){return 0}),bt=b.querySelector('#qa-bt'),o=b.querySelector('#qa-out');C.forEach(function(c,i){var x=document.createElement('button');x.className='bt';x.setAttribute('aria-pressed','false');x.textContent=(i+1)+'. '+c;x.onclick=function(){on[i]=1-on[i];x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var n=on.reduce(function(a,c){return a+c},0);o.innerHTML='확인 <b>'+n+'/5</b>'+(n==5?' — 현장 배포 전 마지막으로 작업자 한 명에게 보여 주세요.':'');}f();};
W['w5-mae']=function(b){var R=[[4,80,'예시 0.21'],[52,225,''],[13,134,''],[60,173,''],[19,78,'']],tb=b.querySelector('#ma-tb'),o=b.querySelector('#ma-out');var init=[.21,.78,.45,.62,.25];tb.innerHTML='<table class="tb"><tr><th>UID</th><th>가동(분)</th><th>실제 wear_proxy</th><th>QWEN 답 (고쳐 넣기)</th></tr>'+R.map(function(r,i){return '<tr><td>'+AI4I.UID[r[0]]+'</td><td class="n">'+AI4I.tool_wear_min[r[0]]+'</td><td class="n">'+AI4I.wear_proxy[r[0]].toFixed(2)+'</td><td><input type="number" step="0.01" min="0" max="1" value="'+init[i]+'" data-i="'+i+'" style="width:90px;background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:6px;padding:4px"></td></tr>'}).join('')+'</table>';function f(){var e=[];tb.querySelectorAll('input').forEach(function(x,i){e.push(parseFloat(x.value)-AI4I.wear_proxy[R[i][0]]);});var mae=e.reduce(function(a,c){return a+Math.abs(c)},0)/e.length,rmse=Math.sqrt(e.reduce(function(a,c){return a+c*c},0)/e.length),bias=e.reduce(function(a,c){return a+c},0)/e.length;o.innerHTML='MAE <b>'+mae.toFixed(3)+'</b> · RMSE <b>'+rmse.toFixed(3)+'</b> · 평균 치우침 <em>'+(bias>0?'+':'')+bias.toFixed(3)+'</em> '+(bias<-.03?'→ 늘 낮게 봅니다(위험 경보가 늦어짐)':bias>.03?'→ 늘 높게 봅니다(과잉 경보)':'→ 고르게 빗나감');}tb.querySelectorAll('input').forEach(function(x){x.oninput=f});f();};
W['w5-faq']=function(b){var Q=[['estimated_wear가 1.4로 왔다',2],['같은 행을 두 번 물었더니 0.52, 0.71이 나왔다',1],['카드에 "시한: 검토 후"만 있다',3],['작업자가 "이 카드대로 못 해요"라고 한다',5],['분류는 정상, 회귀는 0.69 — 둘 다 애매하다',4]],i=0,sc=0,q=b.querySelector('#fq-q'),o=b.querySelector('#fq-out');function sh(){q.textContent='('+(i+1)+'/5) '+Q[i][0];}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var ok=+x.dataset.a===Q[i][1];if(ok)sc++;o.innerHTML=(ok?'✔ ':'✘ 정답 Q'+Q[i][1]+' · ')+'점수 '+sc+'/'+(i+1);i=(i+1)%5;if(!i)sc=0;sh();};});sh();};
W['w5-duel']=function(b){b.querySelector('#du5-run').onclick=function(){var rows=[];AI4I.UID.forEach(function(u,i){if(!AI4I.machine_failure[i])return;var w=AI4I.wear_proxy[i],t=['twf','hdf','pwf','osf','rnf'].filter(function(c){return AI4I[c][i]});var z1=zone(w);var c2=mk(u,w,t[0]);rows.push([u,w.toFixed(2),t.join('·'),z1,c2.zone+' · '+c2.act]);});var miss=rows.filter(function(r){return r[3]!=='위험'&&r[3]!=='이미 늦음'}).length;b.querySelector('#du5-tb').innerHTML='<table class="tb"><tr><th>UID</th><th>wear</th><th>유형</th><th>주판봇(점수형)</th><th>초파리(혼합형)</th></tr>'+rows.map(function(r){return '<tr><td>'+r[0]+'</td><td class="n">'+r[1]+'</td><td>'+r[2]+'</td><td style="color:'+(r[3]=='위험'?'var(--gfp)':'var(--eye)')+'">'+r[3]+'</td><td>'+r[4]+'</td></tr>'}).join('')+'</table>';b.querySelector('#du5-k').innerHTML='<div class="kpi r"><b>'+miss+'/6</b><span>주판봇: 위험 카드를 못 받은 고장</span></div><div class="kpi g"><b>0/6</b><span>초파리: 못 받은 고장</span></div><div class="kpi a"><b>11</b><span>점수형 위험 카드 중 고장 아닌 것</span></div><div class="kpi m"><b>A0095</b><span>과부하인데 "정상" 카드</span></div>';sayDoc('e10','초파리 연구원 승. 점수형만 쓰면 고장 6건 중 '+miss+'건이 정상·주의 카드를 받고, 과부하 A0095는 "정상 가동" 카드를 받습니다. 반대로 위험 카드 13장 중 11장은 고장이 아니었습니다. 마모 숫자 하나로는 고장의 종류를 볼 수 없습니다.');};};
'''

RP = {
 'title': '마모 점수 하나로 100대를 나누면, 누가 잘못된 카드를 받을까?',
 'eyebrow': '5주차 실습 리포트 · 분기형 작업지시서 · AI4I 미니 100행',
 'desc': '스마트 제조 5주차 실습 리포트 — AI4I 미니 100행에 점수형·혼합형 분기를 돌려 카드 분포를 비교하고, 회귀 카드 few-shot 예시값이 데이터의 마모 정의보다 낮다는 점을 박사가 정리합니다.',
 'lead': '작업지시서의 분기 규칙을 실제 데이터 100행에 돌려 봤습니다. 점수형만 쓰면 고장 6건 중 4건이 위험 카드를 받지 못했고, 회귀 카드의 예시값은 데이터보다 약 0.1 낮게 적혀 있었습니다.',
 'cover_mood': 'e07', 'back': ('index.html', '5주차 본문으로'), 'next': ('../w06/practice.html', '6주차 REVIEW 실습 리포트'),
 'summary': {
   'finding': 'AI4I 미니 100행에서 마모 점수(0.40/0.70)만으로 카드를 나누면 고장 6건 중 4건이 정상·주의 카드를 받았고, 유형 분기를 먼저 보는 혼합형으로 바꾸면 6건 모두 위험 카드를 받았습니다.',
   'evidence': ['<span class="fact">사실</span> 점수형 카드 분포는 정상 48 · 주의 39 · 위험 13이고, 위험 13장 중 실제 고장은 2장입니다(<a href="#tab-r5-1">표 1</a>).',
                '<span class="fact">사실</span> 과부하 고장 A0095는 마모 0.30이라 점수형에서 "정상 가동" 카드를 받습니다(<a href="#tab-r5-2">표 2</a>).',
                '<span class="fact">사실</span> 회귀 카드 few-shot 예시(80분 → 0.21, 220분 → 0.78)는 데이터 정의(가동 ÷ 약 253 → 0.32, 0.87)보다 약 0.10 낮습니다(<a href="#fig-r5-1">그림 1</a>).',
                '<span class="interp">해석</span> 예시를 따라 답하는 모델은 위험 경계 0.70에 실제보다 약 24분 늦게 닿습니다. few-shot 예시는 데이터에서 직접 뽑아야 합니다.'],
   'fig': ('fig', {'id': 'fig-r5-1', 'cap': '[그림 1] 가동 시간과 마모 — 데이터(점)와 회귀 카드 예시(빨강)', 'w': 'r5-ex', 'alt': 'AI4I 미니 100행의 가동 시간 대비 wear_proxy 점과 직선, 회귀 카드 예시 두 점이 직선 아래에 있다', 'src': '출처: ai4i_2024_mini.csv(100행), 수업 회귀 프롬프트 few-shot 예시, 저자 계산'}),
 },
 'sections': [
  {'id': 'sec-r5-1', 'nav': '들어가며', 'title': '들어가며 — 규칙을 데이터에 돌려 본다', 'blocks': [
    ('memo', 'e08', '작업지시서 분기는 종이 위에서는 늘 깔끔해 보여요. 데이터 100행에 한 번 돌려 보면 다른 얼굴이 보입니다.'),
    ('p', '3·4회차는 0.40/0.70 점수 분기와 여섯 갈래 유형 분기를 만들었습니다. 이 리포트는 그 규칙을 AI4I 미니 100대에 그대로 적용해 누가 어떤 카드를 받는지 봅니다.'),
    ('p', '질문은 셋입니다. ① 점수형만으로 충분한가 ② 혼합형은 무엇을 바꾸나 ③ 회귀 카드의 예시값은 데이터와 맞나.')]},
  {'id': 'sec-r5-2', 'nav': '배경', 'title': '배경 — 두 분기의 차이', 'blocks': [
    ('p', '점수형은 wear_proxy를 0.40·0.70으로 갈라 정상·주의·위험 카드를 냅니다. 혼합형은 고장 유형(twf·hdf·pwf·osf·rnf)이 있으면 그 유형 카드를 먼저 내고, 없을 때만 점수로 가릅니다.'),
    ('p', '비유하면 점수형은 체온만 보는 문진표, 혼합형은 증상(기침·복통)을 먼저 묻고 체온을 보는 문진표입니다.'),
    ('memo', 'e09', '여기서 유형은 데이터의 정답 라벨을 그대로 썼어요. 실제 현장에서는 분류 모델의 답이 들어가니, 혼합형 결과는 "분류가 맞았을 때의 최선"으로 읽어 주세요.')]},
  {'id': 'sec-r5-3', 'nav': '방법', 'title': '방법', 'blocks': [
    ('p', '데이터: ai4i_2024_mini.csv 100행(고장 6건). 점수형 경계 0.40·0.70(0.95 이상은 "이미 늦음"도 위험으로 셈), 혼합형은 유형 우선. 회귀 예시 비교는 wear_proxy와 tool_wear_min의 최소제곱 직선(기울기 0.00396, 절편 0.0006)을 기준으로 했습니다.'),
    ('p', '계산은 저장소 analysis/w05_branch.py와 같고, 본문 5.6 실험·대결에서 브라우저로 다시 돌릴 수 있습니다.')]},
  {'id': 'sec-r5-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3>결과 1 · 점수형 카드 분포</h3>'),
    ('table', {'id': 'tab-r5-1', 'cap': '<표 1> 점수형 카드와 실제 고장 (단위: 대)', 'head': ['카드', '정상 설비', '고장 설비', '합계'],
               'rows': [['정상 (< 0.40)', '47', '1', '48'], ['주의 (0.40~0.70)', '36', '3', '39'], ['위험 (≥ 0.70)', '11', '2', '13'], ['합계', '94', '6', '100']],
               'src': '출처: ai4i_2024_mini.csv, 저자 계산'}),
    ('p', '<span class="fact">사실</span> 위험 카드 13장 중 고장은 2장(A0091 twf, A0094 twf·hdf)뿐입니다. 나머지 11장은 마모만 높고 고장은 없던 설비입니다.'),
    ('p', '<span class="interp">해석</span> 점수형은 "공구가 닳았나"에는 답하지만 "왜 멈췄나"에는 답하지 못합니다. 마모가 높아 미리 교체하는 것은 좋은 일이지만, 열·전력·과부하 고장은 마모와 따로 옵니다.'),
    ('html', '<h3>결과 2 · 고장 6건이 받은 카드</h3>'),
    ('table', {'id': 'tab-r5-2', 'cap': '<표 2> 고장 6건의 카드 비교', 'head': ['UID', 'wear', '유형', '점수형', '혼합형'],
               'rows': [['A0091', '0.94', 'twf', '위험', '위험 · 공구 교체'], ['A0092', '0.43', 'hdf', '주의', '위험 · 라인 정지·냉각'], ['A0093', '0.55', 'pwf', '주의', '위험 · 전원 점검·UPS'], ['A0094', '0.90', 'twf·hdf', '위험', '위험 · 공구 교체 (+hdf 기록)'], ['A0095', '0.30', 'osf', '<b>정상</b>', '위험 · 절삭 조건 낮춤'], ['A0099', '0.63', 'hdf', '주의', '위험 · 라인 정지·냉각']],
               'src': '출처: ai4i_2024_mini.csv, 저자 계산 (osf 행동은 이 리포트의 예시)'}),
    ('key', '점수형만 쓰면 과부하로 멈춘 설비에 "정상 가동 기록" 카드가 나갑니다.'),
    ('html', '<h3>결과 3 · 회귀 카드 예시값이 낮다</h3>'),
    ('table', {'id': 'tab-r5-3', 'cap': '<표 3> few-shot 예시와 데이터 정의 비교 (단위: 분, wear 0~1)', 'head': ['예시', '가동(분)', '예시값', '데이터 직선', '차이'],
               'rows': [['회귀 예시 01', '80', '0.21', '0.32', '−0.11'], ['회귀 예시 02', '220', '0.78', '0.87', '−0.09'], ['분류 예시 01 (정상)', '130', '—', '0.51 (주의 부근)', '—'], ['분류 예시 02 (twf)', '232', '—', '0.92', '—']],
               'src': '출처: 수업 분류·회귀 프롬프트 예시, ai4i_2024_mini.csv 직선, 저자 계산'}),
    ('p', '<span class="fact">사실</span> 두 회귀 예시는 데이터 직선보다 평균 0.10 낮습니다. 예시의 기울기(약 0.00407/분)를 따라가면 0.70은 약 200분, 데이터 직선으로는 약 177분입니다.'),
    ('p', '<span class="interp">해석</span> 예시를 그대로 따르는 언어 모델은 위험 경보를 약 24분 늦게 낼 수 있습니다. 분류 예시 01도 "다섯 입력 모두 정상 부근"이라 했지만, 같은 130분은 데이터 기준 주의 부근입니다.'),
    ('memo', 'e16', 'few-shot 예시는 "말투 견본"이 아니라 "숫자 견본"이기도 해요. 견본이 0.1 낮으면 답도 0.1 낮아질 수 있습니다.')]},
  {'id': 'sec-r5-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 예시는 다섯 입력을 모두 본 추정이라 tool_wear만으로 만든 직선과 비교하면 안 된다. 그러나 이 데이터의 wear_proxy는 가동 시간과 거의 일대일이라(잔차 매우 작음), 다른 입력이 0.1을 설명하기는 어렵습니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 혼합형은 위험 카드가 늘어 작업자가 지칠 수 있다. 맞습니다. 이 데이터에서 혼합형 위험 카드는 점수형(13장)에 유형 고장 4건을 더한 17장입니다. 카드 수보다 놓친 고장 수를 먼저 봅니다.'),
    ('p', '<span class="guess">추측</span> 실제 QWEN에 예시를 데이터 값으로 바꿔 넣으면 MAE가 줄어들 것입니다. 수업에서 본문 5.11 계산기로 확인할 수 있습니다.')]},
  {'id': 'sec-r5-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 분기 규칙을 종이가 아닌 데이터 위에서 시험하는 방법을 보였습니다. 규칙을 바꿀 때마다 "고장이 받은 카드" 표를 다시 뽑으면 됩니다.'),
    ('p', '한계: ① 100행·고장 6건 ② 혼합형은 분류가 맞았다는 가정 ③ osf·rnf 행동은 예시 ④ wear_proxy는 수업용 파생 열입니다.'),
    ('prompt', '[예시 01 — 정상 부근]\nair 300.1 · process 309.5 · rotation 1520 · torque 36.0 · wear 80\n→ {"estimated_wear": 0.32, "rationale": "마모 80분 — 정상 부근"}\n\n[예시 02 — 위험 부근]\nair 304.0 · process 312.1 · rotation 1620 · torque 40.0 · wear 220\n→ {"estimated_wear": 0.87, "rationale": "마모 220분 — 위험 임계"}'),
    ('memo', 'e07', '위는 예시값을 데이터 직선에 맞춰 고친 회귀 카드의 few-shot 부분이에요. 원래 카드와 바꿔 넣고 결과를 비교해 보세요.'),
    ('p', '다음 편 예고: 6주차 REVIEW 리포트에서는 면류 3사의 2027년 여름 수요를 계절성으로 내다보고, 라인·인력·원재료 계획까지 이어 봅니다.')]},
 ],
 'refs': ['안상선, 「코딩 없는 제조업의 AI 데이터 분석」 3·4회차 「오류를 잡는 작업지시서」 강의 교안, 2026', '수업 분류·회귀 결과 출력 프롬프트(few-shot 예시 포함), 2026', 'Matzka, S. (2020). AI4I 2020 Predictive Maintenance Dataset. UCI Machine Learning Repository', '이 저장소 analysis/w05_branch.py — 저자 계산'],
 'sources': [('원자료', 'ai4i_2024_mini.csv · 수업 프롬프트'), ('계산', '저자 계산 (analysis/w05_branch.py)')],
 'notes': 'osf 행동은 예시입니다. 혼합형 결과는 고장 유형 라벨이 맞았다는 가정의 결과입니다.',
}
RP['js'] = _AI + r'''
W['r5-ex']=function(s){var idx=AI4I.tool_wear_min.map(function(v,i){return i}).sort(function(a,b){return AI4I.tool_wear_min[a]-AI4I.tool_wear_min[b]});var L=idx.map(function(i){return AI4I.tool_wear_min[i]});var ex=L.map(function(t){return t==78?.21:t==225?.78:null});var c=Chart.line(s,{labels:L.map(function(v){return v+'분'}),series:[{name:'데이터 wear_proxy',color:'#5ee39c',values:idx.map(function(i){return AI4I.wear_proxy[i]}),dots:true,width:.5},{name:'데이터 직선',color:'#f1b646',values:L.map(function(t){return .0006+.00396*t}),dash:'5 4'}],ref:.7,min:0,max:1,h:250,ticks:8});var NS='http://www.w3.org/2000/svg';[[80,.21],[220,.78]].forEach(function(p){var j=0,best=1e9;L.forEach(function(t,k){if(Math.abs(t-p[0])<best){best=Math.abs(t-p[0]);j=k;}});var e=document.createElementNS(NS,'circle');e.setAttribute('cx',c.X(j));e.setAttribute('cy',c.Y(p[1]));e.setAttribute('r',6);e.setAttribute('fill','#f0604d');s.appendChild(e);var t=document.createElementNS(NS,'text');t.setAttribute('x',c.X(j)+8);t.setAttribute('y',c.Y(p[1])+14);t.textContent='예시 '+p[0]+'분 → '+p[1];t.style.fill='#f0604d';s.appendChild(t);});};
'''
