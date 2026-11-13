# 부록 A · 데이터 창고
import json
DS = [
 {'id': 'ds-foods', 'short': '식품 공장', 'name': '빙과·호빵·군고구마 월별 판매', 'file': 'week03_seasonal_foods.csv', 'color': '#ff86b8', 'desc': '2019-01~2025-12, 84개월', 'week': '3주',
  'cols': 'month, icecream, hoppang, sweet_potato, avg_temp(월평균 기온)', 'check': '아이스크림 8월 계절지수 1.87, 호빵 12월 2.59, 1칸 자기상관 0.79 · 12칸 0.94', 'note': '가상 데이터. 계절과 추세가 뚜렷합니다.'},
 {'id': 'ds-vacc', 'short': '백신', 'name': '호흡기 감염병 X 백신 접종량', 'file': 'week03_vaccine_1.csv', 'color': '#82b8ff', 'desc': '2014-01~2025-12, 144개월', 'week': '3주',
  'cols': 'month, doses', 'check': '연간 봉우리 2015·2019·2023, 2023→2025 약 −28%', 'note': '가상 데이터. 몇 년 주기의 순환을 보여 줍니다.'},
 {'id': 'ds-petro', 'short': '석유화학', 'name': '두바이유·나프타·에틸렌·NCC 가동률', 'file': 'week03_petrochem.csv', 'color': '#f1b646', 'desc': '2015-01~2026-08, 140개월', 'week': '3주',
  'cols': 'month, dubai($/bbl), naphtha($/t), ethylene($/t), ncc_util(%)', 'check': 'NCC 가법 계절 효과 4월 −5.7%p · 5월 −3.3%p, 스프레드 2022년부터 한 계단 하락', 'note': '가상 데이터. 사건의 시점·방향만 현실에서 가져왔습니다.'},
 {'id': 'ds-defect', 'short': '판재 판정', 'name': '불량품 판정 데이터', 'file': 'defect_judgement.csv', 'color': '#f0604d', 'desc': '1,000행 · 불량 100', 'week': '4주',
  'cols': 'sample_id, with_mm(폭), surface_roughness_um, UT_dB, oven_temp_c, nomal_abnormal(0/1) — 열 이름은 원자료 철자 그대로', 'check': '기준 셋(거칠기 4.9 · 초음파 27.5 · 폭 302.5)으로 TP 77 · FN 23 · FP 1 · TN 899', 'note': '원래 파일 이름: 불량품_판정_데이터.csv. 끝에 빈 열 두 개가 있습니다.'},
 {'id': 'ds-ai4i', 'short': 'AI4I 미니', 'name': 'AI4I 2024 미니 (예지보전)', 'file': 'ai4i_2024_mini.csv', 'color': '#d672d6', 'desc': '100행 · 고장 6', 'week': '4·5주',
  'cols': 'UID, air_temp_k, process_temp_k, rotational_speed_rpm, torque_nm, tool_wear_min, machine_failure, twf, hdf, pwf, osf, rnf, wear_proxy, temp_diff', 'check': '고장 6건(twf 2 · hdf 3 · pwf 1 · osf 1), rnf 1건은 고장 0, wear_proxy ≈ 가동 ÷ 253', 'note': 'UCI AI4I 2020 데이터 구성을 따른 수업용 미니판입니다.'},
 {'id': 'ds-ai4i2', 'short': 'AI4I 미니 v2', 'name': 'AI4I 2024 미니 v2 (7주 불량 분석판)', 'file': 'ai4i_2024_mini_v2.csv', 'color': '#e8a33d', 'desc': '100행 · 불량 13', 'week': '7·8주',
  'cols': 'UID, air_temp_k, process_temp_k, rotational_speed_rpm, torque_nm, tool_wear_min, machine_failure, twf, hdf, pwf, osf, rnf, temp_diff, wear_proxy(0~100)', 'check': '불량 13행(13.0%), 원인 건수 twf 4 · hdf 4 · osf 3 · pwf 2 · rnf 1 = 14, 겹침 UID 042, (나) 회전×온도차 최고 칸 5/13 = 38%', 'note': '원래 파일 이름: ai4i_2024_mini.csv (7주차 배포판). 4·5주 판과 값이 다릅니다.'},
 {'id': 'ds-defect2', 'short': '판재 판정 v2', 'name': '불량품 판정 데이터 v2 (7주 층별판)', 'file': 'defect_judgement_v2.csv', 'color': '#c0504d', 'desc': '1,000행 · 불량 33', 'week': '7·8주',
  'cols': 'with_mm(약 5), surface_roughness_um, UT_dB(약 60), oven_temp_c(약 200), nomal_abnormal(nomal/abnormal) — 열 이름은 원자료 철자 그대로', 'check': 'abnormal 33(3.3%), 거칠기 5구간 최고 6.1%(12/198), 거칠기 ≥ 3.6µm 11/159 = 6.9%', 'note': '원래 파일 이름: 불량품_판정_데이터.csv (7주차 배포판). 4주 판과 값·라벨 표기가 다릅니다.'},
 {'id': 'ds-noodle', 'short': '면류 일별', 'name': '면류 일별 검색·판매·프로모션', 'file': 'noodle_search_sales_daily.csv', 'color': '#5ee39c', 'desc': '2016-01-01~2026-10-03, 3,929일', 'week': '6주 REVIEW',
  'cols': '날짜, 연도, 월, 요일, 냉면·콩국수·비빔면_검색지수, 냉면·콩국수·비빔면_판매량, 프로모션', 'check': '냉면 검색·판매 상관 0.818, 여름 일평균 2025 냉면 78,434팩', 'note': '검색지수만 네이버 데이터랩 원본, 판매량은 가상입니다.'},
 {'id': 'ds-plan', 'short': '면류 계획', 'name': '면류 생산계획 시트 묶음 (xlsx)', 'file': 'noodle_planning.xlsx', 'color': '#2bb3a8', 'desc': '13시트', 'week': '6주 REVIEW',
  'cols': 'README, 가정_파라미터, 일별_검색판매, 주별_판매, 제품, BOM, 원재료, 공장_라인, 교대_가동시간, 인력기준, 공정_검사, 공장_DC_운송, DC_매장', 'check': '보통 시나리오 냉면 가동률 83.1%, 환산 인원 387명', 'note': '공장·원재료·물류 값은 가상입니다.'},
 {'id': 'ds-m12', 'short': 'm1·m2 묶음', 'name': '판정 샘플·모델 비교 묶음 (목록만)', 'file': None, 'color': '#56506e', 'desc': '파일 8개', 'week': '4주',
  'cols': 'm1_판정샘플_40.csv, m1_판정샘플_40_정답키.csv, m2_모델성능_비교표.csv, m2_테스트데이터_공통.csv, m2_테스트데이터_정답포함.csv, m2_학습데이터_불량18/50/100.csv', 'check': '—', 'note': '이번에 받은 자료에 파일이 없어 이름만 적었습니다. 파일을 주시면 이 칸과 4주 리포트에 더합니다.'},
 {'id': 'ds-six', 'short': '가상 공장 6종', 'name': '업종별 가상 공장 6종 (OT 계획)', 'file': None, 'color': '#3f7fb5', 'desc': '한 학기 동안 쓸 데이터', 'week': '7~15주',
  'cols': '사출성형 A라인(기준) · 자동차 부품 조립 · 석유화학 연속 · 철강·소재 · 식음료 배치 · 전자부품 SMT', 'check': '%와 ppm은 같은 말이 아님 · 같은 OEE 공식이 다른 분모', 'note': '7주부터 빈 슬롯과 함께 채워질 데이터입니다.'},
]

def _sub(i, d):
    dl = f'<p><a class="bt primary" style="text-decoration:none;display:inline-block" href="../../data/{d["file"]}" download>내려받기 — {d["file"]}</a></p>' if d['file'] else '<p class="lim">파일 없음 — 목록만</p>'
    return {'id': d['id'], 'title': d['name'], 'tags': [f'쓰는 주차: {d["week"]}', d['desc']],
            'body': [f'<div class="tw"><table class="tb"><tr><th>열</th><td>{d["cols"]}</td></tr><tr><th>검수 기준 숫자</th><td>{d["check"]}</td></tr><tr><th>메모</th><td>{d["note"]}</td></tr></table></div>', dl],
            'talk': [[('moa', 'e07', '이 상자는 제가 정리했어요. 검수 기준 숫자를 AI 결과와 맞춰 보세요.')], [('sia', 'e10', '열 이름 철자가 원자료와 같은지 확인했습니다.')], [('x3', 'e16', '(삐빅)')]][i % 3],
            'quiz': [{'q': f'{d["short"]} 데이터를 쓰는 주차는?', 'o': [d['week'], '15주'], 'a': 0, 'why': '데이터 상자 꼬리표에 적혀 있습니다.'}]}

CH = {
 'slug': 'appA', 'num': 'A', 'title': '부록 A · 데이터 창고',
 'eyebrow': '부록 A · 자재창고 = 수업 데이터 보관소',
 'desc': '스마트 제조 수업 데이터 11묶음 — 열 구성, 기간, 쓰는 주차, AI 결과를 검수할 기준 숫자와 내려받기.',
 'q': '이 데이터는 무엇이고, AI 결과가 맞는지 무엇으로 확인하나?',
 'lead': '공장의 자재창고처럼, 수업에서 쓰는 데이터를 선반에 정리했습니다. 상자마다 열 구성, 기간, 쓰는 주차, 그리고 AI 결과를 대조할 "검수 기준 숫자"를 붙였습니다.',
 'scene_alt': '자재창고 3D. 선반 열한 개에 데이터 상자가 놓여 있고 지게차가 오간다. 상자를 누르면 해당 데이터 설명으로 이동한다.',
 'scene_hud': '3D · 자재창고 — 상자를 누르면 설명으로 이동합니다',
 'scene_opts': {'cam': [0, 15, 24], 'target': [0, 1, 0]},
 'kpis': [('11묶음', '수업 데이터', 'g'), ('9개', '내려받을 수 있는 파일', 'a'), ('검수 숫자', '묶음마다 하나 이상', 'm'), ('가상', '대부분 수업용 가상 데이터', 'r')],
 'hero_talk': [('moa', 'e12', '창고 정리 끝! 상자마다 이름표를 붙였어요.'), ('fly', 'e09', '이름표에 "검수 기준 숫자"가 있는 게 핵심이야.'), ('doc', 'e08', 'AI에게 계산을 시켰다면, 결과를 이 숫자와 먼저 맞춰 보세요.')],
 'three': ['수업 데이터 11묶음의 열 구성·기간·쓰는 주차를 한곳에 모았습니다.', '데이터마다 "검수 기준 숫자"가 있어, AI가 낸 결과를 바로 대조할 수 있습니다.', '실습 전에 파일을 내려받고, 열 이름과 행 수부터 확인하세요(1주 ③ 검수).'],
 'abbr': [('CSV', 'Comma-Separated Values', '쉼표로 구분한 표 파일'), ('xlsx', 'Excel Workbook', '엑셀 통합 문서')],
 'why': [('같은 숫자가 나와야 한다', '같은 데이터, 같은 절차면 사람·엑셀·AI 누구든 같은 숫자가 나와야 합니다.'), ('가상 데이터', '사내 실데이터 대신 가상 공장 데이터로 연습합니다(OT 원칙).'), ('출처 표기', '어떤 값이 실제(검색지수)이고 어떤 값이 가상인지 구분해 씁니다.')],
 'big': [('3주', '식품 · 백신 · 석유화학'), ('4·5주', '판재 판정 · AI4I 미니'), ('6주', '면류 일별 · 계획 시트'), ('7주~', 'm1·m2 · 가상 공장 6종 (준비 중)')],
 'glossary': {},
 'subs': [_sub(i, d) for i, d in enumerate(DS)],
 'summary': {'head': ['데이터', '주차', '검수 기준'], 'rows': [[d['short'], d['week'], d['check']] for d in DS],
             'limits': ['데이터는 수업용이며 실제 기업·공장 수치가 아닙니다(검색지수 제외).', 'm1·m2 묶음은 파일을 받지 못해 목록만 있습니다.']},
 'outro': [('moa', 'e01', '필요한 상자를 꺼내 가세요!'), ('sia', 'e07', '반납할 때는 열 이름을 바꾸지 말아 주세요.'), ('doc', 'e10', '검수 기준 숫자부터 맞추는 습관, 잊지 마세요.'), ('fly', 'e10', '숫자가 안 맞으면 AI보다 데이터 읽기부터 의심해.')],
 'sources': [('데이터', '스마트 제조 수업 자료 (안상선) · 검색지수: 네이버 데이터랩 · AI4I: UCI Machine Learning Repository 구성 참고')],
 'notes': '모든 데이터는 수업용입니다.',
 'practice': None,
}
CH['js'] = 'window.DS=' + json.dumps([{'id': d['id'], 'short': d['short'], 'name': d['name'], 'desc': d['desc'], 'color': d['color']} for d in DS], ensure_ascii=False) + ';'
