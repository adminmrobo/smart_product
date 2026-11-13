"""8주차 예시 주제 카드 풀이 — 거칠기 몇 µm부터 불량률 2배인가 (저자 계산)
python3 analysis/w08_threshold.py
"""
import pandas as pd
D = pd.read_csv('data/defect_judgement_v2.csv'); D['y'] = (D.nomal_abnormal == 'abnormal').astype(int)
r = D.surface_roughness_um; base = D.y.mean(); print('abnormal', D.y.sum(), f'{base:.1%}', '2배', f'{2*base:.1%}')
for k in (4, 5, 10, 20):
    g = D.groupby(pd.qcut(r, k), observed=True).y.agg(['sum', 'size', 'mean']); print(k, g.tail(2).round(3).to_string())
for t in [3.0, 3.2, 3.42, 3.6, 3.8, 4.0, 4.2, 4.5]:
    s = D[r >= t]; print(f't={t}: {len(s)}행 {s.y.sum()}건 {s.y.mean():.1%} ({s.y.mean()/base:.1f}배)')
rest = D[r <= pd.qcut(r, 20, retbins=True)[1][19]]
print('나머지', len(rest), rest.y.sum(), f'{rest.y.mean():.2%}')
print(rest.groupby(pd.qcut(rest.surface_roughness_um, 5), observed=True).y.agg(['sum', 'size', 'mean']).round(3).to_string())
