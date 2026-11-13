"""6주차 REVIEW 실습 — 면류 3사 2027 여름(6~8월) 생산계획 계산.
데이터: 면류 일별 CSV(2016-01-01~2026-10-03) + 계획용 xlsx 시트 값(아래 상수로 옮김). 모두 수업용 가상 데이터(검색지수만 실제).
사용: python3 w06_plan.py <일별 csv>"""
import sys, pandas as pd, math
n = pd.read_csv(sys.argv[1]); n['날짜'] = pd.to_datetime(n['날짜'])
P = {'냉면': '냉면_판매량', '콩국수': '콩국수_판매량', '비빔면': '비빔면_판매량'}
LINE = {'냉면': (4, 1000), '콩국수': (3, 850), '비빔면': (3, 1100)}      # 라인 수, 시간당 팩/라인 (공장 합계)
HOURS = {1: 7.5, 2: 15, 3: 21}; CREW = {'냉면': 9, '콩국수': 8, '비빔면': 7}; INDIRECT = 6; FACTOR = 1.4
BOM = {'냉면': {'밀가루': .1, '메밀가루': .06, '감자전분': .04, '냉면육수농축액': .12, '겨자·식초소스': .02, '포장필름': 1},
       '콩국수': {'밀가루': .18, '대두분말': .12, '감자전분': .01, '포장필름': 1},
       '비빔면': {'밀가루': .19, '감자전분': .02, '팜유': .04, '비빔장': .08, '포장필름': 1}}
summer = {k: n[n['날짜'].dt.month.isin([6, 7, 8])].groupby(n['날짜'].dt.year)[c].mean() for k, c in P.items()}
SC = {k: {'낮음': s[2026], '보통': s[[2023, 2024, 2025, 2026]].mean(), '높음': s[[2023, 2024, 2025, 2026]].max()} for k, s in summer.items()}
for sc in ['낮음', '보통', '높음']:
    print('== 시나리오', sc); people = 0; mat = {}
    for k in P:
        d = SC[k][sc]; ln, cap = LINE[k]
        for sh in (1, 2, 3):
            u = d / (ln * cap * HOURS[sh])
            if u <= .85 or sh == 3: break
        print(f'  {k}: 일 {d:,.0f}팩 · {sh}교대 가동률 {u:.1%}' + (' (목표 85% 초과)' if u > .85 else '') + (' (최대 95% 초과)' if u > .95 else ''))
        people += ln * CREW[k] * sh
        for m, q in BOM[k].items(): mat[m] = mat.get(m, 0) + q * d * 7
    people += 3 * INDIRECT * 3
    print(f'  하루 필요 인원 {people}명 → 환산 {math.ceil(people * FACTOR)}명')
    print('  주간 원재료:', {m: round(v) for m, v in mat.items()})
