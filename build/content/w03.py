# 3주차 · 생산실적 추세 분석 — 시계열의 원리
import os
_DATA = open(os.path.join(os.path.dirname(__file__), '..', 'data_w03.js'), encoding='utf-8').read()

CH = {
 'slug': 'w03', 'num': '03',
 'title': '생산실적 추세 분석 — 시계열의 원리',
 'eyebrow': '3주차 · SECTION 2 · 데이터 · 빙과·호빵 식품 공장',
 'desc': '스마트 제조 3주차 — 추세·계절·순환·불규칙 네 조각, 계절지수, 가법·승법, 이동평균과 계절조정, 예측 채점, 석유화학의 빗나간 예측, 예측에서 결정까지를 식품 공장 3D와 실제 계산으로 봅니다.',
 'q': '다음 달에 얼마를 만들고, 얼마를 사 둘 것인가?',
 'lead': '같은 숫자라도 "언제"가 붙으면 다른 데이터가 됩니다. 시계열은 순서가 정보이고, 예측은 한 점이 아니라 범위입니다. 그 범위가 곧 재고이고 계약입니다.',
 'scene_alt': '빙과·호빵 식품 공장 3D. 배합, 살균, 동결, 충진·포장, 경화 터널로 아이스크림이 흐르고, 앞쪽 냉동창고에 1월부터 12월까지 계절지수 높이만큼 재고 더미가 쌓여 있다. 버튼으로 아이스크림·호빵·군고구마를 바꿀 수 있다.',
 'scene_hud': '3D · 빙과·호빵 공장 — 냉동창고 더미 높이 = 계절지수',
 'scene_opts': {'cam': [0, 17, 27], 'target': [-1, 1, 0]},
 'kpis': [('1.87', '아이스크림 8월 계절지수', 'm'), ('2.6', '호빵 12월 계절지수', 'a'), ('−5.7%p', 'NCC 가동률 4월 (가법)', 'r'), ('8.9%', '계절 나이브 2025 오차(MAPE)', 'g')],
 'hero_talk': [
   ('doc', 'e07', '오늘은 빙과·호빵 공장입니다. 여름엔 아이스크림 라인이, 겨울엔 호빵 라인이 바쁩니다. 숫자 안에 네 가지 힘이 섞여 있습니다.'),
   ('robo', 'e19', '지난달보다 30% 늘었습니다! 대박입니다!'),
   ('fly', 'e09', '봄엔 원래 그맘때 느는 거 아니야? 계절을 빼고 다시 봐.'),
   ('moa', 'e12', '창고 더미 높이가 달마다 달라요. 저게 계절지수래요!'),
 ],
 'three': ['시간 순서로 쌓인 생산·판매 숫자를 추세·계절·순환·불규칙 네 조각으로 나누고, 그 조각을 미래로 이어 붙이는 원리를 봅니다.',
           '계절을 빼지 않으면 "봄에 30% 늘었다"처럼 정보가 없는 보고를 하게 됩니다. 예측은 틀리므로 범위와 대비책이 함께 필요합니다.',
           '월별 생산 목표 배분, 안전재고, 선생산, 원료 구매 계획이 모두 이 원리 위에 있습니다.'],
 'abbr': [('MA', 'Moving Average', '이동평균'), ('MAPE', 'Mean Absolute Percentage Error', '평균 절대 백분율 오차 — 예측이 평균 몇 % 빗나갔나'),
          ('NCC', 'Naphtha Cracking Center', '나프타 분해 공장 — 에틸렌 등 기초유분 생산'), ('TA', 'Turnaround', '정기보수 — 설비를 세우고 점검'),
          ('RMSE', 'Root Mean Square Error', '오차를 제곱해 평균 낸 뒤 제곱근 — 큰 오차에 민감'), ('T·S·C·I', 'Trend·Season·Cycle·Irregular', '추세·계절·순환·불규칙')],
 'why': [('생산실적 ≠ 수요', '만든 양은 설비·가동일수·원료에 묶입니다. 둘을 섞으면 설비 고장을 수요 감소로 읽습니다.'),
         ('계절이 숫자를 속인다', '계절 품목의 "전월 대비 +30%"는 거의 정보가 없습니다. 계절을 빼고 봐야 좋은 달·나쁜 달이 보입니다.'),
         ('예측은 범위', '모든 예측은 틀립니다. 틀리는 크기를 재면 대비할 크기(안전재고·계약)가 나옵니다.')],
 'big_lead': '오늘의 흐름은 다섯 단계입니다.',
 'big': [('① 다르다', '시계열은 순서가 정보 — 자기상관, 정상성, 시간 순 분할'), ('② 쪼갠다', '추세·계절·순환·불규칙, 가법과 승법'),
         ('③ 내다본다', '이동평균, 계절지수, 분해, 기준선, 지수평활, 채점'), ('④ 빗나간다 → ⑤ 결정한다', '구조 변화·충격·변동성 → 안전재고·신문팔이·시나리오')],
 'glossary': {
   '시계열': ['시계열', '데이터', '한 대상을 시간 순서대로 여러 번 잰 데이터입니다. 순서를 섞으면 정보 대부분을 잃습니다.'],
   '자기상관': ['자기상관', '지표', '같은 시계열에서 k개월 떨어진 값끼리의 상관입니다. 12개월 자기상관이 크면 계절성이 강합니다.'],
   '정상성': ['정상성', '성질', '평균과 흔들림의 크기가 시간에 따라 변하지 않는 성질입니다.'],
   '계절지수': ['계절지수', '지표', '그 달이 평균적인 달의 몇 배인지 나타내는 숫자입니다. 12개 평균은 1입니다.'],
   '이동평균': ['이동평균', '방법', '정해진 기간(예: 12개월)의 평균을 한 달씩 옮기며 구한 값입니다. 계절을 지우고 추세를 꺼냅니다.'],
   '계절조정': ['계절조정', '방법', '원래 값을 계절지수로 나눠 계절 효과를 뺀 값입니다.'],
   '누설': ['누설(leakage)', '함정', '검증 때 미래 정보가 학습에 섞여 들어가 모델이 실제보다 좋아 보이는 현상입니다.'],
   '스프레드': ['스프레드', '지표', '제품 가격 − 원료 가격. NCC에서는 에틸렌 − 나프타가 공장이 버는 몫입니다.'],
   '안전재고': ['안전재고', '결정', '예측이 빗나갈 때를 대비해 더 갖고 있는 재고입니다. 예측 오차 크기 × 서비스 수준 계수로 정합니다.'],
 },
 'subs': [
  {'id': 'sec-3-1', 'title': '생산실적은 수요가 아니다', 'tags': ['함정: 잘린 관측', '현장: 라인 능력 900'],
   'pair': ('일상으로 치면', '식당이 하루 100그릇만 끓일 수 있다면, 100그릇 판매는 "손님이 100명"이 아니라 "100그릇에서 잘렸다"일 수 있다.',
            '공장에서는', '아이스크림 라인이 월 900천 개까지만 만들 수 있으면 7~9월 생산실적은 900으로 평평하다. 그걸 수요로 읽으면 내년에도 900을 계획한다.'),
   'body': ['생산실적은 설비·가동일수·원료에 묶여 있습니다. 수요는 시장의 신호이며, 품절이면 관측이 잘립니다.',
            '원료 수입이 막히면 가동률은 수요와 무관하게 떨어집니다. 그래서 먼저 가동일수로 나눈 일평균으로 바꾸고, 정비·고장·원료 부족 달을 표시한 뒤 추세를 봅니다.'],
   'talk': [('robo', 'e16', '7월도 900, 8월도 900! 수요가 아주 안정적입니다!'), ('fly', 'e03', '라인이 900에서 막힌 거잖아. 아래 막대를 봐.'), ('asst', 'e07', '수요 예측값과 생산 상한을 같이 그려 볼게요.')],
   'widget': ('w3-cap', '<div class="ptitle">실험 · 생산 상한이 수요를 가린다 (2026 아이스크림 예측, 천 개)</div><div class="ctrl"><div class="group"><span class="glabel">월 생산 능력</span><input type="range" min="700" max="1600" step="50" value="900" id="cp-c"><span class="val" id="cp-v"></span></div></div><div class="cwrap"><svg id="cp-svg"></svg></div><div class="eq" id="cp-out" aria-live="polite"></div>'),
   'limit': '수요 예측값(576~1,472)은 교안의 2026년 예측 표입니다. 실제 수요는 품절 기간의 관측이 잘려 정확히 알기 어렵습니다.',
   'quiz': [{'q': '7~9월 생산실적이 모두 900으로 같다. 가장 먼저 의심할 것은?', 'o': ['수요가 안정적이다', '생산 능력에서 잘렸다', '데이터가 정확하다'], 'a': 1, 'why': '실적이 상한에 붙어 평평하면 수요가 아니라 능력의 한계일 수 있습니다.'}]},

  {'id': 'sec-3-2', 'title': '두 종류의 데이터 — 횡단면과 시계열', 'tags': ['비교: 8줄 표', '방법: 시간 순 검증'],
   'body': ['한 시점에 여러 대상을 재면 횡단면 데이터, 한 대상을 여러 시점에 재면 시계열입니다. 관측의 모양보다 "순서가 무엇을 하느냐"가 핵심입니다.',
            '<div class="tw"><table class="tb"><tr><th>비교 항목</th><th>횡단면</th><th>시계열</th></tr>'
            '<tr><td>관측끼리</td><td>서로 독립이라고 가정</td><td>이웃한 관측끼리 닮는다(자기상관)</td></tr>'
            '<tr><td>평균·분산</td><td>고정</td><td>시간에 따라 바뀔 수 있다(정상성)</td></tr>'
            '<tr><td>검증</td><td>무작위로 나눈다</td><td>시간 순서대로 나눈다</td></tr>'
            '<tr><td>핵심 질문</td><td>무엇이 차이를 만드나</td><td>다음에 무엇이 오나</td></tr>'
            '<tr><td>이상치의 뜻</td><td>측정 오류일 가능성</td><td>사건일 가능성(폭염, 전쟁)</td></tr>'
            '<tr><td>데이터가 늘면</td><td>추정이 정확해진다</td><td>오래된 데이터는 이미 다른 세상일 수 있다</td></tr>'
            '<tr><td>흔한 실수</td><td>표본 편향</td><td>미래 정보로 과거 맞히기(누설)</td></tr></table></div>'],
   'talk': [('sia', 'e07', '마지막 두 줄이 강의 후반의 복선이라고 교안에 적혀 있습니다.'), ('fly', 'e09', '"데이터가 많을수록 좋다"가 시계열에선 안 통한다는 거지.'), ('x2', 'e09', '(…메모)')],
   'widget': ('w3-kind', '<div class="ptitle">분류 · 이 데이터는 어느 쪽?</div><div class="eq" id="kd-q"></div><div class="ctrl"><button class="bt" data-a="0" type="button">횡단면</button><button class="bt" data-a="1" type="button">시계열</button></div><div class="eq" id="kd-out" aria-live="polite"></div>'),
   'limit': '현장 데이터는 둘이 섞인 경우(여러 라인 × 여러 날, 패널 데이터)가 많습니다. 그때는 시간 순서 규칙을 따릅니다.',
   'quiz': [{'q': '시계열 모델을 검증할 때 맞는 방법은?', 'o': ['무작위로 20% 가린다', '마지막 기간을 가리고 맞혀 본다'], 'a': 1, 'why': '무작위로 가리면 미래가 학습에 남아 누설이 생깁니다.'}]},

  {'id': 'sec-3-3', 'title': '순서가 정보다 — 84개를 섞으면', 'tags': ['데이터: 아이스크림 84개월', '실험: 섞기'],
   'fx': {'q': '숫자를 섞어도 평균이 같으면 같은 데이터 아니에요?',
          'school': '상관계수(고등 수학 확률과 통계 · 두 변수의 관계)',
          'eq': 'k개월 자기상관 = corr( x<sub>t</sub> , x<sub>t−k</sub> ) · <b>−1 ~ 1</b>',
          'rows': [('x<sub>t</sub>', '이번 달 판매'), ('x<sub>t−1</sub>', '지난달 판매 (k = 1)'), ('x<sub>t−12</sub>', '작년 같은 달 (k = 12)')],
          'calc': '날짜순 아이스크림은 1개월 0.79, 12개월 0.94입니다. 섞으면 평균 852.5는 그대로인데 상관이 0 근처로 떨어집니다. 아래 버튼으로 직접 섞어 보세요.',
          'comment': '평균은 같아도 "지난달을 알면 이번 달이 보인다"는 관계가 사라지는 거군요!'},
   'body': ['평균·합계·최댓값처럼 순서를 모르는 요약 통계는 섞어도 같습니다. 그래서 엑셀 요약표만 보면 두 표가 똑같아 보입니다.',
            '판매·생산 표를 금액순·크기순으로 정렬한 채 저장하면 이 정보가 사라집니다. 시계열 파일은 날짜순 정렬을 풀지 않습니다.'],
   'talk': [('robo', 'e07', '평균이 같으니 같은 데이터입니다!'), ('asst', 'e04', '섞었더니 12개월 상관이 0.94에서 거의 0이 됐어요!')],
   'widget': ('w3-shuf', '<div class="ptitle">실험 · 아이스크림 84개월을 섞어 보기 (실제 수업 데이터 계산)</div><div class="ctrl"><button class="bt on" id="sh-o" type="button">날짜순</button><button class="bt" id="sh-s" type="button">섞기</button></div><div class="cwrap"><svg id="sh-svg"></svg></div><div class="kpis" id="sh-k"></div>'),
   'limit': '섞은 결과의 상관은 섞을 때마다 조금씩 다릅니다(0 근처에서 흔들림). 교안의 0.01·0.06도 한 번 섞은 결과입니다.',
   'quiz': [{'q': '84개월을 섞어도 변하지 않는 것은?', 'o': ['12개월 자기상관', '평균', '계절 모양'], 'a': 1, 'why': '평균은 순서를 모르는 요약 통계입니다.'}]},

  {'id': 'sec-3-4', 'title': '오늘은 어제를 닮는다 — 자기상관', 'tags': ['원리: 자기상관', '현장: 관리도 주의'],
   'pair': ('일상으로 치면', '오늘 기온을 알면 내일 기온을 대충 맞힌다. 열은 천천히 식고 데워지기 때문이다.',
            '공장에서는', '반응기 온도(관성), 창고 재고(어제 재고 + 입고 − 출고), 설비 마모(한 번 나빠지면 점점), 원료 가격(어제에서 출발)이 강한 자기상관을 가진다.'),
   'body': ['독립이 아니라는 것은 정보가 겹친다는 뜻입니다. 84개월 데이터는 서로 무관한 84개 관측만큼의 정보를 담지 못합니다.',
            '품질 관리도의 관리한계선은 관측끼리 독립이라고 가정합니다. 자기상관이 강한 공정 데이터에 그대로 쓰면 경보가 너무 자주 또는 너무 늦게 울립니다.'],
   'talk': [('fly', 'e09', '그럼 몇 칸 떨어진 게 제일 닮았는지 막대로 보자.'), ('asst', 'e07', '1개월부터 24개월까지 계산할게요.')],
   'widget': ('w3-acf', '<div class="ptitle">계산 · 아이스크림 자기상관 1~24개월</div><div class="cwrap"><svg id="ac-svg"></svg></div><div class="eq" id="ac-out" aria-live="polite"></div>'),
   'limit': '자기상관이 높다고 원인 관계가 있다는 뜻은 아닙니다. 같은 계절 힘이 두 달 모두에 작용한 결과입니다.',
   'quiz': [{'q': '아이스크림에서 12개월 자기상관(0.94)이 1개월(0.79)보다 큰 뜻은?', 'o': ['지난달이 더 좋은 단서', '작년 같은 달이 더 좋은 단서'], 'a': 1, 'why': '계절성의 숫자적 정체입니다.'}]},

  {'id': 'sec-3-5', 'title': '평균과 흔들림이 변하는가 — 정상성', 'tags': ['원리: 정상성', '데이터: 나프타 140개월'],
   'body': ['정상 시계열은 평균과 흔들림의 크기가 시간에 따라 변하지 않습니다. 과거 평균이 미래에도 평균일 거라고 기대할 수 있습니다.',
            '나프타 가격 수준은 비정상입니다. 앞 절반 평균으로 뒤 절반을 예측하면 크게 빗나갑니다. 그래서 가격은 보통 변화율로 바꿔 분석합니다.',
            '그러나 변화율도 완전하지 않습니다. 흔들림의 크기(표준편차)가 뒤 절반에 약 1.6배로 커졌습니다. 이것이 3.14의 변동성 군집입니다.'],
   'talk': [('robo', 'e19', '나프타 평균 600달러로 예측하면 됩니다!'), ('fly', 'e03', '어느 기간의 평균? 앞 절반이랑 뒤 절반이 다르잖아.'), ('sia', 'e10', '아래에서 수준과 변화율을 바꿔 보겠습니다.')],
   'widget': ('w3-stat', '<div class="ptitle">계산 · 나프타 가격 — 수준 vs 월 변화율 (앞 절반 / 뒤 절반)</div><div class="ctrl"><button class="bt on" data-m="0" type="button">가격 수준</button><button class="bt" data-m="1" type="button">월 변화율</button></div><div class="cwrap"><svg id="stt-svg"></svg></div><div class="eq" id="stt-out" aria-live="polite"></div>'),
   'explain': ['교안은 2015–2020과 2020–2026으로 나눠 수준 평균 518 · 762, 변화율 표준편차 7.9 · 12.5%p를 보여 줍니다. 이 페이지는 140개월을 정확히 반으로 나눠 다시 계산하므로 값이 조금 다릅니다.'],
   'limit': '정상성은 "정도"의 문제입니다. 여기서는 앞뒤 절반 비교라는 쉬운 방법만 씁니다.',
   'quiz': [{'q': '가격 시계열을 분석할 때 흔히 먼저 하는 일은?', 'o': ['수준 그대로 평균', '변화율로 바꾼다', '무작위로 섞는다'], 'a': 1, 'why': '수준은 떠돌지만 변화율은 0 근처에 머뭅니다.'}]},

  {'id': 'sec-3-6', 'title': '무작위 분할의 함정 — 미래를 보고 과거 맞히기', 'tags': ['함정: 누설', '현장: AI에게 되묻기'],
   'why': {'problem': '일반 데이터는 무작위로 20%를 떼어 검증합니다.',
           'limit': '시계열에 그대로 쓰면, 가린 달의 바로 다음 달(미래)이 학습에 남아 있습니다. 모델은 미래를 슬쩍 보고 과거를 맞힙니다.',
           'solve': '시간 순서대로 마지막 구간을 떼어 검증합니다. 교안은 같은 140개월에서 무작위 3.9%, 마지막 28개월 21.6%로 오차가 5.5배 차이 났다고 보여 줍니다.',
           'easy': '내일 신문을 보고 어제 주가를 "예측"하는 것과 같습니다.'},
   'body': ['AI에게 "이 가격 데이터로 예측 모델을 만들고 정확도를 알려 줘"라고 하면 무작위 분할을 쓰는지 확인합니다. 쓴다면 "시간 순서대로 마지막 20%를 테스트로 다시 해 줘"라고 요구합니다.'],
   'talk': [('robo', 'e16', '정확도 96%! 이 모델로 구매 계획을 세우겠습니다!'), ('fly', 'e09', '테스트 달의 다음 달이 학습에 있었어? 아래 실험으로 확인해 봐.'), ('x3', 'e24', '(삐빅!)')],
   'widget': ('w3-leak', '<div class="ptitle">실험 · 같은 데이터, 두 가지 검증 (이 페이지 계산 · 나프타)</div><button class="bt primary" id="lk-run" type="button">검증 두 번 돌리기</button><div class="kpis" id="lk-k"></div><div class="eq" id="lk-out" aria-live="polite"></div>'),
   'explain': ['무작위 검증에서는 가린 달을 "앞뒤 달의 평균"으로 채웠습니다. 앞뒤를 다 아니까 쉽게 맞힙니다. 시간 순 검증에서는 마지막 학습 달 값을 그대로 이어 붙였습니다(나이브).', '방법이 교안과 달라 숫자는 다르지만, "무작위 검증이 훨씬 좋아 보인다"는 결론은 같습니다.'],
   'limit': '두 방법 모두 단순한 방법입니다. 복잡한 모델일수록 누설로 좋아 보이는 폭이 더 커질 수 있습니다.',
   'quiz': [{'q': 'AI가 시계열 정확도 96%를 보고했다. 먼저 물을 것은?', 'o': ['더 높일 수 있나?', '테스트 데이터가 학습에 들어갔나? 시간 순으로 나눴나?'], 'a': 1, 'why': '누설이 있으면 정확도는 의미가 없습니다.'}]},

  {'id': 'sec-3-7', 'title': '빈도·집계·달력·빠진 시점', 'tags': ['결정 네 가지', '현장: MES 내려받기'],
   'body': ['<div class="tw"><table class="tb"><tr><th>결정</th><th>선택지</th><th>원칙</th></tr>'
            '<tr><td>빈도</td><td>분·시간·일·주·월</td><td>결정의 주기에 맞춘다 (월간 구매계획 → 월, 설비 이상 감지 → 분)</td></tr>'
            '<tr><td>집계</td><td>합계·평균·마지막 값</td><td>생산·판매는 합계, 가동률·가격·온도는 평균, 재고는 월말 값</td></tr>'
            '<tr><td>달력 효과</td><td>월 일수 28~31일, 설·추석</td><td>가동일수로 나눈 일평균으로 비교</td></tr>'
            '<tr><td>빠진 시점</td><td>설비 정지, 시스템 오류</td><td>0으로 채우지 않는다. 빈칸으로 두고 원인을 적는다</td></tr></table></div>',
            'MES에서 내려받은 데이터를 월별로 묶을 때 합계와 평균을 틀리면, 가동률이 300%로 찍히거나 생산량이 하루치로 줄어드는 사고가 납니다.'],
   'talk': [('asst', 'e15', '가동률을 합계로 묶었더니 2,700%가 나왔어요…'), ('robo', 'e14', '저도 그 표를 그대로 보고했습니다.'), ('doc', 'e10', '가동률은 평균입니다. 아래에서 집계 방식을 바꿔 보세요.')],
   'widget': ('w3-agg', '<div class="ptitle">실험 · 일별 기록을 월로 묶기 (가상 30일)</div><div class="ctrl" id="ag-bt"></div><div class="tw" id="ag-tb"></div><div class="eq" id="ag-out" aria-live="polite"></div>'),
   'limit': '설·추석은 음력이라 해마다 들어가는 달이 바뀝니다. 월 평균 계절지수로는 잘 잡히지 않습니다.',
   'quiz': [{'q': '월말 재고를 월로 묶을 때 맞는 방식은?', 'o': ['합계', '평균', '마지막 값'], 'a': 2, 'why': '재고는 그 시점의 잔량이므로 월말 값을 씁니다.'}]},

  {'id': 'sec-3-8', 'title': '하나의 숫자 안의 네 가지 힘 — T·S·C·I', 'tags': ['분해: 추세·계절·순환·불규칙', '예제: 8가지 분류'],
   'body': ['<div class="tw"><table class="tb"><tr><th>요소</th><th>주기</th><th>식품·백신 예</th><th>석유화학 예</th></tr>'
            '<tr><td>추세 T</td><td>없음(한 방향)</td><td>군고구마 연 +10.8%</td><td>에틸렌 스프레드 장기 하락</td></tr>'
            '<tr><td>계절 S</td><td>1년 이내, 일정</td><td>아이스크림 8월, 호빵 12월</td><td>봄철 정기보수(TA)</td></tr>'
            '<tr><td>순환 C</td><td>여러 해, 들쭉날쭉</td><td>백신 약 4년 주기 유행</td><td>호황–증설–공급과잉–불황</td></tr>'
            '<tr><td>불규칙 I</td><td>없음(일회성)</td><td>2024년 8월 폭염</td><td>중동 전쟁·해협 봉쇄</td></tr></table></div>',
            '예측의 난이도는 계절 < 추세 < 순환 < 불규칙 순입니다. 불규칙은 예측하지 않고 대비합니다.'],
   'talk': [('sia', 'e07', '교안의 예제 ①, 여덟 가지 현상을 분류해 보겠습니다.'), ('fly', 'e09', '"주의"가 붙은 세 개가 핵심이야. 현실 사건은 한 항목에 깔끔하게 안 들어가.')],
   'widget': ('w3-tsci', '<div class="ptitle">예제 ① · 이건 어떤 요소일까?</div><div class="eq" id="ts-q"></div><div class="ctrl"><button class="bt" data-a="T" type="button">T 추세</button><button class="bt" data-a="S" type="button">S 계절</button><button class="bt" data-a="C" type="button">C 순환</button><button class="bt" data-a="I" type="button">I 불규칙</button></div><div class="eq" id="ts-out" aria-live="polite"></div>'),
   'limit': '네 조각은 생각의 틀입니다. 실제 분해 결과의 "추세" 칸에는 순환이 섞여 들어갑니다(3.13).',
   'quiz': [{'q': '"호빵이 매년 12월에 가장 많이 팔린다"는?', 'o': ['T', 'S', 'C', 'I'], 'a': 1, 'why': '매년 같은 달에 반복되는 계절입니다.'}]},

  {'id': 'sec-3-9', 'title': '계절지수 — "평균적인 달의 몇 배인가"', 'tags': ['방법: 비율-이동평균 3단계', '만화: 아이스크림 1.87'],
   'why': {'problem': '판매에는 성장(추세)과 계절이 곱해져 섞여 있습니다. 8월이 큰 게 여름 때문인지 가게가 커져서인지 구분이 안 됩니다.',
           'limit': '같은 달 평균만 내면 성장 효과가 섞이고, 한 해만 보면 그해의 우연(폭염·장마)이 섞입니다.',
           'solve': '① 12개월 중심 이동평균(추세)으로 나눠 추세를 빼고 ② 같은 달끼리 평균해 불규칙을 희석하고 ③ 12개 평균이 1이 되게 맞춥니다.',
           'easy': '케이크 12조각을 똑같이 자르지 않고, 8월 조각은 평균의 1.87배로 크게 자른다.'},
   'fx': {'q': '계절지수로 월 목표를 나누는 식이 궁금해요. 왜 12로 나눠요?',
          'school': '비와 비율, 평균(중학 수학)',
          'eq': '월 목표 = 연간 목표 × <b>계절지수</b> ÷ 12',
          'rows': [('연간 목표 ÷ 12', '계절이 없을 때 평균적인 달의 몫'), ('× 계절지수', '그 달이 평균의 몇 배인지 반영'), ('12개 평균 = 1', '12조각을 다 합치면 연간 목표와 같다')],
          'calc': '연간 10,000개면 평균적인 달 833개입니다. 8월은 833 × 1.87 ≈ 1,558개(10,000 × 1.87 ÷ 12 = 1,558.3)입니다.',
          'comment': '12로 나눈 몫에 배수를 곱하는 거라서, 다 더하면 원래 10,000개가 되는 거군요!'},
   'body': ['이 페이지가 수업 데이터로 다시 계산한 결과도 교안과 같습니다. 아이스크림 8월 1.87, 1월 0.46, 호빵 12월 2.59(≈2.6), 7월 0.08입니다.',
            '아이스크림과 호빵은 정확히 반대로 움직입니다. 두 곡선이 봄(3~4월)과 가을(9~10월)에 엇갈리는 곳이 한 라인에서 빙과와 호빵을 번갈아 만드는 라인 전환 시점입니다.'],
   'talk': [('moa', 'e01', '3D 냉동창고 더미 높이가 이 숫자예요! 호빵 버튼도 눌러 보세요.'), ('robo', 'e07', '그럼 1월 목표는 833 × 0.46…'), ('asst', 'e10', '383개요. 아래 배분기로 열두 달을 한 번에 볼게요.')],
   'widget': ('w3-alloc', '<div class="ptitle">배분기 · 연간 목표를 계절지수로 월별 배분</div><div class="ctrl"><div class="group"><span class="glabel">연간 목표</span><input type="range" min="1000" max="30000" step="500" value="10000" id="al-n"><span class="val" id="al-vn"></span></div><button class="bt on" data-k="icecream" type="button">아이스크림</button><button class="bt" data-k="hoppang" type="button">호빵</button><button class="bt" data-k="sweet_potato" type="button">군고구마</button></div><div class="cwrap"><svg id="al-svg"></svg></div><div class="eq" id="al-out" aria-live="polite"></div>'),
   'code': [('df.rolling(12, center=True).mean()', '12개월 중심 이동평균(추세)'), ('ratio = sales / trend', '① 추세로 나누기'), ('ratio.groupby(month).mean()', '② 같은 달끼리 평균'), ('si / si.mean()', '③ 평균이 1이 되게 맞추기')],
   'limit': '맨 앞·맨 뒤 6개월은 12개월 창을 채울 수 없어 이동평균이 비어 있습니다. 최근 달의 추세는 따로 처리(창 줄이기, 추세선 연장)해야 합니다.',
   'quiz': [{'q': '연간 12,000개, 계절지수 1.5인 달의 목표는?', 'o': ['1,000개', '1,500개', '18,000개'], 'a': 1, 'why': '12,000 × 1.5 ÷ 12 = 1,500개입니다.'}]},

  {'id': 'sec-3-10', 'title': '더하기(가법)냐 곱하기(승법)냐', 'tags': ['모형: 가법·승법', '판단: 파도 높이'],
   'pair': ('더하기 (가법)', '계절마다 일정한 "폭"을 더하거나 뺀다. "4월엔 −5.7%p" — NCC 가동률처럼 0~100% 안에 갇혀 규모가 커져도 파도 폭이 일정한 데이터.',
            '곱하기 (승법)', '계절마다 일정한 "비율"을 곱한다. "8월엔 평균의 1.87배" — 아이스크림·호빵·군고구마·백신처럼 규모가 커지면 파도도 같이 커지는 데이터.'),
   'body': ['판단법은 간단합니다. 선 그래프를 그렸을 때 추세는 오르는데 파도 높이가 예나 지금이나 같으면 가법, 파도 높이도 점점 커지면 승법입니다.',
            '아이스크림 가게가 겨울 100개·여름 200개(+100개)를 팔다가 대박이 나서 겨울 1,000개를 팔면, 여름은 2,000개(+1,000개)쯤 팔릴 것입니다. 그래서 곱하기가 어울립니다.',
            '승법은 로그를 씌우면 가법이 됩니다. 회귀에서 판매량에 로그를 씌워 계수를 "몇 배"로 읽는 이유입니다(3.12).'],
   'talk': [('robo', 'e16', '그럼 가동률도 "4월은 평균의 0.94배"로 쓰면 되지 않습니까?'), ('fly', 'e09', '가동률이 95%인 공장과 70%인 공장에서 정기보수 5.7%p가 같은 배수일까?'), ('asst', 'e07', '아래에서 추세를 키우며 두 모형의 파도를 비교해 볼게요.')],
   'widget': ('w3-am', '<div class="ptitle">실험 · 추세가 커질 때 두 모형의 파도</div><div class="ctrl"><div class="group"><span class="glabel">성장 속도</span><input type="range" min="0" max="10" value="5" id="am-g"><span class="val" id="am-vg"></span></div><button class="bt on" data-m="m" type="button">곱하기(승법)</button><button class="bt" data-m="a" type="button">더하기(가법)</button></div><div class="cwrap"><svg id="am-svg"></svg></div><div class="eq" id="am-out" aria-live="polite"></div>'),
   'explain': ['NCC 가동률의 계절 효과를 가법으로 다시 계산하면 4월 −5.7%p, 5월 −3.3%p로 교안과 같습니다. 석유화학 공장이 봄 비수기에 정기보수(TA)를 몰아 하는 일정이 만든 계절성입니다.'],
   'limit': '현실 데이터는 둘 사이 어딘가일 때가 많습니다. 판단이 어려우면 두 모형을 모두 돌려 채점(3.12)으로 고릅니다.',
   'quiz': [{'q': '파도 높이가 추세를 따라 점점 커진다면?', 'o': ['가법', '승법'], 'a': 1, 'why': '규모에 비례해 계절 폭이 커지는 것이 승법입니다.'}]},

  {'id': 'sec-3-11', 'title': '이동평균·분해·계절조정 — "지난달보다 늘었다"를 공정하게', 'tags': ['방법: 분해', '현장: 월간 보고'],
   'body': ['12개월 이동평균을 그리면 톱니는 크지만 추세선은 거의 평평합니다. 판매의 큰 흔들림은 대부분 계절이었다는 뜻입니다.',
            '원래 값을 계절지수로 나누면 계절을 뺀 값이 됩니다. 2025년 아이스크림은 원래 값으로 봄에 매달 25~30%씩 늘었지만, 계절을 빼면 대부분 "원래 그맘때 느는 만큼"이었습니다.',
            '6월은 원래 값으로 +27%지만 계절을 빼면 −10%로 나쁜 달이었고, 7월은 조정 후에도 +24%로 평년보다 더웠던 달입니다.'],
   'talk': [('robo', 'e24', '6월 +27%가 사실은 나쁜 달이었다고요?'), ('fly', 'e10', '6월은 원래 1.55배 파는 달이야. 27%로는 모자라.'), ('moa', 'e09', '월간 보고서는 계절조정 전월비나 전년 동월비로 써야겠네요.')],
   'widget': ('w3-adj', '<div class="ptitle">계산 · 2025 아이스크림 전월 대비 — 원래 값 vs 계절조정</div><div class="cwrap"><svg id="aj-svg"></svg></div><div class="eq" id="aj-out" aria-live="polite"></div>'),
   'explain': ['막대는 수업 데이터로 이 페이지가 직접 계산했습니다. 4월 조정 후 값은 교안의 −0.2%와 소수점 아래에서 조금 다릅니다(계절지수 반올림 차이).'],
   'limit': '분해의 "불규칙" 칸은 1 근처에 흩어진 점이어야 정상입니다. 모양(물결·기울기)이 보이면 덜 떼어 낸 요소가 남아 있다는 신호입니다.',
   'quiz': [{'q': '계절 품목의 월간 보고에 알맞은 비교는?', 'o': ['원래 값 전월비', '계절조정 전월비 또는 전년 동월비'], 'a': 1, 'why': '원래 값 전월비는 계절 효과가 대부분입니다.'}]},

  {'id': 'sec-3-12', 'title': '기준선부터 이겨라 — 나이브·지수평활·채점', 'tags': ['방법: 홀드아웃', '지표: MAPE'],
   'fx': {'q': 'MAPE 8.9%라는 건 무슨 뜻이에요? 정확도 91%예요?',
          'school': '절댓값과 백분율, 평균(중학 수학)',
          'eq': 'MAPE = 평균( |실제 − 예측| ÷ 실제 ) × 100',
          'rows': [('|실제 − 예측|', '빗나간 크기 (부호 무시)'), ('÷ 실제', '그 달 규모에 비해 몇 %인가'), ('평균', '열두 달을 고르게 평균')],
          'calc': '2025년 아이스크림을 "작년 같은 달 값"(계절 나이브)으로 예측하면 MAPE 8.9%입니다. 최근 12개월 평균 하나로 예측하면 62%까지 커집니다.',
          'comment': '평균 9% 정도 빗나간다는 뜻이고, "정확도 91%"라고 부르면 오해가 생기겠네요.'},
   'body': ['가장 단순한 두 기준선은 나이브(다음 달 = 이번 달)와 계절 나이브(다음 달 = 작년 같은 달)입니다. 새 모델을 들일 때 첫 질문은 "계절 나이브보다 얼마나 나은가?"입니다.',
            '지수평활은 최근을 더 믿습니다. 다음 달 예측 = α × 이번 달 실제 + (1 − α) × 이번 달 예측. α가 크면 빨리 반응하고(잡음에도 흔들림), 작으면 안정적입니다. 추세·계절까지 평활하면 홀트-윈터스입니다.',
            '교안의 2025 채점 결과는 계절 나이브 8.9%, 추세 + 월 더미 회귀 7.3%, 홀트-윈터스 7.4%입니다. 회귀와 홀트-윈터스가 사실상 동점이면 설명하기 쉬운 쪽을 고릅니다.'],
   'talk': [('robo', 'e19', '복잡한 모델이 무조건 이깁니다!'), ('fly', 'e09', '8.9% → 7.3%면 1.6%p 차이야. 그 차이가 도입 비용만큼 값어치가 있어?'), ('asst', 'e07', '아래에서 α를 바꿔 지수평활을 직접 채점해 볼게요.')],
   'widget': ('w3-es', '<div class="ptitle">채점 · 2025년 12개월을 가리고 맞히기 (이 페이지 계산)</div><div class="ctrl"><div class="group"><span class="glabel">지수평활 α (계절조정 값에 적용)</span><input type="range" min="0.05" max="0.95" step="0.05" value="0.3" id="es-a"><span class="val" id="es-va"></span></div></div><div class="cwrap"><svg id="es-svg"></svg></div><div class="kpis" id="es-k"></div>'),
   'limit': '교안의 회귀·홀트-윈터스 값(7.3%, 7.4%)은 교안 계산을 옮긴 것입니다. 이 페이지의 지수평활은 계절조정 값에 단순 지수평활을 한 뒤 계절지수를 다시 곱한 간이 방법입니다.',
   'quiz': [{'q': '새 예측 모델 도입 때 첫 질문은?', 'o': ['파라미터가 몇 개인가', '계절 나이브보다 얼마나 나은가'], 'a': 1, 'why': '단순 기준선을 못 이기면 도입할 이유가 없습니다.'}]},

  {'id': 'sec-3-13', 'title': '외삽과 순환 — 선을 멀리 늘이면', 'tags': ['함정: 외삽', '데이터: 백신 144개월'],
   'body': ['군고구마 연 판매를 직선으로 늘이면 2035년 7,524, 연 10.8% 성장률로 늘이면 11,716입니다. 둘 다 지난 7년에는 잘 맞지만 10년 뒤에는 1.6배 차이입니다. 흔한 어림 규칙은 "추세는 데이터 기간의 절반 이내까지만 믿는다"입니다.',
            '백신 접종은 12년 동안 전체로는 늘었지만, 연간 증감률은 몇 년마다 부호를 바꿉니다. 2015 · 2019 · 2023년에 정점, 약 4년 간격입니다. 2023→2025년 28% 감소는 시장 축소가 아니라 물결의 골짜기였습니다.',
            '12년에 정점 3번으로는 주기를 확정할 수 없습니다. 순환은 점으로 맞히지 않고 낮음 · 보통 · 높음 시나리오로 범위를 잡고, 해외 유행 소식·감시 환자 수·검색량 같은 선행 신호로 어느 쪽인지 가늠합니다.'],
   'talk': [('robo', 'e24', '2년 연속 감소! 백신 라인을 줄입시다!'), ('fly', 'e03', '정점 사이의 저점이야. 아래 연간 막대를 봐.'), ('x1', 'e04', '(헉)')],
   'widget': ('w3-vac', '<div class="ptitle">계산 · 백신 연간 접종량과 증감률 (수업 데이터)</div><div class="cwrap"><svg id="vc-svg"></svg></div><div class="eq" id="vc-out" aria-live="polite"></div>'),
   'limit': '백신 데이터는 가상 데이터입니다. 실제 감염병 순환은 더 불규칙하고 정책·변이의 영향을 받습니다.',
   'quiz': [{'q': '순환을 다루는 알맞은 방법은?', 'o': ['정확한 주기를 맞힌다', '낮음·보통·높음 시나리오와 선행 신호'], 'a': 1, 'why': '주기와 높이가 매번 달라 범위로 대비합니다.'}]},

  {'id': 'sec-3-14', 'title': '석유화학 — 예측이 빗나갈 때', 'tags': ['구조 변화 · 충격 · 변동성 · 시차', '데이터: 2015-01~2026-08'],
   'body': ['NCC 공장의 수익성은 에틸렌 가격 − 나프타 가격(스프레드)입니다. 원료가는 원유를 따라 크게 출렁이지만, 스프레드는 업황을 따라 움직입니다.',
            '빗나가는 이유는 네 가지입니다. ① 구조 변화 — 스프레드는 2022년부터 한 계단 내려앉아 돌아오지 않았습니다(과거 7년 평균 481로 돌아온다고 본 예측은 실제 191보다 152% 높음). ② 처음 보는 충격 — 2026년 1월 말에 그린 80% 예측구간 밖으로 일곱 달 연속 나갔습니다. ③ 변동성 군집 — 한 번 흔들리면 계속 흔들립니다. ④ 전가 시차 — 원료가는 먼저, 제품가는 나중에 따라와 그사이 마진이 눌립니다.',
            '다섯 번째로 정책·행동의 반작용(수출 금지, 매점매석 금지)이 더해집니다. 다섯 모두 과거 데이터 안에 정보가 없다는 공통점이 있습니다. 데이터를 더 모으거나 모델을 복잡하게 해도 해결되지 않습니다.'],
   'talk': [('robo', 'e21', '제 80% 구간이… 일곱 번 다 틀렸습니다.'), ('fly', 'e10', '계산 실수가 아니라 "미래의 흔들림은 과거와 같다"는 가정이 깨진 거야.'), ('doc', 'e09', '데이터는 가상이지만, 사건의 시점과 방향은 현실에서 가져왔습니다.')],
   'widget': ('w3-pet', '<div class="ptitle">계산 · 에틸렌 스프레드와 두바이유 (수업 데이터, 월)</div><div class="ctrl"><button class="bt on" data-m="0" type="button">스프레드 ($/t)</button><button class="bt" data-m="1" type="button">두바이유 ($/bbl)</button><button class="bt" data-m="2" type="button">NCC 가동률 (%)</button></div><div class="cwrap"><svg id="pt-svg"></svg></div><div class="eq" id="pt-out" aria-live="polite"></div>'),
   'limit': '석유화학 데이터는 수업용 가상 데이터입니다. 가격 수준은 실제와 다르며, 사건 시점·방향만 흉내 냈습니다.',
   'quiz': [{'q': '80% 예측구간 밖으로 일곱 달 연속 나간 이유는?', 'o': ['계산 실수', '과거 흔들림이 미래에도 같다는 가정이 깨짐'], 'a': 1, 'why': '처음 보는 충격과 변동성 군집 때문입니다.'}]},

  {'id': 'sec-3-15', 'title': '예측에서 결정으로 — 틀릴 것을 알고 정하는 법', 'tags': ['결정: 안전재고 · 신문팔이 · 시나리오', '현장: 품목별 전략'],
   'fx': {'q': '호빵을 예측보다 더 만들라는 게 이해가 안 돼요. 남으면 버리잖아요?',
          'school': '확률과 기댓값(고등 수학), 비율',
          'eq': '임계비율 = <b>Cu</b> ÷ (Cu + Co) · Cu = 판매가 − 원가, Co = 원가 − 처분가',
          'rows': [('Cu', '하나 모자랄 때 잃는 이익 (부족 비용)'), ('Co', '하나 남을 때 잃는 돈 (과잉 비용)'), ('임계비율', '수요가 이 확률 이하가 되도록 생산량을 정한다')],
          'calc': '판매 1,500원, 원가 600원, 처분 100원이면 Cu = 900, Co = 500, 임계비율 = 900 ÷ 1,400 = 0.643입니다. 50%보다 크니 예측(844)보다 조금 많은 870을 만듭니다.',
          'comment': '모자라서 잃는 돈이 남아서 버리는 돈보다 크니까, 조금 넉넉히 만드는 게 이득이군요!'},
   'body': ['안전재고는 틀리는 크기에서 나옵니다. 아이스크림 여름 예측 오차(RMSE) 174.8천 개 × 1.65(서비스 수준 95%) ≈ 288천 개입니다. 99%로 올리면 계수가 2.33이 되어 재고가 약 1.4배로 늘어납니다.',
            '품목의 성격이 전략을 정합니다. 아이스크림은 선생산, 호빵은 신문팔이, 군고구마는 계약재배, 백신은 시나리오 + 옵션, 나프타는 장기 + 현물 혼합입니다.',
            '예측을 잘하는 공장보다, 틀렸을 때 덜 다치는 공장이 오래 갑니다.'],
   'talk': [('robo', 'e07', '서비스 수준 100%로 하면 품절이 없습니다!'), ('fly', 'e09', 'z가 무한대로 가. 창고가 공장보다 커질걸?'), ('sia', 'e10', '서비스 수준은 통계가 아니라 경영 결정이라고 교안에 적혀 있습니다.'), ('x2', 'e16', '(끄덕끄덕)')],
   'widget': ('w3-nv', '<div class="ptitle">계산기 · 신문팔이(호빵)와 안전재고(아이스크림)</div><div class="ctrl"><div class="group"><span class="glabel">판매가</span><input type="range" min="800" max="3000" step="50" value="1500" id="nv-p"><span class="val" id="nv-vp"></span></div><div class="group"><span class="glabel">원가</span><input type="range" min="200" max="1500" step="50" value="600" id="nv-c"><span class="val" id="nv-vc"></span></div><div class="group"><span class="glabel">처분가</span><input type="range" min="0" max="500" step="50" value="100" id="nv-s"><span class="val" id="nv-vs"></span></div></div><div class="eq" id="nv-out" aria-live="polite"></div><div class="ctrl"><div class="group"><span class="glabel">서비스 수준</span><input type="range" min="0.80" max="0.99" step="0.01" value="0.95" id="ss-q"><span class="val" id="ss-vq"></span></div></div><div class="eq" id="ss-out" aria-live="polite"></div>'),
   'explain': ['신문팔이 생산량은 교안처럼 수요가 정규분포(평균 844, 표준편차는 교안 870에 맞춘 약 70)라고 놓고 계산했습니다. 표준편차는 이 페이지가 정한 설명용 값입니다.'],
   'limit': '정규분포 가정은 꼬리 위험(드물고 큰 사건)을 과소평가합니다. 봉쇄 같은 충격은 시나리오로 따로 다룹니다.',
   'quiz': [{'q': '임계비율이 0.5보다 크면 생산량은?', 'o': ['예측보다 적게', '예측보다 많게', '예측과 같게'], 'a': 1, 'why': '부족 비용이 과잉 비용보다 크면 넉넉히 만듭니다.'}]},
 ],
 'duel': {
   'q': '2025년 아이스크림, 무엇으로 예측할까?',
   'intro': [('doc', 'e07', '2019~2024년으로 배우고 2025년 열두 달을 맞힙니다. 주판봇은 최근 12개월 평균, 초파리 연구원은 작년 같은 달(계절 나이브)입니다.'), ('sia', 'e12', '시작 신호!')],
   'fly': '작년 같은 달을 그대로. 계절이 이렇게 센데 평균 하나로는 안 돼.',
   'robo': '최근 12개월 평균이면 충분! 평균은 거짓말을 안 합니다!',
   'widget': 'w3-duel',
   'panel': '<div class="ptitle">채점 · 2025년 12개월 MAPE (수업 데이터 계산)</div><button class="bt primary" id="du3-run" type="button">채점하기</button><div class="cwrap"><svg id="du3-svg"></svg></div><div class="kpis" id="du3-k"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('moa', 'e12', '초파리 연구원님 최고!'), ('x3', 'e01', '(짝짝짝)')],
 },
 'summary': {
   'head': ['단계', '한 줄', '공장에서 쓰는 곳'],
   'rows': [['① 다르다', '순서가 정보 · 자기상관 · 정상성 · 시간 순 검증', 'MES 데이터 날짜순 보관, AI에게 분할 방식 되묻기'],
            ['② 쪼갠다', 'T·S·C·I, 가법(가동률)·승법(판매)', '보정수치 보고(%p vs 배)'],
            ['③ 내다본다', '이동평균 → 계절지수 → 계절조정 → 기준선 → 채점', '월별 목표 배분, 계절조정 전월비 보고'],
            ['④ 빗나간다', '구조 변화 · 충격 · 변동성 군집 · 전가 시차 · 정책', '시나리오와 선행 신호'],
            ['⑤ 결정한다', '안전재고 · 신문팔이 · 시나리오+옵션 · 장기+현물', '선생산·발주·계약 구조']],
   'limits': ['식품·백신·석유화학 데이터는 모두 수업용 가상 데이터입니다(사건의 시점·방향만 현실에서 가져옴).',
              '3D 냉동창고의 더미 높이는 계절지수를 보여 주는 그림이지 실제 재고량이 아닙니다.',
              '이 페이지 계산(누설 실험, 지수평활)은 교안과 방법이 달라 숫자가 다를 수 있습니다. 교안 숫자는 교안 숫자라고 밝혔습니다.'],
 },
 'outro': [('doc', 'e16', '시계열은 순서가 정보입니다. 과거 패턴이 이어진다는 가정 위에서 예측하되, 그 가정이 깨지는 순간을 대비합니다.'),
           ('asst', 'e01', '실습 리포트에서 계절지수 12개를 직접 뽑아 볼게요!'),
           ('fly', 'e10', '이번 주 안에 자기 공정 월별 실적 2년치에서 네 조각 중 무엇이 제일 큰지 한 문장으로 적어 와.'),
           ('robo', 'e14', '저는 "봄에 30% 늘었다" 보고서를 다시 쓰겠습니다…')],
 'sources': [('강의 교안', '스마트 제조 3주차 「생산실적 추세 분석 — 시계열의 원리」(50장) · 3주차 실습 부록 「파이썬으로 따라 하는 시계열 예측」 · 계절지수 만화(EP.1~4) · 가법과 승법 참고 자료 — 안상선'),
             ('수업 데이터', 'week03_seasonal_foods.csv(2019-01~2025-12), week03_vaccine_1.csv(2014-01~2025-12), week03_petrochem.csv(2015-01~2026-08) — 모두 수업용 가상 데이터'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '2026 아이스크림 예측 수요, 신문팔이 표준편차(약 70), 집계 실험의 30일 기록, 가법·승법 실험의 파도는 설명용 값입니다. 나머지 숫자는 수업 데이터로 계산했습니다.',
 'practice': ('practice.html', '계절지수 12개를 직접 뽑고 검산하다'),
}

CH['js'] = _DATA + r'''
(function(){var D=window.D3;D.yr=function(i){return +D.m[i].slice(0,4)};})();
function acf(x,k){var n=x.length,m=x.reduce(function(a,b){return a+b})/n,num=0,den=0;for(var i=0;i<n;i++){den+=(x[i]-m)*(x[i]-m);if(i>=k)num+=(x[i]-m)*(x[i-k]-m);}return num/den;}
function mape(a,p){var s=0;for(var i=0;i<a.length;i++)s+=Math.abs(a[i]-p[i])/a[i];return s/a.length*100;}
function sayDoc(mood,html){var v=document.getElementById('verdict');v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
W['w3-cap']=function(b){var M=['3월','4월','5월','6월','7월','8월','9월'],Dm=[576,747,908,1251,1439,1472,1054];var c=b.querySelector('#cp-c'),s=b.querySelector('#cp-svg'),o=b.querySelector('#cp-out');function f(){var C=+c.value;b.querySelector('#cp-v').textContent=C;var P=Dm.map(function(d){return Math.min(d,C)});var inv=0,short=0,first=null;Dm.forEach(function(d,i){inv+=C-d;if(inv<0&&first==null)first=M[i];});Chart.bars(s,{labels:M,series:[{name:'예측 수요',color:'#82b8ff',values:Dm},{name:'생산실적(상한 '+C+')',color:'#f1b646',values:P}],min:0,max:1600,h:230});o.innerHTML='3월부터 월 '+C+'씩 만들면 9월 말 누적 재고 <b>'+inv.toLocaleString()+'</b>천 개'+(first?' · <em>'+first+'부터 모자랍니다</em> · 실적표만 보면 수요가 '+C+'에서 평평해 보입니다':' · 모자라는 달이 없습니다')+'. 교안: 안전재고까지 지키려면 월 1,114 필요.';}c.oninput=f;f();};
W['w3-kind']=function(b){var Q=[['오늘 라인 6개의 불량률',0],['A라인의 지난 2년 일별 불량률',1],['협력사 30곳의 납기 준수율(2026년)',0],['2015~2026 월별 나프타 가격',1],['설비 1대의 분 단위 진동 로그',1],['작업자 50명의 교육 이수 시간',0]],i=0,sc=0,q=b.querySelector('#kd-q'),o=b.querySelector('#kd-out');function sh(){q.textContent='('+(i+1)+'/'+Q.length+') '+Q[i][0];}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var ok=+x.dataset.a===Q[i][1];if(ok)sc++;o.innerHTML=(ok?'✔ 맞습니다.':'✘ 정답은 <b>'+['횡단면','시계열'][Q[i][1]]+'</b>입니다.')+' 점수 '+sc+'/'+(i+1);i=(i+1)%Q.length;if(!i)sc=0;sh();};});sh();};
W['w3-shuf']=function(b){var x=D3.ic.slice(),s=b.querySelector('#sh-svg'),k=b.querySelector('#sh-k'),r=rng(84);function f(v,lab){Chart.line(s,{labels:D3.m,series:[{name:lab,color:'#ff86b8',values:v}],h:220,ticks:7});var m=v.reduce(function(a,c){return a+c})/v.length;k.innerHTML='<div class="kpi a"><b>'+m.toFixed(1)+'</b><span>평균</span></div><div class="kpi g"><b>'+acf(v,1).toFixed(2)+'</b><span>1개월 전과의 상관</span></div><div class="kpi m"><b>'+acf(v,12).toFixed(2)+'</b><span>12개월 전과의 상관</span></div><div class="kpi r"><b>'+Math.max.apply(null,v)+'</b><span>최댓값</span></div>';}b.querySelector('#sh-o').onclick=function(){this.classList.add('on');b.querySelector('#sh-s').classList.remove('on');f(x,'날짜순');};b.querySelector('#sh-s').onclick=function(){this.classList.add('on');b.querySelector('#sh-o').classList.remove('on');var y=x.slice();for(var i=y.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var t=y[i];y[i]=y[j];y[j]=t;}f(y,'섞은 뒤');};f(x,'날짜순');};
W['w3-acf']=function(b){var L=[],V=[];for(var k=1;k<=24;k++){L.push(k);V.push(acf(D3.ic,k));}Chart.bars(b.querySelector('#ac-svg'),{labels:L,series:[{name:'자기상관',color:'#82b8ff',values:V,colorAt:function(v,i){return (i+1)%12==0?'#5ee39c':v<0?'#f0604d':'#82b8ff'}}],min:-1,max:1,h:220});b.querySelector('#ac-out').innerHTML='12개월 <b>'+V[11].toFixed(2)+'</b>, 24개월 <b>'+V[23].toFixed(2)+'</b> (초록) · 6개월 <em>'+V[5].toFixed(2)+'</em> — 반년 차이는 정반대 계절이라 음수입니다.';};
W['w3-stat']=function(b){var na=D3.na,h=Math.floor(na.length/2),ch=na.map(function(v,i){return i?(v/na[i-1]-1)*100:null});var s=b.querySelector('#stt-svg'),o=b.querySelector('#stt-out');function st(a){a=a.filter(function(v){return v!=null});var m=a.reduce(function(x,y){return x+y})/a.length,sd=Math.sqrt(a.reduce(function(x,y){return x+(y-m)*(y-m)},0)/(a.length-1));return [m,sd];}function f(md){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',+x.dataset.m===md)});var v=md?ch:na;var A=st(v.slice(0,h)),B=st(v.slice(h));var mA=v.map(function(_,i){return i<h?A[0]:null}),mB=v.map(function(_,i){return i>=h?B[0]:null});Chart.line(s,{labels:D3.pm,series:[{name:md?'월 변화율(%)':'나프타($/t)',color:'#f1b646',values:v},{name:'앞 절반 평균',color:'#5ee39c',values:mA,dash:'5 4'},{name:'뒤 절반 평균',color:'#f0604d',values:mB,dash:'5 4'}],h:230,ticks:7});o.innerHTML=(md?'월 변화율':'가격 수준')+' · 앞 절반 평균 <b>'+A[0].toFixed(1)+'</b>, 표준편차 '+A[1].toFixed(1)+' → 뒤 절반 평균 <b>'+B[0].toFixed(1)+'</b>, 표준편차 <em>'+B[1].toFixed(1)+'</em> ('+(B[1]/A[1]).toFixed(1)+'배)';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(+x.dataset.m)}});f(0);};
W['w3-leak']=function(b){b.querySelector('#lk-run').onclick=function(){var x=D3.na,n=x.length,k=28,r=rng(28),idx=[];while(idx.length<k){var j=1+Math.floor(r()*(n-2));if(idx.indexOf(j)<0)idx.push(j);}var e1=0;idx.forEach(function(j){var p=(x[j-1]+x[j+1])/2;e1+=Math.abs(x[j]-p)/x[j];});e1=e1/k*100;var e2=0,last=x[n-k-1];for(var j=n-k;j<n;j++)e2+=Math.abs(x[j]-last)/x[j];e2=e2/k*100;b.querySelector('#lk-k').innerHTML='<div class="kpi g"><b>'+e1.toFixed(1)+'%</b><span>무작위로 28개월 가림 · 평균 오차</span></div><div class="kpi r"><b>'+e2.toFixed(1)+'%</b><span>마지막 28개월 가림 · 평균 오차</span></div><div class="kpi a"><b>'+(e2/e1).toFixed(1)+'배</b><span>차이</span></div><div class="kpi m"><b>3.9% · 21.6%</b><span>교안 결과(다른 방법)</span></div>';b.querySelector('#lk-out').innerHTML='무작위 검증은 가린 달의 <em>다음 달(미래)</em>을 보고 맞혔습니다. 그 숫자를 믿고 구매 계획을 세웠다면 2026년 봄에 크게 당했을 것입니다.';};};
W['w3-agg']=function(b){var r=rng(30),day=[];for(var i=0;i<30;i++){var stop=(i==12||i==13);day.push({prod:stop?null:Math.round(950+r()*120),util:stop?null:Math.round(86+r()*8),inv:Math.round(400+i*6+r()*30)});}var M=[['생산(합계)','prod','sum'],['생산(평균)','prod','avg'],['가동률(합계)','util','sum'],['가동률(평균)','util','avg'],['재고(합계)','inv','sum'],['재고(마지막 값)','inv','last']],ok={'prod-sum':1,'util-avg':1,'inv-last':1};var bt=b.querySelector('#ag-bt'),tb=b.querySelector('#ag-tb'),o=b.querySelector('#ag-out');M.forEach(function(m){var x=document.createElement('button');x.className='bt';x.textContent=m[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.toggle('on',y===x)});var v=day.map(function(d){return d[m[1]]}).filter(function(v){return v!=null});var res=m[2]=='sum'?v.reduce(function(a,c){return a+c}):m[2]=='avg'?v.reduce(function(a,c){return a+c})/v.length:v[v.length-1];var good=ok[m[1]+'-'+m[2]];o.innerHTML=m[0]+' = <b style="color:'+(good?'var(--gfp)':'var(--eye)')+'">'+Math.round(res).toLocaleString()+(m[1]=='util'?'%':'')+'</b> '+(good?'✔ 알맞은 집계':'✘ '+(m[1]=='util'?'가동률을 더하면 100%를 훌쩍 넘습니다':m[1]=='prod'?'생산을 평균하면 하루치로 줄어듭니다':'재고를 더하면 30일치 재고를 겹쳐 셉니다'))+' · 13·14일은 설비 정지로 <i>빈칸</i>(0으로 채우지 않음)';};bt.appendChild(x);});tb.innerHTML='<table class="tb"><tr><th>일</th><th>생산</th><th>가동률</th><th>재고</th></tr>'+day.slice(10,16).map(function(d,i){return '<tr><td>'+(i+11)+'일</td><td class="n">'+(d.prod==null?'(정지)':d.prod)+'</td><td class="n">'+(d.util==null?'(정지)':d.util+'%')+'</td><td class="n">'+d.inv+'</td></tr>'}).join('')+'<tr><td colspan="4" style="color:var(--muted)">… 30일 중 일부</td></tr></table>';bt.firstChild.click();};
W['w3-tsci']=function(b){var Q=[['호빵이 매년 12월에 가장 많이 팔린다','S','매년 같은 달, 달력으로 예약 가능'],['편의점 군고구마 판매가 7년째 늘고 있다','T','한 방향의 장기 변화'],['감염병 X가 대략 4년마다 크게 유행한다','C','여러 해 주기, 길이가 들쭉날쭉'],['NCC 가동률이 매년 4월에 낮다','S','정기보수 일정이 만든 계절'],['중국 대규모 증설 이후 에틸렌 마진이 몇 년째 낮다','T','주의: 수준 자체가 바뀐 구조 변화에 가깝다'],['호황기 증설 → 공급과잉 → 불황이 반복된다','C','투자 시차가 만드는 사이클'],['호르무즈 해협 봉쇄로 한 달 새 유가가 급등했다','I','일회성 충격. 단 여파가 수개월 이어진다'],['설 연휴가 있는 달은 공장 생산량이 적다','S','주의: 음력이라 해마다 달이 바뀐다 → 월 평균으로 안 잡힌다']],i=0,sc=0,q=b.querySelector('#ts-q'),o=b.querySelector('#ts-out');function sh(){q.textContent='('+(i+1)+'/8) '+Q[i][0];}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var ok=x.dataset.a===Q[i][1];if(ok)sc++;o.innerHTML=(ok?'✔ ':'✘ 정답 <b>'+Q[i][1]+'</b> · ')+Q[i][2]+' · 점수 '+sc+'/'+(i+1);i=(i+1)%8;if(!i)sc=0;sh();};});sh();};
W['w3-alloc']=function(b){var n=b.querySelector('#al-n'),s=b.querySelector('#al-svg'),o=b.querySelector('#al-out'),k='icecream',M=['1','2','3','4','5','6','7','8','9','10','11','12'];function f(){var N=+n.value;b.querySelector('#al-vn').textContent=N.toLocaleString();var si=SI3[k],v=si.map(function(x){return N*x/12});Chart.bars(s,{labels:M.map(function(m){return m+'월'}),series:[{name:'월 목표',color:{icecream:'#ff86b8',hoppang:'#f1b646',sweet_potato:'#c48a5a'}[k],values:v}],ref:N/12,values:true,fmt:function(x){return Math.round(x).toLocaleString()},h:240});var mx=v.indexOf(Math.max.apply(null,v));o.innerHTML='평균적인 달 '+Math.round(N/12).toLocaleString()+'개(노란 점선) · 최대 <b>'+(mx+1)+'월 '+Math.round(v[mx]).toLocaleString()+'개</b> (지수 '+si[mx].toFixed(2)+') · 12달 합계 '+Math.round(v.reduce(function(a,c){return a+c})).toLocaleString()+'개';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){k=x.dataset.k;b.querySelectorAll('.ctrl .bt').forEach(function(y){y.classList.toggle('on',y===x)});f();}});n.oninput=f;f();};
W['w3-am']=function(b){var g=b.querySelector('#am-g'),s=b.querySelector('#am-svg'),o=b.querySelector('#am-out'),md='m';function f(){var G=+g.value;b.querySelector('#am-vg').textContent=G;var L=[],V=[],T=[];var amp=[];for(var t=0;t<60;t++){var tr=100*(1+G*t/100),se=Math.sin(t/12*2*Math.PI);var v=md=='m'?tr*(1+.4*se):tr+40*se;L.push(Math.floor(t/12)+1+'년');V.push(v);T.push(tr);}for(var y=0;y<5;y++){var seg=V.slice(y*12,y*12+12);amp.push(Math.max.apply(null,seg)-Math.min.apply(null,seg));}Chart.line(s,{labels:L,series:[{name:md=='m'?'곱하기':'더하기',color:md=='m'?'#ff86b8':'#82b8ff',values:V},{name:'추세',color:'#f1b646',values:T,dash:'5 4'}],h:220,ticks:5});o.innerHTML='해마다 파도 높이: '+amp.map(function(a){return Math.round(a)}).join(' → ')+' · '+(md=='m'?'<b>추세가 커질수록 파도도 커집니다</b>':'<b>추세가 커져도 파도 폭은 그대로입니다</b>');}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){md=x.dataset.m;b.querySelectorAll('.ctrl .bt').forEach(function(y){y.classList.toggle('on',y===x)});f();}});g.oninput=f;f();};
W['w3-adj']=function(b){var n=D3.ic.length,y=D3.ic.slice(n-13),si=SI3.icecream,M=['2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'];var raw=[],adj=[];for(var i=1;i<13;i++){var m=i===0?11:(i-1)%12;}var vals=D3.ic.slice(n-12),prev=D3.ic[n-13];var a=[prev/si[11]].concat(vals.map(function(v,i){return v/si[i]}));var r=[prev].concat(vals);for(var i=1;i<13;i++){raw.push((r[i]/r[i-1]-1)*100);adj.push((a[i]/a[i-1]-1)*100);}var L=['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'];Chart.bars(b.querySelector('#aj-svg'),{labels:L,series:[{name:'원래 값 전월비(%)',color:'#f1b646',values:raw},{name:'계절조정 전월비(%)',color:'#5ee39c',values:adj}],h:240});b.querySelector('#aj-out').innerHTML='6월: 원래 <b>'+raw[5].toFixed(1)+'%</b> → 조정 후 <em>'+adj[5].toFixed(1)+'%</em> · 7월: 원래 '+raw[6].toFixed(1)+'% → 조정 후 <b>'+adj[6].toFixed(1)+'%</b> · 4월 조정 후 '+adj[3].toFixed(1)+'%';};
W['w3-es']=function(b){var a=b.querySelector('#es-a'),s=b.querySelector('#es-svg'),k=b.querySelector('#es-k'),si=SI3.icecream,x=D3.ic,n=x.length,tr=x.slice(0,n-12),te=x.slice(n-12);var sn=x.slice(n-24,n-12);function f(){var A=+a.value;b.querySelector('#es-va').textContent=A.toFixed(2);var lv=tr[0]/si[0];for(var i=1;i<tr.length;i++){lv=A*(tr[i]/si[i%12])+(1-A)*lv;}var es=si.map(function(v){return lv*v});var m1=mape(te,sn),m2=mape(te,es);Chart.line(s,{labels:['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],series:[{name:'2025 실제',color:'#eceaf3',values:te,dots:true},{name:'계절 나이브',color:'#5ee39c',values:sn,dash:'5 4'},{name:'지수평활×계절지수',color:'#d672d6',values:es,dash:'2 3'}],h:230});k.innerHTML='<div class="kpi g"><b>'+m1.toFixed(1)+'%</b><span>계절 나이브 MAPE</span></div><div class="kpi m"><b>'+m2.toFixed(1)+'%</b><span>지수평활(α='+A.toFixed(2)+') MAPE</span></div><div class="kpi a"><b>7.3%</b><span>교안: 추세+월 더미 회귀</span></div><div class="kpi r"><b>7.4%</b><span>교안: 홀트-윈터스</span></div>';}a.oninput=f;f();};
W['w3-vac']=function(b){var Y={},yrs=[];D3.vm.forEach(function(m,i){var y=m.slice(0,4);if(!(y in Y)){Y[y]=0;yrs.push(y);}Y[y]+=D3.vd[i];});var v=yrs.map(function(y){return Y[y]});var g=v.map(function(x,i){return i?Math.round((x/v[i-1]-1)*100):0});Chart.bars(b.querySelector('#vc-svg'),{labels:yrs,series:[{name:'연간 접종량',color:'#82b8ff',values:v,colorAt:function(x,i){return ['2015','2019','2023'].indexOf(yrs[i])>=0?'#5ee39c':'#82b8ff'}}],values:true,h:230});b.querySelector('#vc-out').innerHTML='증감률(%): '+yrs.slice(1).map(function(y,i){return y+' <b style="color:'+(g[i+1]<0?'var(--eye)':'var(--gfp)')+'">'+(g[i+1]>0?'+':'')+g[i+1]+'</b>'}).join(' · ')+' · 초록 막대 = 정점 · 2023→2025 '+Math.round((v[11]/v[9]-1)*100)+'%';};
W['w3-pet']=function(b){var s=b.querySelector('#pt-svg'),o=b.querySelector('#pt-out');var sp=D3.et.map(function(e,i){return e-D3.na[i]});var S=[[sp,'에틸렌 − 나프타','#5ee39c'],[D3.du,'두바이유','#f1b646'],[D3.nc,'NCC 가동률','#82b8ff']];var i22=D3.pm.indexOf('2022-01'),i26=D3.pm.indexOf('2026-03');function f(m){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',+x.dataset.m===m)});Chart.line(s,{labels:D3.pm,series:[{name:S[m][1],color:S[m][2],values:S[m][0]}],vline:[i22,i26],h:240,ticks:7});var pre=sp.slice(0,i22),post=sp.slice(i22,D3.pm.indexOf('2026-01'));var avg=function(a){return a.reduce(function(x,y){return x+y})/a.length};o.innerHTML=m==0?'스프레드 평균: 2015–2021 <b>'+Math.round(avg(pre))+'</b> → 2022–2025 <em>'+Math.round(avg(post))+'</em> $/t · 빨간 점선 = 2022-01, 2026-03':m==1?'2026년 3월 '+D3.du[i26]+', 4월 '+D3.du[i26+1]+' $/bbl — 교안의 80% 구간 상한(69.6, 71.5)을 크게 넘었습니다.':'2026년 4월 가동률 '+D3.nc[i26+1]+'% — 원료 부족이 만든 하락은 수요 신호가 아닙니다(3.1).';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(+x.dataset.m)}});f(0);};
W['w3-nv']=function(b){function z(p){var a=[[.8,.842],[.85,1.036],[.9,1.282],[.95,1.645],[.97,1.881],[.98,2.054],[.99,2.326]];for(var i=0;i<a.length-1;i++)if(p<=a[i+1][0])return a[i][1]+(a[i+1][1]-a[i][1])*(p-a[i][0])/(a[i+1][0]-a[i][0]);return 2.326;}function zi(p){if(p<=.5)return -zi(1-p);var t=Math.sqrt(-2*Math.log(1-p));return t-(2.515517+.802853*t+.010328*t*t)/(1+1.432788*t+.189269*t*t+.001308*t*t*t);}var P=b.querySelector('#nv-p'),C=b.querySelector('#nv-c'),S=b.querySelector('#nv-s'),Q=b.querySelector('#ss-q');function f(){var p=+P.value,c=+C.value,s=+S.value;b.querySelector('#nv-vp').textContent=p;b.querySelector('#nv-vc').textContent=c;b.querySelector('#nv-vs').textContent=s;var cu=p-c,co=c-s,cr=cu/(cu+co);var q=844+70*zi(Math.min(.999,Math.max(.001,cr)));b.querySelector('#nv-out').innerHTML=cu<=0?'<em>판매가가 원가보다 낮습니다.</em>':'Cu = '+cu+', Co = '+co+' → 임계비율 <b>'+cr.toFixed(3)+'</b> → 호빵 12월 생산 <b>'+Math.round(q)+'</b> (예측 844, 표준편차 약 70 가정)';var qq=+Q.value;b.querySelector('#ss-vq').textContent=Math.round(qq*100)+'%';var zz=z(qq);b.querySelector('#ss-out').innerHTML='서비스 수준 '+Math.round(qq*100)+'% → z ≈ <b>'+zz.toFixed(2)+'</b> → 안전재고 = '+zz.toFixed(2)+' × 174.8 ≈ <b>'+Math.round(zz*174.8)+'천 개</b> (95% 대비 '+(zz/1.645).toFixed(2)+'배)';}[P,C,S,Q].forEach(function(e){e.oninput=f});f();};
W['w3-duel']=function(b){b.querySelector('#du3-run').onclick=function(){var x=D3.ic,n=x.length,te=x.slice(n-12),sn=x.slice(n-24,n-12),mv=x.slice(n-24,n-12).reduce(function(a,c){return a+c})/12,mn=te.map(function(){return mv});var m1=mape(te,sn),m2=mape(te,mn);Chart.line(b.querySelector('#du3-svg'),{labels:['1','2','3','4','5','6','7','8','9','10','11','12'].map(function(m){return m+'월'}),series:[{name:'2025 실제',color:'#eceaf3',values:te,dots:true},{name:'초파리: 작년 같은 달',color:'#ef5b5b',values:sn,dash:'5 4'},{name:'주판봇: 12개월 평균',color:'#57d0dc',values:mn,dash:'2 3'}],h:230});b.querySelector('#du3-k').innerHTML='<div class="kpi g"><b>'+m1.toFixed(1)+'%</b><span>초파리 MAPE</span></div><div class="kpi r"><b>'+m2.toFixed(1)+'%</b><span>주판봇 MAPE</span></div><div class="kpi a"><b>'+(m2/m1).toFixed(1)+'배</b><span>오차 차이</span></div><div class="kpi m"><b>'+Math.round(mv)+'</b><span>주판봇의 매달 예측값</span></div>';sayDoc('e10','초파리 연구원 승. 계절이 강한 품목에서 평균 하나는 여름엔 모자라고 겨울엔 넘칩니다. 계절 나이브 '+m1.toFixed(1)+'% 대 평균 '+m2.toFixed(1)+'%. 계절 나이브가 이 공장의 기준선입니다.');};};
'''

RP = {
 'title': '계절지수 12개, 교안 숫자는 다시 나올까?',
 'eyebrow': '3주차 실습 리포트 · 시계열 · 식품·백신·석유화학 데이터',
 'desc': '스마트 제조 3주차 실습 리포트 — 수업 데이터로 아이스크림·호빵·군고구마 계절지수, NCC 가법 계절 효과, 계절 나이브 오차를 직접 계산해 교안 숫자와 대조합니다.',
 'lead': '실습 부록의 단계를 따라 세 묶음의 수업 데이터를 직접 계산했습니다. 교안의 대표 숫자 여섯 개가 모두 같은 값으로 다시 나왔고, 계절지수를 반올림하는 과정에서 생기는 작은 차이 하나를 찾았습니다.',
 'cover_mood': 'e07', 'back': ('index.html', '3주차 본문으로'), 'next': ('../w04/practice.html', '4주차 실습 리포트'),
 'summary': {
   'finding': '수업 데이터로 다시 계산한 결과, 교안의 대표 숫자(1.87 · 2.6 · −5.7%p · −3.3%p · 0.79/0.94 · 8.9%)가 모두 재현되었습니다.',
   'evidence': ['<span class="fact">사실</span> 아이스크림 8월 1.87, 1월 0.46, 호빵 12월 2.59, 7월 0.08입니다(<a href="#fig-r3-1">그림 1</a>, 2019-01~2025-12, 84개월).',
                '<span class="fact">사실</span> NCC 가동률의 가법 계절 효과는 4월 −5.7%p, 5월 −3.3%p입니다(<a href="#fig-r3-2">그림 2</a>, 2015-01~2026-08).',
                '<span class="fact">사실</span> 2025년 아이스크림을 계절 나이브로 맞히면 MAPE 8.9%입니다(<a href="#tab-r3-1">표 1</a>).',
                '<span class="interp">해석</span> 계절조정 전월비는 계절지수를 소수 둘째 자리에서 반올림하느냐에 따라 0.1~0.2%p 달라집니다. 보고서에는 쓴 계절지수의 자릿수를 함께 적는 것이 안전합니다.'],
   'fig': ('fig', {'id': 'fig-r3-1', 'cap': '[그림 1] 세 품목의 계절지수 12개 (평균 = 1)', 'w': 'r3-si', 'alt': '아이스크림·호빵·군고구마 월별 계절지수 막대. 아이스크림은 8월 1.87로 가장 높고, 호빵은 12월 2.59로 가장 높다', 'src': '출처: week03_seasonal_foods.csv(가상 데이터), 2019-01~2025-12, 저자 계산(12개월 중심 이동평균 비율법)'}),
 },
 'sections': [
  {'id': 'sec-r3-1', 'nav': '들어가며', 'title': '들어가며 — 숫자를 믿기 전에 한 번 뽑아 본다', 'blocks': [
    ('memo', 'e08', '본문에서 1.87이라는 숫자를 수없이 봤죠? 오늘은 그 숫자를 직접 만들어 볼 차례예요.'),
    ('p', '교안은 계절지수를 "평균적인 달의 몇 배"로 설명하고, 연간 목표를 월별로 나누는 데 바로 씁니다. 그렇다면 그 숫자가 같은 데이터에서 정말 다시 나오는지부터 확인해야 합니다.'),
    ('p', '이 리포트가 답할 질문은 셋입니다. ① 계절지수 1.87·2.6이 다시 나오나 ② NCC는 왜 "배"가 아니라 "%p"로 읽나 ③ 가장 단순한 예측은 얼마나 빗나가나.')]},
  {'id': 'sec-r3-2', 'nav': '배경', 'title': '배경 — 비율-이동평균법 세 단계', 'blocks': [
    ('p', '비유 하나로 시작합니다. 계절지수는 케이크 12조각을 달마다 다른 크기로 자르는 비율표입니다. 8월 조각은 평균의 1.87배, 1월 조각은 0.46배입니다.'),
    ('p', '계산은 세 단계입니다. ① 12개월 중심 이동평균(추세)으로 원래 값을 나눕니다. ② 같은 달끼리 평균합니다. ③ 12개 평균이 1이 되도록 맞춥니다.'),
    ('memo', 'e09', '12개월은 짝수라서 창의 가운데가 달과 달 사이에 걸려요. 그래서 이동평균을 한 번 더 2개씩 평균해서 가운데를 달에 맞춥니다. 실습 부록이 "앞뒤 반씩 겹친다"고 한 부분이에요.')]},
  {'id': 'sec-r3-3', 'nav': '방법', 'title': '방법 — 데이터 세 묶음, 계산 네 가지', 'blocks': [
    ('table', {'id': 'tab-r3-0', 'cap': '<표 0> 이 리포트가 쓴 데이터', 'head': ['묶음', '기간', '열', '쓴 계산'],
               'rows': [['식품 공장', '2019-01~2025-12 (84개월)', '아이스크림·호빵·군고구마·기온', '승법 계절지수, 자기상관, 계절 나이브'], ['백신', '2014-01~2025-12 (144개월)', '접종량', '연간 합계와 증감률'], ['석유화학', '2015-01~2026-08 (140개월)', '두바이유·나프타·에틸렌·NCC 가동률', '가법 계절 효과, 스프레드']],
               'src': '출처: week03_*.csv — 모두 수업용 가상 데이터(사건 시점·방향만 현실에서 가져옴)'}),
    ('p', '계산은 저장소의 analysis/w03_timeseries.py로 다시 돌릴 수 있습니다. 페이지의 그림은 같은 결과를 브라우저에서 다시 그린 것입니다.'),
    ('p', '가법 계절 효과는 비율 대신 차이를 씁니다. 원래 값 − 이동평균을 같은 달끼리 평균한 뒤, 12개 합이 0이 되게 맞춥니다.')]},
  {'id': 'sec-r3-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3 id="sec-r3-4-1">결과 1 · 승법 계절지수는 교안과 같다</h3>'),
    ('p', '<span class="fact">사실</span> 아이스크림 계절지수는 1월 0.46에서 8월 1.87까지 올라갑니다. 호빵은 12월 2.59, 1월 2.39로 겨울에 몰리고 7월은 0.08입니다(그림 1).'),
    ('p', '<span class="interp">해석</span> 군고구마(12월 1.96)는 호빵과 같은 겨울 품목이지만 계절 폭이 작습니다. 대신 연 10.8%로 빠르게 크는 추세가 있습니다. 같은 겨울 라인이라도 "계절형"과 "성장형"이 다르게 계획되어야 합니다.'),
    ('key', '연간 10,000개면 아이스크림 8월 몫은 10,000 × 1.87 ÷ 12 ≈ 1,558개입니다.'),
    ('html', '<h3 id="sec-r3-4-2">결과 2 · NCC 가동률은 "%p"로 읽는다</h3>'),
    ('fig', {'id': 'fig-r3-2', 'cap': '[그림 2] NCC 가동률의 가법 계절 효과 (단위: %p)', 'w': 'r3-ncc', 'alt': 'NCC 가동률 월별 가법 계절 효과 막대. 4월 −5.7, 5월 −3.3으로 가장 낮다', 'src': '출처: week03_petrochem.csv(가상 데이터), 2015-01~2026-08, 저자 계산(이동평균과의 차이를 같은 달끼리 평균)'}),
    ('p', '<span class="fact">사실</span> 4월 −5.7%p, 5월 −3.3%p, 3월 −1.7%p로 봄에 골짜기가 있고, 11·12월은 +2.3·+2.1%p입니다.'),
    ('p', '<span class="interp">해석</span> 정기보수 일정이 만든 계절입니다. 가동률은 0~100% 안에 갇혀 있어 "몇 배"보다 "몇 %p"가 자연스럽습니다. 4월 가동률이 올랐다는 보고는 "보수가 끝났다"일 뿐일 수 있습니다.'),
    ('html', '<h3 id="sec-r3-4-3">결과 3 · 가장 단순한 예측의 오차</h3>'),
    ('table', {'id': 'tab-r3-1', 'cap': '<표 1> 2025년 아이스크림 12개월 예측 오차 (단위: %)', 'head': ['방법', '규칙', 'MAPE', '출처'],
               'rows': [['계절 나이브', '다음 해 같은 달 = 작년 같은 달', '8.9', '저자 계산 · 교안 8.9'], ['12개월 평균', '매달 = 2024년 평균', '62.5', '저자 계산'], ['추세 + 월 더미 회귀', '—', '7.3', '교안'], ['홀트-윈터스', '—', '7.4', '교안']],
               'src': '출처: week03_seasonal_foods.csv, 학습 2019~2024 · 평가 2025, 저자 계산 및 교안'}),
    ('p', '<span class="fact">사실</span> 평균 하나로 예측하면 오차가 62.5%로, 계절 나이브의 7배입니다.'),
    ('p', '<span class="interp">해석</span> 계절이 강한 품목에서 첫 기준선은 계절 나이브입니다. 복잡한 모델의 이득(1.5%p 안팎)은 그 기준선 위에서 따져야 합니다.'),
    ('html', '<h3 id="sec-r3-4-4">결과 4 · 반올림이 만드는 작은 차이</h3>'),
    ('p', '<span class="fact">사실</span> 2025년 4월 계절조정 전월비는 이 리포트 계산으로 −0.4%, 교안 표기는 −0.2%입니다. 6월(−10.0%)·7월(+24.3%)은 같습니다.'),
    ('p', '<span class="interp">해석</span> 계절지수를 둘째 자리에서 반올림해 쓰느냐, 반올림 전 값을 쓰느냐의 차이로 읽습니다. 결론(4월은 사실상 평년 수준)은 바뀌지 않습니다.'),
    ('memo', 'e16', '숫자가 다 맞아서 기쁘지만, 4월의 0.2%p 차이도 그냥 넘기지 않았다는 게 오늘의 수확이에요.')]},
  {'id': 'sec-r3-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 가상 데이터라 맞는 게 당연하다. 맞습니다. 이 리포트의 목적은 "같은 절차를 따르면 같은 숫자가 나온다"는 재현성 확인입니다. 실제 공장 데이터에서는 결측·달력 효과 때문에 더 흔들릴 것입니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 계절지수는 해마다 변한다. 7년 평균은 2024년 폭염 같은 해를 희석합니다. 최근 해에 더 무게를 주고 싶다면 기간을 줄이거나 지수평활을 쓸 수 있습니다.'),
    ('p', '<span class="guess">추측</span> 기온 편차를 설명변수로 넣으면(교안 R² 0.979 → 0.996) 여름 오차가 줄 것입니다. 다만 내년 기온도 예측해야 하므로 오차가 두 번 쌓입니다.')]},
  {'id': 'sec-r3-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 계절지수는 엑셀만으로도, AI에게 말로 시켜서도 같은 숫자가 나와야 합니다. 이 리포트의 숫자를 AI 결과의 검수 기준표로 쓸 수 있습니다.'),
    ('p', '한계: ① 가상 데이터 ② 승법·가법 판단은 눈대중 기준 ③ 석유화학의 구조 변화·충격은 계절지수로 다루지 못함 ④ 맨 앞·뒤 6개월은 이동평균이 비어 계절지수 계산에서 빠짐.'),
    ('prompt', '#역할\n너는 식품 공장 생산계획 담당 분석가다.\n#맥락\n첨부한 week03_seasonal_foods.csv는 2019-01~2025-12 월별 판매량이다.\n#조건\n12개월 중심 이동평균 비율법으로 계산하고, 12개 평균이 1이 되게 맞춘다. 반올림하지 않은 값과 둘째 자리 반올림 값을 함께 적는다.\n#형식\n품목별 1~12월 계절지수 표 + 각 품목의 최대·최소 달 한 줄.\n#검수 기준\n아이스크림 8월 1.87, 호빵 12월 2.59가 나와야 한다. 다르면 계산 단계를 다시 보여 달라.'),
    ('memo', 'e07', '위 프롬프트를 QWEN에 그대로 넣어 보세요. "검수 기준" 칸을 프롬프트에 넣는 건 3주차의 작은 요령이에요.'),
    ('p', '다음 편 예고: 4주차 실습 리포트에서는 불량품 판정 데이터 1,000개로 "AI가 무슨 기준으로 불량을 골랐는지" 판정 기준을 데이터에서 직접 뽑습니다.')]},
 ],
 'refs': ['안상선, 「스마트제조 3주차 생산실적 추세 분석 — 시계열의 원리」 강의 교안, 2026', '안상선, 「스마트제조 3주차 실습 부록 — 파이썬으로 따라 하는 시계열 예측」, 2026', '수업 데이터 week03_seasonal_foods.csv · week03_vaccine_1.csv · week03_petrochem.csv (가상)', '이 저장소 analysis/w03_timeseries.py — 저자 계산'],
 'sources': [('원자료', '스마트 제조 3주차 교안·실습 부록·계절지수 만화'), ('계산', '저자 계산 (analysis/w03_timeseries.py)')],
 'notes': '데이터는 모두 수업용 가상 데이터입니다.',
}
RP['js'] = _DATA + r'''
W['r3-si']=function(s){Chart.bars(s,{labels:['1','2','3','4','5','6','7','8','9','10','11','12'].map(function(m){return m+'월'}),series:[{name:'아이스크림',color:'#ff86b8',values:SI3.icecream},{name:'호빵',color:'#f1b646',values:SI3.hoppang},{name:'군고구마',color:'#c48a5a',values:SI3.sweet_potato}],ref:1,min:0,max:2.8,h:260});};
W['r3-ncc']=function(s){Chart.bars(s,{labels:['1','2','3','4','5','6','7','8','9','10','11','12'].map(function(m){return m+'월'}),series:[{name:'계절 효과(%p)',color:'#82b8ff',values:SI3.ncc_add,colorAt:function(v){return v<0?'#f0604d':'#82b8ff'}}],values:true,fmt:function(v){return (v>0?'+':'')+v.toFixed(1)},h:240});};
'''
