# 6주차 · REVIEW — 1~5주 다시 보기 + 면류 3사 종합 사례
import os
_H = os.path.dirname(__file__)
_DATA = open(os.path.join(_H, '..', 'data_w06.js'), encoding='utf-8').read()

def rq(sid, title, tags, body, talk, items, quiz):
    """복습 칸: 빠른 문제 세트 위젯"""
    import json
    w = ('w6-rq', f'<div class="ptitle">빠른 복습 · {len(items)}문제</div><div data-items=\'{json.dumps(items, ensure_ascii=False).replace(chr(39), "&#39;")}\' class="rq"></div>')
    return {'id': sid, 'title': title, 'tags': tags, 'body': body, 'talk': talk, 'widget': w, 'quiz': quiz,
            'limit': '복습 문제는 본문 내용을 다시 확인하는 용도입니다. 틀린 문제는 링크로 해당 주차에 돌아가 보세요.'}

CH = {
 'slug': 'w06', 'num': '06',
 'title': 'REVIEW — 1~5주 다시 보기',
 'eyebrow': '6주차 · REVIEW · 면류 공장과 물류센터',
 'desc': '스마트 제조 6주차 REVIEW — 1~5주의 핵심을 빠른 문제로 다시 보고, 면류 3사(냉면·콩국수·비빔면)의 2027년 여름 생산계획 하나로 시계열·분류·작업지시서를 엮습니다.',
 'q': '다섯 주 동안 배운 것으로, 면류 공장의 2027년 여름을 준비할 수 있을까?',
 'lead': '6주는 앞 다섯 주를 다시 보는 REVIEW입니다. 앞부분은 주차별 빠른 복습, 뒷부분은 면류 3사의 여름 성수기 계획 하나로 다섯 주의 도구를 한 번에 씁니다. 8주 제안서의 연습이기도 합니다.',
 'scene_alt': '면류 공장 3D. 반죽 배합, 제면, 숙성·유탕, 냉각, 금속검출, 포장 순서로 면이 흐르고, 출하 도크에서 트럭이 수도권·중부·영남·호남 물류센터로 오간다.',
 'scene_hud': '3D · 면류 공장 — 라인과 출하·물류를 둘러보세요',
 'scene_opts': {'cam': [0, 17, 27], 'target': [-1, 1, -1]},
 'kpis': [('5주', '다시 보는 범위', 'g'), ('3,929일', '면류 일별 판매 (2016-01~2026-10)', 'a'), ('0.82', '냉면 검색지수와 판매의 상관', 'm'), ('83%', '보통 시나리오 냉면 라인 가동률', 'r')],
 'hero_talk': [
   ('doc', 'e08', 'REVIEW 주간입니다. 오늘 공장은 면류 3사, 여름이 대목입니다. 다섯 주의 도구를 하나씩 꺼내 봅시다.'),
   ('asst', 'e12', '복습 문제부터 풀고, 2027년 여름 계획으로 넘어갈게요!'),
   ('robo', 'e19', '여름엔 작년보다 무조건 더 팝니다! 라인 풀가동!'),
   ('fly', 'e09', '2026년 여름은 오히려 줄었어. 그 데이터부터 봐야지.'),
 ],
 'three': ['1~5주의 핵심(스마트공장 수준, 생성형 AI 원리, 시계열, 분류·회귀, 작업지시서)을 빠른 문제로 다시 확인합니다.',
           '배운 도구는 따로따로가 아니라 한 공장 문제에서 함께 쓰입니다. 그 연습이 8주 제안서의 재료가 됩니다.',
           '면류 3사의 2027년 여름(6~8월) 수요를 시나리오로 잡고, 라인·교대·인력·원재료 계획까지 이어 봅니다.'],
 'abbr': [('DC', 'Distribution Center', '물류센터'), ('BOM', 'Bill of Materials', '제품 1개에 드는 원재료 목록과 양'),
          ('MOQ', 'Minimum Order Quantity', '최소 발주량'), ('p90', '90th percentile', '100일 중 90번째로 큰 날의 값')],
 'why': [('따로 배운 도구', '시계열·분류·작업지시서를 각각 배웠지만, 현장 문제는 한꺼번에 옵니다.'),
         ('8주 제안서 연습', '문제 정의 → 현황 분석 → 원인 → 자동화 구상 → 90일 계획의 다섯 칸을 미리 채워 봅니다.'),
         ('여름은 기다려 주지 않는다', '면류는 6~8월에 연간 판매의 큰 몫이 몰립니다. 리드타임 7일 원재료는 미리 사야 합니다.')],
 'big_lead': '오늘은 두 부분입니다.',
 'big': [('① 복습 (6.1~6.6)', '주차별 핵심 + 빠른 문제'), ('② 종합 사례 (6.7~6.13)', '면류 3사 데이터 → 계절·검색·프로모션 → 수요 시나리오 → 라인·인력·원재료 → 8주 제안서')],
 'glossary': {
   '검색지수': ['검색지수', '데이터', '포털 검색량을 0~100으로 바꾼 지수입니다. 이 데이터의 검색지수는 네이버 데이터랩 실제 값입니다.'],
   '가동률': ['가동률', '지표', '유효 가동시간 대비 실제 생산시간의 비율입니다. 이 사례는 목표 85%, 최대 95%로 둡니다.'],
   '리드타임': ['리드타임', '지표', '발주일부터 공장 입고일까지 걸리는 시간입니다. 이 사례의 원재료는 7일입니다.'],
   '시나리오': ['시나리오', '방법', '예측을 한 점이 아니라 낮음·보통·높음 같은 범위로 잡는 방법입니다.'],
 },
 'subs': [
  {'id': 'sec-6-1', 'title': '다섯 주 한 장 지도', 'tags': ['REVIEW', '연결: 1~5주 → 8주'],
   'body': ['<div class="tw"><table class="tb"><tr><th>주차</th><th>공장</th><th>핵심 한 줄</th><th>오늘 사례에서 쓰는 곳</th></tr>'
            '<tr><td><a href="../w01/index.html">1주</a></td><td>사출성형 A라인</td><td>스마트공장은 데이터로 보고 판단하는 공장, ③ 검수가 핵심</td><td>계획표 숫자 검수</td></tr>'
            '<tr><td><a href="../w02/index.html">2주</a></td><td>케이블 하네스</td><td>AI는 다음 말을 확률로 고른다 → 5원칙, 숫자부터 검산</td><td>AI에게 계획을 시킬 프롬프트</td></tr>'
            '<tr><td><a href="../w03/index.html">3주</a></td><td>빙과·호빵</td><td>T·S·C·I, 계절지수, 생산실적 ≠ 수요, 예측은 범위</td><td>수요 시나리오, 라인 능력</td></tr>'
            '<tr><td><a href="../w04/index.html">4주</a></td><td>판재 검사</td><td>라벨은 분류, 숫자는 회귀, 정확도의 함정</td><td>"검색이 오르면 판매가 오른다"의 함정</td></tr>'
            '<tr><td><a href="../w05/index.html">5주</a></td><td>CNC 가공 셀</td><td>숫자 한 줄을 누가·무엇을·언제까지로</td><td>교대·발주 작업지시서</td></tr></table></div>'],
   'talk': [('sia', 'e07', '공장이 매주 달랐어요. 사출, 하네스, 빙과, 판재, CNC. 그리고 오늘은 면류입니다.'), ('moa', 'e12', '다섯 주 기록 모아 온 거 여기 있어요!'), ('x1', 'e01', '(반짝)')],
   'widget': ('w6-map', '<div class="ptitle">자가 진단 · 주차별 자신감</div><div class="ctrl" id="mp6-bt"></div><div class="eq" id="mp6-out" aria-live="polite"></div>'),
   'limit': '자가 진단은 저장되지 않습니다.',
   'quiz': [{'q': '8주 제출물의 성격은?', 'o': ['분석 보고서', '15주 자동화를 위한 구상 단계의 제안서'], 'a': 1, 'why': '8주는 구상, 15주는 구현입니다.'}]},
  rq('sec-6-2', '1주 다시 보기 — 스마트공장과 검수', ['1주 복습', '사출성형 A라인'],
     ['스마트공장은 데이터로 보고·판단·제어하는 공장이고, 수준은 미적용·기초·중간1·중간2·고도화입니다. 매주 다섯 단계 중 ③ 검수(합계·단위·행 수)가 핵심입니다. 업종이 다르면 지표 정의가 다릅니다(%와 ppm).'],
     [('robo', 'e07', '1% = 1,000ppm!'), ('fly', 'e10', '10,000ppm이야. 1주에 한 번 틀렸던 그 문제.')],
     [['실시간 현황판으로 라인 실적을 본다 — 어느 수준?', ['기초', '중간1', '고도화'], 1, '실시간 집계·모니터링은 중간1입니다.'],
      ['다섯 단계 중 합계·단위·행 수를 원본과 대조하는 단계는?', ['② 지시', '③ 검수', '⑤ 판단'], 1, '③ 검수입니다.'],
      ['불량률 0.3%는 몇 ppm?', ['300', '3,000', '30,000'], 1, '0.3 × 10,000 = 3,000ppm.'],
      ['불량률 120%가 나왔다. 먼저 의심할 것은?', ['AI 계산 실수', '표 구조(중복 집계·단위 섞임)'], 1, '100%를 넘으면 데이터 구조 문제입니다.']],
     [{'q': '수업 실습에 회사 실데이터를 쓸 수 있나?', 'o': ['그대로 가능', '익명화 후 개인 실습으로만'], 'a': 1, 'why': '입력 데이터가 학습에 쓰일 수 있기 때문입니다.'}]),
  rq('sec-6-3', '2주 다시 보기 — 생성형 AI의 원리와 프롬프트', ['2주 복습', '케이블 하네스'],
     ['AI는 글을 토큰과 숫자 ID로 바꾸고, 임베딩으로 의미 좌표를 주고, 어텐션으로 중요한 말에 집중해, 다음 토큰을 확률로 골라 문장을 만듭니다. 그래서 그럴듯하게 틀릴 수 있고, 숫자가 든 답부터 검산합니다. 프롬프트는 역할·맥락·조건·형식·예시.'],
     [('asst', 'e07', '진동 0.70g 예시, 직선으로 이으면 0.82g였죠!'), ('robo', 'e14', '그 얘기는 그만…')],
     [['「떨림」 앞의 단어를 "모터"에서 "작업자"로 바꾸면 답이 바뀌는 원리는?', ['토큰화', '맥락', '미세조정'], 1, '주변 단어가 의미 좌표를 옮깁니다.'],
      ['"JSON 한 줄로"는 5원칙 중?', ['역할', '형식', '예시'], 1, '출력 모양은 형식입니다.'],
      ['사례 4의 "38건/44건 = 87%"를 검산하면?', ['87.0%', '86.4%', '88.4%'], 1, '38 ÷ 44 = 0.864.'],
      ['어텐션 가중치를 다 더하면?', ['1', '단어 수', '100'], 0, '주의력을 나눠 갖는 비율입니다.']],
     [{'q': 'AI 답에서 가장 먼저 검산할 곳은?', 'o': ['말투', '숫자·비율·시각'], 'a': 1, 'why': '매끄러운 문장보다 숫자가 먼저 틀립니다.'}]),
  rq('sec-6-4', '3주 다시 보기 — 시계열', ['3주 복습', '빙과·호빵'],
     ['시계열은 순서가 정보입니다(자기상관). 추세·계절·순환·불규칙으로 쪼개고, 계절지수로 월별 배분하며, 기준선(계절 나이브)부터 이깁니다. 생산실적은 수요가 아니고, 예측은 범위입니다.'],
     [('fly', 'e09', '봄에 30% 늘었다는 보고, 계절 빼고 다시 봤어?'), ('robo', 'e14', '계절조정 전월비로 다시 쓰겠습니다.')],
     [['연간 12,000개, 계절지수 1.87인 달의 목표는?', ['1,558개', '1,870개', '22,440개'], 1, '12,000 × 1.87 ÷ 12 = 1,870개.'],
      ['NCC 가동률의 계절 효과를 읽는 방식은?', ['몇 배(승법)', '몇 %p(가법)'], 1, '0~100% 안의 값이라 가법이 자연스럽습니다.'],
      ['시계열 모델 검증 방법은?', ['무작위 20%', '마지막 기간을 가리고 맞히기'], 1, '무작위로 가리면 누설이 생깁니다.'],
      ['생산실적이 7~9월 모두 900으로 같다면?', ['수요가 안정적', '능력에서 잘렸을 수 있다'], 1, '생산실적은 수요가 아닙니다.']],
     [{'q': '순환을 다루는 방법은?', 'o': ['주기를 정확히 맞힌다', '시나리오와 선행 신호'], 'a': 1, 'why': '주기와 높이가 매번 다릅니다.'}]),
  rq('sec-6-5', '4주 다시 보기 — 분류와 회귀', ['4주 복습', '판재 검사'],
     ['라벨은 분류, 숫자는 회귀입니다. 분류는 TP·TN·FP·FN으로 읽고, 불량이 적은 데이터에서는 정확도보다 재현율을 함께 봅니다. 판재 데이터의 판정 기준은 거칠기 4.9 · 초음파 27.5 · 폭 302.5였습니다.'],
     [('asst', 'e04', '"모두 정상"이 정확도 90%인데 재현율은 0%!'), ('fly', 'e10', '그게 정확도의 함정이야.')],
     [['"이 공구는 몇 분 더 쓸 수 있나?"', ['분류', '회귀'], 1, '답이 숫자입니다.'],
      ['TP 77, FN 23이면 재현율은?', ['77%', '23%', '97.6%'], 0, '77 ÷ (77+23) = 77%.'],
      ['판재 데이터에서 판정과 거의 무관했던 변수는?', ['거칠기', '오븐 온도', '폭'], 1, '정상 179.98℃, 불량 179.89℃로 같습니다.'],
      ['학습·테스트의 불량 비율을 같게 나누는 것은?', ['교차검증', '층화', '정규화'], 1, '층화(stratify)입니다.']],
     [{'q': '정확도가 비슷한 모델 중 고를 것은?', 'o': ['파라미터가 많은 것', '기준을 읽을 수 있는 것'], 'a': 1, 'why': '현장에서 따르고 설명할 수 있어야 합니다.'}]),
  rq('sec-6-6', '5주 다시 보기 — 작업지시서', ['5주 복습', 'CNC 가공 셀'],
     ['작업지시서는 점검표(결과) + 회의록(결정) + 매뉴얼(방법)을 한 장에 모은 카드입니다. 점수 분기(0.40/0.70)와 유형 분기(6갈래)를 섞은 혼합형이 고장을 놓치지 않습니다. 빈칸 다섯: 책임자 · 임계값 · 시한 · 동사+사물 · 보고 회선.'],
     [('moa', 'e07', '정장 다시 입고 왔어요. 카드 결재 받으러요.'), ('x3', 'e16', '(삐빅)')],
     [['wear 0.52의 자리는?', ['정상', '주의', '위험'], 1, '0.40~0.70은 주의입니다.'],
      ['과부하 고장인데 wear 0.30 — 점수형 카드는?', ['정상', '위험'], 0, '그래서 혼합형이 필요합니다.'],
      ['"시한: ASAP"은 몇 번 빈칸?', ['①', '③', '⑤'], 1, '시한은 시간 단위로 씁니다.'],
      ['한 페이지 앱의 약속이 아닌 것은?', ['입력 폼', '결과 카드', '여러 페이지 이동'], 2, '페이지 이동이 없어야 합니다.']],
     [{'q': 'few-shot 예시값이 데이터보다 0.1 낮으면?', 'o': ['영향 없다', '추정이 낮게 나와 경보가 늦어질 수 있다'], 'a': 1, 'why': '예시는 숫자 견본이기도 합니다.'}]),

  {'id': 'sec-6-7', 'title': '종합 사례 — 면류 3사의 데이터', 'tags': ['사례: 냉면·콩국수·비빔면', '데이터: 일별 3,929일 + 계획 시트 13'],
   'body': ['면류 데이터는 2016-01-01부터 2026-10-03까지 일별 기록입니다. 검색지수(네이버 데이터랩 실제 값), 판매량(팩, 가상), 프로모션이 있습니다. 함께 받은 엑셀에는 제품·BOM·원재료·공장_라인·교대·인력·공정_검사·공장→DC 운송·DC→매장 시트와 가정 파라미터가 있습니다.',
            '<div class="tw"><table class="tb"><tr><th>제품</th><th>규격·보관</th><th>유통기한</th><th>공장·라인</th><th>시간당 능력(라인당)</th></tr>'
            '<tr><td>냉면 NM-01</td><td>물냉면 2인분 · 냉장</td><td>30일</td><td>평택 2 + 김해 2</td><td>1,000팩</td></tr>'
            '<tr><td>콩국수 KG-01</td><td>콩국수 2인분 · 냉장</td><td>25일</td><td>김해 2 + 음성 1</td><td>850팩</td></tr>'
            '<tr><td>비빔면 BB-01</td><td>비빔면 2인분 · 상온</td><td>180일</td><td>평택 2 + 음성 1</td><td>1,100팩</td></tr></table></div>',
            '가정 파라미터: 예측 대상 2027-06-01~08-31(92일), 원재료 리드타임 7일(매주 월요일 발주), 완제품 안전재고 2일분, 목표 가동률 85% · 최대 95%, 여름 주 7일 운영, 인력 환산계수 1.4.'],
   'talk': [('fly', 'e09', '판매량이 가상이라면, 이게 "생산실적"이야 "수요"야?'), ('doc', 'e10', '이 사례에서는 수요로 봅니다. 3주의 경고대로, 실제 공장이라면 품절일을 먼저 확인해야 합니다.'), ('asst', 'e07', '월별로 묶어서 그려 볼게요.')],
   'widget': ('w6-data', '<div class="ptitle">데이터 · 월별 판매 (2016-01~2026-09, 수업 데이터)</div><div class="ctrl"><button class="bt on" data-k="nm" type="button">냉면</button><button class="bt" data-k="kg" type="button">콩국수</button><button class="bt" data-k="bb" type="button">비빔면</button></div><div class="cwrap"><svg id="dt6-svg"></svg></div><div class="eq" id="dt6-out" aria-live="polite"></div>'),
   'limit': '판매·공장·원재료·물류 값은 교육용 가상 데이터이고, 검색지수만 실제 데이터입니다(엑셀 README).',
   'quiz': [{'q': '이 데이터에서 실제(가상 아님) 값은?', 'o': ['판매량', '검색지수', 'BOM'], 'a': 1, 'why': '검색지수만 네이버 데이터랩 원본입니다.'}]},

  {'id': 'sec-6-8', 'title': '검색이 오르면 판매가 오른다? — 상관과 선행 신호', 'tags': ['4주 연결: 상관 ≠ 인과', '3주 연결: 선행 신호'],
   'fx': {'q': '상관 0.82면 검색 때문에 판매가 오른다는 거예요?',
          'school': '상관계수(고등 수학 확률과 통계)',
          'eq': 'r = corr(검색지수, 판매량) · <b>−1 ~ 1</b> · <i>원인은 말하지 않는다</i>',
          'rows': [('r ≈ 1', '같이 오르고 같이 내린다'), ('r ≈ 0', '관계가 거의 없다'), ('공통 원인', '더위가 검색과 판매를 함께 올릴 수 있다')],
          'calc': '일별 냉면 검색지수와 판매량의 상관은 0.818, 콩국수 0.911, 비빔면 0.817입니다. 셋 다 높지만, 날씨라는 공통 원인이 두 숫자를 함께 움직였을 수 있습니다.',
          'comment': '같이 움직이는 것과 원인인 것은 다르구나. 그래도 판매보다 먼저 움직이면 신호로는 쓸 수 있겠네요!'},
   'body': ['3주에서 순환은 맞히지 말고 선행 신호로 가늠한다고 했습니다. 검색지수는 판매보다 먼저 움직인다면 좋은 선행 신호 후보입니다. 며칠 앞서 움직이는지는 시차를 바꿔 가며 상관을 보면 됩니다.'],
   'talk': [('robo', 'e16', '검색 광고를 두 배로 하면 판매도 두 배!'), ('fly', 'e03', '더위가 둘 다 올린 거면? 광고로 날씨를 바꿀 순 없어.'), ('sia', 'e07', '아래에서 시차별 상관을 보겠습니다.')],
   'widget': ('w6-lag', '<div class="ptitle">계산 · 월별 검색 대신 판매 자체의 계절 모양 비교</div><div class="cwrap"><svg id="lg-svg"></svg></div><div class="eq" id="lg-out" aria-live="polite"></div>'),
   'explain': ['이 페이지에는 용량 때문에 일별 검색지수를 싣지 않았습니다. 시차별 상관 계산은 실습 리포트의 프롬프트로 AI에게 시켜 보세요. 아래 그림은 세 제품의 계절 모양(계절지수)입니다.'],
   'limit': '상관 0.82는 2016~2026 전체 일별 데이터의 값입니다. 계절을 뺀 뒤의 상관은 더 낮을 수 있습니다.',
   'quiz': [{'q': '검색지수와 판매의 상관이 높을 때 가장 안전한 해석은?', 'o': ['검색이 판매의 원인', '같이 움직이니 선행 신호 후보로 검토'], 'a': 1, 'why': '상관은 인과가 아닙니다.'}]},

  {'id': 'sec-6-9', 'title': '계절지수와 프로모션 — 여름 모양이 셋 다 다르다', 'tags': ['3주 연결: 계절지수', '프로모션 효과'],
   'body': ['월 계절지수로 보면 냉면은 7월 2.02, 콩국수는 7월 3.07, 비빔면은 6월 1.50이 최대입니다. 콩국수는 여름에 가장 날카롭게 몰리고, 비빔면은 상온 제품답게 봄부터 완만하게 오릅니다.',
            '프로모션이 있던 날의 판매를 같은 달 프로모션 없는 날 평균과 비교하면, 냉면 약 1.24배, 비빔면 약 1.26배, 콩국수 약 1.04배입니다. 같은 행사라도 제품마다 효과가 다릅니다.'],
   'talk': [('asst', 'e04', '콩국수 7월 3.07배! 평균적인 달의 세 배예요.'), ('moa', 'e09', '그런데 콩국수는 프로모션 효과가 거의 없네요.'), ('fly', 'e10', '이미 여름에 다 사는 제품엔 할인이 덜 먹히는 거지.')],
   'widget': ('w6-si', '<div class="ptitle">계산 · 세 제품의 계절지수 (2016~2026 월별, 이 페이지 계산)</div><div class="cwrap"><svg id="si6-svg"></svg></div><div class="eq" id="si6-out" aria-live="polite"></div>'),
   'limit': '프로모션 효과는 같은 달 평균과의 단순 비교라, 요일·날씨 차이가 섞여 있습니다.',
   'quiz': [{'q': '여름 쏠림이 가장 날카로운 제품은?', 'o': ['냉면', '콩국수', '비빔면'], 'a': 1, 'why': '콩국수 7월 계절지수 3.07이 가장 큽니다.'}]},

  {'id': 'sec-6-10', 'title': '2027년 여름 수요 — 한 점이 아니라 세 갈래', 'tags': ['3주 연결: 예측은 범위', '시나리오: 낮음·보통·높음'],
   'why': {'problem': '2023~2025년 여름 판매는 늘다가 2026년 여름에 20~25% 줄었습니다.',
           'limit': '"작년보다 무조건 더"도, "2026년처럼 계속 감소"도 근거가 약합니다. 한 점으로 정하면 틀렸을 때 손해가 큽니다.',
           'solve': '최근 4년(2023~2026) 여름 일평균으로 세 시나리오를 잡습니다. 낮음 = 2026년, 보통 = 4년 평균, 높음 = 4년 중 최대.',
           'easy': '우산을 챙길지 말지 대신, 비 올 확률별로 준비물을 나눠 두는 것.'},
   'body': ['<div class="tw"><table class="tb"><tr><th>제품 (6~8월 일평균, 팩)</th><th>낮음 (2026)</th><th>보통 (2023~26 평균)</th><th>높음 (최대)</th></tr>'
            '<tr><td>냉면</td><td class="n">59,661</td><td class="n">69,801</td><td class="n">78,434 (2025)</td></tr>'
            '<tr><td>콩국수</td><td class="n">36,328</td><td class="n">44,242</td><td class="n">48,998 (2023)</td></tr>'
            '<tr><td>비빔면</td><td class="n">29,895</td><td class="n">42,021</td><td class="n">52,401 (2024)</td></tr></table></div>',
            '세 시나리오의 차이가 곧 위험의 크기입니다. 냉면은 낮음과 높음이 하루 약 1만 9천 팩, 비빔면은 약 2만 2천 팩 차이 납니다.'],
   'talk': [('robo', 'e07', '보통 시나리오 하나만 쓰면 깔끔합니다!'), ('fly', 'e09', '깔끔하지만, 높음이 오면? 아래 대결에서 숫자로 보자.'), ('x2', 'e09', '(…)')],
   'widget': ('w6-scen', '<div class="ptitle">비교 · 여름 일평균 추이와 2027 세 시나리오 (수업 데이터 계산)</div><div class="ctrl"><button class="bt on" data-k="냉면" type="button">냉면</button><button class="bt" data-k="콩국수" type="button">콩국수</button><button class="bt" data-k="비빔면" type="button">비빔면</button></div><div class="cwrap"><svg id="sc6-svg"></svg></div><div class="eq" id="sc6-out" aria-live="polite"></div>'),
   'limit': '세 시나리오는 과거 4년의 범위일 뿐입니다. 2027년이 그 밖으로 나갈 수도 있습니다(3주 석유화학의 교훈).',
   'quiz': [{'q': '시나리오를 쓰는 가장 큰 이유는?', 'o': ['정확한 값을 맞히려고', '틀렸을 때 덜 다치게 대비하려고'], 'a': 1, 'why': '예측은 범위이고, 그 범위가 대비의 크기입니다.'}]},

  {'id': 'sec-6-11', 'title': '라인 능력과 교대 — 가동률 85%와 95%', 'tags': ['3주 연결: 생산실적 ≠ 수요', '계산: 라인 × 시간당 × 시간'],
   'fx': {'q': '가동률은 어떻게 계산해요? 교대를 늘리면 왜 낮아져요?',
          'school': '비율, 일차식(곱셈과 나눗셈)',
          'eq': '가동률 = 하루 수요 ÷ (라인 수 × 시간당 능력 × <b>유효 가동시간</b>)',
          'rows': [('유효 가동시간', '1교대 7.5h · 2교대 15h · 3교대 21h'), ('목표 85%', '이 아래면 여유 있음'), ('최대 95%', '넘으면 교대 추가 또는 공장 추가 가동')],
          'calc': '냉면 보통 69,801팩 ÷ (4라인 × 1,000팩 × 21h = 84,000) = 83.1%입니다. 높음 78,434팩이면 93.4%로 목표를 넘지만 최대 안쪽입니다.',
          'comment': '분모(하루에 만들 수 있는 양)가 커지면 같은 수요라도 가동률이 낮아지는 거네요!'},
   'body': ['보통 시나리오는 냉면·콩국수 3교대(83.1%, 82.6%), 비빔면 2교대(84.9%)로 목표 85% 안에 들어옵니다. 높음이 오면 냉면 93.4%, 콩국수 91.5%로 목표를 넘고, 비빔면은 2교대로는 106%라 3교대(75.6%)가 필요합니다.',
            '하루 최대 판매일은 일평균의 1.5~1.9배라 라인 능력을 넘습니다. 이 봉우리는 기초 재고(냉면 9만 · 콩국수 5만 · 비빔면 16만 팩)와 안전재고 2일분으로 받습니다.'],
   'talk': [('asst', 'e07', '아래 계산기에서 제품과 시나리오를 바꿔 보세요.'), ('robo', 'e19', '전부 3교대면 다 해결!'), ('fly', 'e09', '인력이 1.4배씩 붙어. 다음 칸에서 사람 수부터 세 봐.')],
   'widget': ('w6-cap', '<div class="ptitle">계산기 · 제품별 교대와 가동률</div><div class="ctrl"><span class="glabel">시나리오</span><button class="bt" data-s="낮음" type="button">낮음</button><button class="bt on" data-s="보통" type="button">보통</button><button class="bt" data-s="높음" type="button">높음</button></div><div class="tw" id="cp6-tb"></div><div class="eq" id="cp6-out" aria-live="polite"></div>'),
   'limit': '라인 간 전환(냉면 라인으로 콩국수 생산 등)과 공장 간 이동은 고려하지 않았습니다. 엑셀의 공장_라인 시트대로 제품별 라인이 고정이라고 봤습니다.',
   'quiz': [{'q': '가동률이 95%를 넘으면?', 'o': ['그대로 둔다', '교대 추가 또는 공장 추가 가동'], 'a': 1, 'why': '가정 파라미터의 최대 허용 가동률입니다.'}]},

  {'id': 'sec-6-12', 'title': '인력·원재료·리드타임 — 월요일 발주서', 'tags': ['5주 연결: 작업지시서', '계산: BOM × 수요'],
   'body': ['하루 필요 인원 = Σ(라인 수 × 교대당 인원 × 교대 수) + 공장 3곳 × 간접 6명 × 교대 수. 보통 시나리오는 하루 276명이고, 주 7일 운영을 주 5일 근무자로 채우려면 × 1.4 = 387명이 필요합니다. 높음은 비빔면이 3교대가 되어 297명 → 416명입니다.',
            '원재료는 BOM × 수요 × 7일로 주간 소요량을 구합니다. 보통 시나리오의 밀가루는 주 약 160톤, 포장필름은 약 109만 매입니다. 리드타임이 7일이므로 월요일 발주가 다음 주 생산을 정합니다.',
            '이 숫자 한 줄을 5주의 작업지시서로 옮기면 "구매팀 ○○씨 · 밀가루 160.5톤 발주 · 월요일 12:00까지 · 생산팀 보고"가 됩니다.'],
   'talk': [('moa', 'e12', '발주서 양식은 제가 만들어 둘게요!'), ('sia', 'e10', 'MOQ와 발주 단위로 올림하는 것도 확인하겠습니다.'), ('x1', 'e04', '(오)')],
   'widget': ('w6-mat', '<div class="ptitle">발주서 · 시나리오별 주간 원재료 (BOM 기준, 이 페이지 계산)</div><div class="ctrl"><button class="bt" data-s="낮음" type="button">낮음</button><button class="bt on" data-s="보통" type="button">보통</button><button class="bt" data-s="높음" type="button">높음</button></div><div class="tw" id="mt6-tb"></div><div id="mt6-wo"></div>'),
   'limit': '안전재고 3일분(원재료 시트)과 현재 재고는 넣지 않은 "소요량"입니다. 실제 발주량 = 소요량 + 안전재고 − 현재고를 발주 단위로 올림합니다.',
   'quiz': [{'q': '보통 시나리오 하루 필요 인원 276명, 환산계수 1.4면?', 'o': ['276명', '387명', '552명'], 'a': 1, 'why': '276 × 1.4 = 386.4 → 387명.'}]},

  {'id': 'sec-6-13', 'title': '8주 제안서로 잇기 — 다섯 칸 미리 채우기', 'tags': ['8주 연결: 제안서 다섯 칸', '실습 리포트로'],
   'body': ['면류 사례를 8주 제안서 다섯 칸에 넣어 보면 이렇습니다. ① 문제 정의 — 여름 성수기 수요가 해마다 크게 흔들려 라인·인력·원재료 계획이 늦다. ② 현황 분석 — 계절지수, 여름 일평균 추이, 시나리오 범위. ③ 원인 규명 — 날씨·검색·프로모션(상관 ≠ 인과).',
            '④ 자동화 구상 — 매주 월요일 판매·검색지수를 받아 시나리오를 다시 계산하고, 교대·발주 작업지시서 초안을 자동으로 만든다. ⑤ 기대효과·90일 — 결품일 수, 폐기량, 초과근무 시간을 기준선으로 재고 90일 계획을 세운다.',
            '여러분의 제안서는 자기 공정으로 이 다섯 칸을 채우면 됩니다.'],
   'talk': [('doc', 'e16', 'REVIEW의 결론입니다. 다섯 주의 도구는 따로가 아니라 하나의 계획표로 이어집니다.'), ('asst', 'e01', '실습 리포트에서 2027년 여름 계획을 숫자로 다 채웠어요!'), ('fly', 'e10', '7주부터는 불량 분석이 기다려. 빈 슬롯이지만.')],
   'widget': ('w6-prop', '<div class="ptitle">미리 쓰기 · 8주 제안서 다섯 칸 (면류 사례 예시)</div><div class="ctrl" id="pp-bt"></div><div class="insight" id="pp-out" aria-live="polite"></div>'),
   'limit': '이 예시는 수업용 가상 공장의 것입니다. 8주 제안서는 자기 공정(익명화)으로 씁니다.',
   'quiz': [{'q': '"매주 월요일 시나리오 재계산 → 발주 초안 자동 생성"은 다섯 칸 중?', 'o': ['① 문제 정의', '④ 자동화 구상', '⑤ 기대효과'], 'a': 1, 'why': '어떤 문서·보고를 자동으로 만들지가 자동화 구상입니다.'}]},
 ],
 'duel': {
   'q': '2027년 여름, 보통 시나리오 하나로 충분할까?',
   'intro': [('doc', 'e07', '주판봇은 보통 시나리오대로 비빔면을 2교대로 고정합니다. 초파리 연구원은 3교대로 갈 수 있는 대기조(옵션)를 미리 확보합니다. 실제 여름이 "높음"이었다고 해 봅시다.'), ('moa', 'e12', '시작!')],
   'fly': '보통으로 계획하되, 높음이 오면 3교대로 넘어갈 옵션을 미리 사 둔다.',
   'robo': '보통 하나로 고정! 대기조는 돈 낭비입니다!',
   'widget': 'w6-duel',
   'panel': '<div class="ptitle">시뮬레이션 · 비빔면 92일 (판매가 3,980원/팩, 대기조 비용은 예시값)</div><div class="ctrl"><div class="group"><span class="glabel">대기조 비용(만원/일)</span><input type="range" min="50" max="1000" step="50" value="300" id="du6-c"><span class="val" id="du6-vc"></span></div><button class="bt primary" id="du6-run" type="button">여름 돌려 보기</button></div><div class="kpis" id="du6-k"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('x1', 'e01', '(짝짝)'), ('x2', 'e16', '(끄덕)'), ('x3', 'e01', '(삐빅!)')],
 },
 'summary': {
   'head': ['주차', '도구', '면류 사례에서'],
   'rows': [['1주', '수준 · 검수 · 지표 정의', '계획표 숫자를 원본과 대조'],
            ['2주', '원리 · 5원칙 · 숫자 검산', 'AI에게 계획 계산을 시키는 프롬프트'],
            ['3주', '계절지수 · 시나리오 · 생산실적 ≠ 수요', '여름 수요 범위, 라인 능력'],
            ['4주', '분류·회귀 · 상관 ≠ 인과', '검색지수는 선행 신호 후보'],
            ['5주', '작업지시서 · 분기', '교대 전환·발주 작업지시서']],
   'limits': ['면류 판매·공장·원재료·물류는 가상 데이터, 검색지수만 실제입니다.',
              '시나리오는 최근 4년 범위로 잡았고, 날씨 예보 같은 외부 정보는 넣지 않았습니다.',
              '대결의 대기조 비용은 예시값입니다.'],
 },
 'outro': [('doc', 'e16', '다섯 주를 한 장의 계획표로 엮었습니다. 예측은 범위, 계획은 작업지시서, 그리고 모든 숫자는 검수.'),
           ('asst', 'e01', '실습 리포트에 2027년 여름 계획을 정리해 뒀어요.'),
           ('fly', 'e10', '7주 "불량 분석 ① 어디서 터지는가"는 아직 빈 슬롯이야. 자료가 오면 채우자.'),
           ('robo', 'e12', '그때까지 보통 시나리오 말고 세 시나리오로 생각하겠습니다!')],
 'sources': [('강의 자료', '스마트 제조 1~5주 교안 · 면류 수요예측·생산계획 실습 데이터(일별 CSV, 계획 시트 xlsx)'),
             ('수업 데이터', '면류 일별 검색·판매 2016-01-01~2026-10-03 (검색지수: 네이버 데이터랩 원본, 판매량·공장·원재료·물류: 교육용 가상 데이터)'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '대결의 대기조 비용, 8주 제안서 예시 문장은 예시입니다. 계절지수·시나리오·가동률·인원·원재료는 수업 데이터로 계산했습니다.',
 'practice': ('practice.html', '2027년 여름 생산계획을 숫자로 채우다'),
}

CH['js'] = _DATA + r'''
var PL={냉면:{ln:4,cap:1000,crew:9,price:6980,bom:{밀가루:.1,메밀가루:.06,감자전분:.04,냉면육수농축액:.12,'겨자·식초소스':.02,포장필름:1}},콩국수:{ln:3,cap:850,crew:8,price:7480,bom:{밀가루:.18,대두분말:.12,감자전분:.01,포장필름:1}},비빔면:{ln:3,cap:1100,crew:7,price:3980,bom:{밀가루:.19,감자전분:.02,팜유:.04,비빔장:.08,포장필름:1}}};
var HR={1:7.5,2:15,3:21},UNIT={밀가루:['kg',20,1000],메밀가루:['kg',25,500],감자전분:['kg',25,500],대두분말:['kg',20,500],냉면육수농축액:['kg',18,360],팜유:['kg',180,1800],비빔장:['kg',20,400],'겨자·식초소스':['kg',10,200],포장필름:['매',5000,50000]};
function scen(k){var s=D6.sum[k],y=[2023,2024,2025,2026].map(function(t){return s[t]});return {낮음:s[2026],보통:y.reduce(function(a,c){return a+c})/4,높음:Math.max.apply(null,y)};}
function shiftFor(k,d){var p=PL[k];for(var sh=1;sh<=3;sh++){var u=d/(p.ln*p.cap*HR[sh]);if(u<=.85||sh==3)return [sh,u];}}
function sayDoc(mood,html){var v=document.getElementById('verdict');v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
W['w6-rq']=function(b){var box=b.querySelector('.rq'),I=JSON.parse(box.getAttribute('data-items')),i=0,sc=0;function sh(){if(i>=I.length){box.innerHTML='<div class="eq">점수 <b>'+sc+'/'+I.length+'</b> '+(sc==I.length?'— 완벽합니다!':'— 틀린 문제는 해당 주차로 돌아가 보세요.')+' <button class="bt" type="button">다시</button></div>';box.querySelector('button').onclick=function(){i=0;sc=0;sh();};return;}var q=I[i];box.innerHTML='<p>('+(i+1)+'/'+I.length+') '+q[0]+'</p><div class="ctrl">'+q[1].map(function(o,j){return '<button class="bt" data-j="'+j+'" type="button">'+o+'</button>'}).join('')+'</div><div class="eq" aria-live="polite"></div>';box.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var ok=+x.dataset.j===q[2];if(ok)sc++;x.classList.add(ok?'on':'no');box.querySelector('.eq').innerHTML=(ok?'✔ ':'✘ ')+q[3];box.querySelectorAll('.ctrl .bt').forEach(function(y){y.disabled=true});setTimeout(function(){i++;sh();},1100);};});}sh();};
W['w6-map']=function(b){var T=['1주 수준·검수','2주 원리·프롬프트','3주 시계열','4주 분류·회귀','5주 작업지시서'],on=T.map(function(){return 0}),bt=b.querySelector('#mp6-bt'),o=b.querySelector('#mp6-out');T.forEach(function(t,i){var x=document.createElement('button');x.className='bt';x.setAttribute('aria-pressed','false');x.textContent=t;x.onclick=function(){on[i]=1-on[i];x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var n=on.reduce(function(a,c){return a+c},0);o.innerHTML='자신 있는 주차 <b>'+n+'/5</b>'+(n<5?' · 먼저 볼 칸: <a href="#sec-6-'+(on.indexOf(0)+2)+'">'+T[on.indexOf(0)]+' 복습</a>':' · 종합 사례로 바로 가세요: <a href="#sec-6-7">6.7</a>');}f();};
W['w6-data']=function(b){var s=b.querySelector('#dt6-svg'),o=b.querySelector('#dt6-out'),N={nm:'냉면',kg:'콩국수',bb:'비빔면'};function f(k){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',x.dataset.k===k)});Chart.line(s,{labels:D6.m,series:[{name:N[k]+' 월 판매(팩)',color:{nm:'#82b8ff',kg:'#f1b646',bb:'#f0604d'}[k],values:D6[k]}],h:240,ticks:8});var Y={};D6.m.forEach(function(m,i){var y=m.slice(0,4);Y[y]=(Y[y]||0)+D6[k][i];});o.innerHTML='연간 합계(백만 팩): '+Object.keys(Y).map(function(y){return y+' <b>'+(Y[y]/1e6).toFixed(1)+'</b>'}).join(' · ')+' (2026은 9월까지)';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(x.dataset.k)}});f('nm');};
W['w6-lag']=function(b){var L=['1','2','3','4','5','6','7','8','9','10','11','12'].map(function(m){return m+'월'});Chart.line(b.querySelector('#lg-svg'),{labels:L,series:[{name:'냉면',color:'#82b8ff',values:D6.si.냉면,dots:true},{name:'콩국수',color:'#f1b646',values:D6.si.콩국수,dots:true},{name:'비빔면',color:'#f0604d',values:D6.si.비빔면,dots:true}],ref:1,min:0,h:230});b.querySelector('#lg-out').innerHTML='일별 상관(검색지수·판매): 냉면 <b>0.818</b> · 콩국수 <b>0.911</b> · 비빔면 <b>0.817</b> (2016-01~2026-10, 이 페이지 계산) — 세 제품 모두 여름에 함께 오르는 공통 계절이 상관을 키웁니다.';};
W['w6-si']=function(b){var L=['1','2','3','4','5','6','7','8','9','10','11','12'].map(function(m){return m+'월'});Chart.bars(b.querySelector('#si6-svg'),{labels:L,series:[{name:'냉면',color:'#82b8ff',values:D6.si.냉면},{name:'콩국수',color:'#f1b646',values:D6.si.콩국수},{name:'비빔면',color:'#f0604d',values:D6.si.비빔면}],ref:1,min:0,max:3.3,h:250});var mx=function(a){var i=a.indexOf(Math.max.apply(null,a));return (i+1)+'월 '+a[i].toFixed(2)};b.querySelector('#si6-out').innerHTML='최대: 냉면 <b>'+mx(D6.si.냉면)+'</b> · 콩국수 <b>'+mx(D6.si.콩국수)+'</b> · 비빔면 <b>'+mx(D6.si.비빔면)+'</b> · 프로모션 효과(같은 달 비교): 냉면 1.24배 · 콩국수 1.04배 · 비빔면 1.26배';};
W['w6-scen']=function(b){var s=b.querySelector('#sc6-svg'),o=b.querySelector('#sc6-out');function f(k){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',x.dataset.k===k)});var S=D6.sum[k],yrs=Object.keys(S),sc=scen(k);var L=yrs.concat(['2027']),v=yrs.map(function(y){return S[y]}).concat([null]);var band=L.map(function(y,i){return y=='2027'?[sc.낮음,sc.높음]:[null,null]});Chart.line(s,{labels:L,series:[{name:k+' 여름 일평균',color:'#82b8ff',values:v,dots:true},{name:'2027 보통',color:'#5ee39c',values:L.map(function(y){return y=='2027'||y=='2026'?(y=='2027'?sc.보통:S[2026]):null}),dash:'5 4',dots:true},{name:'2027 높음',color:'#f0604d',values:L.map(function(y){return y=='2027'||y=='2026'?(y=='2027'?sc.높음:S[2026]):null}),dash:'3 3',dots:true},{name:'2027 낮음',color:'#f1b646',values:L.map(function(y){return y=='2027'||y=='2026'?(y=='2027'?sc.낮음:S[2026]):null}),dash:'3 3',dots:true}],min:0,h:240});o.innerHTML=k+' 2027 여름 일평균: 낮음 <b>'+Math.round(sc.낮음).toLocaleString()+'</b> · 보통 <b>'+Math.round(sc.보통).toLocaleString()+'</b> · 높음 <b>'+Math.round(sc.높음).toLocaleString()+'</b> 팩 (폭 '+Math.round(sc.높음-sc.낮음).toLocaleString()+')';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(x.dataset.k)}});f('냉면');};
W['w6-cap']=function(b){var tb=b.querySelector('#cp6-tb'),o=b.querySelector('#cp6-out');function f(S){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',x.dataset.s===S)});var rows='',ppl=0;Object.keys(PL).forEach(function(k){var d=scen(k)[S],r=shiftFor(k,d),p=PL[k];ppl+=p.ln*p.crew*r[0];rows+='<tr><td>'+k+'</td><td class="n">'+Math.round(d).toLocaleString()+'</td><td class="n">'+p.ln+' × '+p.cap.toLocaleString()+'</td><td class="n">'+r[0]+'교대 ('+HR[r[0]]+'h)</td><td class="n" style="color:'+(r[1]>.95?'var(--eye)':r[1]>.85?'var(--amber)':'var(--gfp)')+'">'+(r[1]*100).toFixed(1)+'%</td></tr>';});ppl+=3*6*3;tb.innerHTML='<table class="tb"><tr><th>제품</th><th>하루 수요(팩)</th><th>라인 × 시간당</th><th>교대</th><th>가동률</th></tr>'+rows+'</table>';o.innerHTML='하루 필요 인원 <b>'+ppl+'명</b> (직접 + 간접 54명) × 1.4 = <b>'+Math.ceil(ppl*1.4)+'명</b> · 노랑 = 목표 85% 초과, 빨강 = 최대 95% 초과';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(x.dataset.s)}});f('보통');};
W['w6-mat']=function(b){var tb=b.querySelector('#mt6-tb'),wo=b.querySelector('#mt6-wo');function f(S){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',x.dataset.s===S)});var M={};Object.keys(PL).forEach(function(k){var d=scen(k)[S];for(var m in PL[k].bom)M[m]=(M[m]||0)+PL[k].bom[m]*d*7;});tb.innerHTML='<table class="tb"><tr><th>원재료</th><th>주간 소요량</th><th>발주 단위</th><th>MOQ</th><th>단위 올림</th></tr>'+Object.keys(M).map(function(m){var u=UNIT[m],q=Math.max(u[2],Math.ceil(M[m]/u[1])*u[1]);return '<tr><td>'+m+'</td><td class="n">'+Math.round(M[m]).toLocaleString()+' '+u[0]+'</td><td class="n">'+u[1].toLocaleString()+'</td><td class="n">'+u[2].toLocaleString()+'</td><td class="n">'+q.toLocaleString()+'</td></tr>'}).join('')+'</table>';var fl=Math.ceil(M.밀가루/20)*20;wo.innerHTML='<div class="wo"><h4>작업지시서 · 월요일 원재료 발주 <span class="lv" style="background:#2e8b57">'+S+' 시나리오</span></h4><table><tr><td>① 결과</td><td>다음 주 밀가루 소요 '+Math.round(M.밀가루).toLocaleString()+'kg · 리드타임 7일</td></tr><tr><td>② 작업자</td><td>구매팀 박씨</td></tr><tr><td>③ 작업 항목</td><td>A제분에 밀가루 '+fl.toLocaleString()+'kg 발주 (20kg 단위 올림), 나머지 8종 표대로 발주</td></tr><tr><td>④ 완료 시각</td><td>월요일 12:00</td></tr><tr><td>⑤ 메모</td><td>생산팀·품질팀 공유 · 안전재고 3일분은 현재고 확인 후 추가</td></tr></table></div>';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){f(x.dataset.s)}});f('보통');};
W['w6-prop']=function(b){var P=[['① 문제 정의','여름 성수기(6~8월) 수요가 해마다 ±20% 넘게 흔들려 라인·인력·원재료 계획이 늦다.'],['② 현황 분석','계절지수(콩국수 7월 3.07), 여름 일평균 추이, 2027 세 시나리오 범위.'],['③ 원인 규명','날씨·검색·프로모션 — 검색과 판매 상관 0.82는 인과가 아님, 선행 신호 후보.'],['④ 자동화 구상','매주 월요일 판매·검색 데이터 → 시나리오 재계산 → 교대·발주 작업지시서 초안 자동 생성.'],['⑤ 기대효과·90일','기준선: 결품일 수·폐기량·초과근무. 1~30일 데이터 연결, 31~60일 초안 시범, 61~90일 현장 적용.']],bt=b.querySelector('#pp-bt'),o=b.querySelector('#pp-out');P.forEach(function(p,i){var x=document.createElement('button');x.className='bt';x.textContent=p[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y,j){y.classList.toggle('on',j<=i)});o.innerHTML=P.slice(0,i+1).map(function(q,j){return '<p class="'+(j==i?'g':'')+'"><b>'+q[0]+'</b> — '+q[1]+'</p>'}).join('');};bt.appendChild(x);});bt.lastChild.click();};
W['w6-duel']=function(b){var c=b.querySelector('#du6-c');function lab(){b.querySelector('#du6-vc').textContent=c.value;}c.oninput=lab;lab();b.querySelector('#du6-run').onclick=function(){var d=scen('비빔면').높음,cap2=3*1100*15,short=Math.max(0,d-cap2)*92,lost=short*3980/1e4,opt=+c.value*92;b.querySelector('#du6-k').innerHTML='<div class="kpi r"><b>'+Math.round(short).toLocaleString()+'팩</b><span>주판봇: 92일 결품 (2교대 고정)</span></div><div class="kpi a"><b>'+Math.round(lost).toLocaleString()+'만원</b><span>주판봇: 잃은 매출</span></div><div class="kpi g"><b>0팩</b><span>초파리: 3교대 전환으로 결품 없음</span></div><div class="kpi m"><b>'+opt.toLocaleString()+'만원</b><span>초파리: 대기조 비용(92일)</span></div>';var win=lost>opt;sayDoc('e10',(win?'초파리 연구원 승. ':'주판봇 승. ')+'높음 시나리오에서 비빔면 2교대 능력은 하루 '+cap2.toLocaleString()+'팩, 수요는 '+Math.round(d).toLocaleString()+'팩입니다. 92일 결품 '+Math.round(short).toLocaleString()+'팩, 매출 약 '+Math.round(lost).toLocaleString()+'만원을 잃습니다. 대기조 비용 '+opt.toLocaleString()+'만원과 비교하면 '+(win?'옵션을 사 두는 쪽이 낫습니다.':'이 비용이라면 옵션이 더 비쌉니다. 옵션의 값은 비용과 시나리오 확률로 정합니다.'));};};
'''

RP = {
 'title': '2027년 여름, 면류 3사는 몇 교대로 몇 명이 무엇을 사 둬야 할까?',
 'eyebrow': '6주차 REVIEW 실습 리포트 · 면류 3사 · 2027년 6~8월 계획',
 'desc': '스마트 제조 6주차 REVIEW 실습 리포트 — 면류 일별 판매로 2027년 여름 수요를 세 시나리오로 잡고, 라인 가동률·교대·인원·주간 원재료까지 계산한 결과를 박사가 정리합니다.',
 'lead': '1~5주의 도구로 면류 3사의 2027년 여름 계획을 세웠습니다. 보통 시나리오면 지금 라인으로 목표 가동률 85% 안에 들어오지만, 높음이 오면 비빔면이 2교대로는 하루 약 2,900팩씩 모자랍니다.',
 'cover_mood': 'e07', 'back': ('index.html', '6주차 REVIEW 본문으로'), 'next': ('../w07/index.html', '7주차 (준비 중)'),
 'summary': {
   'finding': '2027년 여름 보통 시나리오에서는 냉면·콩국수 3교대, 비빔면 2교대로 가동률 83~85%에 들어오고 하루 387명(환산)이 필요하며, 높음 시나리오에서는 비빔면 3교대 전환과 416명이 필요합니다.',
   'evidence': ['<span class="fact">사실</span> 여름(6~8월) 일평균은 2023~2025년 늘다가 2026년 20~25% 줄었습니다(<a href="#fig-r6-1">그림 1</a>).',
                '<span class="fact">사실</span> 보통 시나리오 가동률은 냉면 83.1% · 콩국수 82.6% · 비빔면 84.9%(2교대)입니다(<a href="#tab-r6-2">표 2</a>).',
                '<span class="fact">사실</span> 높음 시나리오에서 비빔면 2교대 능력(49,500팩/일)은 수요 52,401팩보다 하루 2,901팩 모자랍니다.',
                '<span class="interp">해석</span> 계획은 보통으로 세우되, 비빔면 3교대 전환 옵션과 냉면·콩국수의 기초 재고를 높음 대비 장치로 두는 것이 이 리포트의 권고입니다.'],
   'fig': ('fig', {'id': 'fig-r6-1', 'cap': '[그림 1] 제품별 여름(6~8월) 일평균 판매 추이 (단위: 팩)', 'w': 'r6-summer', 'alt': '2016~2026년 냉면·콩국수·비빔면 여름 일평균 선. 냉면은 2025년 78,434로 최고, 2026년 59,661로 감소', 'src': '출처: 면류 일별 검색·판매 CSV(판매량 가상), 2016-06~2026-08, 저자 계산'}),
 },
 'sections': [
  {'id': 'sec-r6-1', 'nav': '들어가며', 'title': '들어가며 — REVIEW를 계획표 한 장으로', 'blocks': [
    ('memo', 'e08', '복습은 문제 풀이로 끝나기 쉬워요. 그래서 이번엔 다섯 주의 도구를 한 공장에 한꺼번에 써 봤습니다.'),
    ('p', '받은 자료는 면류 일별 판매 3,929일과, 제품·BOM·원재료·라인·교대·인력·검사·물류 시트가 든 엑셀입니다. 가정 파라미터는 2027년 6월 1일~8월 31일(92일)을 계획하라고 적혀 있습니다.'),
    ('p', '이 리포트의 질문은 넷입니다. ① 여름 수요의 범위는 ② 지금 라인으로 감당되나 ③ 몇 명이 필요한가 ④ 매주 무엇을 얼마나 사 둬야 하나.')]},
  {'id': 'sec-r6-2', 'nav': '배경', 'title': '배경 — 여름이 한 해를 정하는 제품', 'blocks': [
    ('p', '계절지수로 보면 콩국수는 7월이 평균적인 달의 3.07배, 냉면은 7월 2.02배, 비빔면은 6월 1.50배입니다. 콩국수와 냉면은 여름 석 달이 한 해 판매의 큰 몫을 차지합니다.'),
    ('p', '유통기한도 다릅니다. 냉면 30일, 콩국수 25일은 냉장이라 미리 많이 만들어 두기 어렵고, 비빔면은 상온 180일이라 재고로 봉우리를 받기 쉽습니다.'),
    ('memo', 'e09', '3주의 아이스크림은 냉동이라 미리 만들어 둘 수 있었죠? 냉장 면은 그게 어려워요. 그래서 라인 능력과 교대가 더 중요해집니다.')]},
  {'id': 'sec-r6-3', 'nav': '방법', 'title': '방법 — 시나리오 → 가동률 → 인원 → 원재료', 'blocks': [
    ('table', {'id': 'tab-r6-1', 'cap': '<표 1> 계산 규칙 (출처: 엑셀 가정 파라미터·시트)', 'head': ['단계', '규칙'],
               'rows': [['수요 시나리오', '여름 일평균 — 낮음 = 2026, 보통 = 2023~2026 평균, 높음 = 2023~2026 최대'], ['라인 능력', '라인 수 × 시간당 능력 × 유효 가동시간(1교대 7.5h · 2교대 15h · 3교대 21h)'], ['교대 선택', '가동률 85% 이하가 되는 가장 적은 교대, 3교대로도 넘으면 3교대'], ['인원', 'Σ 라인 × 교대당 직접인력 × 교대 + 공장 3곳 × 간접 6명 × 3교대, × 환산계수 1.4'], ['원재료', 'BOM 팩당 소요량 × 일 수요 × 7일']],
               'src': '출처: 면류 계획 엑셀(가정_파라미터, 공장_라인, 교대_가동시간, 인력기준, BOM, 원재료)'}),
    ('p', '계산 코드는 저장소 analysis/w06_plan.py에 있습니다. 본문 6.10~6.12와 대결의 계산기가 같은 규칙으로 움직입니다.')]},
  {'id': 'sec-r6-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3>결과 1 · 시나리오별 가동률</h3>'),
    ('table', {'id': 'tab-r6-2', 'cap': '<표 2> 2027년 여름 하루 수요와 가동률 (단위: 팩/일, %)', 'head': ['제품', '낮음', '보통', '높음'],
               'rows': [['냉면 (4라인 × 1,000)', '59,661 · 3교대 71.0%', '69,801 · 3교대 83.1%', '78,434 · 3교대 93.4%'], ['콩국수 (3라인 × 850)', '36,328 · 3교대 67.8%', '44,242 · 3교대 82.6%', '48,998 · 3교대 91.5%'], ['비빔면 (3라인 × 1,100)', '29,895 · 2교대 60.4%', '42,021 · 2교대 84.9%', '52,401 · 3교대 75.6%']],
               'src': '출처: 저자 계산 (analysis/w06_plan.py)'}),
    ('p', '<span class="fact">사실</span> 낮음에서도 냉면은 2교대(능력 60,000팩)로 99.4%라 3교대가 필요합니다. 높음에서는 냉면·콩국수가 목표 85%를 넘지만 최대 95% 안입니다.'),
    ('p', '<span class="interp">해석</span> 냉면과 콩국수는 어느 시나리오든 3교대가 기본입니다. 계획의 갈림길은 비빔면의 2교대 ↔ 3교대 전환입니다.'),
    ('html', '<h3>결과 2 · 인원</h3>'),
    ('p', '<span class="fact">사실</span> 하루 필요 인원은 낮음·보통 276명(환산 387명), 높음 297명(환산 416명)입니다. 차이 21명(환산 29명)은 비빔면 3교대의 직접인력 3라인 × 7명입니다.'),
    ('key', '보통으로 387명을 확보하고, 비빔면 3교대용 29명을 옵션(대기조·단기 계약)으로 둡니다.'),
    ('html', '<h3>결과 3 · 주간 원재료 (보통)</h3>'),
    ('table', {'id': 'tab-r6-3', 'cap': '<표 3> 보통 시나리오 주간 원재료 소요량', 'head': ['원재료', '소요량', '발주 단위·MOQ', '공급사'],
               'rows': [['밀가루', '160,493 kg', '20 kg · 1,000 kg', 'A제분'], ['포장필름', '1,092,447 매', '5,000 매 · 50,000 매', 'G포장'], ['냉면육수농축액', '58,633 kg', '18 kg · 360 kg', 'E소스'], ['대두분말', '37,163 kg', '20 kg · 500 kg', 'D식품'], ['메밀가루', '29,317 kg', '25 kg · 500 kg', 'B곡물'], ['감자전분', '28,524 kg', '25 kg · 500 kg', 'C전분'], ['비빔장', '23,532 kg', '20 kg · 400 kg', 'E소스'], ['팜유', '11,766 kg', '180 kg · 1,800 kg', 'F유지'], ['겨자·식초소스', '9,772 kg', '10 kg · 200 kg', 'E소스']],
               'src': '출처: BOM × 보통 시나리오 일 수요 × 7일, 저자 계산 (안전재고·현재고 미반영)'}),
    ('p', '<span class="interp">해석</span> E소스 한 곳에서 육수·비빔장·소스 세 가지(주 약 92톤)를 받습니다. 높음 시나리오나 공급 차질에 가장 민감한 곳으로 읽습니다.'),
    ('html', '<h3>결과 4 · 높음이 오면 무엇이 모자라나</h3>'),
    ('p', '<span class="fact">사실</span> 비빔면을 2교대로 고정한 채 높음이 오면 하루 2,901팩, 92일 266,892팩이 모자라고, 판매가 3,980원 기준 약 10.6억 원의 매출을 잃습니다.'),
    ('memo', 'e16', '이게 3주에서 말한 "시나리오 + 옵션"이에요. 대기조 비용이 92일에 10.6억 원보다 싸다면, 옵션을 사 두는 게 맞습니다.')]},
  {'id': 'sec-r6-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 2026년 감소가 새 추세(구조 변화)라면 높음은 오지 않는다. 가능합니다. 그래서 낮음도 함께 계산했고, 낮음에서는 비빔면 2교대 60%로 오히려 인력이 남습니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 일평균으로 계획하면 하루 최대(일평균의 1.5~1.9배)를 못 받는다. 맞습니다. 그 봉우리는 기초 재고(냉면 9만, 콩국수 5만, 비빔면 16만 팩)와 안전재고 2일분이 받는다고 가정했습니다. 냉장 제품의 유통기한 안에서 재고가 돌아야 합니다.'),
    ('p', '<span class="guess">추측</span> 검색지수가 판매보다 며칠 앞선다면, 6월 초 검색 추이로 어느 시나리오인지 일찍 판정할 수 있습니다. 시차별 상관 확인이 다음 과제입니다.')]},
  {'id': 'sec-r6-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 계절지수(3주) → 시나리오(3주) → 가동률·인원(1주 지표 정의) → 발주 작업지시서(5주)로 다섯 주가 한 계획표에 이어졌습니다. 8주 제안서의 "현황 분석·자동화 구상"이 이 흐름입니다.'),
    ('p', '한계: ① 판매·공장·원재료·물류는 가상 데이터 ② 라인 간 전환·공장 간 이동·운송시간 미반영 ③ 품질검사·출하대기(6~12시간)와 DC 처리 시간은 리드타임에 넣지 않음 ④ 날씨 예보 미사용.'),
    ('prompt', '#역할\n너는 면류 공장의 여름 생산계획 담당자다.\n#맥락\n첨부한 일별 판매 CSV와 계획 엑셀(가정_파라미터, 공장_라인, 교대_가동시간, 인력기준, BOM, 원재료)을 쓴다.\n#조건\n2027-06-01~08-31을 계획한다. 수요는 6~8월 일평균으로 낮음(2026)·보통(2023~2026 평균)·높음(최대) 세 시나리오.\n교대는 가동률 85% 이하가 되는 최소 교대. 인력은 환산계수 1.4를 곱한다.\n#형식\n① 시나리오별 제품 가동률 표 ② 하루·환산 인원 ③ 보통 시나리오 주간 원재료 표(발주 단위 올림) ④ 월요일 발주 작업지시서 1장(누가·무엇을·언제까지·보고)\n#검수 기준\n보통 시나리오 냉면 가동률 83.1%, 환산 인원 387명이 나와야 한다. 다르면 계산 과정을 보여 달라.'),
    ('memo', 'e07', '마지막 "검수 기준" 줄, 3주부터 계속 쓰고 있죠? AI 결과를 이 리포트 숫자와 맞춰 보는 게 오늘 숙제예요.'),
    ('p', '다음 편 예고: 7주차 "불량 분석 ① 어디서 터지는가"는 빈 슬롯입니다. 자료가 준비되는 대로 파레토와 공정·설비 분포를 같은 형식으로 채웁니다.')]},
 ],
 'refs': ['면류 수요예측·생산계획 실습 데이터: 일별 검색·판매 CSV(2016-01-01~2026-10-03), 계획 엑셀 13시트 — 판매·공장·원재료·물류는 교육용 가상 데이터, 검색지수는 네이버 데이터랩 원본', '안상선, 스마트 제조 1~5주 강의 교안, 2026', '이 저장소 analysis/w06_plan.py — 저자 계산'],
 'sources': [('원자료', '면류 일별 CSV · 계획 엑셀'), ('계산', '저자 계산 (analysis/w06_plan.py)')],
 'notes': '판매·공장·원재료·물류는 가상 데이터입니다. 시나리오는 최근 4년 범위로만 잡았습니다.',
}
RP['js'] = _DATA + r'''
W['r6-summer']=function(s){var yrs=Object.keys(D6.sum.냉면);Chart.line(s,{labels:yrs,series:[{name:'냉면',color:'#82b8ff',values:yrs.map(function(y){return D6.sum.냉면[y]}),dots:true},{name:'콩국수',color:'#f1b646',values:yrs.map(function(y){return D6.sum.콩국수[y]}),dots:true},{name:'비빔면',color:'#f0604d',values:yrs.map(function(y){return D6.sum.비빔면[y]}),dots:true}],min:0,h:250});};
'''
