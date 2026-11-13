# 스마트 제조 연구실 — 3D로 보는 15주

AI212 · 2026-2학기 「스마트 제조」 강의를 **차시마다 다른 3D 공장**과 연구실 식구들이 안내하는 해설 사이트입니다. 코딩 없이 생성형 AI로 공장 데이터를 분석하고 현장 문서를 자동화합니다.

**▶ 바로 보기:** https://adminmrobo.github.io/smart_product/

글 · 안상선 (www.ahnboat.xyz) · (주)M-Robo 대표 · 참고 사례: [스마트 팩토리 World](https://adminmrobo.github.io/smart_factory_world/)

> 모든 공장은 교육용 가상 공장입니다. 데이터는 수업용 가상값이며 실제 기업·공장 수치가 아닙니다(면류 검색지수만 네이버 데이터랩 원본).

## 챕터 17개 (15주 + 부록 2)

| # | 챕터 | 3D 공장 | 세부 챕터 | 실습 리포트 |
|---|---|---|---|---|
| 01 | [오리엔테이션 & 스마트 제조란](weeks/w01/) | 사출성형 A라인 + 스마트공장 수준 레이어 | 12 | — |
| 02 | [생성형 AI 원리 & 프롬프트 기초](weeks/w02/) | 케이블 하네스 조립 + 토큰·어텐션 | 13 | [숫자 답 검산](weeks/w02/practice.html) |
| 03 | [생산실적 추세 분석 — 시계열의 원리](weeks/w03/) | 빙과·호빵 공장 + 계절지수 냉동창고 | 15 | [계절지수 12개](weeks/w03/practice.html) |
| 04 | [분류와 회귀 — 데이터에 말 걸기](weeks/w04/) | 금속 판재 경화·검사 라인 | 12 | [판정 기준 세 개](weeks/w04/practice.html) |
| 05 | [작업지시서와 한 페이지 앱](weeks/w05/) | CNC 밀링 가공 셀 (AI4I) | 12 | [분기 규칙 100대](weeks/w05/practice.html) |
| 06 | [REVIEW — 1~5주 다시 보기](weeks/w06/) | 면류 공장 + 물류센터 | 13 | [2027 여름 생산계획](weeks/w06/practice.html) |
| 07~14 | 불량 분석 ①·중간 제출·불량 분석 ②·OEE·대시보드·문서 자동화 ①②·SOP | 빈 슬롯 (준비 중) | — | — |
| 15 | REVIEW — 공정 자동화와 기말 제출 | 빈 슬롯 (준비 중) | — | — |
| A | [데이터 창고](weeks/appA/) | 자재창고 | 9 | — |
| B | [프롬프트 공구함](weeks/appB/) | 공무실 | 13 | — |

- 형식: 본문은 연구실 해설(비전공자판) — 3줄 요약, 왜 이 방법/조수 수식 상자, 칸 대화, 실험 패널, 확인 퀴즈, 대결. 실습은 박사 단독 서술의 발견 리포트(Summary·방법·결과·반론·한계, 사실/해석/추측 구분).
- 등장: 박사 · 조수(하루) · 초파리 연구원 · 주판봇 · 인턴 시아(조수1) · 인턴 모아(조수2) · 미공개 X1~X3(소리 대사만).
- 7주부터는 빈 슬롯입니다. 자료가 준비되면 1~6주와 같은 형식으로 채웁니다.

## 구조

```
index.html                 첫 화면 — 15주 공장 캠퍼스(3D)
weeks/<slug>/index.html    챕터 본문 (w01~w15, appA, appB)
weeks/<slug>/practice.html 실습 리포트 (w02~w06)
assets/                    lab.css · lab.js(위젯·퀴즈·차트) · sf3d.js(3D 무대·공정 소품) · scenes.js(챕터별 공장) · lab3d.js · kgx.js · char/(캐릭터 그림)
data/                      수업 데이터 (내려받기용)
analysis/                  실습 리포트 계산 코드 (python)
onto/<slug>/               지식 색인 원본(kg·refs·meta)과 점검 보고서
build/                     빌더 — content/*.py → HTML, onto.py → 지식 색인 붙이기
img/                       공유 미리보기(3D 장면 캡처)
docs/IMG_spec.md           글 표지 그림 명세와 생성 프롬프트
```

다시 만들기: `python3 build/build.py` → `python3 build/onto.py <ahnboat_lab_explainer>/packs/task/onto-retrofit/tools`

3D 화면은 three.js 0.170(CDN)을 씁니다. 캐릭터 3D 모델은 fruitfly-lab-expressions의 `chars3d/lab3d.js` 복사본입니다.

## 게시

Settings → Pages → Branch `main` / `/(root)`.

## 저작권

캐릭터 이름·설정·그림 © 안상선. 허락 없이 사용할 수 없습니다. 캐릭터 원본: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions).
