# 2주차 · 생성형 AI 원리 & 프롬프트 기초
CH = {
 'slug': 'w02', 'num': '02',
 'title': '생성형 AI 원리 & 프롬프트 기초',
 'eyebrow': '2주차 · SECTION 1 · 준비 · 케이블 하네스 조립 라인',
 'desc': '스마트 제조 2주차 — 토큰화·임베딩·다음 토큰 예측·어텐션의 원리를 케이블 하네스 조립 라인 작업지시서로 풀고, 환각과 검수, 프롬프트 5원칙을 익힙니다.',
 'q': 'AI는 작업지시서 한 줄을 어떻게 읽고, 왜 그럴듯하게 틀릴까?',
 'lead': '생성형 AI는 정답을 꺼내 오는 기계가 아니라, 글을 숫자로 바꿔 다음에 올 말을 확률로 고르는 시스템입니다. 원리를 알면 어떤 도구가 나와도 무엇을 할 수 있고 무엇을 못 하는지 스스로 판단할 수 있습니다.',
 'scene_alt': '케이블 하네스 조립 3D 라인. 전선 릴, 절단·탈피, 단자 압착, 인출력 시험, 결속·포장 순서로 제품이 흐르고, 위에는 작업지시서 토큰 10개가 떠 있으며 QWEN 단말로 어텐션 빛줄기가 이어진다.',
 'scene_hud': '3D · 케이블 하네스 조립 — 작업지시서 토큰과 어텐션 빛줄기',
 'scene_opts': {'cam': [4, 13, 24], 'target': [-1, 3, 0]},
 'kpis': [('12조각', '작업지시서 한 줄 → 토큰', 'm'), ('0.32', '「커피를」 어텐션 가중치 (교안 예시)', 'g'), ('3단계', '사전학습 → 다음 토큰 → 미세조정', 'a'), ('5원칙', '역할·맥락·조건·형식·예시', 'r')],
 'hero_talk': [
   ('doc', 'e07', '오늘은 케이블 하네스 라인입니다. 라인장이 작업지시서를 AI에 붙여넣는 순간, AI 안에서 무슨 일이 일어나는지 봅니다.'),
   ('robo', 'e16', 'AI는 작업지시서를 사람처럼 읽고 이해합니다!'),
   ('fly', 'e09', '정말 "이해"할까? 숫자로 바꿔서 계산하는 거 아니야?'),
   ('asst', 'e04', '글자가 숫자가 된다고요? 그럼 "5V/10mA"는요?'),
 ],
 'three': ['AI가 글을 조각(토큰)으로 쪼개 숫자로 바꾸고, 다음에 올 말을 확률로 골라 문장을 만드는 원리를 봅니다.',
           '같은 질문도 단어 하나, 순서 하나에 답이 달라집니다. 그래서 AI는 그럴듯하게 틀릴 수 있고, 검수가 필요합니다.',
           '작업지시서 요약, 불량 원인 대화, 다국어 안전 표지, 설비 로그 해석을 프롬프트 5원칙으로 안정되게 시킵니다.'],
 'abbr': [('LLM', 'Large Language Model', '거대 언어 모델 — 많은 글로 언어 패턴을 배운 AI'), ('RPA', 'Robotic Process Automation', '정해진 사무 절차를 자동으로 반복하는 소프트웨어'),
          ('SPC', 'Statistical Process Control', '통계적 공정 관리 — 관리한계선으로 공정 이상을 감시'), ('ID', 'Identifier', '토큰마다 붙는 고유 번호')],
 'why': [('결과보다 과정', 'AI를 마법 같은 응답 기계로 쓰면, 틀렸을 때 왜 틀렸는지 알 수 없습니다.'),
         ('도구는 바뀐다', '서비스 이름은 금방 바뀝니다. 원리를 알면 새 도구의 능력과 한계를 스스로 판단합니다.'),
         ('프롬프트의 기초 체력', '입력 순서·조건이 결과를 바꾸는 이유를 알면, 좋은 프롬프트를 우연이 아니라 설계로 씁니다.')],
 'big_lead': '대화창의 한 문장은 다섯 단계를 거쳐 답이 됩니다.',
 'big': [('① 입력', '질문과 조건을 넣습니다. 첫 조건이 이후 계산 방향을 크게 정합니다.'), ('② 토큰화', '글을 조각으로 나누고 숫자 ID를 붙입니다.'),
         ('③ 처리', '임베딩과 어텐션으로 맥락을 계산합니다.'), ('④ 선택 → ⑤ 응답', '다음 토큰의 확률을 계산해 하나씩 고르고, 반복해 문장을 만듭니다.')],
 'glossary': {
   '토큰': ['토큰', '개념', 'AI가 글을 처리하는 가장 작은 조각입니다. 띄어쓰기 단위가 아니라 더 잘게 나뉠 수 있습니다.'],
   '임베딩': ['임베딩', '개념', '토큰에 의미 공간의 위치(숫자 묶음)를 주는 일입니다. 뜻이 비슷하면 가깝게 놓입니다.'],
   '어텐션': ['어텐션', '개념', '다음 말을 정할 때 앞의 여러 토큰 중 중요한 것에 더 큰 가중치를 주는 장치입니다.'],
   '트랜스포머': ['트랜스포머', '모델 구조', '어텐션을 겹겹이 쌓은 신경망 구조로, 오늘날 대부분의 생성형 AI의 뼈대입니다.'],
   '미세조정': ['미세조정', '학습 단계', '사전학습된 모델을 특정 목적과 응답 스타일에 맞게 다시 다듬는 단계입니다.'],
   '환각': ['환각', '주의', 'AI가 사실이 아닌 내용을 그럴듯하게 만들어 내는 현상입니다.'],
   'few-shot': ['few-shot', '프롬프트 기법', '프롬프트 안에 답의 예시를 두세 개 보여 주어 형식과 수준을 맞추게 하는 방법입니다.'],
 },
 'subs': [
  {'id': 'sec-2-1', 'title': '왜 도구 설명이 아니라 원리부터인가', 'tags': ['일상: 자동차 운전', '방법: 원리 → 활용'],
   'pair': ('일상으로 치면', '차종이 바뀌어도 운전을 할 수 있는 건, 핸들·브레이크가 어떻게 작동하는지 알기 때문이다.',
            '생성형 AI에서는', 'QWEN·ChatGPT·Gemini·Claude는 이름이 다르지만, 글을 숫자로 바꿔 다음 말을 확률로 고른다는 원리는 같다.'),
   'body': ['이 장은 팁 모음이 아닙니다. 원리를 먼저 보고, 활용은 그 위에 쌓습니다.',
            '교안의 핵심 문장은 이렇습니다. AI를 잘 쓰는 능력은 우연히 좋은 문장을 넣는 감각이 아니라, 모델이 언어를 숫자로 처리하고 맥락을 확률로 계산한다는 이해에서 나옵니다.'],
   'talk': [('robo', 'e07', '저는 좋은 프롬프트 100개를 외웠습니다!'), ('fly', 'e09', '내일 새 모델이 나오면? 외운 100개가 그대로 통할까?'),
            ('asst', 'e10', '원리를 알면 새 도구에서도 스스로 고칠 수 있겠네요.')],
   'widget': ('w2-tools', '<div class="ptitle">비교 · 도구 이름은 달라도 같은 다섯 단계</div><div class="ctrl" id="tl-bt"></div><div class="insight" id="tl-out" aria-live="polite"></div>'),
   'limit': '모델마다 토큰을 나누는 방식, 학습한 데이터, 미세조정 방향은 다릅니다. 원리는 같아도 답의 품질은 다를 수 있습니다.',
   'quiz': [{'q': '이 장이 원리부터 배우는 이유는?', 'o': ['시험에 나와서', '새 도구가 나와도 능력과 한계를 스스로 판단하려고', '코드를 짜려고'], 'a': 1, 'why': '원리는 도구가 바뀌어도 그대로 쓸 수 있습니다.'}]},

  {'id': 'sec-2-2', 'title': '컴퓨터는 숫자만 처리한다 — 토큰화', 'tags': ['원리: 토큰화', '현장: 작업지시서'],
   'pair': ('일상으로 치면', '완성된 레고 작품을 가장 작은 블록으로 분해하고, 블록마다 번호를 붙인다.',
            'AI에서는', '"B7-2203 케이블 2.5m×4가닥 압착…"을 부품명·수치·단위·동작 조각(토큰)으로 나누고, 조각마다 숫자 ID를 붙인다.'),
   'why': {'problem': '컴퓨터는 글자를 뜻으로 이해하지 못하고 숫자만 계산할 수 있습니다.',
           'limit': '글자 하나하나를 번호로 바꾸면 너무 잘게 쪼개져 의미 묶음을 잃습니다. 단어 단위로 바꾸면 처음 보는 단어(부품 코드)를 처리하지 못합니다.',
           'solve': '그래서 자주 함께 나오는 글자 묶음을 조각(토큰)으로 삼아, 처음 보는 단어도 아는 조각들로 나눠 처리합니다.',
           'easy': '모르는 부품 코드도 "B7"과 "2203"처럼 아는 조각으로 쪼개 읽습니다.'},
   'body': ['교안의 표처럼 "생성형 AI를 배운다"는 ["생성", "형", " AI", "를", " 배운", "다"]처럼 쪼개질 수 있습니다. 실제 조각 경계는 모델마다 다릅니다.',
            '작업지시서 한 줄은 20~40개의 조각으로 나뉘어야 AI가 "요약해 줘"를 처리할 수 있습니다. 아래 실험에서 직접 쪼개 보세요.'],
   'talk': [('asst', 'e09', '"5V/10mA"는 한 조각이에요, 세 조각이에요?'), ('robo', 'e19', '당연히 한 조각! 전압과 전류는 붙어 다닙니다!'),
            ('fly', 'e10', '조각 나누는 규칙을 바꿔서 직접 세어 보자. 이걸 눌러 봐.')],
   'widget': ('w2-tok', '<div class="ptitle">실험 · 작업지시서를 조각으로</div><label class="glabel" for="tk-in">작업지시서 (고쳐 써도 됩니다)</label><textarea id="tk-in" rows="2" style="width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--rule);border-radius:8px;padding:8px;font:inherit">B7-2203 케이블 2.5m×4가닥 압착. 단자 HSG-A8P. 인출력 시험 5V/10mA 이상 — 불량 허용 0/100.</textarea><div class="ctrl"><button class="bt on" data-m="0" type="button">띄어쓰기로</button><button class="bt" data-m="1" type="button">부품·수치·단위로</button><button class="bt" data-m="2" type="button">더 잘게(글자 묶음)</button></div><div id="tk-out" style="display:flex;flex-wrap:wrap;gap:4px;margin:8px 0"></div><div class="eq" id="tk-n" aria-live="polite"></div>'),
   'explain': ['세 방식 모두 수업용 흉내입니다. 실제 모델은 학습으로 만든 조각 사전을 씁니다. 그래도 "규칙에 따라 조각 수가 달라진다"는 감각은 같습니다.',
               '조각이 많을수록 처리 비용(토큰 수)이 늘어납니다. 유료 AI 요금과 한 번에 넣을 수 있는 글 길이가 토큰 수로 정해지는 이유입니다.'],
   'code': [('tokenizer.encode(text)', '글을 토큰 번호 목록으로 바꾼다'), ('len(ids)', '토큰이 몇 개인지 센다')],
   'limit': '이 실험의 "숫자 ID"는 예시 번호입니다. 실제 모델의 번호와 다릅니다.',
   'quiz': [{'q': 'AI가 작업지시서를 처리하는 첫 단계는?', 'o': ['뜻을 이해한다', '조각(토큰)으로 나누고 숫자 ID를 붙인다', '인터넷에서 검색한다'], 'a': 1, 'why': '컴퓨터는 숫자만 처리하므로 글을 토큰과 ID로 바꾸는 것이 먼저입니다.'}]},

  {'id': 'sec-2-3', 'title': '의미는 좌표가 된다 — 임베딩', 'tags': ['원리: 임베딩', '현장: 다국어 안전 표지'],
   'pair': ('일상으로 치면', '도서관에서 비슷한 주제의 책은 가까운 서가에 꽂힌다. 위치만 봐도 무슨 책인지 짐작된다.',
            'AI에서는', '「위험」「Danger」「Nguy hiểm」「危险」은 글자는 달라도 의미 공간의 같은 근처에 놓인다. 그래서 다국어 번역·유사어 추천이 자연스럽다.'),
   'fx': {'q': '단어가 "좌표"라는 게 무슨 말이에요? 지도처럼요?',
          'school': '좌표평면과 두 점 사이 거리(피타고라스 정리)',
          'eq': '거리 = √((x₁ − x₂)² + (y₁ − y₂)²) · <i>가까울수록 뜻이 비슷하다</i>',
          'rows': [('(x, y)', '단어의 위치 (실제로는 수백~수천 개의 숫자)'), ('거리', '두 단어 뜻이 얼마나 다른가'), ('방향', '단어 사이 관계 (예: 위험 → 경고)')],
          'calc': '「위험」(2, 8)과 「Danger」(2.3, 7.6) 사이 거리는 √(0.09 + 0.16) = 0.5입니다. 「커피」(8, 1)까지는 √(36 + 49) ≈ 9.2로 멉니다.',
          'comment': '평면 지도는 비유이고, 실제로는 엄청 많은 칸의 숫자 묶음이군요!'},
   'body': ['교안은 이 "지도"를 진짜 눈에 보이는 지도로 착각하지 말라고 강조합니다. 거리·방향은 컴퓨터 안의 숫자 계산을 우리가 상상하기 위한 비유입니다.'],
   'talk': [('moa', 'e12', '외국인 동료용 안전 표지판을 만들 때 이 원리가 쓰이는군요!'), ('fly', 'e09', '근데 지도에서 가깝다고 꼭 같은 뜻일까? 아래 점들을 눌러 봐.'),
            ('x1', 'e04', '(오!)')],
   'widget': ('w2-emb', '<div class="ptitle">실험 · 의미 공간에서 가까운 단어 찾기 (설명용 좌표)</div><div class="cwrap"><svg id="em-svg" viewBox="0 0 560 300" role="img" aria-label="단어들이 의미에 따라 모여 있는 평면 지도"></svg></div><div class="eq" id="em-out" aria-live="polite">점을 누르면 가장 가까운 단어 3개가 나옵니다.</div>'),
   'limit': '좌표는 설명용으로 손으로 놓은 값입니다. 실제 임베딩은 수백 차원이라 평면에 그대로 그릴 수 없습니다.',
   'quiz': [{'q': '임베딩 공간에서 「위험」과 가장 가까울 것은?', 'o': ['커피', 'Danger', '사과'], 'a': 1, 'why': '언어가 달라도 뜻이 같으면 같은 근처에 놓입니다.'}]},

  {'id': 'sec-2-4', 'title': '같은 단어, 다른 뜻 — 맥락이 좌표를 옮긴다', 'tags': ['원리: 맥락', '현장: 「떨림」'],
   'pair': ('일상으로 치면', '"문을 열다"와 "마음이 열렸다"의 "열다"는 같은 글자지만 뜻이 다르다.',
            '공장에서는', '"1라인 모터에서 떨림"이면 베어링·정렬 불량을, "작업자 손이 떨림"이면 피로·저혈당·냉방을 의심한다. 주변 단어가 「떨림」의 좌표를 옮긴다.'),
   'body': ['AI는 단어를 고립된 사전 항목으로 처리하지 않고, 앞뒤 단어와 함께 읽으며 뜻을 조정합니다. 이것이 맥락(context)입니다.',
            '그래서 품질 반장이 상황을 한 줄 더 적으면 답의 방향이 바뀝니다. 아래에서 문맥 단어 하나만 바꿔 보세요.'],
   'talk': [('asst', 'e07', '"작업자"를 "컴프레서"로 바꾸면 답이 다시 기계 쪽으로 간대요.'), ('robo', 'e15', '저는 떨림이면 무조건 베어링이라고 답했었는데…'),
            ('doc', 'e10', '그래서 상황 설명이 프롬프트의 맥락 칸에 들어갑니다. 2.12에서 다시 봅니다.')],
   'widget': ('w2-ctx', '<div class="ptitle">실험 · 「떨림」 앞의 단어 바꾸기</div><div class="ctrl" id="cx-bt"></div><div class="eq" id="cx-q"></div><div class="insight" id="cx-out" aria-live="polite"></div>'),
   'explain': ['답 목록은 교안 사례 2의 기대 답변입니다. 실제 AI의 답은 매번 조금씩 다를 수 있습니다.', '원리는 같습니다. 문맥 단어가 바뀌면 「떨림」 주변에서 확률이 높아지는 단어가 바뀝니다.'],
   'limit': 'AI의 원인 추정은 가설입니다. 실제 원인은 측정과 점검으로 확인해야 합니다(9주차 4M 분석).',
   'quiz': [{'q': '같은 질문에서 답의 방향을 가장 크게 바꾸는 것은?', 'o': ['글씨체', '주변 단어(맥락)', '질문 길이'], 'a': 1, 'why': '주변 단어가 단어의 의미 좌표를 옮깁니다.'}]},

  {'id': 'sec-2-5', 'title': '규칙을 쓰는 방식 vs 데이터에서 배우는 방식', 'tags': ['비교: 규칙 기반 · 패턴 학습', '현장: SPC와 불량 조합'],
   'why': {'problem': '불량 원인이 "금요일 오후 + 신입 작업자 + 로트 B"처럼 세 조건이 겹칠 때만 터지는 경우가 있습니다.',
           'limit': '규칙 기반(SPC 관리도 등)은 사람이 미리 정한 항목만 검사합니다. 세 겹 조합 규칙을 미리 써 두기는 사실상 불가능합니다.',
           'solve': '패턴 학습은 데이터를 훑어 사람이 정의하지 않은 조합을 찾아냅니다. 대신 판단 과정을 직접 읽기 어렵습니다.',
           'easy': '레시피대로만 하는 요리(규칙) vs 직접 만들어 보며 감을 쌓는 요리사(학습).'},
   'body': ['<div class="tw"><table class="tb"><tr><th>구분</th><th>규칙 기반</th><th>패턴 학습</th></tr>'
            '<tr><td>누가 규칙을 쓰나</td><td>사람이 명시</td><td>데이터에서 모델이 형성</td></tr>'
            '<tr><td>예외</td><td>생길 때마다 규칙 추가</td><td>비슷한 예외에 유연</td></tr>'
            '<tr><td>강점</td><td>의도가 분명, 수정 경로 명확</td><td>복잡한 패턴 포괄</td></tr>'
            '<tr><td>한계</td><td>분기가 많아지면 관리 어려움</td><td>판단 과정을 읽기 어려움</td></tr>'
            '<tr><td>공장 예</td><td>온도 > 기준이면 경보</td><td>불량 조합 찾기, 생성형 응답</td></tr></table></div>',
            '두 방식은 경쟁이 아니라 보완입니다. 단순한 규칙은 규칙으로, 복잡한 패턴은 학습으로 풉니다. 아래 대결에서 숫자로 확인합니다.'],
   'talk': [('robo', 'e16', '규칙을 1,000개 쓰면 다 잡힙니다!'), ('fly', 'e03', '조합이 세 겹이면 규칙이 몇 개 필요한지 세어 봤어?'), ('sia', 'e07', '요일 7 × 시간대 3 × 숙련 2 × 로트 3이면 126가지입니다.')],
   'widget': ('w2-comb', '<div class="ptitle">계산기 · 조합 규칙은 몇 개?</div><div class="ctrl"><div class="group"><span class="glabel">조건 종류 수</span><input type="range" min="2" max="8" value="4" id="cb-k"><span class="val" id="cb-vk"></span></div><div class="group"><span class="glabel">조건마다 값의 수</span><input type="range" min="2" max="10" value="4" id="cb-v"><span class="val" id="cb-vv"></span></div></div><div class="eq" id="cb-out" aria-live="polite"></div>'),
   'limit': '패턴 학습이 찾은 조합도 우연일 수 있습니다. 표본이 적으면 다음 달 데이터로 다시 확인해야 합니다.',
   'quiz': [{'q': '"금요일 오후 + 신입 + 로트 B" 같은 세 겹 조합을 찾는 데 유리한 것은?', 'o': ['규칙 기반', '패턴 학습'], 'a': 1, 'why': '사람이 미리 쓰기 어려운 조합을 데이터에서 찾는 것이 패턴 학습의 강점입니다.'}]},

  {'id': 'sec-2-6', 'title': '다음 토큰을 하나씩 고른다', 'tags': ['원리: 다음 토큰 예측', '예: 사과 프롬프트'],
   'pair': ('일상으로 치면', '휴대폰 자동 완성이 다음 단어를 추천하는 기능을 아주 똑똑하게 키운 것.',
            'LLM에서는', '지금까지의 입력 + 방금 만든 단어까지 합쳐 다음 토큰의 확률을 계산하고 하나를 고른다. 이 일을 수백 번 반복해 문장을 만든다.'),
   'fx': {'q': '확률로 고른다는데, 그럼 매번 답이 달라질 수도 있어요?',
          'school': '확률과 조건부 확률(고등 수학 확률과 통계)',
          'eq': 'P(다음 토큰 | 지금까지의 글) — <b>조건</b>이 바뀌면 확률표 전체가 바뀐다',
          'rows': [('P(A | B)', 'B가 주어졌을 때 A가 나올 확률'), ('지금까지의 글', '질문 + 이미 만든 답'), ('고르기', '가장 높은 것, 또는 확률대로 뽑기')],
          'calc': '"사과에 대해 설명해줘"에서 「비타민」 0.30, 「새빨간」 0.05라고 해 봅시다. "유치원생이 이해하기 쉽게 동화처럼"을 더하면 「새빨간」이 0.32로 오르는 식입니다(설명용 값).',
          'comment': '조건 한 줄이 확률표를 통째로 바꾸는 거네요. 그래서 같은 질문도 답이 다르구나!'},
   'body': ['생성은 한 번에 완성된 판단이 아니라 연속된 확률 계산의 누적입니다. 첫 조건 하나가 이어지는 수백 번의 단어 선택에 연쇄로 영향을 줍니다.'],
   'talk': [('robo', 'e19', '그럼 저도 확률 1등만 고르면 완벽한 문장!'), ('fly', 'e09', '1등만 골라도 그 문장이 사실인지는 별개야.'), ('asst', 'e07', '아래에서 조건을 켜고 끄며 막대가 어떻게 바뀌는지 볼게요.')],
   'widget': ('w2-next', '<div class="ptitle">실험 · 조건이 다음 단어 확률을 바꾼다 (설명용 값)</div><div class="ctrl" id="nx-bt"></div><div class="cwrap"><svg id="nx-svg"></svg></div><div class="eq" id="nx-out" aria-live="polite"></div>'),
   'limit': '막대 값은 교안의 예시를 설명하려고 만든 수치입니다. 실제 모델의 확률이 아닙니다.',
   'quiz': [{'q': 'LLM이 두 번째 단어를 고를 때 쓰는 정보는?', 'o': ['질문만', '질문 + 방금 만든 첫 단어', '정답 데이터베이스'], 'a': 1, 'why': '이미 만든 단어도 다음 단어를 고르는 힌트가 됩니다.'}]},

  {'id': 'sec-2-7', 'title': 'LLM 학습 3단계 — 사전학습 → 다음 토큰 → 미세조정', 'tags': ['원리: 학습 단계', '일상: 신입 교육'],
   'pair': ('일상으로 치면', '신입이 ① 업계 책과 문서를 폭넓게 읽고 ② 다음에 무슨 일이 올지 예측하는 감을 키운 뒤 ③ 우리 회사 말투와 규정을 따로 배운다.',
            'LLM에서는', '① 사전학습: 대규모 글에서 표현이 함께 나오는 경향을 쌓는다 ② 다음 토큰 예측 능력이 생긴다 ③ 미세조정: 응답 톤·과업·안전 정책을 다듬는다.'),
   'body': ['사전학습은 지식 저장소를 만드는 일이라기보다, 언어 패턴에 대한 폭넓은 감각을 만드는 일입니다. 외우지 않고 확률 분포로 흡수합니다.',
            '그래서 AI는 "어디서 읽었는지"를 정확히 꺼내 오지 못할 수 있습니다. 출처가 필요한 답은 따로 확인해야 하는 이유입니다.'],
   'talk': [('moa', 'e09', '미세조정은 우리 회사 양식을 배우는 거랑 비슷하네요.'), ('doc', 'e10', '맞습니다. 12주차에 "회사 양식 프롬프트 이식"으로 비슷한 효과를 프롬프트로 냅니다.')],
   'widget': ('w2-stage', '<div class="ptitle">카드 · 세 단계가 바꾸는 것</div><div class="ctrl" id="st-bt"></div><div class="insight" id="st-out" aria-live="polite"></div>'),
   'limit': '실제 학습에는 사람 피드백 강화학습 등 더 많은 단계가 있습니다. 여기서는 교안의 3단계 틀로만 봅니다.',
   'quiz': [{'q': '응답의 말투·안전 정책을 다듬는 단계는?', 'o': ['사전학습', '다음 토큰 예측', '미세조정'], 'a': 2, 'why': '미세조정이 응답 톤과 과업 적합성을 다듬습니다.'}]},

  {'id': 'sec-2-8', 'title': 'Bot · RPA · AI는 어떻게 다른가', 'tags': ['비교: 자동화 세 종류', '현장: 사무 자동화'],
   'body': ['<div class="tw"><table class="tb"><tr><th>구분</th><th>Bot(챗봇)</th><th>RPA</th><th>생성형 AI</th></tr>'
            '<tr><td>작동</td><td>질문 패턴 매칭 → 정해진 답</td><td>정해진 사무 절차를 반복</td><td>데이터·맥락으로 예측해 생성</td></tr>'
            '<tr><td>잘하는 일</td><td>단순 안내</td><td>ERP 입력, 파일 옮기기</td><td>요약·분류·생성·질의응답</td></tr>'
            '<tr><td>약한 곳</td><td>처음 보는 질문</td><td>화면·양식이 바뀌면 멈춤</td><td>그럴듯한 오류(환각)</td></tr></table></div>',
            '15주차 자동화 흐름은 셋을 섞습니다. 정해진 시간에 파일을 가져오는 일(트리거·전달)은 RPA식, 요약·문서 생성은 생성형 AI가 맡습니다.'],
   'talk': [('robo', 'e16', '저는 셋 다입니다!'), ('fly', 'e09', '정해진 절차를 반복할 때 굳이 확률로 답하는 AI를 쓸 이유가 있을까?'), ('sia', 'e10', '일의 성격에 맞춰 고르는 게 맞겠습니다.')],
   'widget': ('w2-bot', '<div class="ptitle">분류 게임 · 이 일은 누구에게?</div><div id="bt-q" class="eq"></div><div class="ctrl"><button class="bt" data-a="0" type="button">Bot</button><button class="bt" data-a="1" type="button">RPA</button><button class="bt" data-a="2" type="button">생성형 AI</button></div><div class="eq" id="bt-out" aria-live="polite"></div>'),
   'limit': '요즘 제품들은 셋을 한 서비스에 섞어 팝니다. 이름보다 "무엇이 규칙이고 무엇이 생성인가"를 봅니다.',
   'quiz': [{'q': '매일 아침 MES 파일을 내려받아 같은 폴더에 저장하는 일에 맞는 것은?', 'o': ['Bot', 'RPA', '생성형 AI'], 'a': 1, 'why': '정해진 절차의 반복은 RPA의 일입니다.'}]},

  {'id': 'sec-2-9', 'title': '트랜스포머 — 읽는 쪽과 쓰는 쪽', 'tags': ['구조: 인코더·디코더', '일상: 통역사'],
   'pair': ('일상으로 치면', '통역사는 먼저 상대 말을 끝까지 듣고 요점을 잡은 뒤(인코더), 한 단어씩 우리말로 옮긴다(디코더).',
            '트랜스포머에서는', '인코더가 입력의 의미를 해석·요약하고, 디코더가 그것을 받아 새 문장을 한 단어씩 짓는다. 디코더는 아직 쓰지 않은 미래 단어를 가리고(마스크) 쓴다.'),
   'body': ['교안이 꼽는 네 가지 열쇠는 ① 인코더 ② 디코더 ③ 병렬 처리(한 단어씩 순서대로 읽던 방식에서 벗어남) ④ 장기 의존성(멀리 떨어진 단어를 연결)입니다.',
            '오늘날 대화형 AI의 상당수는 디코더 쪽을 중심으로 만든 구조입니다. 그래도 "입력을 해석하고 출력을 한 단어씩 만든다"는 흐름은 같습니다.'],
   'talk': [('asst', 'e09', '미래 단어를 가린다는 게 무슨 뜻이에요?'), ('doc', 'e07', '시험 정답을 미리 못 보게 가리는 것과 같습니다. 지금까지 쓴 단어만 보고 다음을 정합니다.'), ('x2', 'e09', '(…끄덕)')],
   'widget': ('w2-mask', '<div class="ptitle">실험 · 디코더는 한 단어씩, 미래는 가린 채</div><div class="ctrl"><button class="bt primary" id="mk-bt" type="button">다음 단어</button><button class="bt" id="mk-rs" type="button">처음으로</button></div><div class="eq" id="mk-out" aria-live="polite"></div>'),
   'limit': '실제 트랜스포머에는 위치 인코딩, 여러 개의 어텐션 머리, 피드포워드 층이 수십 겹 쌓입니다. 여기서는 역할만 봅니다.',
   'quiz': [{'q': '디코더가 미래 단어를 가리는 이유는?', 'o': ['계산을 빨리 하려고', '지금까지 쓴 문맥만으로 다음을 정하게 하려고', '저작권 때문에'], 'a': 1, 'why': '정답을 미리 보지 않고 순서대로 생성하게 하는 장치입니다.'}]},

  {'id': 'sec-2-10', 'title': '어텐션 — 중요한 단어에 더 집중한다', 'tags': ['원리: 어텐션', '3D: 위 빛줄기'],
   'fx': {'q': '"가중치 0.32"는 무슨 숫자예요? 다 더하면 1이에요?',
          'school': '가중평균과 비율(중학 수학), 지수함수(고등 수학)',
          'eq': '다음 단어의 재료 = Σ (가중치ᵢ × 단어ᵢ의 정보) · <b>가중치의 합 = 1</b>',
          'rows': [('가중치ᵢ', '단어 i를 얼마나 볼지 (0~1)'), ('Σ', '모두 더한다'), ('합 = 1', '주의력 100%를 나눠 갖는다')],
          'calc': '"나는 오늘 아침에 카페에서 따뜻한 커피를 마셨다" 다음 「맛있었다」를 고를 때, 교안 예시는 「커피를」 0.32, 「카페에서」 0.28이 가장 큽니다. 둘만 합쳐도 주의력의 60%입니다.',
          'comment': '주의력 100%를 나눠서 커피랑 카페에 몰아준 거군요!'},
   'body': ['어텐션 덕분에 AI는 긴 문장에서도 길을 잃지 않습니다. 프롬프트에서도 핵심 정보를 분명히 적고, 덜 중요한 말을 줄이면 결과가 안정됩니다.'],
   'talk': [('fly', 'e09', '그럼 프롬프트에 쓸데없는 말을 잔뜩 넣으면?'), ('doc', 'e10', '주의력이 흩어질 수 있습니다. 위 3D 장면에서도 「HSG-A8P」「5V」 쪽 빛줄기가 굵습니다.'), ('asst', 'e07', '아래 막대에서 단어 하나를 지우면 나머지 비율이 어떻게 바뀌는지 볼게요.')],
   'widget': ('w2-att', '<div class="ptitle">실험 · 어텐션 가중치 (교안 예시값 기반)</div><div class="ctrl" id="at-bt"></div><div class="cwrap"><svg id="at-svg"></svg></div><div class="eq" id="at-out" aria-live="polite"></div>'),
   'limit': '「커피를」 0.32, 「카페에서」 0.28 외의 값은 교안 그림에 맞춰 이 페이지가 정한 설명용 값입니다. 실제 모델은 여러 머리·여러 층의 가중치를 씁니다.',
   'quiz': [{'q': '어텐션 가중치의 합은?', 'o': ['단어 수', '1', '100'], 'a': 1, 'why': '주의력을 나눠 갖는 비율이라 합이 1입니다.'}]},

  {'id': 'sec-2-11', 'title': '환각과 검수 — 그럴듯하게 틀린다', 'tags': ['주의: 환각', '방법: 숫자 검산'],
   'why': {'problem': 'AI는 "사실을 꺼내는" 것이 아니라 "자연스러운 다음 말"을 고릅니다.',
           'limit': '그래서 문장은 매끄러워도 숫자·출처·계산이 틀릴 수 있습니다. 매끄러움은 정확성의 증거가 아닙니다.',
           'solve': '숫자가 든 답부터 검산합니다. 비율은 분자·분모로 다시 나누고, 추세는 직접 이어 보고, 합계는 원본과 대조합니다.',
           'easy': '말 잘하는 신입의 보고도 숫자는 한 번 계산기로 두드려 본다.'},
   'body': ['교안 사례 5의 기대 출력을 검산해 봅니다. 진동이 14:20 0.15g → 14:23 0.40g로 올랐으니 1분에 평균 약 0.083g씩 올랐습니다.',
            '이 추세가 이어지면 14:28에는 약 0.82g입니다. 교안 예시의 "중립 0.70g"과 다릅니다. 임계 0.50g 도달도 원자료의 "약 14:25"를 이 페이지에서는 "14:24~14:25 사이(약 14:24)"로 바꿉니다.',
            '이 차이는 교안이 틀렸다는 뜻이 아니라, AI가 내놓을 법한 "그럴듯한 예시 답"도 검산하면 어긋날 수 있다는 좋은 연습 문제입니다. 실습 리포트에서 자세히 봅니다.'],
   'talk': [('robo', 'e24', '0.70g이 틀렸다고요? 저는 그대로 보고서에 붙였는데…'), ('fly', 'e10', '네 개 점으로 직선을 그어 보면 금방 보여.'), ('asst', 'e07', '아래에서 직접 이어 볼게요.')],
   'widget': ('w2-vib', '<div class="ptitle">검산 · 진동 로그를 직선으로 이어 보기</div><div class="cwrap"><svg id="vb-svg"></svg></div><div class="ctrl"><div class="group"><span class="glabel">예측 시각</span><input type="range" min="24" max="30" value="28" id="vb-t"><span class="val" id="vb-vt"></span></div></div><div class="eq" id="vb-out" aria-live="polite"></div>'),
   'limit': '직선 연장도 하나의 가정입니다. 실제 설비 진동은 가속될 수도, 멈출 수도 있습니다. 예측은 점검 행동의 근거로만 씁니다.',
   'quiz': [{'q': 'AI 답에서 가장 먼저 검산할 곳은?', 'o': ['문장 길이', '숫자·비율·시각이 든 부분', '말투'], 'a': 1, 'why': '매끄러운 문장보다 숫자가 틀리기 쉽고, 틀리면 비용이 큽니다.'}]},

  {'id': 'sec-2-12', 'title': '프롬프트 5원칙 — 역할·맥락·조건·형식·예시', 'tags': ['방법: 프롬프트 설계', '현장: 작업지시서 요약'],
   'pair': ('일상으로 치면', '외주 업체에 일을 맡길 때 "알아서 잘"보다 누가, 어떤 상황에서, 어떤 조건으로, 어떤 양식으로, 예시처럼 해 달라고 말해야 결과가 맞는다.',
            '프롬프트에서는', '① 역할 ② 맥락 ③ 조건 ④ 형식 ⑤ 예시를 채우면 AI가 고를 단어의 확률 구조가 원하는 쪽으로 좁혀진다.'),
   'body': ['훌륭한 프롬프트는 기계에 규칙을 주입하는 것이 아니라, 모델이 알맞은 패턴과 맥락을 꺼내도록 환경을 설계하는 일입니다.',
            '아래 조립기에서 다섯 칸을 하나씩 켜 보세요. 켤수록 프롬프트가 길어지지만, 답이 흔들릴 여지가 줄어듭니다.'],
   'talk': [('moa', 'e12', '다섯 칸을 다 켜니 신입용 요약 카드가 딱 나와요!'), ('robo', 'e07', '저는 "요약해 줘" 한 줄로도 충분했습니다만…'), ('fly', 'e09', '그 한 줄이 매번 같은 양식으로 나와? 4주차에 형식·예시 칸이 왜 중요한지 또 보게 될 거야.'), ('x3', 'e16', '(삐빅)')],
   'widget': ('w2-five', '<div class="ptitle">조립기 · 5원칙 프롬프트</div><div class="ctrl" id="fv-bt"></div><div class="prompt" id="fv-p"></div><div class="eq" id="fv-out" aria-live="polite"></div>'),
   'explain': ['조립된 프롬프트는 그대로 복사해 QWEN·ChatGPT 등에 붙여 쓸 수 있습니다. 결과는 반드시 원문과 대조합니다(토큰 목록이 원문 순서와 같은지, 수치·단위가 바뀌지 않았는지).',
               '이 다섯 칸은 4주차 분류·회귀 프롬프트 카드(역할·출력 형식·few-shot 예시)로 그대로 이어집니다.'],
   'limit': '5원칙은 출발점입니다. 답이 흔들리면 ④ 형식을 더 좁히거나 ⑤ 예시를 늘리고, 그래도 틀리면 데이터나 질문 자체를 의심합니다.',
   'quiz': [{'q': '"JSON 한 줄로, 항목은 세 개"는 5원칙 중 무엇인가?', 'o': ['역할', '형식', '맥락'], 'a': 1, 'why': '출력의 모양을 정하는 것은 형식입니다.'}]},

  {'id': 'sec-2-13', 'title': '제조 현장 여섯 사례 — 원리 지도', 'tags': ['정리: 6사례 = 6원리', '실습 리포트로'],
   'body': ['교안의 부록은 제조 사례 여섯 개를 원리 하나씩에 연결합니다.',
            '<div class="tw"><table class="tb"><tr><th>사례</th><th>도구(교안)</th><th>원리</th></tr>'
            '<tr><td>1 작업지시서 → 5줄 요약</td><td>QWEN</td><td>토큰화 (2.2)</td></tr>'
            '<tr><td>2 「떨림」 두 문장</td><td>ChatGPT</td><td>맥락·임베딩 (2.4)</td></tr>'
            '<tr><td>3 4개 언어 안전 표지판</td><td>Gemini</td><td>의미 공간 (2.3)</td></tr>'
            '<tr><td>4 불량 500건 숨은 조합</td><td>Claude</td><td>규칙 vs 학습 (2.5)</td></tr>'
            '<tr><td>5 진동 로그 다음 값</td><td>ChatGPT</td><td>다음 토큰 예측 (2.6, 2.11)</td></tr>'
            '<tr><td>6 회의록 요약</td><td>Gemini</td><td>어텐션 (2.10)</td></tr></table></div>',
            '원자료의 도구 이름 "CLADE"는 이 페이지에서 "Claude"로 바꿉니다. 어떤 도구를 써도 프롬프트는 그대로 작동한다는 것이 이 과목의 원칙입니다.'],
   'talk': [('doc', 'e08', '여섯 사례의 프롬프트와, 숫자가 든 예시 답을 검산한 결과는 실습 리포트에 모았습니다.'), ('sia', 'e07', '순서대로 따라 하시면 됩니다.')],
   'widget': ('w2-six', '<div class="ptitle">지도 · 사례를 누르면 원리 칸으로 이동</div><div class="ctrl" id="sx-bt"></div>'),
   'limit': '사례의 "기대 출력"은 교안 예시입니다. 여러분이 직접 돌린 결과와 다를 수 있고, 다른 것이 정상입니다.',
   'quiz': [{'q': '「위험」이 4개 언어에서 같은 근처에 모인다는 것은 어떤 원리인가?', 'o': ['토큰화', '임베딩(의미 공간)', '미세조정'], 'a': 1, 'why': '뜻이 같으면 언어가 달라도 의미 공간에서 가깝습니다.'}]},
 ],
 'duel': {
   'q': '세 겹 조합 불량, 규칙으로 잡을까 학습으로 잡을까?',
   'intro': [('doc', 'e07', '불량 리포트 500건이 있습니다. 주판봇은 변수 하나씩 기준을 세우는 규칙 방식, 초파리 연구원은 조합까지 훑는 학습 방식입니다.'), ('moa', 'e12', '시작합니다!')],
   'fly': '조건을 겹쳐서 봐야 해. 한 칸씩 보면 안 보이는 게 있어.',
   'robo': '변수 하나씩 기준선을 그으면 충분! 규칙이 명확하잖아!',
   'widget': 'w2-duel',
   'panel': '<div class="ptitle">시뮬레이션 · 가상 불량 리포트 500건 (시드 고정)</div><button class="bt primary" id="du2-run" type="button">분석 실행</button><div class="kpis" id="du2-k"></div><div class="tw" id="du2-tb"></div>',
   'verdict': '버튼을 누르면 판정이 나옵니다.',
   'after': [('x1', 'e01', '(짝짝)'), ('x2', 'e09', '(…)'), ('x3', 'e04', '(삐빅?)')],
 },
 'summary': {
   'head': ['원리', '한 줄', '프롬프트에서는'],
   'rows': [['토큰화', '글을 조각과 숫자 ID로', '문장 구성의 기본 단위 감각'],
            ['임베딩', '조각에 의미 좌표', '표현 선택이 의미 관계를 바꾼다'],
            ['맥락', '주변 단어가 뜻을 옮긴다', '상황 설명을 맥락 칸에'],
            ['패턴 학습', '데이터에서 경향을 익힌다', '규칙 명령이 아니라 맥락 설계'],
            ['다음 토큰 예측', '확률로 하나씩 고른다', '입력 순서·조건이 결과를 바꾼다'],
            ['어텐션', '중요한 단어에 집중', '핵심 정보를 분명히'],
            ['환각·검수', '그럴듯하게 틀린다', '숫자부터 검산']],
   'limits': ['의미 공간 지도, 다음 단어 확률, 어텐션 막대의 값은 대부분 설명용 값입니다(교안 예시 0.32·0.28 제외).',
              '실제 모델 구조와 학습 과정은 이 페이지의 3단계·4열쇠보다 훨씬 복잡합니다.',
              '대결의 불량 리포트 500건은 시드를 고정해 만든 가상 데이터입니다.'],
 },
 'outro': [('doc', 'e16', '오늘의 결론입니다. AI는 정답을 꺼내는 게 아니라 맥락에 맞춰 다음 말을 고릅니다. 그래서 프롬프트는 환경 설계이고, 검수는 필수입니다.'),
           ('asst', 'e01', '5원칙 조립기 프롬프트를 복사해서 직접 돌려 볼게요!'),
           ('fly', 'e10', '돌린 결과에 숫자가 있으면 꼭 검산해. 리포트에 방법이 있어.'),
           ('robo', 'e14', '0.70g… 다음부터는 직선부터 그어 보겠습니다.')],
 'sources': [('강의 교안', '스마트 제조 2주차 제1장 「생성형 AI의 개념·작동원리」(ver10, 63장) — 담당교수 안상선'),
             ('3D 캐릭터', 'fruitfly-lab-expressions · chars3d/lab3d.js v1.0')],
 'notes': '토큰 ID, 의미 공간 좌표, 다음 단어 확률, 어텐션 가중치(0.32·0.28 제외), 대결의 불량 리포트 500건은 설명용 값·가상 데이터입니다.',
 'practice': ('practice.html', '여섯 사례를 돌리고, 숫자 답을 검산하다'),
}

CH['js'] = r'''
W['w2-tools']=function(b){var T=['QWEN','ChatGPT','Gemini','Claude','DeepSeek'],bt=b.querySelector('#tl-bt'),o=b.querySelector('#tl-out');T.forEach(function(t){var x=document.createElement('button');x.className='bt';x.textContent=t;x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y){y.classList.remove('on')});x.classList.add('on');o.innerHTML='<p class="g"><b>'+t+'</b>도 같은 순서: ① 입력 → ② 토큰화 → ③ 임베딩·어텐션 처리 → ④ 다음 토큰 확률 → ⑤ 반복해 응답</p><p class="a">다른 점: 조각 사전, 학습한 글, 미세조정 방향 → 같은 프롬프트에도 답의 품질이 다를 수 있음</p>';};bt.appendChild(x);});bt.firstChild.click();};
W['w2-tok']=function(b){var i=b.querySelector('#tk-in'),o=b.querySelector('#tk-out'),n=b.querySelector('#tk-n'),m=0;function split(s){if(m==0)return s.split(/\s+/).filter(Boolean);if(m==1)return s.match(/[A-Z]{1,4}-?[A-Z0-9]*\d[\w-]*|\d+(?:\.\d+)?[a-zA-Z가-힣]*|\d+\/\d+|[×—.,/]|[가-힣]+|[A-Za-z]+/g)||[];return s.match(/[가-힣]{1,2}|[A-Za-z]{1,3}|\d{1,2}|[^\s]/g)||[];}function f(){var t=split(i.value);var h=0;o.innerHTML=t.map(function(x){h=0;for(var k=0;k<x.length;k++)h=(h*31+x.charCodeAt(k))%5000;return '<span class="tag" style="border-color:var(--stain);color:#f1b5f1" title="ID '+h+'">'+x.replace(/</g,'&lt;')+'<small style="color:var(--muted)"> #'+h+'</small></span>';}).join('');n.innerHTML='조각 수 <b>'+t.length+'개</b> · 방식: '+['띄어쓰기','부품·수치·단위','글자 묶음'][m]+' · #뒤 숫자는 예시 ID';}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){m=+x.dataset.m;b.querySelectorAll('.ctrl .bt').forEach(function(y){y.classList.toggle('on',y===x)});f();};});i.oninput=f;f();};
W['w2-emb']=function(b){var P=[['위험',2,8],['Danger',2.3,7.6],['Nguy hiểm',1.6,7.4],['危险',2.6,8.3],['경고',3.1,7.1],['주의',3.4,6.6],['고압',4.2,7.8],['추락',3.6,8.6],['커피',8,1.2],['카페',8.6,1.8],['사과',7.2,2.6],['베어링',6.4,6.2],['진동',5.8,5.6],['떨림',5.2,5]];var s=b.querySelector('#em-svg'),o=b.querySelector('#em-out'),NS='http://www.w3.org/2000/svg';var X=function(x){return 30+x*55},Y=function(y){return 285-y*30};P.forEach(function(p,i){var g=document.createElementNS(NS,'g');g.style.cursor='pointer';var c=document.createElementNS(NS,'circle');c.setAttribute('cx',X(p[1]));c.setAttribute('cy',Y(p[2]));c.setAttribute('r',7);c.setAttribute('fill',i<8?'#f0604d':i<11?'#f1b646':'#82b8ff');var t=document.createElementNS(NS,'text');t.setAttribute('x',X(p[1])+10);t.setAttribute('y',Y(p[2])+4);t.textContent=p[0];t.style.fill='#eceaf3';t.style.fontSize='13px';g.appendChild(c);g.appendChild(t);g.setAttribute('tabindex','0');g.onclick=g.onkeydown=function(e){if(e.type=='keydown'&&e.key!=='Enter')return;var d=P.map(function(q){return [q[0],Math.hypot(q[1]-p[1],q[2]-p[2])]}).filter(function(q){return q[0]!==p[0]}).sort(function(a,b){return a[1]-b[1]}).slice(0,3);o.innerHTML='「<b>'+p[0]+'</b>」과 가까운 단어: '+d.map(function(q){return q[0]+' <i>('+q[1].toFixed(1)+')</i>'}).join(', ');};s.appendChild(g);});};
W['w2-ctx']=function(b){var C=[['1라인 모터에서','기계',['베어링 마모 → 축 흔들림','커플링 정렬 불량 → 회전 불균형','로터 불균형 → 원심 진동']],['1라인 작업자가 손','사람',['피로 누적 → 근육 미세 진동','저혈당 / 카페인 과다','냉방 저체온 → 손 떨림']],['1라인 컴프레서에서','기계',['흡입 밸브·베어링 마모','고정 볼트 풀림','배관 공진']]];var bt=b.querySelector('#cx-bt'),q=b.querySelector('#cx-q'),o=b.querySelector('#cx-out');C.forEach(function(c,i){var x=document.createElement('button');x.className='bt';x.textContent=c[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y,j){y.classList.toggle('on',i==j)});q.innerHTML='프롬프트: "<em>'+c[0]+'</em> <b>떨림</b>이 심해. 원인 3가지 추정해줘."';o.innerHTML='<p class="'+(c[1]=='기계'?'m':'r')+'"><b>「떨림」 좌표 → '+c[1]+' 쪽</b></p>'+c[2].map(function(a,k){return '<p>'+(k+1)+'. '+a+'</p>'}).join('');};bt.appendChild(x);});bt.firstChild.click();};
W['w2-comb']=function(b){var k=b.querySelector('#cb-k'),v=b.querySelector('#cb-v'),o=b.querySelector('#cb-out');function f(){b.querySelector('#cb-vk').textContent=k.value;b.querySelector('#cb-vv').textContent=v.value;var n=Math.pow(+v.value,+k.value),pairs=0,K=+k.value,V=+v.value;for(var a=1;a<=3&&a<=K;a++){var c=1;for(var j=0;j<a;j++)c=c*(K-j)/(j+1);pairs+=c*Math.pow(V,a);}o.innerHTML='모든 값의 조합 <b>'+n.toLocaleString()+'가지</b> · 세 겹까지만 규칙으로 써도 <em>'+Math.round(pairs).toLocaleString()+'개</em> 규칙 필요';}k.oninput=v.oninput=f;f();};
W['w2-next']=function(b){var C=[['조건 없음','사과에 대해 설명해줘',[['비타민',.30],['품종',.22],['재배',.18],['영양소',.15],['새빨간',.05],['달콤한',.05],['동화',.05]]],['+ 유치원생·동화처럼','사과에 대해 유치원생이 이해하기 쉽게 동화처럼 설명해줘',[['비타민',.04],['품종',.03],['재배',.02],['영양소',.03],['새빨간',.32],['달콤한',.30],['동화',.26]]],['+ SNS 광고 카피 3개','사과를 SNS 광고 카피 3개로 써줘',[['비타민',.08],['품종',.05],['재배',.03],['영양소',.06],['새빨간',.26],['달콤한',.34],['동화',.18]]]];var bt=b.querySelector('#nx-bt'),s=b.querySelector('#nx-svg'),o=b.querySelector('#nx-out');C.forEach(function(c,i){var x=document.createElement('button');x.className='bt';x.textContent=c[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y,j){y.classList.toggle('on',i==j)});Chart.bars(s,{labels:c[2].map(function(d){return d[0]}),series:[{name:'다음 단어 확률',color:'#d672d6',values:c[2].map(function(d){return d[1]})}],min:0,max:.4,values:true,fmt:function(v){return v.toFixed(2)},h:220});o.innerHTML='프롬프트: "'+c[1]+'" → 1위 <b>'+c[2].slice().sort(function(a,b){return b[1]-a[1]})[0][0]+'</b>';};bt.appendChild(x);});bt.firstChild.click();};
W['w2-stage']=function(b){var S=[['① 사전학습','책·기사·웹 문서 등 대규모 글에서 표현이 함께 나오는 경향을 쌓습니다. 외우지 않고 확률 분포로 흡수합니다.'],['② 다음 토큰 예측','입력과 이미 만든 글을 보고 다음 후보 중 가능성이 높은 토큰을 고릅니다. 반복해 문장이 됩니다.'],['③ 미세조정','응답 톤(격식·친근), 과업(요약·번역·코드), 안전 정책(거절 응답)을 다듬습니다.']];var bt=b.querySelector('#st-bt'),o=b.querySelector('#st-out');S.forEach(function(s,i){var x=document.createElement('button');x.className='bt';x.textContent=s[0];x.onclick=function(){bt.querySelectorAll('.bt').forEach(function(y,j){y.classList.toggle('on',j<=i)});o.innerHTML='<p class="'+['r','m','g'][i]+'"><b>'+s[0]+'</b> — '+s[1]+'</p>';};bt.appendChild(x);});bt.firstChild.click();};
W['w2-bot']=function(b){var Q=[['고객이 "영업시간?"을 물으면 정해진 답을 보낸다',0],['매일 08:00 MES 실적 파일을 내려받아 공유 폴더에 저장',1],['어제 불량 메모 30줄을 읽고 원인 후보 3개를 요약',2],['ERP 화면에 발주 번호 200개를 차례로 입력',1],['외국인 작업자용 안전 수칙을 베트남어로 쉽게 풀어 쓰기',2],['"비밀번호 초기화" 문의에 안내 링크 보내기',0]];var i=0,sc=0,q=b.querySelector('#bt-q'),o=b.querySelector('#bt-out');function show(){q.innerHTML='('+(i+1)+'/'+Q.length+') '+Q[i][0];}b.querySelectorAll('.ctrl .bt').forEach(function(x){x.onclick=function(){var a=+x.dataset.a,ok=a===Q[i][1];if(ok)sc++;o.innerHTML=(ok?'✔ 맞습니다.':'✘ 정답은 <b>'+['Bot','RPA','생성형 AI'][Q[i][1]]+'</b>입니다.')+' 점수 '+sc+'/'+(i+1);i=(i+1)%Q.length;if(i==0){sc=0;}show();};});show();};
W['w2-mask']=function(b){var S=['작업자는','압착','후','인출력을','반드시','확인한다.'],k=0,o=b.querySelector('#mk-out');function f(){o.innerHTML=S.map(function(w,i){return i<k?'<b>'+w+'</b>':i==k?'<em>[?]</em>':'<span style="color:#555">■■</span>'}).join(' ')+(k<S.length?' — 다음 단어를 고를 때 보는 것: 앞의 <b>'+k+'개</b>뿐':' — 완성');}b.querySelector('#mk-bt').onclick=function(){if(k<S.length)k++;f();};b.querySelector('#mk-rs').onclick=function(){k=0;f();};f();};
W['w2-att']=function(b){var A=[['나는',.05],['오늘',.04],['아침에',.09],['카페에서',.28],['따뜻한',.12],['커피를',.32],['마셨다',.10]],on=A.map(function(){return 1}),bt=b.querySelector('#at-bt'),s=b.querySelector('#at-svg'),o=b.querySelector('#at-out');A.forEach(function(a,i){var x=document.createElement('button');x.className='bt on';x.textContent=a[0];x.setAttribute('aria-pressed','true');x.onclick=function(){on[i]=1-on[i];x.classList.toggle('on',!!on[i]);x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var tot=A.reduce(function(t,a,i){return t+(on[i]?a[1]:0)},0)||1;var v=A.map(function(a,i){return on[i]?a[1]/tot:0});Chart.bars(s,{labels:A.map(function(a){return a[0]}),series:[{name:'가중치(합 1)',color:'#f0604d',values:v}],min:0,max:.6,values:true,fmt:function(x){return x.toFixed(2)},h:220});var top=v.indexOf(Math.max.apply(null,v));o.innerHTML='「맛있었다」를 고를 때 가장 많이 보는 단어: <b>'+A[top][0]+'</b> ('+v[top].toFixed(2)+') · 끈 단어의 몫은 나머지에 다시 나뉩니다.';}f();};
W['w2-vib']=function(b){var t=[0,1,2,3],v=[.15,.22,.31,.40];var n=4,mx=1.5,my=v.reduce(function(a,c){return a+c})/4,sxy=0,sxx=0;t.forEach(function(x,i){sxy+=(x-mx)*(v[i]-my);sxx+=(x-mx)*(x-mx)});var sl=sxy/sxx,ic=my-sl*mx;var s=b.querySelector('#vb-svg'),r=b.querySelector('#vb-t'),o=b.querySelector('#vb-out');function f(){var T=+r.value;b.querySelector('#vb-vt').textContent='14:'+T;var L=[],S1=[],S2=[];for(var m=20;m<=30;m++){L.push('14:'+m);S1.push(m<=23?v[m-20]:null);S2.push(ic+sl*(m-20));}Chart.line(s,{labels:L,series:[{name:'실측',color:'#5ee39c',values:S1,dots:true},{name:'직선 연장',color:'#f1b646',values:S2,dash:'5 4'}],ref:.5,min:0,max:1.0,h:220});var p=ic+sl*(T-20),cross=20+(.5-ic)/sl;o.innerHTML='기울기 <b>'+sl.toFixed(3)+'g/분</b> · 14:'+T+' 예측 <b>'+p.toFixed(2)+'g</b>'+(T==28?' (교안 예시 "중립 0.70g"과 <em>'+(p-.7).toFixed(2)+'g</em> 차이)':'')+' · 0.50g 도달 ≈ <i>14:'+Math.floor(cross)+':'+String(Math.round((cross%1)*60)).padStart(2,'0')+'</i>';}r.oninput=f;f();};
W['w2-five']=function(b){var K=[['역할','#역할\n너는 제조 현장 작업지시서를 신입 작업자용으로 정리하는 도우미다.'],['맥락','#맥락\n케이블 하네스 라인. 신입 작업자는 입사 1주차이고 부품 코드에 익숙하지 않다.'],['조건','#조건\n원문의 수치·단위·부품 코드는 바꾸지 않는다. 모르는 것은 "확인 필요"로 적는다.'],['형식','#형식\n1) 토큰 목록(/로 구분) 2) 총 조각 수 3) 신입용 5줄 요약(①~⑤)'],['예시','#예시\n입력: "A1-0001 전선 1m 절단" → 토큰: A1-0001 / 전선 / 1m / 절단 → 총 4조각']],on=[1,0,0,0,0],bt=b.querySelector('#fv-bt'),p=b.querySelector('#fv-p'),o=b.querySelector('#fv-out');K.forEach(function(k,i){var x=document.createElement('button');x.className='bt';x.textContent=(i+1)+' '+k[0];x.setAttribute('aria-pressed',on[i]?'true':'false');x.onclick=function(){on[i]=1-on[i];x.setAttribute('aria-pressed',on[i]?'true':'false');f();};bt.appendChild(x);});function f(){var t=K.filter(function(k,i){return on[i]}).map(function(k){return k[1]}).join('\n\n')+'\n\n#입력\n"B7-2203 케이블 2.5m×4가닥 압착. 단자 HSG-A8P. 인출력 시험 5V/10mA 이상 — 불량 허용 0/100."';p.textContent=t;p.setAttribute('data-raw',t);if(!p.querySelector('.copy')){}var n=on.reduce(function(a,c){return a+c},0);o.innerHTML='켠 원칙 <b>'+n+'/5</b> · '+(n<3?'<em>답의 양식이 매번 달라질 수 있습니다.</em>':n<5?'답이 안정되기 시작합니다.':'<b>다섯 칸 완성</b> — 4주차 프롬프트 카드의 뼈대입니다.');var c=document.createElement('button');c.className='bt copy';c.type='button';c.textContent='복사';c.onclick=function(){navigator.clipboard&&navigator.clipboard.writeText(t);c.textContent='복사됨';};p.appendChild(c);}f();};
W['w2-six']=function(b){var S=[['1 작업지시서','sec-2-2'],['2 떨림','sec-2-4'],['3 안전 표지','sec-2-3'],['4 불량 조합','sec-2-5'],['5 진동 로그','sec-2-11'],['6 회의록','sec-2-10']],bt=b.querySelector('#sx-bt');S.forEach(function(s){var a=document.createElement('a');a.className='bt';a.href='#'+s[1];a.textContent=s[0];a.style.textDecoration='none';bt.appendChild(a);});};
W['w2-duel']=function(b){b.querySelector('#du2-run').onclick=function(){var r=rng(500),D=[];var days=['월','화','수','목','금'],lots=['A','B','C'];for(var i=0;i<500;i++){var d=days[Math.floor(r()*5)],pm=r()<.4,nw=r()<.3,lt=lots[Math.floor(r()*3)];var p=.08+(d=='금'?.04:0)+(pm?.03:0)+(nw?.04:0)+(lt=='B'?.03:0);if(d=='금'&&pm&&nw&&lt=='B')p=.85;D.push([d,pm,nw,lt,r()<p]);}function rate(f){var s=D.filter(f);return [s.filter(function(x){return x[4]}).length,s.length];}var single=[['금요일',function(x){return x[0]=='금'}],['오후',function(x){return x[1]}],['신입',function(x){return x[2]}],['로트 B',function(x){return x[3]=='B'}]].map(function(s){var q=rate(s[1]);return [s[0],q[0],q[1],q[0]/q[1]]});var all=rate(function(){return true});var combo=rate(function(x){return x[0]=='금'&&x[1]&&x[2]&&x[3]=='B'});var best=single.slice().sort(function(a,b){return b[3]-a[3]})[0];b.querySelector('#du2-tb').innerHTML='<table class="tb"><tr><th>조건</th><th>불량/건수</th><th>불량률</th></tr><tr><td>전체</td><td class="n">'+all[0]+'/'+all[1]+'</td><td class="n">'+(all[0]/all[1]*100).toFixed(1)+'%</td></tr>'+single.map(function(s){return '<tr><td>'+s[0]+' (하나만)</td><td class="n">'+s[1]+'/'+s[2]+'</td><td class="n">'+(s[3]*100).toFixed(1)+'%</td></tr>'}).join('')+'<tr><td><b>금요일+오후+신입+로트 B</b></td><td class="n">'+combo[0]+'/'+combo[1]+'</td><td class="n"><b>'+(combo[0]/combo[1]*100).toFixed(1)+'%</b></td></tr></table>';b.querySelector('#du2-k').innerHTML='<div class="kpi r"><b>'+(best[3]*100).toFixed(0)+'%</b><span>주판봇: 하나씩 본 최고 불량률('+best[0]+')</span></div><div class="kpi g"><b>'+(combo[0]/combo[1]*100).toFixed(0)+'%</b><span>초파리: 네 조건이 겹친 곳</span></div><div class="kpi a"><b>'+combo[1]+'건</b><span>조합에 해당하는 리포트 수</span></div><div class="kpi m"><b>'+(all[0]/all[1]*100).toFixed(0)+'%</b><span>전체 평균 불량률</span></div>';var v=document.getElementById('verdict');v.innerHTML='';var s=document.createElement('div');s.className='say';s.setAttribute('data-who','doc');s.innerHTML='<img class="who" alt="" aria-hidden="true"><div class="bub"><b class="name">박사</b><p></p></div>';s.querySelector('img').src=Cast.src('doc','e10');s.querySelector('p').innerHTML='초파리 연구원 승. 변수를 하나씩 보면 불량률이 최고 '+(best[3]*100).toFixed(0)+'%에 그치지만, 네 조건이 겹친 '+combo[1]+'건에서는 '+(combo[0]/combo[1]*100).toFixed(0)+'%입니다. 다만 '+combo[1]+'건은 적은 표본이라, 다음 달 데이터로 다시 확인하는 것까지가 학습 방식의 몫입니다.';v.appendChild(s);};};
'''

# ── 실습 리포트 (발견편) ───────────────────────────────────────────
P1 = '''#역할
너는 제조 현장 작업지시서를 신입 작업자용으로 정리하는 도우미다.
#입력
"B7-2203 케이블 2.5m×4가닥 압착. 단자 HSG-A8P. 인출력 시험 5V/10mA 이상 — 불량 허용 0/100."
#요청
1) 위 문장에서 부품·수치·단위를 각각 한 조각(토큰)으로 분리해 나열.
2) 총 몇 조각인지 세기.
3) 그 조각들을 다시 조합해 신입 작업자용 5줄 요약.'''
P2 = '''# 프롬프트 A
"1라인 모터에서 떨림이 심하고 진동이 커졌어. 원인 3가지 추정해줘."

# 프롬프트 B
"1라인 작업자가 손 떨림이 심해 정밀 작업이 어려워. 원인 3가지 추정해줘."'''
P3 = '''#역할
너는 다국적 작업자 대상 산업 안전 표지판 번역 도우미다.
#요청
다음 표지 문구를 한국어 · 영어 · 베트남어 · 중국어 네 언어로 번역해 표로 정리:
① "고압 · 접근 금지" ② "회전체 주의" ③ "화학물질 취급"
번역 후 각 언어에서 「위험」에 해당하는 단어를 굵게 표시해라.'''
P4 = '''# 첨부
quality_report_2025Q3.csv (500행 · 컬럼: 날짜, 시간, 라인, 작업자, 재료 로트, 결함 종류)
# 요청
1) 데이터에서 2개 이상 조건이 함께 나타날 때 불량률이 급증하는 패턴 3개를 찾아라.
2) 각 패턴에 대해 (조건 조합 · 불량률 · 발생 건수)를 표로.
3) 각 패턴에 대한 가설적 원인과 확인 방법 제시.'''
P5 = '''#역할
너는 설비 진동 데이터를 분석해 다음 값을 예측하는 정비 도우미다.
# 입력 로그
14:20 → 0.15g / 14:21 → 0.22g / 14:22 → 0.31g / 14:23 → 0.40g
# 요청
1) 5분 뒤(14:28) 진동값을 확률 분포로 3가지 시나리오 제시 (낙관·중립·비관)
2) 임계값 0.50g 도달 예상 시각을 계산
3) 현재 시점에서 정비반장이 취해야 할 행동 3가지
4) (추가) 1)과 2)의 숫자를 직선 추세로 다시 계산해 서로 맞는지 스스로 점검하라.'''
P6 = '''# 첨부
weekly_quality_meeting_2025W37.pdf (10페이지)
# 요청
1) 회의록을 5줄로 요약 — 결정 사항만.
2) 요약 시 가장 무겁게 반영한 단어 10개를 나열.
3) 반대로 거의 무시한 단어 5개도 나열.
4) 결정 사항 각각에 담당자 · 기한 표로 정리.'''

RP = {
 'title': '같은 프롬프트, 다른 답 — 숫자가 든 답부터 검산하라',
 'eyebrow': '2주차 실습 리포트 · 생성형 AI 원리 · 제조 사례 6',
 'desc': '스마트 제조 2주차 실습 리포트 — 교안의 제조 사례 6개를 돌리는 법과, 숫자가 든 기대 출력 예시 2개를 검산한 결과를 박사가 정리합니다.',
 'lead': '교안의 여섯 사례를 직접 돌릴 때 무엇을 관찰하고 무엇을 의심해야 하는지 정리했습니다. 특히 숫자가 든 "기대 출력 예시" 두 개를 검산해 보니, 둘 다 숫자가 조금씩 어긋났습니다.',
 'cover_mood': 'e07',
 'back': ('index.html', '2주차 본문으로'),
 'next': ('../w03/index.html', '3주차 생산실적 추세 분석'),
 'summary': {
   'finding': '교안 기대 출력 예시 중 숫자가 든 두 답(불량 조합 87%, 진동 0.70g·14:25)을 검산하니, 두 곳 모두 계산과 표기가 어긋났습니다.',
   'evidence': ['<span class="fact">사실</span> 사례 4의 "38건/44건 = 87%"는 실제로 86.4%입니다(<a href="#tab-r2-1">표 1</a>).',
                '<span class="fact">사실</span> 사례 5의 진동 네 점(0.15→0.40g)을 직선으로 이으면 14:28은 약 0.82g, 0.50g 도달은 약 14:24입니다. 예시는 0.70g, 14:25였습니다(<a href="#fig-r2-1">그림 1</a>).',
                '<span class="interp">해석</span> 매끄러운 문장보다 숫자가 먼저 틀립니다. 검수는 숫자가 든 줄부터 하는 것이 효율적입니다.'],
   'fig': ('fig', {'id': 'fig-r2-1', 'cap': '[그림 1] 진동 로그 네 점과 직선 연장 — 예시 답 0.70g와의 차이', 'w': 'r2-vib', 'alt': '14시 20분부터 23분까지 진동값 네 점과 직선 연장선. 14시 28분 직선 값 0.82g, 예시 답 0.70g, 임계 0.5g 선', 'src': '출처: 스마트 제조 2주차 교안 사례 5 입력 로그, 저자 계산(최소제곱 직선)'}),
 },
 'sections': [
  {'id': 'sec-r2-1', 'nav': '들어가며', 'title': '들어가며 — 왜 예시 답을 검산했나', 'blocks': [
    ('memo', 'e08', '여러분, 교안의 "기대 출력"을 정답표로 쓰고 싶은 마음은 이해합니다. 그런데 그것도 결국 AI가 낼 법한 답의 모양을 보여 주는 예시예요.'),
    ('p', '2주차 실습은 여섯 사례를 QWEN·ChatGPT·Gemini·Claude에 직접 넣어 보는 것입니다. 제가 먼저 해 본 것은 돌리기 전에 교안 예시부터 검산하는 일이었습니다.'),
    ('p', '이 리포트가 답할 질문은 세 가지입니다. ① 여섯 사례를 어떤 프롬프트로 돌리나 ② 숫자가 든 예시 답은 맞나 ③ 그렇다면 검수를 어디서부터 하나.')]},
  {'id': 'sec-r2-2', 'nav': '배경', 'title': '배경 — AI는 계산기가 아니라 다음 말 고르기', 'blocks': [
    ('p', '본문 2.6에서 본 것처럼 LLM은 다음 토큰을 확률로 고릅니다. "87%"라는 글자도 계산 결과가 아니라 그 자리에 자연스러운 토큰일 수 있습니다.'),
    ('p', '그래서 비율·추세·시각처럼 계산으로 확인할 수 있는 숫자는 사람이 다시 계산해야 합니다. 이 리포트는 그 방법을 보여 줍니다.'),
    ('memo', 'e09', '헷갈리기 쉬운 점 하나. 요즘 AI는 계산 도구를 붙여 정확히 계산하기도 합니다. 그래도 "도구를 썼는지"는 답만 봐서는 모릅니다.')]},
  {'id': 'sec-r2-3', 'nav': '방법', 'title': '방법 — 여섯 프롬프트와 두 가지 검산', 'blocks': [
    ('p', '사례별 프롬프트는 교안 그대로입니다. 사례 5에만 "스스로 점검하라"는 4번 요청을 덧붙였습니다. 복사해서 바로 쓰면 됩니다.'),
    ('html', '<h3>사례 1 · 작업지시서 → 토큰 → 5줄 요약 (QWEN)</h3>'), ('prompt', P1),
    ('html', '<h3>사례 2 · 「떨림」 두 문장 (ChatGPT)</h3>'), ('prompt', P2),
    ('html', '<h3>사례 3 · 4개 언어 안전 표지판 (Gemini)</h3>'), ('prompt', P3),
    ('html', '<h3>사례 4 · 불량 500건의 숨은 조합 (Claude)</h3><p style="font-size:14px;color:var(--muted)">원자료의 도구 이름 "CLADE"를 이 리포트에서는 "Claude"로 바꿉니다. 첨부 파일은 교안 예시 이름이며, 수업 데이터 대신 본문 대결의 가상 500건을 써도 됩니다.</p>'), ('prompt', P4),
    ('html', '<h3>사례 5 · 진동 로그 다음 값 (ChatGPT)</h3>'), ('prompt', P5),
    ('html', '<h3>사례 6 · 회의록 10쪽 → 결정 5줄 (Gemini)</h3>'), ('prompt', P6),
    ('p', '검산은 두 가지입니다. ① 비율 검산: 분자 ÷ 분모를 다시 나눕니다. ② 추세 검산: 네 점에 최소제곱 직선을 맞추고 같은 시각의 값을 읽습니다.')]},
  {'id': 'sec-r2-4', 'nav': '결과', 'title': '결과 — 숫자 답 두 개, 두 곳 모두 어긋났다', 'blocks': [
    ('html', '<h3 id="sec-r2-4-1">결과 1 · 비율 표기가 반올림과 다르다</h3>'),
    ('table', {'id': 'tab-r2-1', 'cap': '<표 1> 사례 4 기대 출력의 비율 검산 (단위: 건, %)', 'head': ['패턴', '예시 표기', '분자/분모', '다시 계산', '차이'],
               'rows': [['금요일 15~17시 · 신입 · 로트 B', '87%', '38 / 44', '86.4%', '+0.6%p'], ['월요일 08~10시 · 라인 3 · 22℃ 미만', '64%', '표기 없음', '검산 불가', '—'], ['야간조 · 로트 C · 습도 70% 이상', '52%', '표기 없음', '검산 불가', '—']],
               'src': '출처: 스마트 제조 2주차 교안 사례 4-B 기대 출력, 저자 계산'}),
    ('p', '<span class="fact">사실</span> 38 ÷ 44 = 0.8636이므로 반올림하면 86%입니다. 87%는 계산과 맞지 않습니다. 나머지 두 패턴은 건수가 없어 검산할 수 없습니다.'),
    ('p', '<span class="interp">해석</span> 0.6%p는 작아 보입니다. 하지만 "분모를 안 적은 비율"이 두 개나 있다는 점이 더 큰 문제로 읽힙니다. 프롬프트에 "불량률은 반드시 건수/전체로 함께 적어라"를 넣어야 합니다.'),
    ('html', '<h3 id="sec-r2-4-2">결과 2 · 시나리오 값이 추세와 다르다</h3>'),
    ('table', {'id': 'tab-r2-2', 'cap': '<표 2> 사례 5 기대 출력과 직선 추세 비교 (단위: g, 시각)', 'head': ['항목', '예시 답', '직선 추세(저자 계산)', '차이'],
               'rows': [['분당 상승', '0.09g', '0.083g', '+0.007g'], ['14:28 중립 시나리오', '0.70g', '0.82g', '−0.12g'], ['0.50g 도달 시각', '약 14:25', '약 14:24 (14:24:07)', '약 1분 늦게 봄']],
               'src': '출처: 스마트 제조 2주차 교안 사례 5-B, 저자 계산(최소제곱 직선: 기울기 0.083g/분, 절편 0.146g)'}),
    ('p', '<span class="fact">사실</span> 예시 답 스스로 "매 분 0.09g 상승"이라고 적었는데, 이 속도면 14:28은 0.40 + 5 × 0.09 = 0.85g입니다. 같은 답 안에서도 "중립 0.70g"과 맞지 않습니다.'),
    ('p', '<span class="interp">해석</span> 이 리포트는 이 차이를 "중립"이라는 말에 끌린 표현으로 읽습니다. 숫자 자체보다 "선형 지속"이라는 말과 값이 서로 안 맞는다는 점이 검수 포인트입니다.'),
    ('key', '숫자가 든 줄은 문장보다 먼저, 같은 답 안의 다른 숫자와 맞는지부터 봅니다.'),
    ('memo', 'e16', '임계 도달을 1분 늦게 보는 건 현장에서는 작지 않아요. 알람 시각이 1분 늦어지는 거니까요.')]},
  {'id': 'sec-r2-5', 'nav': '반론', 'title': '반론과 다른 설명', 'blocks': [
    ('p', '<span class="interp">해석</span> 첫째 반론: 예시는 설명용이라 정밀할 필요가 없다. 맞는 말입니다. 그래서 이 리포트는 교안이 틀렸다고 하지 않고, "AI가 낼 법한 답도 이렇게 어긋난다"는 연습 재료로 씁니다.'),
    ('p', '<span class="interp">해석</span> 둘째 반론: 진동은 직선이 아니라 가속될 수 있다. 그렇다면 14:28 값은 0.82g보다 더 커야 합니다. 어느 쪽이든 0.70g은 "선형 지속"이라는 설명과 맞지 않습니다.'),
    ('p', '<span class="guess">추측</span> 실제 AI에 사례 5를 돌리면, 4번 "스스로 점검" 요청이 있을 때 숫자 일관성이 좋아질 수 있습니다. 수업에서 같이 확인해 보면 좋겠습니다.')]},
  {'id': 'sec-r2-6', 'nav': '의의와 한계', 'title': '의의와 한계', 'blocks': [
    ('p', '의의: 검수를 "전부 다시 하기"가 아니라 "숫자 줄부터, 같은 답 안의 숫자끼리"로 좁히면 시간이 크게 줄어듭니다.'),
    ('p', '한계: ① 검산한 것은 교안 예시 두 개뿐입니다. ② 실제 AI를 돌린 결과가 아닙니다. ③ 진동은 네 점이라 추세 자체가 불확실합니다.'),
    ('memo', 'e09', '다음 주에는 숫자가 훨씬 많은 시계열이 나옵니다. 오늘의 습관이 바로 쓰여요.'),
    ('p', '다음 편 예고: 3주차 실습 리포트에서는 식품 공장 84개월 판매로 계절지수 12개를 직접 뽑고, 교안의 1.87·2.6을 검산합니다.')]},
 ],
 'refs': ['안상선, 「스마트 제조 2주차 제1장 생성형 AI의 개념·작동원리」 강의 교안(ver10), 2026 — 사례 1~6', '이 리포트의 계산: 사례 4 비율, 사례 5 최소제곱 직선 — 저자 계산(브라우저 안 계산과 같음)'],
 'sources': [('원자료', '스마트 제조 2주차 교안 §1.8 제조업 실습 사례'), ('계산', '저자 계산')],
 'notes': '교안 기대 출력은 예시이며, 이 리포트의 비교는 그 예시끼리의 일관성 점검입니다.',
}
RP['js'] = r'''
W['r2-vib']=function(s){var v=[.15,.22,.31,.40],sl=.083,ic=.146;var L=[],A=[],B=[],C=[];for(var m=20;m<=30;m++){L.push('14:'+m);A.push(m<=23?v[m-20]:null);B.push(ic+sl*(m-20));C.push(m==28?.70:null);}Chart.line(s,{labels:L,series:[{name:'실측',color:'#5ee39c',values:A,dots:true},{name:'직선 연장',color:'#f1b646',values:B,dash:'5 4'},{name:'예시 답(14:28)',color:'#f0604d',values:C,dots:true}],ref:.5,min:0,max:1.0,h:240});};
'''
