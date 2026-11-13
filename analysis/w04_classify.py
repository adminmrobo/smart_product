"""4주차 실습 리포트 계산 — 불량품 판정 데이터 6개 분류 모델 + 판정 기준.
사용: python3 w04_classify.py ../data/defect_judgement.csv"""
import sys, pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score
d = pd.read_csv(sys.argv[1]).iloc[:, :6]
X = d[['with_mm', 'surface_roughness_um', 'UT_dB', 'oven_temp_c']]; y = d.nomal_abnormal
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, stratify=y, random_state=42)
M = {'로지스틱 회귀': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), '결정나무': DecisionTreeClassifier(max_depth=4, random_state=42),
     '랜덤 포레스트': RandomForestClassifier(n_estimators=300, random_state=42), '그래디언트 부스팅': GradientBoostingClassifier(random_state=42),
     'KNN': make_pipeline(StandardScaler(), KNeighborsClassifier(5)), 'SVM': make_pipeline(StandardScaler(), SVC())}
cv = StratifiedKFold(5, shuffle=True, random_state=42)
for n, m in M.items():
    s = cross_val_score(m, Xtr, ytr, cv=cv); m.fit(Xtr, ytr); p = m.predict(Xte)
    print(f'{n}: CV {s.mean():.3f} · 테스트 정확도 {accuracy_score(yte, p):.3f} · 재현율 {recall_score(yte, p):.2f} · 정밀도 {precision_score(yte, p):.3f} · {confusion_matrix(yte, p).tolist()}')
print(export_text(DecisionTreeClassifier(max_depth=3, random_state=42).fit(X, y), feature_names=list(X.columns)))
r = (d.with_mm > 302.5) | (d.surface_roughness_um > 4.9) | (d.UT_dB > 27.5)
print(pd.crosstab(y, r.astype(int)))
