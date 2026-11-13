# 이미지 명세서 — 스마트 제조 연구실

지금 공유 미리보기(`img/*.webp`)는 각 챕터 3D 장면을 캡처한 것입니다. 2D 픽셀아트 글 표지(1600×900)가 필요하면 아래 프롬프트로 Genspark 등에 의뢰하고, 받은 그림은 `img/cover_<slug>.webp`로 넣어 각 챕터 히어로 위에 붙입니다(연구실 기본 스킬 18-14·18-15).

## 1. 공통
- 참고 그림: fruitfly-lab-expressions `images/_sheets/lab6_lineup.png`, 각 캐릭터 `E13_neutral.png`, 이 저장소 `img/<slug>.webp`(장면 배치 참고)
- STYLE_EN: `detailed 16-bit SNES-era pixel art, crisp pixels, thick dark outlines, flat colors with light dithering, chibi proportions about 2.5 heads tall, 16:9, no text, no letters, no numbers`
- 고정: 박사(청록 사각 안경·흰 가운) 오른쪽, 조수 하루(분홍 머리·라벤더 후드) 왼쪽, 초파리 연구원(빨간 겹눈), 주판봇(CRT 머리·주판), 인턴 시아(흑발 메이드)·모아(베이지 웨이브), 미공개 X1~X3는 남흑색 실루엣 + 포인트 색 하나
- NEGATIVE_EN: `text, watermark, realistic proportions, 3D render, extra characters, wrong outfit`

## 2. 챕터별 표지 프롬프트 (장면 문장)

| slug | 장면 |
|---|---|
| w01 | an injection-molding production line (hopper, injection machine, robot arm, vision gate, packing) with five glowing level steps beside it; the lab team stands at the line entrance |
| w02 | a cable-harness assembly line (wire reels, cutting, crimping press, pull test gate); floating token blocks above the line connected by red attention beams to a terminal |
| w03 | an ice-cream and steamed-bun food factory (mixing tanks, freezer tunnel, packing) with a cold storage of twelve crate stacks of different heights for each month |
| w04 | a metal sheet curing and inspection line (curing oven, cutter, three sensor gates) splitting sheets into a green box and a red box |
| w05 | a CNC milling cell with six machines and loading robots, status lamps green, yellow, red; a work-order board on the wall |
| w06 | a noodle factory line (dough mixer, noodle cutter, frying/aging tunnel, metal detector, packing) with trucks leaving for four distribution centers |
| appA | a factory material warehouse with shelves of labeled data crates and a forklift |
| appB | a maintenance workshop with a long workbench of prompt "tools" standing upright |

## 3. 받은 그림 반영
1. 1600×900 WebP로 줄여 `img/cover_<slug>.webp`에 저장 (한 장 300KB 이하)
2. `cover_manifest.json`에 `role: cover` 항목 추가, `status: ok`
3. 각 챕터 `og:image`를 표지로 바꾸려면 `build/build.py`의 `og=` 값을 수정
