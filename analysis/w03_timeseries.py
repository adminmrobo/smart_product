"""3주차 실습 리포트 계산 — 계절지수(승법·가법), 자기상관, 계절 나이브 MAPE.
사용: python3 w03_timeseries.py ../data"""
import sys, pandas as pd, numpy as np
D = sys.argv[1] if len(sys.argv) > 1 else '../data'
f = pd.read_csv(f'{D}/week03_seasonal_foods.csv'); f['m'] = pd.to_datetime(f.month).dt.month
def si_mult(s, m):
    cma = s.rolling(12, center=True).mean().rolling(2).mean().shift(-1)
    g = (s / cma).groupby(m).mean(); return g / g.mean()
for c in ['icecream', 'hoppang', 'sweet_potato']: print(c, si_mult(f[c], f.m).round(2).tolist())
ic = f.icecream; print('자기상관 1칸', round(ic.autocorr(1), 2), '12칸', round(ic.autocorr(12), 2))
a, p = ic.values[-12:], ic.values[-24:-12]; print('계절 나이브 2025 MAPE', round(np.mean(abs(a - p) / a) * 100, 1))
p2 = np.full(12, ic.values[-24:-12].mean()); print('12개월 평균 MAPE', round(np.mean(abs(a - p2) / a) * 100, 1))
pc = pd.read_csv(f'{D}/week03_petrochem.csv'); pc['m'] = pd.to_datetime(pc.month).dt.month
s = pc.ncc_util; cma = s.rolling(12, center=True).mean().rolling(2).mean().shift(-1)
d = (s - cma).groupby(pc.m).mean(); print('NCC 가법 계절 효과(%p)', (d - d.mean()).round(1).tolist())
v = pd.read_csv(f'{D}/week03_vaccine_1.csv'); y = v.groupby(v.month.str[:4]).doses.sum(); print('백신 연간', y.to_dict())
