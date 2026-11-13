"""7주차 불량 분석 ① — 세기 · 파레토 · 층별 · 자리 지도 · 무작위 섞기 (저자 계산)
python3 analysis/w07_defect_map.py
"""
import numpy as np, pandas as pd
A = pd.read_csv('data/ai4i_2024_mini_v2.csv'); D = pd.read_csv('data/defect_judgement_v2.csv')
C = ['twf', 'hdf', 'pwf', 'osf', 'rnf']; y = A.machine_failure
print('행', len(A), '불량', y.sum(), f'{y.mean():.1%}')
cnt = A[C].sum().sort_values(ascending=False); print('원인 건수', cnt.to_dict(), '합', cnt.sum())
print('겹친 행', A.loc[A[C].sum(axis=1) > 1, 'UID'].tolist(), '원인 없는 불량', A.loc[(y == 1) & (A[C].sum(axis=1) == 0), 'UID'].tolist())
print('누적 %', (cnt.cumsum() / cnt.sum() * 100).round(1).to_dict())
for c in ['tool_wear_min', 'torque_nm', 'rotational_speed_rpm', 'temp_diff']:
    print(A.groupby(pd.qcut(A[c], 4), observed=True).machine_failure.agg(['size', 'sum', 'mean']).round(3).to_string(), '\n')
D['y'] = (D.nomal_abnormal == 'abnormal').astype(int); print('abnormal', D.y.sum(), D.y.mean())
for c in ['with_mm', 'surface_roughness_um', 'UT_dB', 'oven_temp_c']:
    print(D.groupby(pd.qcut(D[c], 5), observed=True).y.agg(['size', 'sum', 'mean']).round(4).to_string(), '\n')
for x, z in [('tool_wear_min', 'torque_nm'), ('rotational_speed_rpm', 'temp_diff'), ('rotational_speed_rpm', 'torque_nm')]:
    t = A.assign(X=pd.qcut(A[x], 3), Z=pd.qcut(A[z], 3))
    print(t.pivot_table(index='X', columns='Z', values='machine_failure', aggfunc=['sum', 'size'], observed=False).to_string(), '\n')
# 무작위 섞기: 우연만으로 이런 모양이 얼마나 자주 나오나
rng = np.random.default_rng(1); v = y.values; N = 20000
Q = [pd.qcut(A[c], 4, labels=False).values for c in ['tool_wear_min', 'torque_nm', 'rotational_speed_rpm', 'temp_diff']]
X = pd.qcut(A.rotational_speed_rpm, 3, labels=False).values * 3 + pd.qcut(A.temp_diff, 3, labels=False).values
a = b = 0
for _ in range(N):
    p = rng.permutation(v)
    a += max(np.bincount(q, weights=p).max() for q in Q) >= 7
    b += (np.bincount(X, weights=p, minlength=9) >= 5).any()
print('16구간 중 하나 이상 7/25 이상:', a / N, ' (나) 지도 한 칸에 5건 이상:', b / N)
