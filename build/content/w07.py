# 7주차 · 불량 분석 ① 어디서 터지는가 — 세기 · 파레토 · 층별 · 불량 분포도
import os
_H = os.path.dirname(__file__)
_DATA = open(os.path.join(_H, '..', 'data_w07.js'), encoding='utf-8').read()

def _p(t):
    return '<div class="prompt" data-raw="' + t.replace('&', '&amp;').replace('"', '&quot;') + '">' + t.replace('&', '&amp;').replace('<', '&lt;') + '</div>'

C01 = '''[역할] 당신은 제조 라인의 품질 분석가다. 자연스러운 한국어로 짧게 답한다.
[데이터] 첨부한 ai4i_2024_mini.csv
[할 일]
1) 전체 행 수, machine_failure = 1인 행 수, 불량률(%)을 구한다.
2) twf, hdf, pwf, osf, rnf 각각 1인 행 수를 구한다.
3) 원인 라벨이 두 개 이상 1인 행의 UID를 모두 적는다.
4) machine_failure = 1인데 원인 라벨이 모두 0인 행이 있으면 UID를 적는다.
[출력] 표 2개(요약표, 원인별 건수표) + 겹친 행 목록. 계산 과정은 한 줄로만.'''
C02 = '''[역할] 당신은 제조 라인의 품질 분석가다. 한국어로 답한다.
[데이터] 첨부한 ai4i_2024_mini.csv
[할 일]
1) twf, hdf, pwf, osf, rnf 각각의 건수를 내림차순으로 정렬한다.
2) 각 원인의 비율(%)과 누적 비율(%)을 구한다.
3) 막대(건수) + 꺾은선(누적 %) 파레토 차트를 그린다. 80% 기준선을 점선으로 표시한다.
4) 누적 80%에 처음 도달하는 원인까지를 '핵심 원인'으로 적는다.
[출력 형식]
- 표: 순위 | 원인 | 건수 | 비율 | 누적 비율
- 차트 1개
- 해석 3줄 (현장 관리자에게 말하듯)
[주의] 원인이 겹치는 행은 원인마다 한 번씩 센다고 차트 제목에 적는다.'''
C03 = '''[역할] 당신은 제조 라인의 품질 분석가다. 한국어로 답한다.
[데이터] 첨부한 ai4i_2024_mini.csv
[할 일]
1) tool_wear_min, torque_nm, rotational_speed_rpm, temp_diff 각각을
   행 수가 같은 4개 구간(분위)으로 나눈다. 구간 경계값을 적는다.
2) 구간마다 행 수(n), 불량 건수, 불량률(%)을 구한다. (불량 = machine_failure = 1)
3) 컬럼마다 구간별 불량률 막대 차트를 그린다. 전체 불량률을 가로 점선으로 표시한다.
4) 전체 불량률의 2배 이상인 구간을 '몰린 구간'으로 표시한다.
[출력 형식]
- 컬럼별 표: 구간 | 범위 | n | 불량 건수 | 불량률
- 차트 4개 (2×2 배치)
- 몰린 구간 목록과 한 줄 해석
[주의] n이 10 미만인 구간은 해석하지 말고 '표본 부족'이라고 적는다.'''
C04 = '''[역할] 당신은 제조 라인의 품질 분석가다. 한국어로 답한다.
[데이터] 첨부한 불량품_판정_데이터.csv (열 이름은 파일 그대로 사용)
[할 일]
1) nomal_abnormal 열의 값 종류와 각 개수, 불량(abnormal) 비율을 구한다.
2) with_mm, surface_roughness_um, UT_dB, oven_temp_c 각각을
   행 수가 같은 5개 구간으로 나누고 구간별 n, 불량 건수, 불량률을 구한다.
3) 4개 측정값의 구간별 불량률 막대 차트를 그리고 전체 불량률을 점선으로 표시한다.
4) 불량률이 전체의 2배 이상인 구간을 적는다.
[출력 형식] 컬럼별 표 + 차트 4개 + 몰린 구간 목록 + 해석 3줄'''
C05 = '''[역할] 당신은 제조 라인의 품질 분석가다. 한국어로 답한다.
[데이터] 첨부한 ai4i_2024_mini.csv
[할 일]
1) 다음 세 짝으로 각각 히트맵을 만든다. 각 축은 행 수가 같은 3~4개 구간으로 나눈다.
   (가) tool_wear_min × torque_nm
   (나) rotational_speed_rpm × temp_diff
   (다) rotational_speed_rpm × torque_nm
2) 칸마다 불량률(%)과 n을 함께 표시한다. 색은 흰색에서 주황색 한 가지로.
3) 짝마다 불량률이 가장 높은 칸을 찾아 아래 형식의 '조건 문장'으로 쓴다.
   "A가 a1~a2 이고 B가 b1~b2 일 때, 불량률 x% (n=k)"
[주의] n이 5 미만인 칸은 조건 문장에 쓰지 않는다.'''
CV = '''방금 쓴 조건 문장 3개를 각각 그대로 필터로 적용해서
해당 행의 UID 목록, 행 수, machine_failure = 1인 행 수를 다시 보여줘.
조건 문장의 숫자와 다르면 어느 쪽이 맞는지 설명해.'''

CH = {
 'slug': 'w07', 'num': '07',
 'title': '불량 분석 ① 어디서 터지는가',
 'eyebrow': '7주차 · SECTION 3 · 분석 · 기어 가공 라인',
 'desc': '스마트 제조 7주차 — 불량을 원인별로 세고(파레토), 측정값을 구간으로 나누고(층별), 두 측정값을 겹쳐(불량 분포도) 불량이 몰리는 곳을 숫자로 찾습니다. 프롬프트 카드 5장과 다시 세기 검증.',
 'q': '불량률 13%라는 숫자 한 줄로, 어디를 먼저 고칠지 알 수 있을까?',
 'lead': '불량은 고르게 나지 않습니다. 오늘은 기어 가공 라인의 부품 100개를 원인별로 세고, 구간으로 나누고, 두 측정값을 겹친 지도에 찍습니다. 손에 남는 것은 원인 순위표 · 구간표 · 불량 분포도, 세 장입니다.',
 'scene_alt': '기어 가공 라인 3D. 소재 투입, 호빙(치형 가공), 열처리, 연삭, 치형 검사, 출하 순서로 기어가 흐르고 검사에서 일부가 빨갛게 바뀐다. 벽 앞에는 원인별 파레토 막대 다섯 개, 바닥에는 3×3 불량 분포도 칸이 높이로 불량률을 보여 준다.',
 'scene_hud': '3D · 기어 가공 라인 — 파레토 막대과 불량 분포도 바닥을 둘러보세요',
 'scene_opts': {'cam': [2, 16, 26], 'target': [0, 1, -1]},
 'kpis': [('13 / 100', '불량 부품 · 불량률 13.0%', 'r'), ('14', '원인 건수 (UID 042 겹침)', 'a'), ('57.1%', '상위 2원인 twf·hdf의 몫', 'm'), ('38%', '회전↓ × 온도차↓ 칸 (n=13)', 'g')],
 'hero_talk': [
   ('doc', 'e08', '오늘 공장은 기어 가공 라인입니다. 부품 100개 중 13개가 불량이었어요. 어디서 터졌는지 찾아봅시다.'),
   ('robo', 'e19', '불량률 13%! 모든 설비 점검 주기를 13% 당기면 끝입니다!'),
   ('fly', 'e09', '같은 13%라도 한 곳에 몰렸는지, 다섯 곳에 흩어졌는지에 따라 처방이 달라.'),
   ('asst', 'e12', '세고, 나누고, 지도에 찍는 순서로 가 볼게요!'),
 ],
 'three': ['불량을 원인별로 세고(파레토), 측정값 구간별로 나누고(층별), 두 측정값을 겹친 칸(불량 분포도)에서 불량이 몰리는 곳을 찾습니다.',
           '불량률 한 줄은 평균일 뿐입니다. 몰린 곳을 숫자로 적어야 어디를 먼저 고칠지 정할 수 있습니다.',
           '업무에서는 「마모 68분 이상 × 토크 51Nm 이상에서 불량률 30% (n=10)」 같은 조건 문장 한 줄이 점검 기준이 됩니다.'],
 'abbr': [('twf', 'Tool Wear Failure', '공구 마모 고장'), ('hdf', 'Heat Dissipation Failure', '열 방출 고장'),
          ('pwf', 'Power Failure', '전력 고장 — 힘(토크×회전)이 너무 크거나 작음'), ('osf', 'Overstrain Failure', '과부하 고장'),
          ('rnf', 'Random Failure', '무작위 고장 — 측정값으로 설명 안 됨'), ('n', 'number of rows', '그 비율을 만든 행(부품) 수')],
 'why': [('평균은 숨긴다', '전체 불량률 13% 안에 0%짜리 구간과 28%짜리 구간이 함께 들어 있습니다.'),
         ('시간은 한정돼 있다', '다섯 원인을 한꺼번에 고칠 수 없습니다. 무엇이 많은지부터 줄을 세웁니다.'),
         ('AI는 그럴듯하게 센다', '생성형 AI가 준 숫자는 한 번 다시 셉니다. 다시 센 숫자만 지도에 남깁니다.')],
 'big_lead': '네 단계로 갑니다. 단계마다 프롬프트 카드가 한 장씩 있습니다.',
 'big': [('① 세기 (7.1~7.4)', '건수 vs 비율 · 원인 라벨 · 겹친 행 · 카드 01'), ('② 파레토 (7.5~7.6)', '원인 순위 · 누적 80% · 모양과 함정 · 카드 02'),
         ('③ 층별 (7.7~7.10)', '구간별 불량률 · n과 우연 · 다른 공장 · 원인·구간 연결 · 카드 03·04'), ('④ 불량 분포도 (7.11~7.13)', '두 축 히트맵 · 조건 문장 · 다시 세기 · 카드 05')],
 'glossary': {
   '불량률': ['불량률', '지표', '불량 건수 ÷ 전체 × 100입니다. 비율 옆에는 항상 n(전체 행 수)을 함께 적습니다.'],
   '파레토': ['파레토 차트', '방법', '원인을 많은 순으로 막대로 세우고, 누적 비율을 선으로 겹친 차트입니다.'],
   '층별': ['층별', '방법', '데이터를 라인·교대·구간 같은 층으로 나눠 층마다 불량률을 비교하는 방법입니다.'],
   '분위': ['분위(같은 행 수 구간)', '방법', '값을 크기 순으로 줄 세운 뒤 행 수가 같도록 자른 구간입니다. 4개면 사분위입니다.'],
   '히트맵': ['히트맵', '시각화', '두 축의 칸마다 값을 색으로 칠한 표입니다. 오늘은 칸의 색 = 불량률, 칸의 숫자 = n입니다.'],
   '조건 문장': ['조건 문장', '산출물', '「A가 a1~a2이고 B가 b1~b2일 때, 불량률 x% (n=k)」. 범위·불량률·n 세 가지가 꼭 들어갑니다.'],
 },
 'subs': [
  {'id': 'sec-7-1', 'title': '불량 건수와 불량률 — 다른 질문에 답한다', 'tags': ['일상: 시험 오답 수 vs 오답률', '약속: 비율 옆에 n'],
   'pair': ('일상으로 치면', '100문제 중 10개 틀린 시험과 20문제 중 4개 틀린 시험. 틀린 수는 앞이 많고, 틀린 비율은 뒤가 높습니다.',
            '기어 공장에서는', '라인 A 1,000개 중 30개(3.0%), 라인 B 200개 중 12개(6.0%). 건수는 A, 비율은 B가 문제입니다.'),
   'body': ['불량 건수는 「몇 개가 나빴나」, 불량률은 「전체 중 몇 %가 나빴나」에 답합니다. 불량률 = 불량 건수 ÷ 전체 × 100입니다.',
            '주의할 점이 하나 있습니다. 행 수가 적은 곳의 비율은 크게 흔들립니다. 20개 중 1개만 바뀌어도 5%p가 움직이니까요. 그래서 비율 옆에는 항상 n을 적습니다.'],
   'talk': [('robo', 'e07', '라인 B가 6%로 두 배! B부터 고치면 됩니다!'), ('fly', 'e09', '건수로는 A가 30개야. 손실이 큰 건 어느 쪽인지도 봐야지.'), ('asst', 'e07', '아래에서 숫자를 바꿔 보면서 비교해 볼게요.')],
   'widget': ('w7-rate', '<div class="ptitle">계산기 · 두 라인의 건수와 비율</div><div class="ctrl"><div class="group"><span class="glabel">라인 A 전체</span><input type="number" id="ra-n" value="1000" min="1" style="width:84px"><span class="glabel">불량</span><input type="number" id="ra-b" value="30" min="0" style="width:64px"></div><div class="group"><span class="glabel">라인 B 전체</span><input type="number" id="rb-n" value="200" min="1" style="width:84px"><span class="glabel">불량</span><input type="number" id="rb-b" value="12" min="0" style="width:64px"></div></div><div class="eq" id="rt-out" aria-live="polite"></div>'),
   'limit': '건수와 비율 중 무엇이 중요한지는 비용으로 정합니다. 이 절은 둘을 구분하는 연습입니다.',
   'quiz': [{'q': '20개 중 2개 불량(10%)과 1,000개 중 50개 불량(5%). 바르게 적은 것은?', 'o': ['10% > 5%', '10% (n=20) · 5% (n=1,000)'], 'a': 1, 'why': 'n이 20이면 1개 차이로 5%p가 움직입니다. n을 함께 적어야 읽는 사람이 판단합니다.'}]},

  {'id': 'sec-7-2', 'title': '원인 라벨 다섯 가지 — machine_failure 뒤에 숨은 것', 'tags': ['데이터: ai4i_2024_mini.csv 100행', '2주 연결: 원인 분석용 라벨'],
   'body': ['<div class="tw"><table class="tb"><tr><th>라벨</th><th>이름</th><th>현장 말로</th><th>함께 볼 컬럼</th></tr>'
            '<tr><td>twf</td><td>공구 마모 고장</td><td>공구가 닳아서</td><td>tool_wear_min</td></tr>'
            '<tr><td>hdf</td><td>열 방출 고장</td><td>열이 빠지지 못해서</td><td>temp_diff, rpm</td></tr>'
            '<tr><td>pwf</td><td>전력 고장</td><td>힘(토크×회전)이 너무 크거나 작아서</td><td>torque_nm, rpm</td></tr>'
            '<tr><td>osf</td><td>과부하 고장</td><td>닳은 공구에 큰 힘이 걸려서</td><td>tool_wear_min, torque_nm</td></tr>'
            '<tr><td>rnf</td><td>무작위 고장</td><td>측정값으로 설명되지 않는</td><td>—</td></tr></table></div>',
            '라벨은 모두 0 또는 1입니다. machine_failure가 1인 행에서는 원인 라벨 중 하나 이상이 1입니다. 이 약속이 실제로 지켜지는지는 데이터에서 직접 확인합니다.',
            '오늘의 기어 라인에 대입하면, 호빙과 연삭에서 공구가 닳고(twf), 열처리 뒤 열이 빠지지 않으며(hdf), 회전과 토크가 만드는 힘이 어긋납니다(pwf, osf).'],
   'talk': [('sia', 'e07', '2주에 「원인 분석용으로 남겨 둔」 다섯 라벨, 오늘 꺼냅니다.'), ('moa', 'e12', '100개 부품을 한 판에 깔아 봤어요. 원인 버튼을 눌러 보세요!'), ('x1', 'e04', '(오)')],
   'widget': ('w7-grid', '<div class="ptitle">데이터 · 부품 100개 (한 칸 = 부품 하나, UID 001~100)</div><div class="ctrl" id="gd-bt"></div><div id="gd-box" style="display:grid;grid-template-columns:repeat(10,1fr);gap:3px;max-width:420px"></div><div class="eq" id="gd-out" aria-live="polite"></div>'),
   'limit': '이 데이터는 수업용 100행 미니판입니다. 원인 라벨 정의는 UCI AI4I 2020 데이터의 설명을 따랐습니다.',
   'quiz': [{'q': '「닳은 공구에 큰 힘이 걸려서」 생기는 고장은?', 'o': ['twf', 'osf', 'pwf'], 'a': 1, 'why': '과부하(osf)는 마모와 토크를 함께 봅니다.'}]},

  {'id': 'sec-7-3', 'title': '원인이 겹치는 행 — 합이 안 맞는 이유', 'tags': ['함정: 원인 건수 ≠ 불량 부품 수', '사례: UID 042'],
   'fx': {'q': '불량 부품은 13개인데 원인을 더하면 14예요. 하나는 어디서 왔어요?',
          'school': '집합 — 합집합의 원소 수 (n(A∪B) = n(A) + n(B) − n(A∩B))',
          'eq': '불량 부품 수 = Σ 원인 건수 − <b>겹친 횟수</b>',
          'rows': [('Σ 원인 건수', 'twf 4 + hdf 4 + pwf 2 + osf 3 + rnf 1 = 14'), ('겹친 횟수', 'UID 042가 hdf와 osf 둘 → 1'), ('불량 부품 수', '14 − 1 = 13')],
          'calc': '14 − 1 = 13. 원인이 하나도 없는 불량 행은 0개라, 겹침만 빼면 정확히 맞습니다.',
          'comment': '합이 안 맞으면 틀린 게 아니라 겹친 거구나. 파레토 제목에 「원인 건수 기준」이라고 적어야겠어요!'},
   'body': ['UID 042는 열도 빠지지 않았고(hdf), 닳은 공구에 큰 힘도 걸렸습니다(osf). 원인별로 세면 2건이지만 불량 부품은 1개입니다.',
            '그래서 원인별 건수의 합은 불량 부품 수보다 크거나 같습니다. 파레토는 「원인 건수」 기준임을 차트 제목에 적습니다. rnf는 측정값으로 설명이 안 되는 불량이라 따로 표시합니다.'],
   'talk': [('robo', 'e16', '합계 14건이니 불량 14개! 보고서에 그렇게 쓰겠습니다!'), ('fly', 'e10', '13개야. 042가 두 번 세어졌어.'), ('x3', 'e16', '(삐빅)')],
   'widget': ('w7-ovl', '<div class="ptitle">확인 · 불량 부품 13개와 원인 라벨</div><div class="tw" id="ov-tb"></div><div class="eq" id="ov-out" aria-live="polite"></div>'),
   'limit': '이 데이터에서는 원인 없는 불량이 0개였습니다. 다른 데이터에서는 원인이 비어 있는 불량 행이 나올 수 있으니 매번 확인합니다.',
   'quiz': [{'q': '원인 건수 합 20, 불량 부품 17, 원인 없는 불량 0이면 겹친 횟수는?', 'o': ['3', '17', '37'], 'a': 0, 'why': '20 − 17 = 3입니다.'}]},

  {'id': 'sec-7-4', 'title': '카드 01 · 세는 일부터 AI에게 — 그리고 다시 세기', 'tags': ['프롬프트 카드 01', '2주 연결: 숫자부터 검산'],
   'body': ['숫자를 먼저 확정해야 그 위의 차트가 흔들리지 않습니다. 카드 01은 행 수, 불량률, 원인별 건수, 겹친 행을 한 번에 묻습니다. 3)과 4)는 다음 장 파레토를 읽는 데 씁니다.',
            _p(C01),
            '참고 답: 전체 100행 · 불량 13행 · 불량률 13.0%. 원인별 twf 4 · hdf 4 · pwf 2 · osf 3 · rnf 1(합 14). 원인이 둘인 행 UID 042(hdf+osf). 원인 없는 불량 행 없음.'],
   'talk': [('asst', 'e07', 'AI가 이렇게 답했다고 해 볼게요. 틀린 줄을 골라 보세요.'), ('fly', 'e03', '그럴듯한 숫자가 제일 위험해.'), ('doc', 'e10', '고른 뒤에는 데이터로 다시 세어 확인합니다.')],
   'widget': ('w7-ai', '<div class="ptitle">다시 세기 · AI 답(예시) 중 틀린 줄 고르기</div><div id="ai-box"></div><div class="ctrl"><button class="bt primary" id="ai-go" type="button">데이터로 다시 세기</button></div><div class="eq" id="ai-out" aria-live="polite"></div>'),
   'limit': 'AI 답은 이 페이지가 만든 예시입니다. 실제 AI는 매번 다르게 틀릴 수 있어, 카드마다 다시 세는 습관이 필요합니다.',
   'quiz': [{'q': 'AI가 「원인 합계 14 = 불량 14개」라고 답했다. 무엇을 확인하나?', 'o': ['원인이 겹친 행', '전체 행 수'], 'a': 0, 'why': '겹친 행이 있으면 원인 합계가 불량 부품 수보다 큽니다.'}]},

  {'id': 'sec-7-5', 'title': '파레토 — 많은 것부터 줄을 세운다', 'tags': ['방법: 파레토 차트', '프롬프트 카드 02'],
   'why': {'problem': '다섯 원인을 한꺼번에 고칠 시간과 돈이 없습니다.',
           'limit': '원인별 건수를 표로만 보면 「어디까지가 핵심인가」가 눈에 들어오지 않습니다.',
           'solve': '많은 순으로 막대를 세우고 누적 비율 선을 겹칩니다. 선이 80%를 처음 넘는 곳까지가 핵심 소수입니다.',
           'easy': '대청소 때 가장 큰 짐부터 치우면, 몇 개만 옮겨도 방이 거의 빈다.'},
   'fx': {'q': '누적 비율은 어떻게 계산해요?',
          'school': '수열의 합(부분합), 비율',
          'eq': '누적 비율(k위) = (1위 + … + k위 건수) ÷ <b>원인 건수 합계 14</b> × 100',
          'rows': [('분모', '불량 부품 13이 아니라 원인 건수 14'), ('80% 선', '「80/20」은 법칙이 아니라 경향 — 실제 값을 확인'), ('rnf', '순위와 관계없이 「측정값으로 설명 안 됨」 표시')],
          'calc': 'twf 4 → 28.6%, + hdf 4 → 57.1%, + osf 3 → 78.6%, + pwf 2 → 92.9%(80% 돌파), + rnf 1 → 100%.',
          'comment': '상위 두 원인만 잡아도 원인 건수의 절반이 넘네요. 80%는 네 번째에서 넘고요.'},
   'body': [_p(C02),
            '차트는 막대(건수)와 선(누적 비율) 두 겹입니다. 읽는 순서는 ① 가장 왼쪽 막대(1순위) ② 선이 80%를 넘는 곳까지(핵심 소수) ③ 오른쪽의 작은 막대들(나중에)입니다.',
            'twf와 hdf는 4건으로 동률입니다. 동률일 때 순서는 정하기 나름이니, 해석할 때는 「공동 1위」로 읽습니다.'],
   'talk': [('robo', 'e19', '1위 twf만 고치면 끝!'), ('fly', 'e09', 'hdf도 4건, 동률이야. 그리고 80%는 pwf까지 가야 넘어.'), ('sia', 'e10', '기준을 「건수」에서 「정지 시간」으로도 바꿔 보겠습니다.')],
   'widget': ('w7-par', '<div class="ptitle">파레토 · 원인 건수 기준 (겹치는 행은 원인마다 한 번씩)</div><div class="ctrl"><button class="bt on" data-k="n" type="button">건수 기준</button><button class="bt" data-k="t" type="button">정지 시간 기준 (예시값)</button></div><div class="cwrap"><svg id="pa-svg"></svg></div><div class="eq" id="pa-out" aria-live="polite"></div>'),
   'limit': '정지 시간은 원인별 1건당 정지 시간을 가정한 예시값(twf 20분 · hdf 45분 · osf 90분 · pwf 60분 · rnf 30분)입니다. 데이터에는 없습니다.',
   'quiz': [{'q': '이 데이터에서 누적 80%를 처음 넘는 원인은?', 'o': ['hdf', 'osf', 'pwf'], 'a': 2, 'why': 'osf까지 78.6%, pwf를 더하면 92.9%입니다.'}]},

  {'id': 'sec-7-6', 'title': '파레토의 네 가지 모양과 세 가지 함정', 'tags': ['읽기: 모양 → 다음 행동', '함정: 건수만 · 작은 데이터 · 겹침'],
   'body': ['차트의 모양이 다음 행동을 고릅니다. ① 막대 하나가 크게 솟으면 그 원인부터 집중 ② 큰 막대가 두세 개면 상위 2~3개 동시 대응 ③ 평평하면 분류가 너무 굵으니 다시 나누기 ④ rnf가 크면 측정 항목을 늘릴 신호입니다. 오늘 데이터는 ②에 가깝습니다.',
            '함정도 셋입니다. 함정 01 — 건수 1위가 손실 1위는 아닙니다(정지 시간을 함께 적기). 함정 02 — 100행에서 몇 건 차이는 우연일 수 있습니다(n 적기). 함정 03 — 원인 합계를 불량 부품 수로 착각합니다(겹친 행 확인).'],
   'talk': [('moa', 'e09', '평평한 모양이면 뭘 해야 해요?'), ('doc', 'e07', '원인을 더 잘게 나눕니다. 「기타」가 1위인 파레토도 같은 신호예요.'), ('x2', 'e09', '(…)')],
   'widget': ('w7-shape', '<div class="ptitle">모양 고르기 · 네 가지 파레토 (그림 모양은 예시값)</div><div class="ctrl" id="sh-bt"></div><div class="cwrap"><svg id="sh-svg"></svg></div><div class="eq" id="sh-out" aria-live="polite"></div>'),
   'limit': '네 모양의 막대 높이는 설명용 예시값입니다. 「우리 데이터」 버튼만 실측입니다.',
   'quiz': [{'q': '원인 다섯 개가 모두 비슷한 높이다. 다음 행동은?', 'o': ['1위부터 집중', '분류를 더 잘게 다시 나눈다'], 'a': 1, 'why': '평평하면 분류가 너무 굵다는 신호입니다.'}]},

  {'id': 'sec-7-7', 'title': '층별 — 평균 안에 숨은 구간을 꺼낸다', 'tags': ['방법: 같은 행 수로 4구간(분위)', '프롬프트 카드 03'],
   'why': {'problem': '전체 불량률 13%는 100개를 섞은 평균입니다.',
           'limit': '이 데이터에는 라인·교대 열이 없어, 교과서식 「라인별 층별」을 할 수 없습니다.',
           'solve': '측정값을 같은 행 수의 구간으로 나눠 층을 만듭니다. 구간마다 불량률을 비교하고, 전체의 2배 이상을 「몰린 구간」으로 미리 정해 둡니다.',
           'easy': '반 평균 70점 안에 90점 모둠과 50점 모둠이 함께 있는 것과 같다.'},
   'fx': {'q': '「같은 행 수로 4구간」은 어떻게 잘라요? 경계값은요?',
          'school': '통계 — 사분위수(중학교 상자그림)',
          'eq': '값을 작은 순으로 줄 세움 → 25% · 50% · 75% 지점에서 자름 → 구간당 <b>25행</b>',
          'rows': [('경계값', 'tool_wear_min 23.6 · 50.9 · 74.0분'), ('2배 기준', '전체 13.0% × 2 = 26.0%'), ('표본 부족', 'n < 10인 구간은 해석하지 않음')],
          'calc': '마모 구간별 불량: 4/25 = 16% · 0/25 = 0% · 2/25 = 8% · 7/25 = 28%. 상위 구간 28%가 26%를 넘습니다.',
          'comment': '평균 13% 안에 0%랑 28%가 같이 있었네요. 나누니까 보여요!'},
   'body': [_p(C03),
            '네 컬럼을 같은 방식으로 나누면 몰린 구간은 둘입니다. 마모 상위(74.0분 초과) 28%(n=25), 회전 하위(1,438.6rpm 이하) 28%(n=25)입니다. 온도차 하위(24.6K 이하) 24%와 토크 하위(47.5Nm 이하) 20%는 2배(26%)에 못 미치는 경계 사례입니다.',
            '<p class="lim">원자료의 「온도차 하위 구간 24%를 몰린 구간(2배 이상)으로 표시」를 이 페이지에서는 「2배 기준(26%)에 조금 못 미치는 경계 사례」로 바꿉니다. 24 ÷ 13 = 1.85배입니다.</p>'],
   'talk': [('asst', 'e04', '마모 두 번째 구간은 0%예요! 25개 중 하나도 없어요.'), ('robo', 'e07', '온도차 하위 24%도 몰린 구간!'), ('fly', 'e10', '2배면 26%야. 24%는 경계. 기준을 먼저 적어 둔 이유가 그거야.')],
   'widget': ('w7-strat', '<div class="ptitle">층별 · 컬럼별 4구간 불량률 (점선 = 전체 13.0%, 주황 = 2배 이상)</div><div class="ctrl" id="st-bt"></div><div class="cwrap"><svg id="st-svg"></svg></div><div class="tw" id="st-tb"></div>'),
   'limit': '경계값 위의 동점 처리에 따라 도구마다 구간 행 수가 1~2개 다를 수 있습니다. 이 페이지는 「경계값 포함은 아래 구간」 규칙입니다.',
   'quiz': [{'q': '전체 불량률 13%일 때 「몰린 구간」 기준(2배)은?', 'o': ['15%', '26%', '13%p 이상'], 'a': 1, 'why': '13 × 2 = 26%입니다.'}]},

  {'id': 'sec-7-8', 'title': '구간을 얼마나 잘게 — 너무 잘면 우연이 패턴이 된다', 'tags': ['함정 02: 작은 데이터', '규칙: 구간당 최소 행 수'],
   'body': ['100행을 4구간으로 나누면 구간당 25행입니다. 20구간으로 나누면 구간당 5행이고, 1건만 불량이어도 20%가 됩니다. 구간이 잘수록 우연이 패턴처럼 보입니다.',
            '그래서 약속은 둘입니다. ① 100행이면 4구간보다 잘게 나누지 않는다 ② n이 10 미만인 구간은 「표본 부족」이라고만 적는다. 1,000행이면 5구간(구간당 약 200행)까지 나눌 수 있습니다.'],
   'talk': [('robo', 'e19', '20구간으로 나눴더니 60%짜리 구간 발견! 대박!'), ('fly', 'e09', '그 구간 n이 몇이야? 5개 중 3개면 우연일 수도 있어.'), ('asst', 'e07', '구간 수를 직접 바꿔 볼게요.')],
   'widget': ('w7-bins', '<div class="ptitle">실험 · 마모(tool_wear_min) 구간 수를 바꾸면 (회색 = n &lt; 10, 표본 부족)</div><div class="ctrl"><div class="group"><span class="glabel">구간 수</span><input type="range" min="2" max="20" value="4" id="bn-k"><span class="val" id="bn-v"></span></div></div><div class="cwrap"><svg id="bn-svg"></svg></div><div class="eq" id="bn-out" aria-live="polite"></div>'),
   'explain': ['구간 수를 10 이상으로 올리면 막대가 들쭉날쭉해지고, 가장 높은 막대는 대개 n이 10이 안 되는 구간에서 나옵니다. 그 높이는 「몇 개 중 몇 개」를 같이 보지 않으면 믿을 수 없습니다.'],
   'limit': '「n ≥ 10」은 이 수업의 실용 규칙입니다. 엄밀한 판단은 9주차 이후 검정(우연일 확률)으로 다룹니다.',
   'quiz': [{'q': '1,000행 데이터를 5구간으로 나누면 구간당 약 몇 행?', 'o': ['50행', '200행', '500행'], 'a': 1, 'why': '1,000 ÷ 5 = 200행입니다.'}]},

  {'id': 'sec-7-9', 'title': '카드 04 · 다른 공장, 같은 질문 — 불량 판정 데이터', 'tags': ['데이터: 불량품 판정 1,000행', '카드는 재사용된다'],
   'body': ['같은 카드를 데이터만 바꿔 다시 씁니다. 이번 데이터는 판재 1,000장의 폭(with_mm) · 표면 거칠기(surface_roughness_um) · 초음파(UT_dB) · 오븐 온도(oven_temp_c)와 판정(nomal_abnormal)입니다. 열 이름의 철자는 파일 그대로 씁니다.',
            _p(C04),
            '세어 보면 abnormal 33장, 불량률 3.3%입니다. 2배 기준은 6.6%입니다. 5구간 중 가장 높은 곳은 거칠기 상위 구간(3.42µm 초과) 6.1%(12/198)로, 1.8배입니다.',
            '<p class="lim">원자료의 「거칠기 상위 구간 6.0% (n=201) — 2배 이상 몰린 구간」을 이 페이지에서는 「6.1% (12/198), 전체의 1.8배 — 2배 기준에 조금 못 미치는 경계 사례」로 바꿉니다. 경계값 3.42µm의 동점 처리에 따라 n은 198~201로 달라질 수 있습니다.</p>'],
   'talk': [('sia', 'e07', '4주 판재 데이터와 이름은 같은데, 이번 파일은 새로 받은 판입니다. 숫자가 달라요.'), ('fly', 'e09', '5구간으로는 2배를 넘는 데가 없네. 그럼 「몇 µm부터」 넘는지가 진짜 질문이겠다.'), ('doc', 'e16', '좋은 질문입니다. 8주 주제 카드 예시가 바로 그 질문이에요.')],
   'widget': ('w7-d2', '<div class="ptitle">층별 · 불량 판정 데이터 (점선 = 전체 3.3%, 주황 = 2배 6.6% 이상)</div><div class="ctrl" id="d2-bt"></div><div class="ctrl"><span class="glabel">구간 수</span><button class="bt" data-k="4" type="button">4</button><button class="bt on" data-k="5" type="button">5</button><button class="bt" data-k="10" type="button">10</button></div><div class="cwrap"><svg id="d2-svg"></svg></div><div class="eq" id="d2-out" aria-live="polite"></div>'),
   'limit': '이 데이터는 판정 결과만 있고 원인 라벨이 없습니다. 「어느 구간에 몰렸나」까지만 말할 수 있습니다.',
   'quiz': [{'q': '전체 3.3%, 어떤 구간 6.1%. 2배 기준으로 판정하면?', 'o': ['몰린 구간', '경계 사례 (6.6%에 미달)'], 'a': 1, 'why': '3.3 × 2 = 6.6%이므로 6.1%는 미달입니다.'}]},

  {'id': 'sec-7-10', 'title': '원인과 구간 연결하기 — 「함께 나타남」까지만', 'tags': ['연결: 7.5 무엇 × 7.7 어디', '상관 ≠ 인과 (4주)'],
   'body': ['파레토의 「무엇」과 층별의 「어디」를 한 표에서 만나게 합니다. twf·osf는 마모 상위 구간(28%)과, hdf는 회전 하위·온도차 하위 구간(24~28%)과 함께 나타납니다. pwf는 토크 양 끝(하위 20% · 상위 12%)이 후보지만 2배 기준에 못 미칩니다.',
            '주의할 점은 하나입니다. 둘이 함께 나타난다고 원인이 증명된 것은 아닙니다. 오늘은 「함께 나타난다」까지만 말하고, 「왜」는 9주차 「불량 분석 ②」에서 다룹니다.'],
   'talk': [('robo', 'e16', '마모 상위에 불량이 몰렸으니 마모가 원인 확정!'), ('fly', 'e03', '「함께 나타남」이야. 마모가 높은 부품이 다른 이유로 같이 묶였을 수도 있어.'), ('moa', 'e12', '연결하기 퀴즈 만들어 왔어요!')],
   'widget': ('w7-pair', '<div class="ptitle">연결하기 · 원인 라벨 ↔ 몰린 구간</div><div class="tw" id="pr-tb"></div><div class="ctrl"><button class="bt primary" id="pr-go" type="button">채점</button></div><div class="eq" id="pr-out" aria-live="polite"></div>'),
   'limit': '이 연결은 「원인 라벨의 함께 볼 컬럼」(7.2 표)과 층별 결과를 겹친 것입니다. 원인을 밝히는 실험이 아닙니다.',
   'quiz': [{'q': '「마모 상위 구간에 twf가 몰렸다」에서 오늘 말할 수 있는 것은?', 'o': ['마모가 불량의 원인이다', '마모 상위 구간에 twf가 함께 나타난다'], 'a': 1, 'why': '인과는 다음 회차에 확인합니다.'}]},

  {'id': 'sec-7-11', 'title': '불량 분포도 — 두 조건이 겹치는 칸에 불량이 몰린다', 'tags': ['방법: 두 변수 히트맵', '프롬프트 카드 05'],
   'why': {'problem': '마모만 높아도, 토크만 높아도 괜찮을 수 있습니다.',
           'limit': '층별은 한 번에 한 컬럼만 봅니다. 두 조건이 함께 있을 때만 생기는 불량은 평균에 묻힙니다.',
           'solve': '두 측정값을 각각 3~4구간으로 나눠 격자를 만들고, 칸마다 불량률과 n을 적습니다. 진한 칸 하나가 「불량이 몰리는 곳」입니다.',
           'easy': '지하철 노선도에서 환승역이 붐비는 것처럼, 두 줄이 만나는 칸이 붐빈다.'},
   'fx': {'q': '칸의 불량률은 어떻게 계산해요? 층별이랑 뭐가 달라요?',
          'school': '확률 — 조건부 확률 (두 조건을 동시에 만족하는 경우)',
          'eq': '칸 불량률 = (A 구간 <b>이고</b> B 구간인 불량 수) ÷ (A 구간 이고 B 구간인 행 수 n)',
          'rows': [('축 구간', '각 축을 같은 행 수로 3구간(약 33행씩)'), ('칸의 n', '두 조건을 함께 만족하는 행 — 칸마다 다름'), ('n < 5', '조건 문장에 쓰지 않음')],
          'calc': '회전 1,418~1,443rpm이고 온도차 6.6~26.8K인 행은 13개, 그중 불량 5개 → 5 ÷ 13 = 38%. 층별(한 컬럼)의 24~28%보다 진합니다.',
          'comment': '조건이 둘이 되니까 n은 줄었는데 불량률은 더 올라갔네요. 그래서 n을 꼭 같이 적는구나!'},
   'body': [_p(C05),
            '두 축의 조합은 우리가 정합니다. 7.2 원인 표의 「함께 볼 컬럼」에서 고른 세 조합입니다. (가) 마모 × 토크는 osf·twf, (나) 회전 × 온도차는 hdf, (다) 회전 × 토크는 pwf를 겨냥합니다.',
            '<p class="lim">원자료 그림 7-4(마모 × 토크, 3×3)의 「14% (n=14)」「7% (n=15)」「15% (n=13)」을 이 페이지에서는 다시 센 값 「12.5% (n=16)」「5.9% (n=17)」「16.7% (n=12)」로 바꿉니다. 40%(n=5) · 27%(n=11) · 30%(n=10)는 같습니다.</p>'],
   'talk': [('asst', 'e04', '(나) 지도에서 회전 느림 × 온도차 작음 칸이 38%예요!'), ('fly', 'e09', '(가)의 40% 칸은 n=5야. 2개짜리 칸이지.'), ('x1', 'e01', '(반짝)')],
   'widget': ('w7-heat', '<div class="ptitle">불량 분포도 · 칸의 색 = 불량률, 칸 안 = 불량/n (빗금 = n &lt; 5)</div><div class="ctrl" id="ht-bt"></div><div class="ctrl"><span class="glabel">축 구간 수</span><button class="bt on" data-k="3" type="button">3×3</button><button class="bt" data-k="4" type="button">4×4</button></div><div class="tw" id="ht-tb"></div><div class="eq" id="ht-out" aria-live="polite"></div>'),
   'limit': '4×4로 나누면 칸당 평균 6행이라 대부분 칸이 표본 부족에 가깝습니다. 100행 데이터의 불량 분포도는 3×3을 기본으로 둡니다.',
   'quiz': [{'q': '불량 분포도의 칸에 꼭 함께 적는 것은?', 'o': ['불량률과 n', '불량률과 평균값'], 'a': 0, 'why': '칸마다 n이 달라 비율만으로는 믿을 수 없습니다.'}]},

  {'id': 'sec-7-12', 'title': '조건 문장과 검증 — 다시 센 숫자만 지도에 남긴다', 'tags': ['산출물: 조건 문장 3줄', '검증 프롬프트 + 엑셀 필터'],
   'body': ['불량이 몰리는 곳은 한 문장으로 적습니다. 「A가 a1~a2이고 B가 b1~b2일 때, 불량률 x% (n=k)」. 범위 · 불량률 · n 셋 중 하나라도 없으면 문장이 아니라 추측입니다.',
            '<div class="tw"><table class="tb"><tr><th>지도</th><th>조건 문장 (3×3, n ≥ 5 중 최고 칸 · 다시 센 값)</th><th>관련 원인 후보</th></tr>'
            '<tr><td>(가) 마모 × 토크</td><td>마모 2.1~31.5분이고 토크 42.8~48.0Nm일 때 40% (n=5) — 불량 2건뿐인 칸. 두 번째로 높은 칸: 마모 67.9~117.1분이고 토크 51.0~56.2Nm일 때 30% (n=10)</td><td>hdf·pwf / osf</td></tr>'
            '<tr><td>(나) 회전 × 온도차</td><td>회전 1,418~1,443rpm이고 온도차 6.6~26.8K일 때 38% (n=13)</td><td>hdf</td></tr>'
            '<tr><td>(다) 회전 × 토크</td><td>회전 1,418~1,443rpm이고 토크 48.0~51.0Nm일 때 27% (n=11)</td><td>twf·hdf</td></tr></table></div>',
            '<p class="lim">원자료의 조건 문장 (나) 「24–28% (n=25)」는 한 컬럼 층별 값이라, 이 페이지에서는 불량 분포도 칸의 값 「38% (n=13)」으로 바꿉니다. (다) 「실측 후 채운다」는 「27% (n=11)」로 채웁니다.</p>',
            '그다음이 검증입니다. 생성형 AI는 그럴듯한 숫자를 만들 수 있습니다. 조건 문장을 그대로 필터로 걸어 UID 목록과 행 수를 다시 셉니다. 엑셀 필터로 한 번 더 세어 두 경로가 같은 숫자를 말해야 지도에 남깁니다.',
            _p(CV)],
   'talk': [('robo', 'e07', 'AI가 (나) 칸을 「45% (n=20)」이라고 했습니다. 그대로 씁시다!'), ('fly', 'e10', '필터로 다시 세 봐. 13행에 5건일걸.'), ('sia', 'e10', '아래에서 조건 문장을 고르면 UID까지 다시 셉니다.')],
   'widget': ('w7-ver', '<div class="ptitle">검증 · 조건 문장을 필터로 다시 세기</div><div class="ctrl" id="vf-bt"></div><div class="eq" id="vf-out" aria-live="polite"></div>'),
   'limit': '다시 셀 때도 경계값 포함 규칙(「이상/초과」)을 조건 문장과 똑같이 맞춰야 합니다. 규칙이 다르면 n이 1~2개 달라집니다.',
   'quiz': [{'q': 'AI의 조건 문장 n과 다시 센 n이 다르다. 어떻게 하나?', 'o': ['평균을 낸다', '그 문장은 버리고 다시 센 숫자로 고친다'], 'a': 1, 'why': '다시 센 숫자만 지도에 남깁니다.'}]},

  {'id': 'sec-7-13', 'title': '자주 하는 실수 다섯과 세 장의 산출물', 'tags': ['정리: 세 장', '8주 연결: 주제 카드 재료'],
   'body': ['불량 분석에서 자주 하는 실수는 다섯 가지입니다. ① 비율만 적고 n을 뺀다 ② 원인 합계를 불량 부품 수로 읽는다 ③ 구간을 너무 잘게 나눈다 ④ 「함께 나타남」을 「원인」이라고 말한다 ⑤ AI가 준 숫자를 그대로 쓴다.',
            '오늘 손에 남는 것은 세 장입니다. 산출물 01 원인 순위표(파레토, 누적 80% 표시), 산출물 02 구간별 불량률 표(몰린 구간, n 포함), 산출물 03 불량 분포도(조건 문장 3줄, 검증 완료 표시). 이 세 장이 8주차 주제 카드의 재료가 됩니다.'],
   'talk': [('doc', 'e16', '세고, 나누고, 지도에 찍었습니다. 몰린 곳을 숫자로 적는 사람이 먼저 고칩니다.'), ('moa', 'e12', '세 장 체크리스트 만들었어요!'), ('x3', 'e01', '(삐빅!)')],
   'widget': ('w7-chk', '<div class="ptitle">점검 · 세 장을 들고 가기 전에</div><div class="ctrl" id="ck-bt" style="flex-direction:column;align-items:flex-start"></div><div class="eq" id="ck-out" aria-live="polite"></div>'),
   'limit': '체크 상태는 저장되지 않습니다.',
   'quiz': [{'q': '세 장 중 「조건 문장 3줄」이 들어가는 산출물은?', 'o': ['원인 순위표', '구간별 불량률 표', '불량 분포도'], 'a': 2, 'why': '불량 분포도의 최고 칸을 조건 문장으로 적습니다.'}]},
 ],
 'duel': {
   'q': '정밀 검사를 25개만 할 수 있다면, 어떤 부품을 고를까?',
   'intro': [('doc', 'e07', '검사 인력이 부족해 100개 중 25개만 정밀 검사할 수 있다고 합시다. 주판봇은 「불량은 13%로 고르게 난다」며 무작위로 고르고, 초파리 연구원은 층별 결과로 고릅니다.'), ('sia', 'e12', '시작!')],
   'fly': '층별에서 몰린 구간을 먼저 고른다. 마모 높은 순, 회전 낮은 순, 온도차 작은 순 중 하나로.',
   'robo': '불량률 13%면 어디서 골라도 같습니다! 무작위로 25개!',
   'widget': 'w7-duel',
   'panel': '<div class="ptitle">시뮬레이션 · 25개 정밀 검사로 불량 몇 개를 잡나 (실측 100행)</div><div class="ctrl"><span class="glabel">초파리의 기준</span><button class="bt on" data-s="wr" type="button">마모 높은 순</button><button class="bt" data-s="rpm" type="button">회전 낮은 순</button><button class="bt" data-s="td" type="button">온도차 작은 순</button></div><div class="ctrl"><div class="group"><span class="glabel">검사 개수</span><input type="range" min="10" max="50" step="5" value="25" id="du7-n"><span class="val" id="du7-vn"></span></div><button class="bt primary" id="du7-run" type="button">검사 돌려 보기</button></div><div class="kpis" id="du7-k"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('x1', 'e01', '(짝짝)'), ('x2', 'e16', '(끄덕)'), ('x3', 'e01', '(삐빅!)')],
 },
 'summary': {
   'head': ['단계', '오늘 한 일', '이 데이터의 결과 (다시 센 값)'],
   'rows': [['세기', '건수 · 비율 · 원인 · 겹침', '100행 · 불량 13 (13.0%) · 원인 건수 14 · 겹침 UID 042'],
            ['파레토', '많은 순 + 누적 80%', 'twf 4 · hdf 4 (57.1%) → osf 3 (78.6%) → pwf 2 (92.9%) → rnf 1'],
            ['층별', '같은 행 수 4구간 + 2배 기준', '마모 상위 28% · 회전 하위 28% (몰림) · 온도차 하위 24% · 토크 하위 20% (경계)'],
            ['다른 공장', '카드 04 · 5구간', 'abnormal 33 (3.3%) · 거칠기 상위 6.1% (경계, 1.8배)'],
            ['불량 분포도', '두 축 3×3 + 조건 문장', '회전 1,418~1,443 × 온도차 6.6~26.8 → 38% (n=13)']],
   'limits': ['100행 데이터라 몇 건 차이는 우연일 수 있습니다. 칸·구간마다 n을 함께 적었습니다.',
              '원인·구간 연결과 불량 분포도는 「함께 나타남」까지입니다. 원인은 9주차에서 다룹니다.',
              '파레토의 정지 시간, 대결의 검사 개수는 예시값입니다.'],
 },
 'outro': [('doc', 'e16', '불량률 한 줄이 원인 순위표, 구간표, 불량 분포도 세 장이 됐습니다. 다음 주에는 이 세 장으로 각자 보고서 주제를 정합니다.'),
           ('asst', 'e01', '실습 리포트에 다시 센 숫자를 모두 정리해 뒀어요.'),
           ('fly', 'e10', '「어디」 다음은 「왜」야. 9주차 불량 분석 ②에서 이어 가자.'),
           ('robo', 'e12', '앞으로 조건 문장에는 꼭 n을 붙이겠습니다!')],
 'sources': [('강의 자료', '스마트 제조 7주차 교안 「불량 분석 ① 어디서 터지는가」 · 7주차 실습 가이드(프롬프트 카드 01~05, 검증 프롬프트)'),
             ('수업 데이터', 'ai4i_2024_mini.csv (100행, UCI AI4I 2020 기반 수업용 미니판) · 불량품_판정_데이터.csv (1,000행, 교육용 가상 데이터)'),
             ('원인 라벨 정의', 'S. Matzka, "Explainable Artificial Intelligence for Predictive Maintenance Applications", AI4I 2020 · UCI Machine Learning Repository'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '파레토의 원인별 정지 시간, 파레토 네 모양의 막대 높이, 7.1 라인 A·B, AI 답 예시는 예시값입니다. 원인 건수·구간 불량률·불량 분포도·조건 문장은 수업 데이터로 다시 센 값입니다. 원자료와 다른 값(온도차 하위 24%, 거칠기 상위 6.0%·n=201, 그림 7-4 세 칸, 조건 문장 (나)·(다))은 본문에 「바꿉니다」로 표시했습니다.',
 'practice': ('practice.html', '불량 13개는 어디에 몰렸나'),
}

_JS = r'''
var A7=D7.A.map(function(r){return {id:r[0],rpm:r[1],tq:r[2],wr:r[3],td:r[4],f:r[5],m:r[6]};});
var D7R=D7.D.map(function(r){return {w:r[0],r:r[1],u:r[2],o:r[3],f:r[4]};});
var CS=[['twf','공구 마모','#f1b646'],['hdf','열 방출','#f0604d'],['pwf','전력','#82b8ff'],['osf','과부하','#d672d6'],['rnf','무작위','#9aa5aa']];
var COL7={wr:['tool_wear_min','마모','분'],tq:['torque_nm','토크','Nm'],rpm:['rotational_speed_rpm','회전','rpm'],td:['temp_diff','온도차','K']};
var COLD={w:['with_mm','폭','mm'],r:['surface_roughness_um','표면 거칠기','µm'],u:['UT_dB','초음파','dB'],o:['oven_temp_c','오븐 온도','℃']};
function JS7(w){var c=w.charCodeAt(w.length-1)-44032;return (c>=0&&c<11172&&c%28)?'이':'가';}
function uid(i){return ('00'+i).slice(-3);}
function qedges(v,k){var s=v.slice().sort(function(a,b){return a-b}),n=s.length,e=[];for(var i=0;i<=k;i++){var p=i/k*(n-1),lo=Math.floor(p),hi=Math.ceil(p);e.push(s[lo]+(s[hi]-s[lo])*(p-lo));}return e;}
function qbin(x,e){for(var i=1;i<e.length-1;i++)if(x<=e[i])return i-1;return e.length-2;}
function strat(rows,key,k){var e=qedges(rows.map(function(r){return r[key]}),k),B=[];for(var i=0;i<k;i++)B.push({lo:e[i],hi:e[i+1],n:0,b:0});rows.forEach(function(r){var j=qbin(r[key],e);B[j].n++;B[j].b+=r.f;});B.forEach(function(b){b.r=b.n?b.b/b.n:0;});return B;}
function grid(xk,yk,k){var ex=qedges(A7.map(function(r){return r[xk]}),k),ey=qedges(A7.map(function(r){return r[yk]}),k),G=[];for(var a=0;a<k;a++){G.push([]);for(var b=0;b<k;b++)G[a].push({n:0,b:0,ids:[],fid:[]});}A7.forEach(function(r){var c=G[qbin(r[xk],ex)][qbin(r[yk],ey)];c.n++;c.b+=r.f;c.ids.push(r.id);if(r.f)c.fid.push(r.id);});return {ex:ex,ey:ey,G:G};}
function f1(v,d){return (+v).toFixed(d==null?1:d);}
function rng7(i,j,e,d){return f1(e[i],d)+'~'+f1(e[j],d);}
function causes(m){return CS.filter(function(c,i){return m>>i&1}).map(function(c){return c[0]});}
function sayDoc(mood,html){var v=document.getElementById('verdict');if(!v)return;v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
var PAIRS=[['(가) 마모 × 토크','wr','tq'],['(나) 회전 × 온도차','rpm','td'],['(다) 회전 × 토크','rpm','tq']];
window.H7=PAIRS.slice(0,2).map(function(p){var g=grid(p[1],p[2],3),dx=p[1]=='rpm'?0:1,dy=p[2]=='rpm'?0:1;return {name:p[0],x:COL7[p[1]][1],y:COL7[p[2]][1],xl:[0,1,2].map(function(i){return rng7(i,i+1,g.ex,dx)}),yl:[0,1,2].map(function(i){return rng7(i,i+1,g.ey,dy)}),cells:g.G.map(function(row){return row.map(function(c){return [c.n?c.b/c.n:0,c.n]})})};});
'''

CH['js'] = _DATA + _JS + r'''
W['w7-rate']=function(b){var I=['ra-n','ra-b','rb-n','rb-b'].map(function(i){return b.querySelector('#'+i)}),o=b.querySelector('#rt-out');function f(){var v=I.map(function(x){return Math.max(0,+x.value||0)}),ra=v[1]/Math.max(1,v[0])*100,rb=v[3]/Math.max(1,v[2])*100,swa=100/Math.max(1,v[0]),swb=100/Math.max(1,v[2]);o.innerHTML='라인 A <b>'+v[1]+'개 · '+ra.toFixed(1)+'% (n='+v[0].toLocaleString()+')</b> · 라인 B <b>'+v[3]+'개 · '+rb.toFixed(1)+'% (n='+v[2].toLocaleString()+')</b><br>건수가 많은 쪽: '+(v[1]==v[3]?'같음':v[1]>v[3]?'A':'B')+' · 비율이 높은 쪽: '+(Math.abs(ra-rb)<1e-9?'같음':ra>rb?'A':'B')+' · 불량 1개가 바꾸는 비율: A '+swa.toFixed(2)+'%p, B '+swb.toFixed(2)+'%p'+(Math.max(swa,swb)>=2?' — <b style="color:var(--amber)">n이 작아 크게 흔들립니다</b>':'');}I.forEach(function(x){x.oninput=f});f();};
W['w7-grid']=function(b){var box=b.querySelector('#gd-box'),bt=b.querySelector('#gd-bt'),o=b.querySelector('#gd-out'),cells=[];A7.forEach(function(r){var d=document.createElement('div');d.style.cssText='aspect-ratio:1;border-radius:3px;font-size:9px;display:flex;align-items:center;justify-content:center;color:#111';d.title='UID '+uid(r.id)+(r.f?' · 불량 '+causes(r.m).join('+'):' · 양품');d.textContent=r.id%10==0||r.f?r.id:'';box.appendChild(d);cells.push(d);});var K=[['전체 불량','#f0604d',function(r){return r.f}]].concat(CS.map(function(c,i){return [c[0]+' '+c[1],c[2],function(r){return r.m>>i&1},i]}));function f(j){bt.querySelectorAll('.bt').forEach(function(x,i){x.classList.toggle('on',i==j)});var k=K[j],ids=[];A7.forEach(function(r,i){var on=k[2](r);cells[i].style.background=on?k[1]:'#2c3046';cells[i].style.color=on?'#111':'#777';if(on)ids.push(uid(r.id));});var see=j?['tool_wear_min','temp_diff, rpm','torque_nm, rpm','tool_wear_min, torque_nm','—'][j-1]:'';o.innerHTML='<b>'+k[0]+'</b> '+ids.length+'건 · UID '+ids.join(', ')+(j?' · 함께 볼 컬럼: '+see:' · 불량률 13.0% (n=100)');}K.forEach(function(k,j){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=k[0];x.onclick=function(){f(j)};bt.appendChild(x);});f(0);};
W['w7-ovl']=function(b){var F=A7.filter(function(r){return r.f}),rows=F.map(function(r){var c=causes(r.m);return '<tr'+(c.length>1?' style="background:rgba(241,182,70,.15)"':'')+'><td>'+uid(r.id)+'</td>'+CS.map(function(s,i){return '<td class="n">'+(r.m>>i&1?'<b style="color:'+s[2]+'">1</b>':'·')+'</td>'}).join('')+'<td class="n">'+c.length+'</td></tr>'}).join(''),T=CS.map(function(s,i){return F.filter(function(r){return r.m>>i&1}).length}),S=T.reduce(function(a,c){return a+c},0),ov=F.filter(function(r){return causes(r.m).length>1}),none=F.filter(function(r){return !r.m});b.querySelector('#ov-tb').innerHTML='<table class="tb"><tr><th>UID</th>'+CS.map(function(s){return '<th>'+s[0]+'</th>'}).join('')+'<th>원인 수</th></tr>'+rows+'<tr><td><b>합계</b></td>'+T.map(function(t){return '<td class="n"><b>'+t+'</b></td>'}).join('')+'<td class="n"><b>'+S+'</b></td></tr></table>';b.querySelector('#ov-out').innerHTML='불량 부품 <b>'+F.length+'</b>개 · 원인 건수 합 <b>'+S+'</b> · 겹친 행 '+ov.map(function(r){return 'UID '+uid(r.id)+' ('+causes(r.m).join('+')+')'}).join(', ')+' · 원인 없는 불량 '+(none.length?none.map(function(r){return uid(r.id)}).join(', '):'없음')+' → '+S+' − '+(S-F.length)+' = '+F.length;};
W['w7-ai']=function(b){var L=[['전체 행 수 100, 불량 13, 불량률 13.0%',1],['원인별: twf 4 · hdf 4 · pwf 2 · osf 4 · rnf 1 (합 15)',0],['원인이 둘 이상인 행: 없음',0],['원인 라벨이 모두 0인 불량 행: 없음',1]],box=b.querySelector('#ai-box'),pick=L.map(function(){return 0});box.innerHTML='<div class="prompt" style="white-space:normal">'+L.map(function(l,i){return '<label style="display:block;margin:4px 0;cursor:pointer"><input type="checkbox" data-i="'+i+'"> AI: '+l[0]+'</label>'}).join('')+'</div>';box.querySelectorAll('input').forEach(function(x){x.onchange=function(){pick[+x.dataset.i]=x.checked?1:0;}});b.querySelector('#ai-go').onclick=function(){var F=A7.filter(function(r){return r.f}),T=CS.map(function(s,i){return F.filter(function(r){return r.m>>i&1}).length}),ok=L.every(function(l,i){return pick[i]==1-l[1]});b.querySelector('#ai-out').innerHTML='다시 센 값: 불량 '+F.length+' · '+CS.map(function(s,i){return s[0]+' '+T[i]}).join(' · ')+' (합 '+T.reduce(function(a,c){return a+c},0)+') · 겹친 행 UID 042 (hdf+osf) · 원인 없는 불량 없음<br>틀린 줄: <b>2번(osf 3건, 합 14)</b>과 <b>3번(UID 042)</b> — '+(ok?'<b style="color:var(--gfp)">정확히 골랐습니다.</b>':'<b style="color:var(--amber)">고른 줄과 다릅니다. 표와 다시 대조해 보세요.</b>');};};
W['w7-par']=function(b){var s=b.querySelector('#pa-svg'),o=b.querySelector('#pa-out'),T={twf:20,hdf:45,osf:90,pwf:60,rnf:30};function draw(k){b.querySelectorAll('.ctrl .bt').forEach(function(x){x.classList.toggle('on',x.dataset.k===k)});var F=A7.filter(function(r){return r.f}),D=CS.map(function(c,i){var n=F.filter(function(r){return r.m>>i&1}).length;return {c:c,n:n,v:k=='n'?n:n*T[c[0]]};});D.sort(function(a,b){return b.v-a.v||(a.c[0]=='rnf')-(b.c[0]=='rnf')});var tot=D.reduce(function(a,d){return a+d.v},0),cum=0;D.forEach(function(d){cum+=d.v;d.cum=cum/tot*100;});var Wd=640,H=250,L=44,R=44,Tp=18,B=30,bw=(Wd-L-R)/D.length,mx=D[0].v*1.1,NS='http://www.w3.org/2000/svg';s.setAttribute('viewBox','0 0 '+Wd+' '+H);s.setAttribute('class','chart');s.innerHTML='';function el(t,a){var e=document.createElementNS(NS,t);for(var q in a)e.setAttribute(q,a[q]);s.appendChild(e);return e;}var Y=function(v){return Tp+(H-Tp-B)*(1-v/mx)},Yp=function(p){return Tp+(H-Tp-B)*(1-p/100)};for(var g=0;g<=4;g++){var yy=Yp(g*25);el('line',{x1:L,x2:Wd-R,y1:yy,y2:yy,stroke:'#363a52'});el('text',{x:Wd-R+4,y:yy+4}).textContent=g*25+'%';}el('line',{x1:L,x2:Wd-R,y1:Yp(80),y2:Yp(80),stroke:'#f1b646','stroke-dasharray':'5 4'});var pts=[],hit=-1;D.forEach(function(d,i){var x=L+bw*i+bw*.15,w=bw*.7;el('rect',{x:x,y:Y(d.v),width:w,height:Y(0)-Y(d.v),fill:d.c[2],rx:2});el('text',{x:x+w/2,y:Y(d.v)-5,'text-anchor':'middle',style:'fill:#eceaf3'}).textContent=d.v+(k=='t'?'분':'건');el('text',{x:x+w/2,y:H-10,'text-anchor':'middle'}).textContent=d.c[0]+(d.c[0]=='rnf'?' *':'');pts.push((x+w/2)+','+Yp(d.cum));if(hit<0&&d.cum>=80)hit=i;});el('polyline',{points:pts.join(' '),fill:'none',stroke:'#5ee39c','stroke-width':2});pts.forEach(function(p,i){var q=p.split(',');el('circle',{cx:q[0],cy:q[1],r:3.5,fill:'#5ee39c'});});o.innerHTML=(k=='n'?'원인 건수 합 '+tot+' (불량 부품 13 · UID 042 겹침)':'정지 시간 합 '+tot+'분 (예시값)')+' · 누적: '+D.map(function(d){return d.c[0]+' '+d.cum.toFixed(1)+'%'}).join(' → ')+' · 80% 돌파: <b>'+D[hit].c[0]+'</b>까지 '+(hit+1)+'개'+(k=='t'?' · <b style="color:var(--amber)">건수 3위 osf가 정지 시간으로는 1위</b> — 함정 01':'')+' · * rnf = 측정값으로 설명 안 됨';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){draw(x.dataset.k)}});draw('n');};
W['w7-shape']=function(b){var S=[['우리 데이터',[4,4,3,2,1],'모양 02에 가깝다 — 상위 두 막대(twf·hdf)이 원인 건수의 57%. 상위 2~3개를 동시에 대응합니다.'],['① 막대 하나가 압도적',[14,2,1,1,1],'하나가 대부분 → 그 원인부터 집중합니다.'],['② 큰 막대 두세 개',[8,7,2,1,1],'핵심 소수 → 상위 2~3개 동시 대응.'],['③ 평평함',[4,4,4,4,3],'고르게 흩어짐 → 분류가 너무 굵다. 원인을 다시 나눕니다.'],['④ rnf가 큼',[3,2,2,1,9],'설명 안 되는 불량이 많다 → 측정 항목을 늘릴 신호입니다.']],bt=b.querySelector('#sh-bt'),o=b.querySelector('#sh-out');function f(i){bt.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',i==j)});var v=S[i][1].slice(),lb=i==0?['twf','hdf','osf','pwf','rnf']:['원인1','원인2','원인3','원인4','rnf'];if(i==4){v=[9,3,2,2,1];lb=['rnf','원인1','원인2','원인3','원인4'];}Chart.bars(b.querySelector('#sh-svg'),{labels:lb,series:[{name:i?'건수 (예시값)':'건수 (실측)',colorAt:function(x,j){return lb[j]=='rnf'?'#9aa5aa':'#82b8ff'},values:v}],min:0,h:200,values:true});o.innerHTML='<b>'+S[i][0]+'</b> — '+S[i][2];}S.forEach(function(s,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=s[0];x.onclick=function(){f(i)};bt.appendChild(x);});f(0);};
W['w7-strat']=function(b){var bt=b.querySelector('#st-bt');function f(key){bt.querySelectorAll('.bt').forEach(function(x){x.classList.toggle('on',x.dataset.k===key)});var B=strat(A7,key,4),d=key=='rpm'?1:2,u=COL7[key];Chart.bars(b.querySelector('#st-svg'),{labels:['하위','중하위','중상위','상위'],series:[{name:u[0]+' 구간 불량률(%)',values:B.map(function(x){return x.r*100}),colorAt:function(v){return v>=26?'#f1b646':'#82b8ff'}}],ref:13,min:0,max:35,h:220,values:true,fmt:function(v){return v.toFixed(0)+'%'}});b.querySelector('#st-tb').innerHTML='<table class="tb"><tr><th>구간</th><th>범위('+u[2]+')</th><th>n</th><th>불량</th><th>불량률</th><th>판정</th></tr>'+B.map(function(x,i){var r=x.r*100;return '<tr><td>'+['하위','중하위','중상위','상위'][i]+'</td><td class="n">'+f1(x.lo,d)+' ~ '+f1(x.hi,d)+'</td><td class="n">'+x.n+'</td><td class="n">'+x.b+'</td><td class="n">'+r.toFixed(1)+'%</td><td>'+(x.n<10?'표본 부족':r>=26?'<b style="color:var(--amber)">몰린 구간</b>':r>=19.5?'경계':'—')+'</td></tr>'}).join('')+'</table>';}['wr','tq','rpm','td'].forEach(function(k){var x=document.createElement('button');x.className='bt';x.type='button';x.dataset.k=k;x.textContent=COL7[k][1]+' ('+COL7[k][0]+')';x.onclick=function(){f(k)};bt.appendChild(x);});f('wr');};
W['w7-bins']=function(b){var k=b.querySelector('#bn-k');function f(){var K=+k.value;b.querySelector('#bn-v').textContent=K+'구간';var B=strat(A7,'wr',K),mx=B.reduce(function(a,x){return x.r>a.r?x:a},B[0]);Chart.bars(b.querySelector('#bn-svg'),{labels:B.map(function(x,i){return ''+(i+1)}),series:[{name:'마모 구간 불량률(%)',values:B.map(function(x){return x.r*100}),colorAt:function(v,i){return B[i].n<10?'#4a4f63':v>=26?'#f1b646':'#82b8ff'}}],ref:13,min:0,max:Math.max(40,mx.r*110),h:220});b.querySelector('#bn-out').innerHTML='구간당 약 <b>'+Math.round(100/K)+'행</b> · 가장 높은 구간 '+(mx.r*100).toFixed(0)+'% = '+mx.b+'/'+mx.n+' ('+f1(mx.lo)+'~'+f1(mx.hi)+'분)'+(mx.n<10?' — <b style="color:var(--amber)">표본 부족: 이 높이는 믿을 수 없습니다</b>':' — n이 10 이상입니다');}k.oninput=f;f();};
W['w7-d2']=function(b){var bt=b.querySelector('#d2-bt'),key='r',K=5;function f(){bt.querySelectorAll('.bt').forEach(function(x){x.classList.toggle('on',x.dataset.c===key)});b.querySelectorAll('.ctrl .bt[data-k]').forEach(function(x){x.classList.toggle('on',+x.dataset.k===K)});var B=strat(D7R,key,K),u=COLD[key],tot=D7R.filter(function(r){return r.f}).length,base=tot/D7R.length*100;Chart.bars(b.querySelector('#d2-svg'),{labels:B.map(function(x,i){return ''+(i+1)}),series:[{name:u[0]+' 구간 불량률(%)',values:B.map(function(x){return x.r*100}),colorAt:function(v){return v>=base*2?'#f1b646':'#82b8ff'}}],ref:base,min:0,max:Math.max(10,Math.max.apply(null,B.map(function(x){return x.r*110}))),h:220,values:true,fmt:function(v){return v.toFixed(1)}});var mx=B.reduce(function(a,x){return x.r>a.r?x:a},B[0]),hot=B.filter(function(x){return x.r*100>=base*2});b.querySelector('#d2-out').innerHTML='abnormal <b>'+tot+'</b> / 1,000 = '+base.toFixed(1)+'% · 2배 기준 '+(base*2).toFixed(1)+'% · 최고 구간 '+f1(mx.lo,2)+'~'+f1(mx.hi,2)+u[2]+' → <b>'+(mx.r*100).toFixed(1)+'%</b> ('+mx.b+'/'+mx.n+', '+(mx.r*100/base).toFixed(1)+'배) · 몰린 구간: '+(hot.length?hot.length+'개':'없음 (경계 사례만)')+(K==10?' — 10구간은 구간당 100행. 1,000행이면 아직 괜찮지만 불량이 33건뿐이라 구간당 불량은 몇 건입니다.':'');}Object.keys(COLD).forEach(function(c){var x=document.createElement('button');x.className='bt';x.type='button';x.dataset.c=c;x.textContent=COLD[c][1]+' ('+COLD[c][0]+')';x.onclick=function(){key=c;f()};bt.appendChild(x);});b.querySelectorAll('.ctrl .bt[data-k]').forEach(function(x){x.onclick=function(){K=+x.dataset.k;f()}});f();};
W['w7-pair']=function(b){var Q=[['twf · 공구 마모','마모 상위'],['osf · 과부하','마모 상위'],['hdf · 열 방출','회전 하위 · 온도차 하위'],['pwf · 전력','토크 양 끝 (경계)']],O=['마모 상위','회전 하위 · 온도차 하위','토크 양 끝 (경계)'];b.querySelector('#pr-tb').innerHTML='<table class="tb"><tr><th>원인</th><th>함께 나타나는 구간</th></tr>'+Q.map(function(q,i){return '<tr><td>'+q[0]+'</td><td><select data-i="'+i+'"><option value="">고르기</option>'+O.map(function(o){return '<option>'+o+'</option>'}).join('')+'</select></td></tr>'}).join('')+'</table>';b.querySelector('#pr-go').onclick=function(){var ok=0;b.querySelectorAll('select').forEach(function(s){var r=s.value===Q[+s.dataset.i][1];if(r)ok++;s.style.outline='2px solid '+(r?'#5ee39c':'#f0604d');});b.querySelector('#pr-out').innerHTML=ok+' / 4 · 근거(층별 4구간): 마모 상위 28% (n=25) · 회전 하위 28% · 온도차 하위 24% (각 n=25) · 토크 하위 20% / 상위 12% — 이 연결은 「함께 나타남」까지입니다.';};};
W['w7-heat']=function(b){var bt=b.querySelector('#ht-bt'),pi=0,K=3;function f(){bt.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',j==pi)});b.querySelectorAll('.ctrl .bt[data-k]').forEach(function(x){x.classList.toggle('on',+x.dataset.k===K)});var p=PAIRS[pi],g=grid(p[1],p[2],K),dx=p[1]=='rpm'?0:1,dy=p[2]=='rpm'?0:1,best=null;var h='<table class="tb" style="text-align:center"><tr><th>'+COL7[p[1]][1]+' ↓ / '+COL7[p[2]][1]+' →</th>'+g.ey.slice(0,K).map(function(e,j){return '<th>'+rng7(j,j+1,g.ey,dy)+'</th>'}).join('')+'</tr>';g.G.forEach(function(row,a){h+='<tr><th>'+rng7(a,a+1,g.ex,dx)+'</th>';row.forEach(function(c,j){var r=c.n?c.b/c.n:0,v=Math.min(1,r/.45),bg=c.n<5?'repeating-linear-gradient(45deg,#2c3046,#2c3046 4px,#383c55 4px,#383c55 8px)':'rgb(255,'+Math.round(245-120*v)+','+Math.round(235-200*v)+')';if(c.n>=5&&(!best||r>best.r||(r==best.r&&c.n>best.c.n)))best={r:r,a:a,j:j,c:c};h+='<td style="background:'+bg+';color:'+(c.n<5?'#bbb':'#111')+';min-width:72px"><b>'+(r*100).toFixed(0)+'%</b><br><span style="font-size:12px">'+c.b+'/'+c.n+'</span></td>';});h+='</tr>';});b.querySelector('#ht-tb').innerHTML=h+'</table>';var c=best.c;b.querySelector('#ht-out').innerHTML='조건 문장 (n ≥ 5 중 최고 칸): <b>「'+COL7[p[1]][1]+JS7(COL7[p[1]][1])+' '+rng7(best.a,best.a+1,g.ex,dx)+COL7[p[1]][2]+'이고 '+COL7[p[2]][1]+JS7(COL7[p[2]][1])+' '+rng7(best.j,best.j+1,g.ey,dy)+COL7[p[2]][2]+'일 때, 불량률 '+(best.r*100).toFixed(0)+'% (n='+c.n+')」</b><br>그 칸의 불량 UID: '+c.fid.map(uid).join(', ')+' · 원인: '+c.fid.map(function(i){return causes(A7[i-1].m).join('+')}).join(', ')+(c.n<10?' — <b style="color:var(--amber)">n이 10 미만, 두 번째로 높은 칸과 함께 읽으세요</b>':'');}PAIRS.forEach(function(p,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=p[0];x.onclick=function(){pi=i;f()};bt.appendChild(x);});b.querySelectorAll('.ctrl .bt[data-k]').forEach(function(x){x.onclick=function(){K=+x.dataset.k;f()}});f();};
W['w7-ver']=function(b){var V=[['(가) 마모 × 토크 · 30% (n=10)','wr',67.9,117.1,'tq',51.0,56.22,30,10],['(나) 회전 × 온도차 · 38% (n=13)','rpm',1418,1443.1,'td',6.6,26.81,38,13],['(다) 회전 × 토크 · 27% (n=11)','rpm',1418,1443.1,'tq',48.03,51.0,27,11],['AI 답(예시) · (나) 45% (n=20)','rpm',1418,1443.1,'td',6.6,26.81,45,20]],bt=b.querySelector('#vf-bt'),o=b.querySelector('#vf-out');function f(i){bt.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',i==j)});var v=V[i],S=A7.filter(function(r){return r[v[1]]>v[2]-1e-9&&r[v[1]]<=v[3]+1e-9&&r[v[4]]>v[5]-1e-9&&r[v[4]]<=v[6]+1e-9}),F=S.filter(function(r){return r.f}),rt=Math.round(F.length/S.length*100),same=S.length==v[8]&&rt==v[7];o.innerHTML='필터: '+COL7[v[1]][1]+' '+v[2]+'~'+v[3]+' 그리고 '+COL7[v[4]][1]+' '+v[5]+'~'+v[6]+'<br>해당 UID ('+S.length+'행): '+S.map(function(r){return r.f?'<b style="color:#f0604d">'+uid(r.id)+'</b>':uid(r.id)}).join(', ')+'<br>machine_failure = 1: <b>'+F.length+'행</b> → '+rt+'% (n='+S.length+') · 문장의 숫자: '+v[7]+'% (n='+v[8]+') → '+(same?'<b style="color:var(--gfp)">일치 — 지도에 남깁니다</b>':'<b style="color:#f0604d">불일치 — 이 문장은 버리고 다시 센 숫자로 고칩니다</b>');}V.forEach(function(v,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=v[0];x.onclick=function(){f(i)};bt.appendChild(x);});f(1);};
W['w7-chk']=function(b){var C=['원인 순위표 — 누적 80% 선과 「원인 건수 기준」 제목','원인 합계 14와 불량 부품 13을 구분해 적었다','구간별 불량률 표 — 경계값 · n · 2배 기준을 적었다','n &lt; 10 구간은 「표본 부족」으로만 적었다','불량 분포도 — 칸마다 불량률과 n','조건 문장 3줄 — 범위 · 불량률 · n','조건 문장을 필터로 다시 세어 일치를 확인했다','「함께 나타남」으로만 썼다 (원인 단정 없음)'],bt=b.querySelector('#ck-bt'),o=b.querySelector('#ck-out'),on=C.map(function(){return 0});C.forEach(function(c,i){var l=document.createElement('label');l.style.cssText='display:block;cursor:pointer';l.innerHTML='<input type="checkbox"> '+c;l.querySelector('input').onchange=function(e){on[i]=e.target.checked?1:0;f();};bt.appendChild(l);});function f(){var n=on.reduce(function(a,c){return a+c},0);o.innerHTML='<b>'+n+' / '+C.length+'</b> '+(n==C.length?'— 세 장 준비 끝. 8주 주제 카드로 가져갑니다.':'— 남은 항목: '+C.filter(function(c,i){return !on[i]}).length+'개');}f();};
W['w7-duel']=function(b){var s='wr',nIn=b.querySelector('#du7-n');function lab(){b.querySelector('#du7-vn').textContent=nIn.value+'개';}nIn.oninput=lab;lab();b.querySelectorAll('.ctrl .bt[data-s]').forEach(function(x){x.onclick=function(){s=x.dataset.s;b.querySelectorAll('.ctrl .bt[data-s]').forEach(function(y){y.classList.toggle('on',y===x)});}});b.querySelector('#du7-run').onclick=function(){var N=+nIn.value,S=A7.slice().sort(function(a,c){return s=='wr'?c.wr-a.wr:a[s]-c[s]}).slice(0,N),fly=S.filter(function(r){return r.f}),R=rng(70),tot=0,mx=0,T=2000;for(var t=0;t<T;t++){var idx=A7.map(function(r,i){return i}),c=0;for(var i=0;i<N;i++){var j=i+Math.floor(R()*(100-i)),tmp=idx[i];idx[i]=idx[j];idx[j]=tmp;c+=A7[idx[i]].f;}tot+=c;if(c>mx)mx=c;}var avg=tot/T,cz={};fly.forEach(function(r){causes(r.m).forEach(function(c){cz[c]=(cz[c]||0)+1})});var nm={wr:'마모 높은 순',rpm:'회전 낮은 순',td:'온도차 작은 순'}[s];b.querySelector('#du7-k').innerHTML='<div class="kpi m"><b>'+avg.toFixed(1)+'개</b><span>주판봇: 무작위 '+N+'개 평균 (2,000번)</span></div><div class="kpi a"><b>'+mx+'개</b><span>주판봇: 운 좋을 때 최대</span></div><div class="kpi g"><b>'+fly.length+'개</b><span>초파리: '+nm+' '+N+'개</span></div><div class="kpi r"><b>'+Object.keys(cz).map(function(c){return c+' '+cz[c]}).join(' · ')+'</b><span>초파리가 잡은 원인</span></div>';var miss=['twf','hdf','pwf','osf','rnf'].filter(function(c){return !cz[c]});sayDoc(fly.length>avg?'e10':'e09',(fly.length>avg?'초파리 연구원 승. ':'주판봇 승. ')+nm+'으로 고른 '+N+'개에서 불량 '+fly.length+'개, 무작위는 평균 '+avg.toFixed(1)+'개입니다. 다만 한 축으로 고르면 '+miss.join('·')+'는 놓칩니다. 그래서 원인마다 다른 축, 두 축을 겹친 불량 분포도가 필요합니다.');};};
'''

# ── 실습 리포트 (발견편) ───────────────────────────────────────
RP = {
 'title': '불량 13개는 어디에 몰렸나? — 기어 라인 100개를 세고, 나누고, 지도에 찍다',
 'eyebrow': '7주차 실습 리포트 · 불량 분석 ① · AI4I 미니 100행 + 불량 판정 1,000행',
 'desc': '스마트 제조 7주차 실습 리포트 — 프롬프트 카드 01~05의 결과를 데이터로 다시 세어, 열 방출 고장 4건이 모두 「회전 1,443rpm 이하 × 온도차 26.8K 이하」 한 칸에 몰렸음을 박사가 근거와 함께 정리합니다.',
 'lead': '카드 다섯 장의 답을 모두 다시 셌습니다. 불량 13개는 고르게 흩어지지 않았고, 원인마다 몰린 칸이 따로 있었습니다. 원자료 참고 답과 다른 값 다섯 곳도 함께 적었습니다.',
 'cover_mood': 'e07', 'back': ('index.html', '7주차 본문으로'), 'next': ('../w08/index.html', '8주차 중간 점검 — 주제 카드'),
 'summary': {
   'finding': '이 데이터(기어 가공 100개, 불량 13개)에서 열 방출 고장(hdf) 4건은 모두 「회전 1,418~1,443rpm × 온도차 6.6~26.8K」 칸(n=13, 불량률 38%)에, 과부하 고장(osf) 3건은 모두 「마모 67.9~117.1분 × 토크 51.0~56.2Nm」 칸(n=10, 30%)에 몰려 있었습니다.',
   'evidence': ['<span class="fact">사실</span> 원인 건수는 14건(UID 042 겹침)이고, twf·hdf 두 원인이 57.1%를 차지합니다(<a href="#fig-r7-1">그림 1</a>).',
                '<span class="fact">사실</span> 한 컬럼 층별에서 2배(26%) 이상인 구간은 마모 상위 28%와 회전 하위 28% 둘뿐입니다(<a href="#tab-r7-2">표 2</a>).',
                '<span class="fact">사실</span> 두 축 불량 분포도에서는 원인 하나가 칸 하나에 모입니다. 마모 상위 × 토크 중간 칸(n=11)의 불량 3건은 모두 twf입니다(<a href="#tab-r7-3">표 3</a>).',
                '<span class="interp">해석</span> 한 축 기준보다 두 축 칸이 원인을 더 날카롭게 가릅니다. 다만 칸마다 n이 10~13이라, 이 결과는 「함께 나타남」의 수준으로 읽습니다.'],
   'fig': ('fig', {'id': 'fig-r7-1', 'cap': '[그림 1] 원인별 파레토 — 원인 건수 기준 (단위: 건, 누적 %)', 'w': 'r7-par', 'alt': 'twf 4, hdf 4, osf 3, pwf 2, rnf 1 막대와 누적 선 28.6, 57.1, 78.6, 92.9, 100%. 80% 점선은 pwf에서 넘는다', 'src': '출처: ai4i_2024_mini.csv (100행), 저자 계산'}),
 },
 'sections': [
  {'id': 'sec-r7-1', 'nav': '들어가며', 'title': '들어가며 — 13%라는 숫자 한 줄', 'blocks': [
    ('memo', 'e08', '불량률 13%. 이 숫자만 들고 현장에 가면 「그래서 어디를요?」라는 질문을 받아요. 오늘은 그 답을 숫자로 적어 봤습니다.'),
    ('p', '7주차 실습은 프롬프트 카드 다섯 장을 AI에 붙여 넣고, 그 답을 데이터로 다시 세는 것입니다. 이 리포트는 다시 센 결과만 모았습니다.'),
    ('p', '답할 질문은 셋입니다. ① 무엇이 많은가(파레토) ② 어느 구간에 몰리는가(층별) ③ 두 조건이 만나는 어느 칸에서 터지는가(불량 분포도).')]},
  {'id': 'sec-r7-2', 'nav': '배경', 'title': '배경 — 원인 라벨 다섯 가지', 'blocks': [
    ('p', 'AI4I 데이터의 machine_failure 뒤에는 원인 라벨 다섯이 있습니다. 공구 마모(twf), 열 방출(hdf), 전력(pwf), 과부하(osf), 무작위(rnf)입니다. 원래 데이터 설명에 따르면 각 원인은 특정 측정값 조합과 묶여 있습니다.'),
    ('p', '그래서 원인마다 「함께 볼 컬럼」이 다릅니다. twf는 마모, hdf는 온도차와 회전, pwf는 토크와 회전, osf는 마모와 토크입니다. 불량 분포도의 세 조합은 여기서 골랐습니다.'),
    ('memo', 'e09', '평균 불량률은 원인 다섯을 한 그릇에 섞은 값이에요. 섞기 전 재료를 따로 보면 맛이 다 다르죠.')]},
  {'id': 'sec-r7-3', 'nav': '방법', 'title': '방법 — 세기 → 파레토 → 층별 → 불량 분포도', 'blocks': [
    ('table', {'id': 'tab-r7-1', 'cap': '<표 1> 분석 규칙 (출처: 7주차 실습 가이드 카드 01~05)', 'head': ['단계', '규칙'],
               'rows': [['세기', '행 수 · 불량 수 · 원인별 건수 · 겹친 행 · 원인 없는 불량'], ['파레토', '원인 건수 내림차순, 분모 = 원인 건수 합계(14), 80% 기준선'], ['층별', '같은 행 수 4구간(1,000행 데이터는 5구간), 2배 이상 = 몰린 구간, n < 10은 표본 부족'], ['불량 분포도', '두 축 각 3구간(3×3), 칸마다 불량률·n, n < 5 칸은 조건 문장에서 제외'], ['검증', '조건 문장을 필터로 다시 걸어 UID·n·불량 수를 재집계']],
               'src': '구간 경계는 선형 보간 분위수, 경계값 포함은 아래 구간 (pandas qcut과 같음)'}),
    ('p', '계산 코드는 저장소 analysis/w07_defect_map.py에 있습니다. 본문 7.7~7.12의 위젯도 같은 규칙으로 페이지 안에서 다시 셉니다.'),
    ('memo', 'e07', '분모 하나를 조심했어요. 파레토는 불량 부품 13이 아니라 원인 건수 14로 나눕니다.')]},
  {'id': 'sec-r7-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3 id="sec-r7-4-1">결과 1 · 무엇이 많은가 — 두 원인이 절반 이상</h3>'),
    ('p', '<span class="fact">사실</span> 100행 중 불량 13행(13.0%)입니다. 원인 건수는 twf 4 · hdf 4 · osf 3 · pwf 2 · rnf 1로 합 14입니다. UID 042가 hdf와 osf를 함께 가지며, 원인 없는 불량은 없습니다(<a href="#fig-r7-1">그림 1</a>).'),
    ('p', '<span class="interp">해석</span> 파레토 모양은 「큰 막대 두세 개」형입니다. 80%는 네 번째 원인(pwf)에서 넘으니, 핵심 소수가 둘로 딱 떨어지지는 않습니다.'),
    ('html', '<h3 id="sec-r7-4-2">결과 2 · 어느 구간에 몰리는가 — 한 축으로 보면</h3>'),
    ('fig', {'id': 'fig-r7-2', 'cap': '[그림 2] 네 컬럼의 4구간 불량률 (단위: %, 점선 = 전체 13.0%)', 'w': 'r7-strat', 'alt': '마모·토크·회전·온도차 각 4구간 불량률. 마모 상위 28, 회전 하위 28이 26% 기준을 넘고, 온도차 하위 24, 토크 하위 20은 미달', 'src': '출처: ai4i_2024_mini.csv, 저자 계산'}),
    ('table', {'id': 'tab-r7-2', 'cap': '<표 2> 4구간 층별 결과 (각 구간 n=25, 불량률 %)', 'head': ['컬럼', '하위', '중하위', '중상위', '상위', '판정'],
               'rows': [['tool_wear_min (경계 23.6 · 50.9 · 74.0)', '16', '0', '8', '<b>28</b>', '상위 몰림'], ['rotational_speed_rpm (1,438.6 · 1,450.3 · 1,467.9)', '<b>28</b>', '4', '8', '12', '하위 몰림'], ['temp_diff (24.6 · 31.0 · 37.8)', '24', '8', '16', '4', '하위 경계(1.85배)'], ['torque_nm (47.5 · 49.4 · 51.5)', '20', '8', '12', '12', '하위 경계(1.54배)']],
               'src': '출처: 저자 계산 (analysis/w07_defect_map.py)'}),
    ('p', '<span class="fact">사실</span> 2배 기준(26%)을 넘는 구간은 마모 상위와 회전 하위 둘입니다. 원자료 참고 답은 온도차 하위 24%도 몰린 구간으로 적었지만, 이 리포트는 기준대로 경계 사례로 바꿉니다.'),
    ('html', '<h3 id="sec-r7-4-3">결과 3 · 두 축이 만나는 칸 — 원인이 칸으로 갈린다</h3>'),
    ('fig', {'id': 'fig-r7-3', 'cap': '[그림 3] 불량 분포도 (나) 회전 × 온도차, 3×3 (칸 = 불량/n)', 'w': 'r7-heat', 'alt': '회전 하위 × 온도차 하위 칸이 5/13 = 38%로 가장 진하다. 나머지 칸은 0~21%', 'src': '출처: ai4i_2024_mini.csv, 저자 계산'}),
    ('table', {'id': 'tab-r7-3', 'cap': '<표 3> 조합별 주요 칸과 그 칸의 불량 UID (3×3)', 'head': ['지도 · 칸', '불량/n', '불량률', '불량 UID (원인)'],
               'rows': [['(나) 회전 1,418~1,443 × 온도차 6.6~26.8', '5/13', '<b>38%</b>', '042 (hdf+osf) · 057 (twf) · 058 · 068 · 092 (hdf)'], ['(가) 마모 67.9~117.1 × 토크 51.0~56.2', '3/10', '30%', '042 · 050 · 085 (모두 osf)'], ['(가) 마모 67.9~117.1 × 토크 48.0~51.0', '3/11', '27%', '049 · 052 · 053 (모두 twf)'], ['(가) 마모 2.1~31.5 × 토크 42.8~48.0', '2/5', '40%', '068 (hdf) · 070 (pwf) — 2건짜리 칸'], ['(다) 회전 1,418~1,443 × 토크 48.0~51.0', '3/11', '27%', '049 · 053 (twf) · 058 (hdf)']],
               'src': '출처: 저자 계산 · 검증: 조건 문장을 필터로 다시 걸어 UID·n 일치 확인'}),
    ('p', '<span class="fact">사실</span> hdf 4건(042, 058, 068, 092)은 모두 (나)의 한 칸에 있습니다. osf 3건은 모두 마모 상위 × 토크 상위 칸에, 그 옆 토크 중간 칸의 불량 3건은 모두 twf입니다.'),
    ('key', '한 축 층별의 「마모 상위 28%」는 사실 두 원인이 섞인 값이었습니다. 토크를 겹치니 twf 칸과 osf 칸으로 갈라졌습니다.'),
    ('memo', 'e04', '이게 오늘 제일 재미있는 장면이에요. 같은 「마모가 높다」도 토크가 중간이면 공구 마모, 토크가 크면 과부하였어요.'),
    ('html', '<h3 id="sec-r7-4-4">결과 4 · 다른 공장 — 불량 판정 데이터</h3>'),
    ('fig', {'id': 'fig-r7-4', 'cap': '[그림 4] 판재 1,000장의 측정값 5구간 불량률 (단위: %, 점선 = 전체 3.3%)', 'w': 'r7-d2', 'alt': '네 측정값의 5구간 불량률. 최고는 거칠기 상위 6.1%로 2배(6.6%)에 미달', 'src': '출처: 불량품_판정_데이터.csv (1,000행), 저자 계산'}),
    ('p', '<span class="fact">사실</span> abnormal 33장(3.3%)입니다. 5구간 중 최고는 거칠기 상위(3.42µm 초과) 6.1%(12/198)로 1.8배이고, 2배(6.6%)를 넘는 구간은 없습니다. 원자료 참고 답의 「6.0% (n=201), 2배 이상」은 이 리포트에서 「6.1% (n=198), 경계 사례」로 바꿉니다.'),
    ('p', '<span class="interp">해석</span> 5구간으로는 신호가 흐려집니다. 거칠기를 더 잘게 보면 상위 5%(4.32µm 초과, 50장)에 9장(18%)이 몰려 있습니다. 「몇 µm부터 위험한가」는 8주차 주제 카드 예시의 질문으로 넘깁니다.')]},
  {'id': 'sec-r7-5', 'nav': '반론', 'title': '반론과 다른 설명 — 100행의 우연', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 100행에서 4컬럼 × 4구간 = 16개 구간을 보면, 우연만으로도 28%짜리 구간이 나올 수 있다. 맞습니다. 불량 라벨 13개를 무작위로 섞어 2만 번 다시 나눠 보니, 16개 구간 중 하나 이상이 7/25(28%) 이상이 된 경우가 약 24%였습니다.'),
    ('p', '<span class="interp">해석</span> 그래서 한 축 층별의 「몰린 구간」 하나만으로는 약한 증거입니다. 반면 (나) 지도에서 한 칸에 불량 5건 이상이 모이는 경우는 무작위 섞기에서 약 6%였고, 그 칸의 불량이 같은 원인(hdf)으로 채워진 점까지 겹치면 우연으로 보기 어렵습니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 구간 경계를 바꾸면 칸이 달라진다. 맞습니다. 4×4로 나누면 (나) 최고 칸은 50%(4/8)가 되고, 많은 칸이 n < 5가 됩니다. 이 리포트는 100행에 맞춰 3×3을 기준으로 삼았습니다.'),
    ('p', '<span class="guess">추측</span> osf 3건의 「마모 × 토크」 값은 5,331~5,487로 비슷합니다. 하지만 이 값이 5,661인 양품도 있어, 곱 하나로 가르는 문턱은 이 데이터에서 확인되지 않습니다. 「왜」는 9주차에서 확인합니다.'),
    ('memo', 'e09', '무작위로 섞어 보는 건 「우연이었다면 얼마나 자주 이런 모양이 나오나」를 묻는 방법이에요. 9주차에 검정으로 다시 다룹니다.')]},
  {'id': 'sec-r7-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 세 장(원인 순위표 · 구간표 · 불량 분포도)이 이어지며, 한 축에서 섞여 있던 원인이 두 축 칸에서 갈라지는 것을 숫자로 확인했습니다. 조건 문장 세 줄은 필터 재집계로 모두 검증했습니다.'),
    ('p', '한계: ① 100행 수업용 미니판이라 칸마다 n이 10~13입니다 ② 라인·교대·날짜 열이 없어 공정 층별은 못 했습니다 ③ 원인 라벨은 주어진 값이고, 「왜」는 확인하지 않았습니다 ④ 불량 판정 데이터는 원인 라벨이 없습니다.'),
    ('table', {'id': 'tab-r7-4', 'cap': '<표 4> 원자료 참고 답과 다른 값 (이 리포트에서 바꾼 것)', 'head': ['항목', '원자료', '이 리포트'],
               'rows': [['카드 03 온도차 하위', '24% — 몰린 구간', '24% — 경계 사례 (26% 미달)'], ['카드 04 거칠기 상위', '6.0% (n=201) — 2배 이상', '6.1% (12/198) — 1.8배, 경계 사례'], ['그림 7-4 세 칸', '14% n=14 · 7% n=15 · 15% n=13', '12.5% n=16 · 5.9% n=17 · 16.7% n=12'], ['조건 문장 (나)', '24–28% (n=25)', '38% (n=13) — 지도 칸 값'], ['조건 문장 (다)', '실측 후 채운다', '27% (n=11)']],
               'src': '출처: 7주차 교안·실습 가이드, 저자 재집계'}),
    ('prompt', '#역할\n너는 기어 가공 라인의 품질 분석가다.\n#맥락\n첨부한 ai4i_2024_mini.csv(100행)를 쓴다. 원인 라벨은 twf·hdf·pwf·osf·rnf.\n#조건\n구간은 같은 행 수로 나누고 경계값 포함은 아래 구간. n<5 칸은 조건 문장에서 뺀다.\n#형식\n① rotational_speed_rpm × temp_diff 3×3 히트맵(칸마다 불량/n) ② 최고 칸 조건 문장 ③ 그 칸의 불량 UID와 원인 라벨\n#검수 기준\n최고 칸은 회전 1,418~1,443rpm × 온도차 6.6~26.8K, 5/13 = 38%여야 한다. 다르면 경계값과 필터를 보여 달라.'),
    ('memo', 'e07', '마지막 「검수 기준」 줄, 이번에도 붙였죠? 칸의 UID까지 맞으면 그 지도는 믿어도 됩니다.'),
    ('p', '다음 편 예고: 8주차는 중간 점검입니다. 이 세 장을 꺼내 놓고 각자의 보고서 질문 한 줄을 정합니다. 「왜 터지는가」는 9주차 「불량 분석 ②」에서 이어 갑니다.')]},
 ],
 'refs': ['ai4i_2024_mini.csv — UCI AI4I 2020 Predictive Maintenance Dataset을 바탕으로 한 수업용 100행 미니판', '불량품_판정_데이터.csv — 교육용 가상 데이터 1,000행', 'S. Matzka, "Explainable Artificial Intelligence for Predictive Maintenance Applications", Third International Conference on Artificial Intelligence for Industries (AI4I), 2020', '안상선, 스마트 제조 7주차 강의 교안·실습 가이드, 2026', '이 저장소 analysis/w07_defect_map.py — 저자 계산'],
 'sources': [('원자료', 'ai4i_2024_mini.csv · 불량품_판정_데이터.csv'), ('계산', '저자 계산 (analysis/w07_defect_map.py)')],
 'notes': '무작위 섞기 비율(약 24%, 약 6%)은 2만 번 시뮬레이션 값이라 다시 돌리면 소수점 아래가 조금 달라집니다.',
}
RP['js'] = _DATA + _JS + r'''
W['r7-par']=function(s){var F=A7.filter(function(r){return r.f}),D=CS.map(function(c,i){return [c,F.filter(function(r){return r.m>>i&1}).length]}).sort(function(a,b){return b[1]-a[1]||(a[0][0]=='rnf')-(b[0][0]=='rnf')}),cum=0,tot=14;var r=Chart.line(s,{labels:D.map(function(d){return d[0][0]}),series:[{name:'누적 비율(%)',color:'#5ee39c',values:D.map(function(d){cum+=d[1];return cum/tot*100}),dots:true},{name:'원인 건수 ×10',color:'#f1b646',values:D.map(function(d){return d[1]*10}),dash:'2 3',dots:true}],ref:80,min:0,max:100,h:240});};
W['r7-strat']=function(s){var K=['wr','tq','rpm','td'];Chart.bars(s,{labels:['하위','중하위','중상위','상위'],series:K.map(function(k,i){return {name:COL7[k][1],color:['#f1b646','#82b8ff','#f0604d','#d672d6'][i],values:strat(A7,k,4).map(function(x){return x.r*100})}}),ref:13,min:0,max:32,h:250});};
W['r7-heat']=function(s){var g=grid('rpm','td',3),NS='http://www.w3.org/2000/svg';s.setAttribute('viewBox','0 0 640 260');s.setAttribute('class','chart');s.innerHTML='';function el(t,a,txt){var e=document.createElementNS(NS,t);for(var q in a)e.setAttribute(q,a[q]);if(txt!=null)e.textContent=txt;s.appendChild(e);return e;}el('text',{x:10,y:16},'회전(rpm) ↓  ×  온도차(K) →');g.G.forEach(function(row,a){el('text',{x:10,y:70+a*62},rng7(a,a+1,g.ex,0));row.forEach(function(c,b){var r=c.n?c.b/c.n:0,v=Math.min(1,r/.45);if(a==0)el('text',{x:200+b*140+65,y:34,'text-anchor':'middle'},rng7(b,b+1,g.ey,1));el('rect',{x:200+b*140,y:42+a*62,width:132,height:56,rx:4,fill:'rgb(255,'+Math.round(245-120*v)+','+Math.round(235-200*v)+')'});el('text',{x:200+b*140+66,y:42+a*62+33,'text-anchor':'middle',style:'fill:#111;font-weight:700'},(r*100).toFixed(0)+'%  ('+c.b+'/'+c.n+')');});});};
W['r7-d2']=function(s){var K=Object.keys(COLD);Chart.bars(s,{labels:['1','2','3','4','5'],series:K.map(function(k,i){return {name:COLD[k][1],color:['#82b8ff','#f1b646','#d672d6','#9aa5aa'][i],values:strat(D7R,k,5).map(function(x){return x.r*100})}}),ref:3.3,min:0,max:7,h:240});};
'''
