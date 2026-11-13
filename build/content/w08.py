# 8주차 · 중간 점검 — 보고서 주제 카드 (질문 한 줄 · 다섯 조건 · 여섯 칸 · 신호등)
import os, json
_H = os.path.dirname(__file__)
_DATA = open(os.path.join(_H, '..', 'data_w07.js'), encoding='utf-8').read()

def _p(t):
    return '<div class="prompt" data-raw="' + t.replace('&', '&amp;').replace('"', '&quot;') + '">' + t.replace('&', '&amp;').replace('<', '&lt;') + '</div>'

TIDY = '''[역할] 당신은 제조 데이터 분석 수업의 조교다. 한국어로 짧게 답한다.
[입력] 아래는 내가 쓴 보고서 주제 카드 초안이다.
(여기에 01~06 칸을 붙여 넣는다)
[할 일]
1) 다음 다섯 조건 각각에 '예/아니오'와 이유 한 줄을 적는다.
   ① 질문 한 줄 ② 데이터가 있다 ③ 수업 도구로 풀린다 ④ 10일 안에 끝난다 ⑤ 검토할 거리가 있다
2) '아니오'인 조건마다 고칠 문장 하나를 제안한다.
3) 질문을 더 좁힌 버전 2개를 제안한다.
[주의] 주제를 새로 바꾸지 말고 내 초안을 다듬는 데만 집중한다.'''

CH = {
 'slug': 'w08', 'num': '08',
 'title': '중간 점검 — 보고서 주제 카드',
 'eyebrow': '8주차 · 중간 점검 · SMT 전자부품 실장 라인',
 'desc': '스마트 제조 8주차 중간 점검 — 1~7주의 도구를 「무엇을 물을 수 있는가」로 다시 묶고, 좋은 주제의 다섯 조건으로 후보를 거른 뒤, 주제 카드 여섯 칸을 채워 신호등 검토를 받습니다.',
 'q': '배운 도구는 많다. 내 보고서는 무엇 하나를 묻는가?',
 'lead': '새 개념은 없습니다. 손에 든 도구로 내 질문 한 줄을 정하는 회차입니다. 주제가 넓으면 10일 안에 끝나지 않고, 좁으면 검토할 거리가 없습니다. 오늘의 산출물은 검토받은 주제 카드 한 장입니다.',
 'scene_alt': 'SMT 전자부품 실장 라인 3D. PCB 투입, 솔더 인쇄, 부품 실장 로봇, 리플로 오븐, AOI 검사, 포장 순서로 기판이 흐른다. 벽에는 주제 카드 여섯 칸 게시판이, 옆에는 초록·노랑·빨강 신호등 탑이 서 있다.',
 'scene_hud': '3D · SMT 실장 라인 — 신호등 버튼으로 검토 판정을 바꿔 보세요',
 'scene_opts': {'cam': [0, 15, 26], 'target': [-1, 2, -2]},
 'kpis': [('1장', '주제 카드 · 여섯 칸', 'g'), ('5개', '좋은 주제의 조건', 'a'), ('10일', 'Take home 제출 기한', 'm'), ('40%', '중간 보고서 비중 · 개인 과제', 'r')],
 'hero_talk': [
   ('doc', 'e08', '오늘 공장은 전자부품 SMT 라인입니다. 그리고 오늘은 중간 점검, 각자 보고서 주제를 카드 한 장으로 정하는 날이에요.'),
   ('robo', 'e19', '제 주제는 「AI로 스마트 팩토리 혁신하기」입니다! 크게 가야죠!'),
   ('fly', 'e09', '그건 분야지 주제가 아니야. 10일 안에 끝나?'),
   ('asst', 'e12', '질문 한 줄부터 정하고, 신호등을 받아 볼게요!'),
 ],
 'three': ['1~7주의 도구를 다시 펼쳐, 내 공정에 던질 질문 한 줄과 데이터·방법·산출물·검증·90일 연결을 주제 카드 한 장에 적습니다.',
           '질문이 정해지면 도구는 따라옵니다. 순서를 바꾸면 보고서가 아니라 연습장이 됩니다.',
           '업무에서는 「거칠기 몇 µm부터 불량률이 2배인가?」 같은 질문 한 줄이 개선 과제의 첫 문장이 됩니다.'],
 'abbr': [('OEE', 'Overall Equipment Effectiveness', '설비 종합 효율 — 가동률 × 성능 × 양품률'), ('SMT', 'Surface Mount Technology', '표면 실장 — 기판 위에 부품을 올려 납땜'),
          ('AOI', 'Automated Optical Inspection', '자동 광학 검사'), ('Take home', 'take-home exam', '집에서 수행해 기한 안에 내는 과제형 시험')],
 'why': [('주제가 넓으면', '「스마트 팩토리 도입」은 10일 안에 끝나지 않습니다. 결과가 흐려 검토할 수도 없습니다.'),
         ('주제가 없으면', '「파레토를 해 보고 싶다」는 도구가 먼저입니다. 보고서가 아니라 연습장이 됩니다.'),
         ('검토가 배점의 중심', '강의계획서: 코드의 작동은 보장되지 않으며, 코멘트·검토 사항이 포함된다.')],
 'big_lead': '네 단계로 갑니다. 끝나면 신호등이 켜진 카드 한 장이 남습니다.',
 'big': [('① 되짚기 (8.1~8.3)', '일곱 주 일곱 질문 · 도구 상자 여섯 칸 · 질문이 먼저'), ('② 주제 고르기 (8.4~8.7)', '다섯 조건 · 좁히기 사다리 · 예시와 고쳐 쓰기 · AI 활용 원칙'),
         ('③ 주제 카드 (8.8~8.9)', '다 채운 예시를 숫자로 확인 · 내 카드 쓰기 · 다듬기 프롬프트'), ('④ 검토 (8.10~8.11)', '신호등 판정 · 제출 안내와 10일 진행표')],
 'glossary': {
   '주제 카드': ['주제 카드', '산출물', '질문 · 데이터 · 방법 · 산출물 · 검증 · 90일 연결, 여섯 칸을 A4 반 장(슬라이드 1장)에 적은 것입니다.'],
   '신호등': ['신호등 판정', '검토', '초록 = 그대로 간다, 노랑 = 좁혀서 간다, 빨강 = 다시 고른다. 성적이 아니라 주제 방향에 대한 판정입니다.'],
   '좁히기': ['좁히기 사다리', '방법', '분야 → 영역 → 문제 → 질문. 대상 · 지표 · 범위 세 손잡이로 한 칸씩 내려갑니다.'],
   '90일': ['90일 연결', '현장 적용', '이 결과로 현장에서 90일 안에 할 첫 행동 한 줄. 동사 + 대상 + 시한으로 씁니다.'],
 },
 'subs': [
  {'id': 'sec-8-1', 'title': '일곱 주 — 일곱 개의 질문', 'tags': ['되짚기: 1~7주', '도구를 「물을 수 있는 것」으로'],
   'body': ['앞 회차들을 「무엇을 물을 수 있는가」로 다시 묶어 봅니다. 주차마다 공장이 달랐듯, 던질 수 있는 질문도 달랐습니다. 일곱 개의 질문 중 하나를 내 공정에 옮겨 묻는 것이 오늘의 일입니다.'],
   'talk': [('sia', 'e07', '사출, 하네스, 빙과, 판재, CNC, 면류, 기어, 그리고 오늘 SMT. 공장이 여덟 개째예요.'), ('moa', 'e12', '주차별로 「남은 것」을 모아 왔어요. 버튼을 눌러 보세요!'), ('x1', 'e04', '(오)')],
   'widget': ('w8-map', '<div class="ptitle">표 8-1 · 앞 회차 지도 (주차를 누르세요)</div><div class="ctrl" id="m8-bt"></div><div class="insight" id="m8-out" aria-live="polite"></div>'),
   'limit': '4~6주는 교안에서 한 묶음(데이터로 말 걸기 · 작업지시서와 한 페이지 앱 · REVIEW)으로 정리됩니다.',
   'quiz': [{'q': '「불량은 어디에 몰리는가」를 물을 수 있게 해 준 주차는?', 'o': ['3주', '5주', '7주'], 'a': 2, 'why': '7주 불량 분석 ①의 원인 순위표·구간표·자리 지도입니다.'}]},

  {'id': 'sec-8-2', 'title': '도구 상자 여섯 칸 — 학습 목표와 짝을 맞춘다', 'tags': ['학습 목표 ①~⑥', '약속: 두 칸 이상 잇기'],
   'pair': ('일상으로 치면', '공구함에 드라이버만 있으면 고칠 수 있는 게 적습니다. 두세 가지를 이어 쓸 때 일이 끝납니다.',
            'SMT 라인에서는', 'AOI 불량 데이터를 이해하고(①) AI로 집계해(②) 차트로 보이고(③) 품질보고서로 묶으면(④) 보고서 한 편입니다.'),
   'body': ['도구 상자는 학습 목표 여섯 칸입니다. ① 데이터 이해 ② AI 분석 ③ 시각화 ④ 문서 자동화 ⑤ 공정 자동화 ⑥ 현장 적용. 보고서는 여섯 칸 중 둘 이상을 이어 쓰면 단단해집니다.',
            '오늘은 학습 목표 ⑥ 「현장 적용」의 첫 단추를 끼우는 회차이기도 합니다. 카드의 마지막 칸이 「90일 연결」인 이유입니다.'],
   'talk': [('robo', 'e19', '여섯 칸 전부 쓰겠습니다! 풀코스!'), ('fly', 'e09', '10일이야. 둘이나 셋이면 충분해.'), ('asst', 'e07', '쓸 칸을 골라 보면 몇 칸인지 세어 줄게요.')],
   'widget': ('w8-tools', '<div class="ptitle">고르기 · 내 보고서가 쓸 칸</div><div class="ctrl" id="tl-bt"></div><div class="eq" id="tl-out" aria-live="polite"></div>'),
   'limit': '칸 수가 많을수록 좋은 보고서는 아닙니다. 10일 안에 끝나는지가 먼저입니다.',
   'quiz': [{'q': '보고서를 단단하게 만드는 칸 수의 약속은?', 'o': ['한 칸에 집중', '두 칸 이상 이어 쓰기', '여섯 칸 모두'], 'a': 1, 'why': '두 칸 이상을 이으면 결과가 문서·행동으로 이어집니다.'}]},

  {'id': 'sec-8-3', 'title': '질문이 먼저다 — 질문 → 데이터 → 도구', 'tags': ['순서: 질문 → 데이터 → 도구', '함정: 도구가 먼저'],
   'body': ['「파레토를 해 보고 싶다」로 시작하면 도구가 먼저입니다. 「우리 라인 불량은 어디에 몰리는가」로 시작하면 질문이 먼저입니다. 질문이 정해지면 도구는 따라옵니다.',
            '이 순서를 바꾸지 않습니다. 도구부터 고르면 결과가 질문에 답하지 않고, 검토할 기준도 사라집니다.'],
   'talk': [('robo', 'e07', '최신 딥러닝 모델부터 고르고 데이터를 찾겠습니다!'), ('fly', 'e03', '그게 도구가 먼저인 대표 사례야.'), ('sia', 'e10', '아래 문장들을 질문 먼저 / 도구 먼저로 나눠 보세요.')],
   'widget': ('w8-order', '<div class="ptitle">분류 · 이 문장은 질문이 먼저인가?</div><div id="od-box"></div><div class="eq" id="od-out" aria-live="polite"></div>'),
   'limit': '도구 이름이 들어 있어도 물음표로 끝나는 질문이 먼저 있으면 「질문 먼저」입니다.',
   'quiz': [{'q': '보고서를 시작하는 순서는?', 'o': ['도구 → 데이터 → 질문', '질문 → 데이터 → 도구'], 'a': 1, 'why': '질문이 정해지면 데이터와 도구가 따라옵니다.'}]},

  {'id': 'sec-8-4', 'title': '좋은 주제의 다섯 조건 — 하나라도 비면 다시 고른다', 'tags': ['표 8-2', '판정: 다섯 칸 모두 「예」'],
   'body': ['<div class="tw"><table class="tb"><tr><th>#</th><th>조건</th><th>한 줄 기준</th><th>점검 질문</th></tr>'
            '<tr><td>1</td><td>질문 한 줄</td><td>물음표로 끝나는 한 문장</td><td>한 숨에 읽히는가?</td></tr>'
            '<tr><td>2</td><td>데이터가 있다</td><td>지금 손에 있는 파일 — 수업·공개·현장(익명화)</td><td>파일 이름을 지금 말할 수 있는가?</td></tr>'
            '<tr><td>3</td><td>수업 도구로 풀린다</td><td>앞 회차 도구 중 둘 이상</td><td>어느 주차의 카드를 쓰는가?</td></tr>'
            '<tr><td>4</td><td>10일 안에 끝난다</td><td>Take home 기한 안에 실행·검토까지</td><td>하루 몇 시간씩 며칠인가?</td></tr>'
            '<tr><td>5</td><td>검토할 거리가 있다</td><td>코멘트·한계·근거(논문·교과서)를 쓸 수 있다</td><td>결과가 틀렸다면 어떻게 알 수 있는가?</td></tr></table></div>',
            '과제에는 코드·실행 결과뿐 아니라 코멘트·검토 사항이 들어갑니다. 조건 5가 바로 그 자리입니다.'],
   'talk': [('asst', 'e07', '후보 주제를 골라 다섯 조건을 하나씩 눌러 볼게요.'), ('robo', 'e16', '제 주제도 넣어 주세요…'), ('fly', 'e10', '좋아. 다섯 칸이 몇 개 켜지는지 보자.')],
   'widget': ('w8-five', '<div class="ptitle">점검 · 후보 주제를 다섯 조건으로 거르기</div><div class="ctrl" id="fv-cand"></div><div class="ctrl" id="fv-bt"></div><div class="eq" id="fv-out" aria-live="polite"></div>'),
   'limit': '후보 주제의 예/아니오는 이 페이지의 판단 예시입니다. 실제 판정은 강사 검토에서 받습니다.',
   'quiz': [{'q': '「데이터가 있다」의 기준은?', 'o': ['구할 예정인 파일', '지금 손에 있고 이름을 말할 수 있는 파일'], 'a': 1, 'why': '「구할 예정」은 자주 비는 칸의 대표입니다.'}]},

  {'id': 'sec-8-5', 'title': '좁히기 사다리 — 「스마트 팩토리 도입」은 분야다', 'tags': ['방법: 대상 · 지표 · 범위', '분야 → 영역 → 문제 → 질문'],
   'why': {'problem': '처음 떠오르는 주제는 대개 분야 이름입니다. 「스마트 팩토리」 「불량」 「AI」.',
           'limit': '분야로는 데이터 파일도, 방법도, 끝나는 날도 정할 수 없습니다.',
           'solve': '사다리를 한 칸씩 내려갑니다. 분야 → 영역 → 문제 → 질문. 손잡이는 셋, 대상(라인·제품·설비) · 지표(불량률·생산량·OEE) · 범위(기간·구간)입니다.',
           'easy': '「여행 가고 싶다」를 「11월 둘째 주말, 부산, 1박」으로 바꾸면 예약이 됩니다.'},
   'body': ['사다리 맨 아래 칸이 보고서의 첫 문장입니다. 예를 들면 분야 「스마트 팩토리」 → 영역 「품질 관리」 → 문제 「불량이 특정 조건에서 몰린다」 → 질문 「공구 마모 몇 분 이후 불량률이 전체의 2배를 넘는가?」입니다.'],
   'talk': [('robo', 'e14', '사다리를 내려가니 제 주제가 점점 작아집니다…'), ('fly', 'e10', '작아진 게 아니라 끝낼 수 있게 된 거야.'), ('x2', 'e09', '(…)')],
   'widget': ('w8-lad', '<div class="ptitle">만들기 · 세 손잡이로 질문 한 줄</div><div class="ctrl"><span class="glabel">대상</span><select id="ld-a"></select></div><div class="ctrl"><span class="glabel">지표</span><select id="ld-b"></select></div><div class="ctrl"><span class="glabel">범위</span><select id="ld-c"></select></div><div class="insight" id="ld-out" aria-live="polite"></div>'),
   'limit': '사다리가 만든 문장은 출발점입니다. 숫자 기준(2배, 몇 분 등)은 데이터를 본 뒤 고칩니다.',
   'quiz': [{'q': '좁히는 세 손잡이가 아닌 것은?', 'o': ['대상', '지표', '모델 이름', '범위'], 'a': 2, 'why': '모델 이름은 도구입니다. 질문이 정해진 뒤에 고릅니다.'}]},

  {'id': 'sec-8-6', 'title': '예시 여섯 개와 나쁜 주제 고쳐 쓰기', 'tags': ['예시: 학습 목표마다 하나', '고쳐 쓰기 네 가지'],
   'body': ['학습 목표마다 예시 주제가 하나씩 있습니다. ① 라인별 불량률과 OEE는 어떻게 다른가? ② 네 측정값 중 어느 구간에 불량이 몰리는가? ③ 판매량의 계절 패턴을 1페이지로 보여줄 수 있는가? ④ 분류 결과를 받아 작업지시서를 만드는 표준 프롬프트는? ⑤ 측정 → 판정 → 지시서 → 발송까지 한 흐름을 만들 수 있는가? ⑥ 불량 1순위 원인을 90일 안에 줄이는 실행계획은?',
            '예시를 그대로 쓰지 말고, 대상 · 지표 · 범위를 바꿔 내 것으로 만듭니다. 고친 주제에는 데이터 이름과 숫자 기준이 들어 있습니다.'],
   'talk': [('moa', 'e09', '나쁜 주제 카드를 뒤집으면 고친 주제가 나와요.'), ('robo', 'e16', '「AI로 제조업 혁신하기」… 제 거네요.'), ('doc', 'e07', '뒤집어 보세요. 고친 문장은 7주 결과에서 나왔습니다.')],
   'widget': ('w8-fix', '<div class="ptitle">고쳐 쓰기 · 나쁜 주제 네 장 (눌러서 뒤집기)</div><div class="toc" id="fx-box" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))"></div>'),
   'limit': '고친 주제도 예시입니다. 자기 공정(익명화) 데이터로 바꿔 쓰면 더 좋습니다.',
   'quiz': [{'q': '「불량률이 높은 이유」의 문제는?', 'o': ['너무 좁다', '검토할 기준(숫자·구간)이 없다'], 'a': 1, 'why': '「마모 구간별 불량률, 교체 기준 몇 분」처럼 기준을 넣어 고칩니다.'}]},

  {'id': 'sec-8-7', 'title': 'AI 활용 원칙 — AI는 써도 된다, 검토는 내가 한다', 'tags': ['강의계획서의 약속', '세 가지: 다시 세기 · 프롬프트 기록 · 한계 문단'],
   'body': ['생성형 AI 활용은 무방합니다. 다만 생성한 코드의 작동은 보장되지 않고, 과제에는 코멘트·검토 사항과 논문·교과서 참고가 들어가야 합니다.',
            '보고서에서 지킬 것은 셋입니다. ① AI가 준 숫자는 다시 센다 ② 어떤 프롬프트를 썼는지 부록에 남긴다 ③ 결과의 한계를 내 말로 한 문단 쓴다. AI가 만든 답에 내 코멘트가 붙어야 보고서가 됩니다.'],
   'talk': [('asst', 'e04', '7주에 AI가 「45% (n=20)」이라고 했던 칸, 다시 세니 38% (n=13)였죠!'), ('fly', 'e10', '그 한 줄이 검토 사항이야. 배점의 중심이고.'), ('x3', 'e16', '(삐빅)')],
   'widget': ('w8-ai', '<div class="ptitle">점검 · 보고서 부록에 들어갈 세 가지</div><div class="ctrl" id="ai8-bt" style="flex-direction:column;align-items:flex-start"></div><div class="eq" id="ai8-out" aria-live="polite"></div>'),
   'limit': '사내 실데이터는 익명화한 뒤 개인 실습으로만 씁니다. 입력 데이터가 학습에 쓰일 수 있기 때문입니다(1주).',
   'quiz': [{'q': '보고서에서 AI 결과에 반드시 붙는 것은?', 'o': ['AI 모델 이름만', '다시 센 숫자 · 프롬프트 기록 · 내 한계 문단'], 'a': 1, 'why': '검토가 배점의 중심입니다.'}]},

  {'id': 'sec-8-8', 'title': '다 채운 카드 한 장 — 예시를 숫자로 확인한다', 'tags': ['그림 8-1 예시 카드', '데이터: 불량 판정 1,000행'],
   'fx': {'q': '「몇 µm 이상에서 2배를 넘는가?」는 어떻게 답해요? 구간이랑 뭐가 달라요?',
          'school': '부등식과 비율 — 「x ≥ t」인 행만 골라 비율 구하기',
          'eq': '불량률(t) = (거칠기 ≥ t 인 불량 수) ÷ (거칠기 ≥ t 인 행 수) · <b>2배 = 6.6%</b>',
          'rows': [('t를 올리면', '고른 행(n)은 줄고 불량률은 대개 오른다'), ('2배 문턱', '불량률(t)가 처음 6.6%를 넘는 t'), ('n', '문턱 위 행 수 — 작으면 흔들림')],
          'calc': 't = 3.42µm면 201행 중 12건(6.0%), t = 3.6µm면 159행 중 11건(6.9%)으로 처음 2배를 넘습니다. t = 4.2µm면 60행 중 9건(15.0%)입니다.',
          'comment': '7주에는 5구간으로 잘라서 2배가 안 됐는데, 문턱을 옮기니 3.6µm 근처에서 넘네요!'},
   'body': ['<div class="tw"><table class="tb"><tr><th>칸</th><th>예시 카드 (그림 8-1)</th><th>왜 초록인가</th></tr>'
            '<tr><td>01 질문</td><td>표면 거칠기 몇 µm 이상 구간에서 불량률이 전체의 2배를 넘는가?</td><td>질문에 숫자 기준</td></tr>'
            '<tr><td>02 데이터</td><td>불량품_판정_데이터.csv · 1,000행 · surface_roughness_um, nomal_abnormal (+ 보조 3컬럼)</td><td>파일 이름 명시</td></tr>'
            '<tr><td>03 방법</td><td>7주 카드 01(세기) → 카드 04(층별) → 카드 05(지도) · 구간 수 바꿔 보기</td><td>수업 카드 재사용</td></tr>'
            '<tr><td>04 산출물</td><td>구간별 불량률 표 1 · 막대 차트 1 · 히트맵 1 · 조건 문장 1</td><td>무엇을 몇 장</td></tr>'
            '<tr><td>05 검증</td><td>조건 문장을 엑셀 필터로 다시 셈 · 층별 분석 교과서 장 1개 인용</td><td>검증 방법 있음</td></tr>'
            '<tr><td>06 90일</td><td>해당 구간 진입 시 재검사하는 작업지시서 분기 1개 추가</td><td>현장 행동 한 줄</td></tr></table></div>',
            '이 예시 카드의 질문을 실제 데이터로 끝까지 풀어 보면 이렇습니다. 아래에서 문턱을 움직여 보세요. 풀이 전체는 이 주의 실습 리포트에 있습니다.'],
   'talk': [('asst', 'e07', '문턱을 3.0에서 4.5까지 움직여 볼게요.'), ('fly', 'e09', '문턱을 결과 보고 고르면 유리한 숫자만 고르기 쉬워. n도 같이 봐.'), ('doc', 'e10', '그래서 카드의 검증 칸에 「엑셀 필터로 다시 셈」이 있습니다.')],
   'widget': ('w8-thr', '<div class="ptitle">확인 · 거칠기 문턱 t 이상의 불량률 (불량 판정 1,000행, 실측)</div><div class="ctrl"><div class="group"><span class="glabel">문턱 t (µm)</span><input type="range" min="2.0" max="5.0" step="0.05" value="3.6" id="th-t"><span class="val" id="th-v"></span></div></div><div class="cwrap"><svg id="th-svg"></svg></div><div class="eq" id="th-out" aria-live="polite"></div>'),
   'limit': '문턱을 데이터를 본 뒤 고르면 우연한 높이를 고를 수 있습니다. 보고서에는 문턱 후보를 미리 적고, n과 함께 표로 보입니다.',
   'quiz': [{'q': '전체 불량률 3.3%일 때 「2배」 기준은?', 'o': ['5.3%', '6.6%', '33%'], 'a': 1, 'why': '3.3 × 2 = 6.6%입니다.'}]},

  {'id': 'sec-8-9', 'title': '내 주제 카드 쓰기 — 자주 비는 다섯 자리', 'tags': ['표 8-3 여섯 칸', '다듬기 프롬프트'],
   'body': ['카드는 A4 반 장, 또는 슬라이드 1장입니다. 문장은 짧게 씁니다. 5주 작업지시서의 「다섯 칸」과 같은 원리입니다. 여섯 칸이 차면 보고서 목차가 이미 나와 있습니다.',
            '자주 비는 자리는 다섯입니다. ① 질문에 물음표가 없다(「~분석」은 질문이 아니다) ② 데이터가 「구할 예정」이다 ③ 방법이 도구 이름뿐이다 ④ 검증 칸이 「AI가 확인」이다 ⑤ 90일 칸이 「도입 검토」다(동사 + 대상 + 시한으로).',
            '초안은 내가 쓰고, 빈칸 찾기는 AI와 함께 합니다. 조건표를 먼저 주면 AI가 아무 말이나 칭찬하지 않고, 「바꾸지 말고 다듬기」로 내 주제를 지킵니다.',
            _p(TIDY)],
   'talk': [('sia', 'e07', '아래 칸을 채우면 자주 비는 다섯 자리를 바로 점검합니다.'), ('moa', 'e12', '다 채우면 다듬기 프롬프트에 내 카드가 붙어서 나와요. 복사만 하면 돼요!'), ('robo', 'e07', '저도 써 보겠습니다. 이번엔 물음표를 붙여서!')],
   'widget': ('w8-card', '<div class="ptitle">작성 · 내 주제 카드 여섯 칸</div><div id="cd-form"></div><div class="ctrl"><button class="bt" id="cd-ex" type="button">예시 채우기</button><button class="bt" id="cd-clr" type="button">지우기</button></div><div class="eq" id="cd-out" aria-live="polite"></div><div id="cd-pr"></div>'),
   'limit': '입력한 내용은 이 브라우저 화면에만 있고 저장되지 않습니다. 점검은 단어 규칙으로 하는 간단한 검사라, 최종 판단은 검토에서 받습니다.',
   'quiz': [{'q': '90일 칸을 바르게 쓴 것은?', 'o': ['AI 도입 검토', '12월 말까지 2라인 작업지시서에 재검사 분기 1개 추가'], 'a': 1, 'why': '동사 + 대상 + 시한이 들어가야 합니다.'}]},

  {'id': 'sec-8-10', 'title': '신호등 검토 — 초록 · 노랑 · 빨강', 'tags': ['표 8-4 신호등 기준', '검토는 발표가 아니라 상담'],
   'body': ['검토는 네 단계입니다. 카드 제출 → 강사가 한 사람씩 2~3분 읽기 → 신호등 하나와 고칠 곳 한 줄 → 노랑·빨강은 기한 안에 수정본. 개별 발표 과제는 없습니다.',
            '초록은 다섯 조건이 모두 「예」이고 여섯 칸이 다 찬 카드입니다. 바로 실행합니다. 노랑은 조건 한두 개가 약한 카드로, 대개 너무 넓거나 검증 칸이 비었습니다. 고칠 곳 한 줄을 반영해 다시 냅니다. 빨강은 데이터가 없거나 10일 안에 끝날 수 없는 카드입니다. 예시 주제에서 다시 출발합니다.',
            '신호등은 성적이 아닙니다. 주제 방향에 대한 판정이고, 최종 평가는 제출한 보고서로 합니다. 노랑은 실패가 아니라 가장 흔한 출발점입니다.'],
   'talk': [('doc', 'e07', '제가 신호등을 들고 왔습니다. 카드 넷을 판정해 보세요.'), ('robo', 'e14', '제 카드는… 빨강이겠죠.'), ('fly', 'e10', '빨강이면 데이터부터 다시 고르면 돼. 이번 주 안에.')],
   'widget': ('w8-light', '<div class="ptitle">판정 연습 · 카드 넷에 신호등 켜기</div><div id="lt-box"></div><div class="eq" id="lt-out" aria-live="polite"></div>'),
   'limit': '카드 넷은 이 페이지가 만든 예시입니다. 실제 판정 기준은 표 8-4와 강사 검토를 따릅니다.',
   'quiz': [{'q': '노랑 판정을 받았다. 다음 행동은?', 'o': ['주제를 버린다', '고칠 곳 한 줄을 반영해 좁힌 수정본을 낸다'], 'a': 1, 'why': '노랑은 좁혀서 간다는 뜻입니다.'}]},

  {'id': 'sec-8-11', 'title': '중간 보고서 — 제출 안내와 10일 진행표', 'tags': ['개인 단독 · 비중 40%', 'Take home · 10일 이내'],
   'body': ['<div class="tw"><table class="tb"><tr><th>항목</th><th>내용</th></tr>'
            '<tr><td>성격</td><td>개인 단독 실습 과제 — 팀 과제 없음 · 발표 없음</td></tr>'
            '<tr><td>비중</td><td>40%</td></tr>'
            '<tr><td>방식</td><td>Take home — 시험일로부터 10일 이내</td></tr>'
            '<tr><td>제출처</td><td>사이버캠퍼스</td></tr>'
            '<tr><td>포함할 것</td><td>코드 또는 프롬프트 · 실행 결과(표·차트·문서) · 결과에 대한 코멘트·검토 사항 · 참고 문헌</td></tr>'
            '<tr><td>일정·배점 세부</td><td>시험 기간 비대면 안내 때 강사가 배점과 예시를 함께 설명 — 학사 일정에 따라 바뀔 수 있음</td></tr></table></div>',
            '10일은 네 구간으로 나눕니다. 1~2일 데이터 정리(컬럼 확인 · 결측치), 3~5일 분석·시각화(수업 카드 재사용), 6~8일 코멘트·검토(다시 세기 · 한계 · 문헌), 9~10일 정리·제출(부록에 프롬프트 기록). 마지막 이틀은 비워 둡니다. 막히면 이메일로 문의한 뒤 상담합니다.'],
   'talk': [('asst', 'e01', '시험일을 넣으면 10일 진행표를 날짜로 바꿔 줄게요.'), ('moa', 'e12', '마지막 이틀은 비워 두기, 꼭이요!'), ('x1', 'e01', '(반짝)')],
   'widget': ('w8-plan', '<div class="ptitle">진행표 · 시험일부터 10일</div><div class="ctrl"><span class="glabel">시험일</span><input type="date" id="pl-d"></div><div class="tw" id="pl-tb"></div><div class="eq" id="pl-out" aria-live="polite"></div>'),
   'limit': '실제 제출 마감은 학사 일정과 강사 안내를 따릅니다. 이 표는 계획용입니다.',
   'quiz': [{'q': '권장 진행표에서 6~8일에 하는 일은?', 'o': ['데이터 정리', '코멘트·검토 (다시 세기 · 한계 · 문헌)', '제출'], 'a': 1, 'why': '검토 구간을 따로 잡아 두어야 배점의 중심을 채웁니다.'}]},
 ],
 'duel': {
   'q': '10일짜리 보고서, 크게 잡을까 좁게 잡을까?',
   'intro': [('doc', 'e07', '주판봇은 「스마트 팩토리 도입 효과 전체 분석」, 초파리 연구원은 「거칠기 몇 µm부터 불량률 2배인가?」로 갑니다. 하루에 쓸 수 있는 시간을 정하고 10일을 돌려 봅시다.'), ('sia', 'e12', '시작!')],
   'fly': '질문 한 줄, 파일 하나, 카드 셋. 남는 시간은 검토에 쓴다.',
   'robo': '크게 가야 점수도 큽니다! 여섯 칸 전부, 데이터는 구하면서!',
   'widget': 'w8-duel',
   'panel': '<div class="ptitle">시뮬레이션 · 10일 동안 끝나는 일 (작업 시간은 예시값)</div><div class="ctrl"><div class="group"><span class="glabel">하루 작업 시간</span><input type="range" min="1" max="6" step="0.5" value="3" id="du8-h"><span class="val" id="du8-vh"></span></div><button class="bt primary" id="du8-run" type="button">10일 돌려 보기</button></div><div class="kpis" id="du8-k"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('x1', 'e01', '(짝짝)'), ('x2', 'e16', '(끄덕)'), ('x3', 'e01', '(삐빅!)')],
 },
 'summary': {
   'head': ['단계', '오늘 한 일', '손에 남는 것'],
   'rows': [['되짚기', '일곱 주 · 일곱 질문 · 도구 상자 여섯 칸', '내가 쓸 칸 두 개 이상'],
            ['주제 고르기', '다섯 조건 · 좁히기 사다리 · 고쳐 쓰기', '물음표로 끝나는 질문 한 줄'],
            ['주제 카드', '여섯 칸 · 자주 비는 다섯 자리 · 다듬기 프롬프트', 'A4 반 장 카드 1장'],
            ['검토', '신호등 판정 · 고칠 곳 한 줄', '초록 / 노랑 / 빨강과 다음 행동'],
            ['제출', '10일 진행표', '시험일로부터 10일, 마지막 이틀 비우기']],
   'limits': ['후보 주제 판정, 카드 넷 신호등, 대결의 작업 시간은 예시값입니다.',
              '거칠기 문턱 계산은 수업 데이터(가상) 1,000행 실측입니다.',
              '제출 일정·배점은 학사 일정과 강사 안내를 따릅니다.'],
 },
 'outro': [('doc', 'e16', '질문 한 줄이 보고서 한 권이 됩니다. 오늘 받은 신호등 색을 들고, 다음 주에는 고친 카드로 오세요.'),
           ('asst', 'e01', '실습 리포트에 예시 카드의 질문을 끝까지 풀어 뒀어요.'),
           ('fly', 'e10', '9주는 「불량 분석 ② 왜 터지는가」야. 7주의 조건 문장을 「왜」로 잇자.'),
           ('robo', 'e12', '제 카드는 노랑입니다. 좁혀서 다시 내겠습니다!')],
 'sources': [('강의 자료', '스마트 제조 8주차 교안 「중간 점검 — 내 공정에 어떤 질문을 던질까」 · 8주차 워크시트(주제 카드 양식 · 다섯 조건 · 다듬기 프롬프트 · 진행표)'),
             ('강의계획서', '중간고사: 개인 단독 실습 과제 · Take home · 시험일로부터 10일 이내 · 비중 40% · 생성형 AI 활용 무방, 코멘트·검토 사항 포함'),
             ('수업 데이터', '불량품_판정_데이터.csv (1,000행, 교육용 가상 데이터) — 8.8 문턱 계산'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '후보 주제·판정 연습 카드·고쳐 쓴 주제·대결의 작업 시간은 예시입니다. 거칠기 문턱별 불량률은 수업 데이터로 계산했습니다. 6주 본문의 「8주 제안서 다섯 칸」은 8주 교안에서 「주제 카드 여섯 칸」으로 정해졌습니다.',
 'practice': ('practice.html', '예시 카드를 끝까지 — 거칠기 몇 µm부터 위험한가'),
}

_JS = r'''
var D7R=D7.D.map(function(r){return {w:r[0],r:r[1],u:r[2],o:r[3],f:r[4]};});
function thr(t){var S=D7R.filter(function(r){return r.r>=t-1e-9}),b=S.filter(function(r){return r.f}).length;return {n:S.length,b:b,r:S.length?b/S.length:0};}
function sayDoc(mood,html){var v=document.getElementById('verdict');if(!v)return;v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc',mood);s.querySelector('p').innerHTML=html;v.appendChild(s);}
'''

CH['js'] = _DATA + _JS + 'var TIDY8=' + json.dumps(TIDY, ensure_ascii=False) + ';\n' + r'''
W['w8-map']=function(b){var M=[['1주','코딩 없이 생성형 AI로 공장 데이터 분석','이 과목에서 무엇을 만드는가','강의 지도 · 스마트공장 수준'],['2주','생성형 AI의 개념·작동원리','AI는 어떻게 답을 만드는가','토큰·임베딩·LLM 이해 · 5원칙'],['3주','생산실적 추세 분석 — 시계열','생산량은 어떻게 오르내리는가','추세·계절·순환 분해 · 계절지수'],['4주','데이터로 말 걸기 — 분류·회귀','이 부품은 이상인가 · 얼마나 닳았나','분류·회귀 카드 · 정확도의 함정'],['5주','작업지시서와 한 페이지 앱','그래서 무엇을 하나','분기형 지시서 · HTML 앱'],['6주','REVIEW — 면류 종합 사례','다섯 도구를 한 계획표로 엮을 수 있나','시나리오 · 가동률 · 발주 지시서'],['7주','불량 분석 ① 어디서 터지는가','불량은 어디에 몰리는가','원인 순위표 · 구간표 · 자리 지도']],bt=b.querySelector('#m8-bt'),o=b.querySelector('#m8-out');function f(i){bt.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',i==j)});var m=M[i];o.innerHTML='<p><b>'+m[0]+' · '+m[1]+'</b></p><p>던질 수 있는 질문 — <b>'+m[2]+'?</b></p><p>손에 남은 것 — '+m[3]+' · <a href="../w0'+(i+1)+'/index.html">'+m[0]+' 다시 보기</a></p>';}M.forEach(function(m,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=m[0];x.onclick=function(){f(i)};bt.appendChild(x);});f(6);};
W['w8-tools']=function(b){var T=[['① 데이터 이해','생산량 · 불량률 · OEE 읽기'],['② AI 분석','정제 · 집계 · 추세 · 원인분석'],['③ 시각화','자연어로 차트 · 1페이지 대시보드'],['④ 문서 자동화','생산일보 · 품질보고서 · 작업지시서 표준 프롬프트'],['⑤ 공정 자동화','수집 → AI 분석 → 보고서 발송 흐름 1개'],['⑥ 현장 적용','개선 과제 정의 + 90일 실행계획']],on=T.map(function(){return 0}),bt=b.querySelector('#tl-bt'),o=b.querySelector('#tl-out');T.forEach(function(t,i){var x=document.createElement('button');x.className='bt';x.type='button';x.setAttribute('aria-pressed','false');x.title=t[1];x.textContent=t[0];x.onclick=function(){on[i]=1-on[i];x.classList.toggle('on',!!on[i]);x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var n=on.reduce(function(a,c){return a+c},0),sel=T.filter(function(t,i){return on[i]});o.innerHTML='고른 칸 <b>'+n+'개</b>'+(n?' — '+sel.map(function(t){return t[0]+'('+t[1]+')'}).join(' → '):'')+'<br>'+(n<2?'<b style="color:var(--amber)">두 칸 이상을 이어 보세요.</b>':n>3?'<b style="color:var(--amber)">10일에 '+n+'칸은 많습니다. 둘이나 셋으로 줄여 보세요.</b>':'<b style="color:var(--gfp)">좋습니다. 10일 안에 이을 수 있는 크기입니다.</b>');}f();};
W['w8-order']=function(b){var S=[['「파레토를 해 보고 싶다」',0],['「우리 라인 불량은 어디에 몰리는가?」',1],['「딥러닝 모델로 뭔가 해 보자」',0],['「마모 몇 분 이후 불량률이 2배를 넘는가?」',1],['「대시보드를 멋지게 만들자」',0],['「여름 성수기에 비빔면을 몇 교대로 돌려야 하나?」',1]],box=b.querySelector('#od-box'),o=b.querySelector('#od-out'),ans=S.map(function(){return -1});box.innerHTML=S.map(function(s,i){return '<div class="ctrl" style="align-items:center"><span style="min-width:280px">'+s[0]+'</span><button class="bt" data-i="'+i+'" data-v="1" type="button">질문 먼저</button><button class="bt" data-i="'+i+'" data-v="0" type="button">도구 먼저</button></div>'}).join('');box.querySelectorAll('.bt').forEach(function(x){x.onclick=function(){var i=+x.dataset.i,v=+x.dataset.v;ans[i]=v;box.querySelectorAll('.bt[data-i="'+i+'"]').forEach(function(y){y.classList.remove('on','no')});x.classList.add(v==S[i][1]?'on':'no');f();};});function f(){var d=ans.filter(function(a){return a>=0}).length,ok=ans.filter(function(a,i){return a==S[i][1]}).length;o.innerHTML='고른 것 '+d+'/6 · 맞은 것 <b>'+ok+'</b>'+(d==6?(ok==6?' — 완벽합니다. 물음표가 있는 쪽이 질문 먼저입니다.':' — 빨간 칸은 도구 이름으로 시작하는지, 물음표로 끝나는지 다시 보세요.'):'');}f();};
W['w8-five']=function(b){var C=['① 질문 한 줄','② 데이터가 있다','③ 수업 도구로 풀린다','④ 10일 안에 끝난다','⑤ 검토할 거리가 있다'],K=[['주판봇: AI로 스마트 팩토리 혁신하기',[0,0,0,0,0]],['면류 2027 여름 비빔면 교대 계획은?',[1,1,1,1,1]],['딥러닝으로 불량 예측 모델 만들기',[0,1,0,0,1]],['우리 회사 데이터 분석',[0,0,1,1,0]],['마모 구간별 불량률과 교체 기준은 몇 분인가?',[1,1,1,1,1]]],ci=0,on=[0,0,0,0,0],cb=b.querySelector('#fv-cand'),bt=b.querySelector('#fv-bt'),o=b.querySelector('#fv-out');K.forEach(function(k,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=k[0];x.onclick=function(){ci=i;on=[0,0,0,0,0];draw();};cb.appendChild(x);});C.forEach(function(c,i){var x=document.createElement('button');x.className='bt';x.type='button';x.textContent=c;x.onclick=function(){on[i]=1-on[i];draw();};bt.appendChild(x);});function draw(){cb.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',j==ci)});bt.querySelectorAll('.bt').forEach(function(x,j){x.classList.toggle('on',!!on[j]);x.setAttribute('aria-pressed',on[j]?'true':'false')});var n=on.reduce(function(a,c){return a+c},0),key=K[ci][1],kn=key.reduce(function(a,c){return a+c},0),lt=function(k){return k==5?['초록','var(--gfp)']:k>=3?['노랑','var(--amber)']:['빨강','#f0604d']},me=lt(n),ref=lt(kn);o.innerHTML='내가 켠 조건 <b>'+n+'/5</b> → <b style="color:'+me[1]+'">'+me[0]+'</b> · 이 페이지의 판단 예시: '+key.map(function(v,i){return C[i].slice(0,1)+(v?'예':'아니오')}).join(' · ')+' → <b style="color:'+ref[1]+'">'+ref[0]+'</b>'+(n==kn&&key.every(function(v,i){return v==on[i]})?' — 같습니다.':'');}draw();};
W['w8-lad']=function(b){var A=[['기어 가공 라인 공구','ai4i_2024_mini.csv','tool_wear_min'],['판재 표면 거칠기','불량품_판정_데이터.csv','surface_roughness_um'],['면류 비빔면 여름 판매','면류 일별 CSV','판매량']],Bm=[['불량률','이 전체의 2배를 넘는 '],['불량률','이 가장 높은 '],['판매량','이 평균의 1.5배를 넘는 ']],Cm=[['몇 분 · 몇 µm 이상','구간은 어디인가?'],['같은 행 수 4구간 중','구간은 어디인가?'],['2023~2026년 6~8월 중','주는 언제인가?']],s=['#ld-a','#ld-b','#ld-c'].map(function(q){return b.querySelector(q)});A.forEach(function(a,i){s[0].add(new Option(a[0],i))});Bm.forEach(function(a,i){s[1].add(new Option(a[0]+' ('+a[1].trim()+')',i))});Cm.forEach(function(a,i){s[2].add(new Option(a[0],i))});function f(){var a=A[+s[0].value],bb=Bm[+s[1].value],c=Cm[+s[2].value],q=a[0]+'에서 '+c[0]+' '+bb[0]+bb[1]+c[1];b.querySelector('#ld-out').innerHTML='<p>분야 — 스마트 팩토리</p><p>영역 — '+(a[2]=='판매량'?'생산계획':'품질 관리')+'</p><p>문제 — '+a[0]+'의 '+bb[0]+'이 조건에 따라 다르다</p><p class="g"><b>질문 — 「'+q+'」</b></p><p style="font-size:13px;color:var(--muted)">데이터: '+a[1]+' · 쓸 컬럼: '+a[2]+' — 「다섯 조건」 ①②가 바로 채워집니다.</p>';}s.forEach(function(x){x.onchange=f});s[1].value=0;f();};
W['w8-fix']=function(b){var F=[['AI로 제조업 혁신하기','너무 넓다 — 10일로 끝나지 않는다','열 방출 고장이 몰리는 회전수·온도차 조건은?'],['딥러닝으로 불량 예측 모델 만들기','수업 도구 밖, 기한 초과','few-shot 예시를 바꾸면 놓침이 줄어드는가?'],['우리 회사 데이터 분석','질문이 없다 — 물음표가 없다','우리 라인 3개월 생산일보에서 불량 상위 2개 원인은?'],['불량률이 높은 이유','검토할 기준이 없다','마모 구간별 불량률은 어떻게 변하고, 교체 기준은 몇 분인가?']],box=b.querySelector('#fx-box');F.forEach(function(f){var d=document.createElement('button');d.type='button';d.className='panel';d.style.cssText='margin:0;text-align:left;cursor:pointer;color:var(--text);font:inherit';var on=0;function sh(){d.innerHTML=on?'<b style="color:var(--gfp)">고친 주제</b><p style="margin:6px 0 0">「'+f[2]+'」</p><p style="font-size:13px;color:var(--muted);margin:6px 0 0">데이터 이름과 숫자 기준이 들어갔습니다.</p>':'<b style="color:#f0604d">나쁜 주제</b><p style="margin:6px 0 0">「'+f[0]+'」</p><p style="font-size:13px;color:var(--muted);margin:6px 0 0">문제: '+f[1]+' · 눌러서 뒤집기</p>';}d.onclick=function(){on=1-on;sh();};sh();box.appendChild(d);});};
W['w8-ai']=function(b){var C=['① AI가 준 숫자는 다시 센다 — 필터·재집계 결과를 함께 적는다','② 쓴 프롬프트를 부록에 남긴다 — 카드 번호와 고친 곳까지','③ 결과의 한계를 내 말로 한 문단 쓴다 — 논문·교과서 1개 인용'],bt=b.querySelector('#ai8-bt'),o=b.querySelector('#ai8-out'),on=[0,0,0];C.forEach(function(c,i){var l=document.createElement('label');l.style.cssText='display:block;cursor:pointer';l.innerHTML='<input type="checkbox"> '+c;l.querySelector('input').onchange=function(e){on[i]=e.target.checked?1:0;f();};bt.appendChild(l);});function f(){var n=on[0]+on[1]+on[2];o.innerHTML='<b>'+n+' / 3</b> '+(n==3?'— AI 답에 내 코멘트가 붙었습니다. 이제 보고서입니다.':'— 빠진 것: '+C.filter(function(c,i){return !on[i]}).map(function(c){return c.split(' — ')[0]}).join(', '));}f();};
W['w8-thr']=function(b){var t=b.querySelector('#th-t'),T=[];for(var x=2.0;x<=5.0001;x+=0.1)T.push(+x.toFixed(1));function f(){var v=+t.value;b.querySelector('#th-v').textContent=v.toFixed(2)+'µm';var R=T.map(function(x){return thr(x)});Chart.line(b.querySelector('#th-svg'),{labels:T.map(function(x){return x.toFixed(1)}),series:[{name:'t 이상 불량률(%)',color:'#f0604d',values:R.map(function(r){return r.n>=20?r.r*100:null}),dots:true}],ref:6.6,vline:[Math.round((v-2)/0.1)],min:0,max:30,h:230,ticks:10});var r=thr(v),base=3.3;b.querySelector('#th-out').innerHTML='거칠기 ≥ <b>'+v.toFixed(2)+'µm</b>: '+r.b+' / '+r.n+'행 = <b>'+(r.r*100).toFixed(2)+'%</b> ('+(r.r*100/base).toFixed(1)+'배) · 점선 = 2배 6.6% · '+(r.n<30?'<b style="color:var(--amber)">n이 30 미만 — 흔들림이 큽니다</b>':r.r*100>=6.6?'<b style="color:var(--gfp)">2배를 넘습니다</b>':'2배 미만')+' · (n 20 미만 지점은 선에서 뺐습니다)';}t.oninput=f;f();};
W['w8-card']=function(b){var F=[['q','01 질문','물음표로 끝나는 한 문장'],['d','02 데이터','파일 이름 · 행 수 · 쓸 컬럼 · 출처'],['m','03 방법','쓸 주차·카드 · 순서'],['o','04 산출물','표·차트·문서·앱 중 무엇을 몇 장'],['v','05 검증·검토','다시 세는 방법 · 참고 문헌 1개'],['n','06 90일 연결','동사 + 대상 + 시한']],EX={q:'불량 판정 데이터에서 표면 거칠기 몇 µm 이상 구간에서 불량률이 전체의 2배를 넘는가?',d:'불량품_판정_데이터.csv · 1,000행 · surface_roughness_um, nomal_abnormal (+ 보조 3컬럼) · 수업 데이터',m:'7주차 카드 01(세기) → 카드 04(층별) → 카드 05(자리 지도) · 구간 수 바꿔 보기',o:'구간별 불량률 표 1 · 막대 차트 1 · 히트맵 1 · 조건 문장 1',v:'조건 문장을 엑셀 필터로 다시 셈 · 층별 분석 교과서 장 1개 인용',n:'12월 말까지 해당 구간 진입 시 재검사하는 작업지시서 분기 1개 추가'},fm=b.querySelector('#cd-form');fm.innerHTML=F.map(function(f){return '<label style="display:block;margin:6px 0"><b>'+f[1]+'</b> <span style="font-size:13px;color:var(--muted)">'+f[2]+'</span><textarea data-k="'+f[0]+'" rows="2" style="width:100%;box-sizing:border-box;margin-top:4px;background:#1b1e2e;color:var(--text);border:1px solid #363a52;border-radius:6px;padding:6px;font:inherit"></textarea></label>'}).join('');var I={};fm.querySelectorAll('textarea').forEach(function(x){I[x.dataset.k]=x;x.oninput=f;});function f(){var v={};F.forEach(function(x){v[x[0]]=I[x[0]].value.trim()});var P=[[v.q&&/[?？]\s*$/.test(v.q),'① 질문이 물음표로 끝난다'],[v.d&&/\.(csv|xlsx|xls|json)|\d+\s*행/.test(v.d)&&!/예정|구할/.test(v.d),'② 데이터에 파일 이름·행 수가 있고 「예정」이 아니다'],[v.m&&/주|카드/.test(v.m),'③ 방법에 주차·카드가 있다 (도구 이름뿐이 아니다)'],[v.v&&!/AI가\s*확인|AI\s*확인/.test(v.v)&&/다시|재집계|필터|엑셀|직접/.test(v.v),'④ 검증이 「AI가 확인」이 아니라 내가 다시 세는 방법이다'],[v.n&&/까지|일\s*안|주\s*안|월|일까지|\d+일/.test(v.n)&&!/검토$|도입 검토/.test(v.n),'⑤ 90일 칸에 시한이 있고 「도입 검토」가 아니다']],ok=P.filter(function(p){return p[0]}).length,fill=F.filter(function(x){return v[x[0]]}).length;b.querySelector('#cd-out').innerHTML='채운 칸 <b>'+fill+'/6</b> · 자주 비는 자리 점검 <b>'+ok+'/5</b><br>'+P.map(function(p){return (p[0]?'✔ ':'✘ ')+p[1]}).join('<br>');var card=F.map(function(x){return x[1]+' — '+(v[x[0]]||'(비어 있음)')}).join('\n'),pr=TIDY8.replace('(여기에 01~06 칸을 붙여 넣는다)',card);b.querySelector('#cd-pr').innerHTML='<div class="prompt" data-raw="'+pr.replace(/&/g,'&amp;').replace(/"/g,'&quot;')+'">'+pr.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</div>';var pp=b.querySelector('#cd-pr .prompt'),cb=document.createElement('button');cb.className='bt copy';cb.type='button';cb.textContent='복사';cb.onclick=function(){var t=pp.getAttribute('data-raw');function d(){cb.textContent='복사됨';setTimeout(function(){cb.textContent='복사'},1500)}if(navigator.clipboard)navigator.clipboard.writeText(t).then(d,d);else d();};pp.appendChild(cb);}b.querySelector('#cd-ex').onclick=function(){F.forEach(function(x){I[x[0]].value=EX[x[0]]});f();};b.querySelector('#cd-clr').onclick=function(){F.forEach(function(x){I[x[0]].value=''});f();};f();};
W['w8-light']=function(b){var K=[['질문: 마모 구간별 불량률은 어떻게 변하고, 교체 기준은 몇 분인가? · 데이터: ai4i_2024_mini.csv 100행 · 방법: 7주 카드 01·03 · 검증: 필터 재집계 · 90일: 12월까지 교체 기준 지시서 반영',0,'다섯 조건 모두 예, 여섯 칸이 찼습니다 → 바로 실행.'],['질문: 우리 공장 품질을 AI로 개선할 수 있는가? · 데이터: 공장 데이터(구할 예정) · 방법: AI 분석',2,'데이터가 없고 범위가 분야 수준입니다 → 예시 주제에서 다시 출발.'],['질문: 면류 비빔면 여름 교대 계획은? · 데이터: 면류 일별 CSV · 방법: 3주 계절지수 · 6주 시나리오 · 검증: (비어 있음)',1,'검증 칸이 비었습니다 → 다시 세는 방법 한 줄을 넣어 수정본.'],['질문: 세 공장(사출·판재·SMT)의 모든 불량 원인과 대책은? · 데이터: 수업 데이터 3개 · 방법: 7주 카드 전부 · 검증: 엑셀 필터',1,'너무 넓습니다 → 공장 하나, 원인 하나로 좁혀서.']],L=[['초록','#5ee39c'],['노랑','#f1b646'],['빨강','#f0604d']],box=b.querySelector('#lt-box'),o=b.querySelector('#lt-out'),ans=K.map(function(){return -1});box.innerHTML=K.map(function(k,i){return '<div class="panel" style="margin:8px 0"><p style="margin:0 0 6px">카드 '+(i+1)+' — '+k[0]+'</p><div class="ctrl" style="margin:0">'+L.map(function(l,j){return '<button class="bt" type="button" data-i="'+i+'" data-j="'+j+'" style="border-color:'+l[1]+'">'+l[0]+'</button>'}).join('')+'</div><div class="eq" data-r="'+i+'" style="margin-top:6px"></div></div>'}).join('');box.querySelectorAll('.bt').forEach(function(x){x.onclick=function(){var i=+x.dataset.i,j=+x.dataset.j;ans[i]=j;box.querySelectorAll('.bt[data-i="'+i+'"]').forEach(function(y){y.classList.remove('on','no')});x.classList.add(j==K[i][1]?'on':'no');box.querySelector('[data-r="'+i+'"]').innerHTML='판정 예시: <b style="color:'+L[K[i][1]][1]+'">'+L[K[i][1]][0]+'</b> — '+K[i][2];f();};});function f(){var d=ans.filter(function(a){return a>=0}).length,ok=ans.filter(function(a,i){return a==K[i][1]}).length;o.innerHTML='판정한 카드 '+d+'/4 · 예시와 같은 판정 <b>'+ok+'</b>';}f();};
W['w8-plan']=function(b){var d=b.querySelector('#pl-d'),S=[[1,2,'데이터 정리','컬럼 확인 · 결측치'],[3,5,'분석·시각화','수업 카드 재사용'],[6,8,'코멘트·검토','다시 세기 · 한계 · 문헌'],[9,10,'정리·제출','부록에 프롬프트 기록 · 마지막 이틀은 비워 두기']];var t=new Date();d.value=t.toISOString().slice(0,10);function f(){var x=new Date(d.value+'T00:00:00');if(isNaN(x)){b.querySelector('#pl-tb').innerHTML='';return;}var fmt=function(k){var y=new Date(x.getTime()+k*864e5);return (y.getMonth()+1)+'/'+y.getDate()+'('+'일월화수목금토'[y.getDay()]+')';};b.querySelector('#pl-tb').innerHTML='<table class="tb"><tr><th>일차</th><th>날짜</th><th>구간</th><th>할 일</th></tr>'+S.map(function(s){return '<tr><td>'+s[0]+'–'+s[1]+'일</td><td class="n">'+fmt(s[0])+' ~ '+fmt(s[1])+'</td><td>'+s[2]+'</td><td>'+s[3]+'</td></tr>'}).join('')+'</table>';b.querySelector('#pl-out').innerHTML='시험일 다음 날을 1일로 셌습니다. 제출 마감 <b>'+fmt(10)+'</b>(10일차) — 실제 마감은 강사 안내를 따릅니다.';}d.oninput=f;f();};
W['w8-duel']=function(b){var h=b.querySelector('#du8-h');function lab(){b.querySelector('#du8-vh').textContent=h.value+'시간/일';}h.oninput=lab;lab();var R=[['데이터 구하기·정리',30],['분석 6칸 전부',45],['시각화·문서',20],['검토·한계·문헌',15]],F=[['데이터 정리',4],['카드 01·04·05 분석',8],['표·차트·조건 문장',5],['검토·한계·문헌',6]];function run(L,cap){var left=cap,done=[],chk=0;L.forEach(function(x){var u=Math.min(left,x[1]);left-=u;done.push(Math.round(u/x[1]*100));});return {done:done,spare:left};}b.querySelector('#du8-run').onclick=function(){var cap=+h.value*10,r=run(R,cap),f=run(F,cap),rt=R.reduce(function(a,x){return a+x[1]},0),ft=F.reduce(function(a,x){return a+x[1]},0);b.querySelector('#du8-k').innerHTML='<div class="kpi r"><b>'+r.done[3]+'%</b><span>주판봇: 검토 구간 완료율 (필요 '+rt+'시간)</span></div><div class="kpi a"><b>'+Math.min(100,Math.round(cap/rt*100))+'%</b><span>주판봇: 전체 진행률</span></div><div class="kpi g"><b>'+f.done[3]+'%</b><span>초파리: 검토 구간 완료율 (필요 '+ft+'시간)</span></div><div class="kpi m"><b>'+f.spare.toFixed(1)+'시간</b><span>초파리: 남는 시간 (마지막 이틀 여유)</span></div>';var win=f.done[3]>r.done[3]||(f.done[3]==100&&r.done[3]==100&&f.spare>r.spare);sayDoc(win?'e10':'e09',(win?'초파리 연구원 승. ':'비겼습니다. ')+'하루 '+h.value+'시간 × 10일 = '+cap+'시간입니다. 넓은 주제는 '+rt+'시간이 필요해 검토 구간이 '+r.done[3]+'%에서 멈춥니다. 배점의 중심은 코멘트·검토 사항입니다. 좁은 질문은 '+ft+'시간에 끝나고 '+f.spare.toFixed(1)+'시간이 남습니다.');};};
'''

# ── 실습 리포트 (발견편) ───────────────────────────────────────
RP = {
 'title': '표면 거칠기, 몇 µm부터 위험한가? — 예시 주제 카드를 끝까지 풀다',
 'eyebrow': '8주차 실습 리포트 · 중간 점검 · 예시 주제 카드 풀이 · 불량 판정 1,000행',
 'desc': '스마트 제조 8주차 실습 리포트 — 주제 카드 예시의 질문 「거칠기 몇 µm 이상에서 불량률이 2배를 넘는가?」를 1,000행 데이터로 풀어, 약 3.6µm 이상에서 2배를 처음 넘고 상위 5%에 불량 9건이 몰렸음을 박사가 정리합니다.',
 'lead': '8주차 예시 카드는 「초록」으로 소개됐지만, 정말 10일 안에 답이 나오는 질문일까요? 제가 직접 끝까지 풀어 봤습니다. 답은 나왔고, 검토할 거리도 넉넉했습니다.',
 'cover_mood': 'e07', 'back': ('index.html', '8주차 본문으로'), 'next': ('../w09/index.html', '9주차 (준비 중)'),
 'summary': {
   'finding': '이 데이터(판재 1,000장, 불량 33장, 3.3%)에서 거칠기 문턱을 올려 가면 약 3.6µm 이상(159장)에서 불량률 6.9%로 전체의 2배를 처음 넘고, 4.32µm 초과 상위 5%(50장)에는 불량 9장(18%)이 몰려 있었습니다.',
   'evidence': ['<span class="fact">사실</span> 같은 행 수 5구간으로 나누면 최고 구간은 거칠기 상위 6.1%(12/198)로 2배(6.6%)에 못 미칩니다(<a href="#tab-r8-1">표 1</a>).',
                '<span class="fact">사실</span> 문턱 3.42µm 이상은 6.0%(12/201), 3.6µm 이상은 6.9%(11/159), 4.2µm 이상은 15.0%(9/60)입니다(<a href="#fig-r8-1">그림 1</a>).',
                '<span class="fact">사실</span> 20구간으로 나누면 맨 위 구간(4.32µm 초과, 50장)에 불량 9장, 바로 아래 구간(48장)은 0장입니다.',
                '<span class="interp">해석</span> 거칠기는 불량 33장 중 약 9장을 가르는 신호입니다. 나머지 24장은 거칠기와 무관하게 약 2.5%로 고르게 퍼져 있어, 다른 원인을 따로 찾아야 합니다.'],
   'fig': ('fig', {'id': 'fig-r8-1', 'cap': '[그림 1] 거칠기 문턱 t 이상의 불량률 (단위: %, 점선 = 2배 6.6%)', 'w': 'r8-thr', 'alt': '문턱 2.0~5.0µm. 3.42에서 6.0, 3.6에서 6.9로 점선을 넘고, 4.2에서 15, 4.5에서 25로 오른다', 'src': '출처: 불량품_판정_데이터.csv (1,000행), 저자 계산 · 문턱 위 행이 20장 미만인 지점은 뺌'}),
 },
 'sections': [
  {'id': 'sec-r8-1', 'nav': '들어가며', 'title': '들어가며 — 예시 카드는 정말 초록일까', 'blocks': [
    ('memo', 'e08', '8주차 교안의 예시 카드는 초록이었어요. 그런데 카드만 보고 초록이라고 하기보다, 한 번 끝까지 풀어 보는 게 제일 확실하죠.'),
    ('p', '예시 카드의 질문은 「불량 판정 데이터에서 표면 거칠기 몇 µm 이상 구간에서 불량률이 전체의 2배를 넘는가?」입니다. 데이터는 1,000행 파일 하나, 방법은 7주 카드 01·04·05입니다.'),
    ('p', '이 리포트가 답할 질문은 셋입니다. ① 같은 행 수 구간으로는 2배를 넘는가 ② 문턱을 옮기면 어디서 넘는가 ③ 거칠기는 불량을 얼마나 설명하는가.')]},
  {'id': 'sec-r8-2', 'nav': '배경', 'title': '배경 — 구간과 문턱은 다른 질문이다', 'blocks': [
    ('p', '7주차 층별은 같은 행 수 구간으로 나눴습니다. 구간은 「이 범위 안」의 불량률이고, 문턱은 「이 값 이상 전부」의 불량률입니다. 현장 기준(「3.6µm 이상이면 재검사」)은 대개 문턱 모양입니다.'),
    ('p', '2배 기준은 전체 불량률 3.3%의 두 배, 6.6%입니다. 7주차에서 미리 정한 숫자 기준을 그대로 씁니다.'),
    ('memo', 'e09', '구간은 「이 반 학생들」, 문턱은 「키 170cm 이상 전부」예요. 질문이 다르면 숫자도 다르게 나옵니다.')]},
  {'id': 'sec-r8-3', 'nav': '방법', 'title': '방법 — 세기 → 구간 → 문턱 → 나머지', 'blocks': [
    ('table', {'id': 'tab-r8-0', 'cap': '<표 0> 계산 규칙', 'head': ['단계', '규칙'],
               'rows': [['세기', 'nomal_abnormal 값 종류와 개수 (abnormal = 불량)'], ['구간', '같은 행 수 4 · 5 · 10 · 20구간, 경계값 포함은 아래 구간'], ['문턱', 't = 2.0~5.0µm, 0.1 간격, 「거칠기 ≥ t」 행의 불량률 · 문턱 위 20장 미만은 해석하지 않음'], ['나머지', '상위 5%를 뺀 950장의 구간별 불량률']],
               'src': '계산 코드: 이 저장소 analysis/w08_threshold.py'}),
    ('p', '본문 8.8의 문턱 위젯도 같은 1,000행으로 페이지 안에서 다시 셉니다.')]},
  {'id': 'sec-r8-4', 'nav': '결과', 'title': '결과', 'blocks': [
    ('html', '<h3 id="sec-r8-4-1">결과 1 · 같은 행 수 구간으로는 — 경계 사례</h3>'),
    ('table', {'id': 'tab-r8-1', 'cap': '<표 1> 거칠기 구간 수별 맨 위 구간 (불량/n, 불량률)', 'head': ['구간 수', '맨 위 구간 범위(µm)', '불량/n', '불량률', '2배(6.6%)'],
               'rows': [['4', '3.26 초과', '15/250', '6.0%', '미달'], ['5', '3.42 초과', '12/198', '6.1%', '미달'], ['10', '3.93 초과', '9/98', '9.2%', '<b>넘음</b>'], ['20', '4.32 초과', '9/50', '18.0%', '<b>넘음</b>']],
               'src': '출처: 불량품_판정_데이터.csv, 저자 계산'}),
    ('p', '<span class="fact">사실</span> 4·5구간에서는 맨 위 구간도 2배에 못 미칩니다. 10구간부터 넘습니다. 10구간이어도 구간당 약 100행이라, 1,000행 데이터에서는 7주의 「n ≥ 10」 규칙 안입니다.'),
    ('html', '<h3 id="sec-r8-4-2">결과 2 · 문턱으로 보면 — 약 3.6µm에서 2배</h3>'),
    ('table', {'id': 'tab-r8-2', 'cap': '<표 2> 문턱별 불량률 (거칠기 ≥ t)', 'head': ['t (µm)', '행 수', '불량', '불량률', '전체 대비'],
               'rows': [['3.0', '357', '18', '5.0%', '1.5배'], ['3.2', '277', '16', '5.8%', '1.8배'], ['3.42', '201', '12', '6.0%', '1.8배'], ['<b>3.6</b>', '159', '11', '<b>6.9%</b>', '<b>2.1배</b>'], ['3.8', '121', '10', '8.3%', '2.5배'], ['4.0', '91', '9', '9.9%', '3.0배'], ['4.2', '60', '9', '15.0%', '4.5배'], ['4.5', '36', '9', '25.0%', '7.6배']],
               'src': '출처: 저자 계산 (analysis/w08_threshold.py)'}),
    ('p', '<span class="fact">사실</span> 2배를 처음 넘는 지점은 3.42µm(6.0%)와 3.6µm(6.9%) 사이입니다. 4.0µm 이상부터 4.5µm 이상까지 불량은 9장으로 그대로이고, 행 수만 91에서 36으로 줄어듭니다.'),
    ('key', '4.0µm를 넘는 불량 9장은 사실상 같은 9장입니다. 문턱을 더 올려 불량률이 오르는 것은, 불량이 늘어서가 아니라 양품이 빠져서입니다.'),
    ('memo', 'e04', '이게 문턱 분석의 함정이에요. 문턱을 올리면 퍼센트는 계속 올라가요. 그래서 n과 「불량 몇 장」을 꼭 같이 적어야 합니다.'),
    ('html', '<h3 id="sec-r8-4-3">결과 3 · 나머지 24장 — 거칠기와 무관하게 퍼져 있다</h3>'),
    ('p', '<span class="fact">사실</span> 거칠기 4.32µm 이하 950장에는 불량 24장(2.5%)이 있습니다. 이 950장을 다시 5구간으로 나누면 구간 불량률은 2.1~3.2%로 거의 평평합니다.'),
    ('p', '<span class="interp">해석</span> 거칠기가 가르는 불량은 33장 중 약 9장입니다. 나머지 24장은 폭·초음파·오븐 온도 같은 다른 측정값, 또는 측정되지 않은 원인에서 찾아야 합니다.')]},
  {'id': 'sec-r8-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 반론 1: 문턱을 결과를 보고 고르면 유리한 숫자만 고르게 된다. 맞습니다. 그래서 문턱 후보(0.1µm 간격)를 미리 정하고 표 전체를 실었습니다. 「3.6µm」는 그 표에서 처음 2배를 넘는 칸일 뿐, 최적 기준이라는 뜻이 아닙니다.'),
    ('p', '<span class="interp">해석</span> 반론 2: 불량 9장이면 우연일 수 있다. 1,000장 중 상위 50장에 불량이 무작위로 들어간다면 평균 1.65장입니다. 9장은 그보다 훨씬 많지만, 엄밀한 확률(검정)은 9주차에서 확인합니다.'),
    ('p', '<span class="guess">추측</span> 상위 5% 거칠기 판재는 같은 롤·같은 날 생산분일 수 있습니다. 이 데이터에는 생산 순서 열이 없어 확인할 수 없습니다.'),
    ('memo', 'e09', '「몇 µm부터?」라는 질문은 답이 한 숫자로 딱 떨어질 것 같지만, 실제로는 「이 근처에서, 이 정도 n으로」라고 답하는 게 정직해요.')]},
  {'id': 'sec-r8-6', 'nav': '의의와 한계', 'title': '의의와 한계 — 그래서 이 카드는 초록인가', 'blocks': [
    ('p', '의의: 예시 카드의 질문은 파일 하나 · 수업 카드 셋으로 하루 안에 답이 나왔습니다. 그리고 「5구간에서는 2배 미만」 「문턱을 올리면 퍼센트만 오른다」 「나머지 24장」처럼 코멘트·검토할 거리가 충분했습니다. 다섯 조건 모두 「예」, 초록이 맞습니다.'),
    ('p', '한계: ① 교육용 가상 데이터 ② 생산 순서·롤·날짜 열이 없음 ③ 문턱은 0.1µm 간격 후보만 봤음 ④ 우연일 확률은 계산하지 않았음.'),
    ('p', '7주 실습 가이드의 카드 04 참고 답 「거칠기 상위 6.0% (n=201) — 2배 이상」은 이 리포트에서도 「6.1% (12/198), 1.8배 — 경계 사례」로 바꿔 씁니다.'),
    ('prompt', '#역할\n너는 판재 라인의 품질 분석가다.\n#맥락\n첨부한 불량품_판정_데이터.csv(1,000행)를 쓴다. 열 이름은 파일 그대로. 불량 = nomal_abnormal이 abnormal.\n#조건\n문턱 t를 3.0, 3.2, 3.42, 3.6, 3.8, 4.0, 4.2, 4.5µm로 미리 정하고, 각 t에 대해 surface_roughness_um ≥ t인 행만 센다.\n#형식\n표: t | 행 수 | 불량 | 불량률 | 전체 대비 배수 + 2배(6.6%)를 처음 넘는 t 한 줄 + 해석 3줄\n#검수 기준\nt = 3.6에서 159행 · 11건 · 6.9%가 나와야 한다. 다르면 필터 조건을 보여 달라.'),
    ('memo', 'e07', '이 프롬프트가 여러분 카드의 「03 방법」 칸 견본이에요. 문턱 후보를 프롬프트 안에 미리 박아 둔 게 핵심입니다.'),
    ('p', '다음 편 예고: 9주차 「불량 분석 ② 왜 터지는가」는 아직 빈 슬롯입니다. 자료가 준비되면 7주의 조건 문장과 오늘의 문턱을 「왜」로 잇습니다.')]},
 ],
 'refs': ['불량품_판정_데이터.csv — 교육용 가상 데이터 1,000행 (7주차 실습 데이터)', '안상선, 스마트 제조 8주차 강의 교안·워크시트(주제 카드), 2026', '이 저장소 analysis/w08_threshold.py — 저자 계산'],
 'sources': [('원자료', '불량품_판정_데이터.csv'), ('계산', '저자 계산 (analysis/w08_threshold.py)')],
 'notes': '문턱 후보 간격(0.1µm)과 「20장 미만은 해석하지 않음」은 이 리포트가 정한 규칙입니다.',
}
RP['js'] = _DATA + _JS + r'''
W['r8-thr']=function(s){var T=[];for(var x=2.0;x<=5.0001;x+=0.1)T.push(+x.toFixed(1));Chart.line(s,{labels:T.map(function(x){return x.toFixed(1)}),series:[{name:'거칠기 ≥ t 불량률(%)',color:'#f0604d',values:T.map(function(x){var r=thr(x);return r.n>=20?r.r*100:null}),dots:true},{name:'전체 3.3%',color:'#82b8ff',values:T.map(function(){return 3.3}),dash:'2 3'}],ref:6.6,min:0,max:30,h:250,ticks:10});};
'''
