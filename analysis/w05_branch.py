"""5주차 실습 리포트 계산 — AI4I 미니 100행에 점수형·혼합형 분기.
사용: python3 w05_branch.py ../data/ai4i_2024_mini.csv"""
import sys, pandas as pd, numpy as np
a = pd.read_csv(sys.argv[1])
z = pd.cut(a.wear_proxy, [-1, .4, .7, 2], labels=['정상', '주의', '위험'], right=False)
print(pd.crosstab(z, a.machine_failure))
f = a[a.machine_failure == 1].copy(); f['점수형'] = z[a.machine_failure == 1]; print(f[['UID', 'wear_proxy', 'twf', 'hdf', 'pwf', 'osf', 'rnf', '점수형']])
print('직선(기울기, 절편)', np.polyfit(a.tool_wear_min, a.wear_proxy, 1).round(5))
