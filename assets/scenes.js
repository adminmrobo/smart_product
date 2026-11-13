// 스마트 제조 연구실 · 챕터별 3D 장면 — 차시마다 업종이 다른 실제 공정 라인
import { P, processLine, wall } from './sf3d.js';

function hudButtons(stage, items, onPick, start = 0) {
  const h = stage.querySelector('#hud2'); if (!h) return;
  h.innerHTML = '';
  items.forEach((t, i) => { const b = document.createElement('button'); b.className = 'bt'; b.type = 'button'; b.textContent = t; b.onclick = () => { h.querySelectorAll('.bt').forEach((x, j) => x.classList.toggle('on', j === i)); onPick(i); }; h.appendChild(b); });
  h.children[start] && h.children[start].classList.add('on');
}
const crowd = (x, z) => [{ key: 'x1', x, z, pose: 'cheer', tip: '미공개 X1' }, { key: 'x2', x: x + 1.4, z: z - .2, pose: 'think', tip: '미공개 X2' }, { key: 'x3', x: x + 2.6, z: z + .2, pose: 'wave', tip: '미공개 X3' }];
const rng = s => () => ((s = (s * 16807) % 2147483647) / 2147483647);

export const scenes = {

  // 첫 화면 · 15주 캠퍼스 공장
  async hub(api, stage) {
    const C = window.CHAPS || [];
    const col = { built: '#2bb3a8', review: '#f1b646', slot: '#4a4f63', app: '#82b8ff' };
    const TYPE = { w01: 'injection', w02: 'cutter', w03: 'freezer', w04: 'oven', w05: 'cnc', w06: 'tank', w07: 'gate', w08: 'panel', w09: 'robot', w10: 'cnc', w11: 'panel', w12: 'packer', w13: 'rack', w14: 'robot', w15: 'tank', appA: 'rack', appB: 'cnc' };
    wall(api, { title: '스마트 제조 연구실 — 15주 공장 캠퍼스', len: 56, z: -12 });
    const pos = [];
    C.forEach((c, i) => {
      let x, z;
      if (c.slug === 'appA') { x = -25; z = 0; } else if (c.slug === 'appB') { x = 25; z = 0; }
      else if (i < 8) { x = -19.5 + i * 5.6; z = 5; } else { x = 19.5 - (i - 8) * 5.6; z = -5; }
      pos.push([x, z]);
      const st = c.status, base = api.box(4.6, .25, 4.2, st === 'slot' ? '#262a36' : '#1f3a3f', { x, z, y: .12, tip: `<b>${c.num} · ${c.title}</b><br>${c.factory}<br>${c.statusKo}`, href: c.href });
      const T = TYPE[c.slug]; const opts = { x, z: z - .4, tip: `<b>${c.num} · ${c.title}</b><br>${c.factory}<br>${c.statusKo}`, href: c.href, onClick: () => { location.href = c.href; } };
      if (T === 'injection') P.injection(api, { ...opts, x: x }).scale.setScalar(.7); else if (T === 'oven') P.oven(api, { ...opts, len: 3.4 }); else if (T === 'freezer') P.freezer(api, { ...opts, len: 3.4 }); else P[T](api, opts);
      api.box(4.6, .12, .3, col[st === 'built' && c.review ? 'review' : st], { x, z: z + 2.05, y: .3, m: { emissive: col[st === 'built' && c.review ? 'review' : st], emissiveIntensity: st === 'slot' ? .1 : .6 } });
      api.label(`${c.num}  ${c.short}`, { x, y: 4.4, z, size: 1.0, border: col[st === 'built' && c.review ? 'review' : st], color: st === 'slot' ? '#9d9bb8' : '#e8f1f2', href: c.href, onClick: () => { location.href = c.href; } });
      if (st === 'slot') api.label('준비 중', { x, y: 3.3, z, size: .45, bg: 'none', color: '#9d9bb8' });
    });
    // 주차 순서 컨베이어
    const T = api.THREE;
    for (let i = 0; i < 14; i++) { const a = pos[i], b = pos[i + 1]; const len = Math.hypot(b[0] - a[0], b[1] - a[1]); const m = api.box(len, .1, .5, '#24404a', { x: (a[0] + b[0]) / 2, z: (a[1] + b[1]) / 2, y: .05, shadow: false }); m.rotation.y = -Math.atan2(b[1] - a[1], b[0] - a[0]); }
    const tokens = []; for (let k = 0; k < 6; k++) { const t = api.box(.5, .4, .5, '#5ee39c', { y: .4 }); t.userData.u = k / 6; tokens.push(t); }
    api.tick((t, dt) => tokens.forEach(m => { m.userData.u = (m.userData.u + dt * .02) % 1; const f = m.userData.u * 14, i = Math.floor(f), r = f - i; const a = pos[i], b = pos[i + 1]; m.position.x = a[0] + (b[0] - a[0]) * r; m.position.z = a[1] + (b[1] - a[1]) * r; m.material = api.mat(i < 5 ? '#5ee39c' : i === 5 ? '#f1b646' : '#4a4f63'); }));
    await api.chars([{ key: 'doctor', x: -6, z: 9.5, ry: .2, pose: 'wave', tip: '박사', unit: 2.4 }, { key: 'haru', x: -3.8, z: 9.8, pose: 'wave', tip: '조수(하루)', unit: 2.4 }, { key: 'fruitfly', x: -1.6, z: 9.6, pose: 'think', tip: '초파리 연구원', unit: 2.4 }, { key: 'jupanbot', x: .6, z: 9.9, pose: 'cheer', tip: '주판봇', unit: 2.4 }, { key: 'sia', x: 2.8, z: 9.6, pose: 'idle', tip: '인턴 시아 (조수1)', unit: 2.4 }, { key: 'moa', x: 5, z: 9.9, pose: 'wave', tip: '인턴 모아 (조수2)', unit: 2.4 }, { key: 'x1', x: 8, z: 10.5, pose: 'cheer', unit: 2.4 }, { key: 'x2', x: 9.8, z: 10.3, unit: 2.4 }, { key: 'x3', x: 11.4, z: 10.6, pose: 'wave', unit: 2.4 }]);
  },
  // 1주차 · 사출성형 A라인 + 스마트공장 수준 레이어
  async w01(api, stage) {
    wall(api, { title: '사출성형 · 플라스틱 — 기준 데이터셋 A라인', len: 44 });
    processLine(api, [
      { type: 'hopper', name: '원료 건조·투입', tip: '플라스틱 알갱이(펠릿)를 말려서 넣습니다.', w: 2 },
      { type: 'injection', name: '사출 성형', tip: '녹인 수지를 금형에 밀어 넣어 모양을 만듭니다. 캐비티별 불량·사이클타임이 여기서 생깁니다.', w: 5 },
      { type: 'robot', name: '취출 로봇', tip: '금형에서 제품을 꺼냅니다.', w: 2 },
      { type: 'gate', name: '비전 검사', tip: '카메라로 외관 불량을 봅니다.', w: 1 },
      { type: 'packer', name: '포장·출하', tip: '박스에 담고 바코드를 붙입니다.', w: 4 },
    ], { x0: -16, colors: ['#c9a24a', '#3f7fb5', '#3f7fb5', '#5ee39c'], itemShape: 'cyl' });
    const L = {}; const add = (lv, o) => { (L[lv] = L[lv] || []).push(o); o.visible = false; return o; };
    add(1, api.label('바코드 실적 입력', { x: 9.5, y: 3, z: 1.6, size: .45 }));
    add(2, P.panel(api, { x: -4, z: 3.5, ry: Math.PI / 2, screen: '#f1b646', tip: '중간1 · 실시간 현황판' })); add(2, api.label('실시간 현황판', { x: -4, y: 2.9, z: 3.5, size: .45 }));
    [-12, -5, 1].forEach((x, i) => add(3, P.sensor(api, { x, z: -1.5, ph: i, tip: '중간2 · 온도·압력 센서 → 원인 분석' })));
    add(3, api.label('센서 → 원인 분석·조건 보정', { x: -5, y: 2.6, z: -1.6, size: .45 }));
    add(4, P.panel(api, { x: 6, z: 3.8, ry: Math.PI / 2, screen: '#5ee39c', tip: '고도화 · AI가 조건을 제안, 사람이 승인' })); add(4, api.label('AI 제안 → 사람 승인', { x: 6, y: 2.9, z: 3.8, size: .45 }));
    const names = ['미적용', '기초', '중간1', '중간2', '고도화'];
    const sign = api.label('', { x: 0, y: 7.2, z: -8.5, size: .8, border: '#2bb3a8' });
    function pick(lv) { for (const k in L) L[k].forEach(o => o.visible = +k <= lv); api.relabel(sign, '스마트공장 수준: ' + names[lv], { border: '#2bb3a8', size: .8 }); api.render(); }
    hudButtons(stage, names, pick, 2); pick(2);
    window.SF_LEVEL = lv => { pick(lv); const h = stage.querySelector('#hud2'); if (h) [...h.children].forEach((b, j) => b.classList.toggle('on', j === lv)); };
    P.forklift(api, { x: 14, z: 5, path: [[12, 5.5], [16, 2]] });
    await api.chars([{ key: 'doctor', x: -10, z: 5, ry: .3, pose: 'explain', tip: '박사' }, { key: 'haru', x: -8.4, z: 5.4, pose: 'wave', tip: '조수(하루)' }, { key: 'fruitfly', x: -2, z: 5, pose: 'think', tip: '초파리 연구원' }, { key: 'jupanbot', x: -.4, z: 5.3, pose: 'cheer', tip: '주판봇' }, { key: 'sia', x: 3.5, z: 5, pose: 'idle', tip: '인턴 시아' }, { key: 'moa', x: 5, z: 5.3, pose: 'wave', tip: '인턴 모아' }, ...crowd(-15, 6)]);
  },

  // 2주차 · 케이블 하네스 조립 라인 + 작업지시서 토큰
  async w02(api, stage) {
    wall(api, { title: '전장 부품 · 케이블 하네스 조립', len: 44 });
    processLine(api, [
      { type: 'rack', name: '전선 릴 보관', tip: '2.5m 케이블 원자재', w: 4, opts: { n: 2, box: '#3f7fb5' } },
      { type: 'cutter', name: '절단·탈피', tip: '케이블을 2.5m로 자르고 피복을 벗깁니다.', w: 2 },
      { type: 'cutter', name: '단자 압착', tip: '단자 HSG-A8P를 4가닥에 압착합니다.', w: 2 },
      { type: 'gate', name: '인출력 시험', tip: '5V/10mA 이상 · 불량 허용 0/100', w: 1, opts: { color: '#f1b646' } },
      { type: 'packer', name: '결속·포장', tip: '묶음 단위로 포장합니다.', w: 4 },
    ], { x0: -16, colors: ['#3f7fb5', '#d672d6', '#e8a33d', '#5ee39c'], itemShape: 'cyl', speed: .04 });
    const toks = ['B7-2203', '케이블', '2.5m', '×4가닥', '압착', 'HSG-A8P', '인출력', '5V', '10mA', '0/100'];
    const Wt = [.10, .04, .08, .07, .12, .14, .09, .12, .12, .12];
    const T = api.THREE; const beams = [];
    P.panel(api, { x: 12, z: 4, ry: -Math.PI / 2, screen: '#d672d6', tip: 'QWEN 단말 · 작업지시서를 토큰으로 읽고 신입용 5줄 요약을 만듭니다' });
    api.label('QWEN 단말', { x: 12, y: 3, z: 4, size: .5 });
    toks.forEach((t, i) => {
      const x = -13 + i * 2.4, y = 6.2 + (i % 2) * .7;
      api.label(t, { x, y, z: -3, size: .5, border: '#d672d6', tip: `토큰 ${i + 1} · 「${t}」` });
      const g = new T.CylinderGeometry(.02 + Wt[i] * .25, .02 + Wt[i] * .25, 1, 6);
      const m = new T.Mesh(g, new T.MeshStandardMaterial({ color: '#f0604d', emissive: '#f0604d', emissiveIntensity: .6, transparent: true, opacity: .2 + Wt[i] * 4 }));
      const a = new T.Vector3(x, y - .4, -3), b = new T.Vector3(12, 2.2, 4);
      m.position.copy(a.clone().add(b).multiplyScalar(.5)); m.scale.y = a.distanceTo(b); m.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), b.clone().sub(a).normalize());
      api.scene.add(m); api.hover(m, `「${t}」 어텐션 가중치 ${Wt[i].toFixed(2)} (설명용 값)`); beams.push(m);
    });
    api.label('작업지시서 한 줄 → 토큰 10조각', { x: -2, y: 8, z: -3, size: .65, border: '#2bb3a8' });
    hudButtons(stage, ['어텐션 보기', '토큰만'], i => { beams.forEach(b => b.visible = i === 0); api.render(); });
    await api.chars([{ key: 'doctor', x: 8, z: 5.4, ry: -.4, pose: 'explain' }, { key: 'haru', x: 6.3, z: 5.8, pose: 'think' }, { key: 'fruitfly', x: -3, z: 5, pose: 'think' }, { key: 'jupanbot', x: -4.8, z: 5.3, pose: 'cheer' }, { key: 'sia', x: 1, z: 5.2, pose: 'idle' }, { key: 'moa', x: 2.6, z: 5.5, pose: 'hold' }, ...crowd(-15, 6)]);
  },

  // 3주차 · 아이스크림·호빵 식품 공장 + 계절지수 냉동창고
  async w03(api, stage) {
    wall(api, { title: '식음료 · 빙과/호빵 공장 — 계절을 타는 라인', len: 46, z: -11 });
    processLine(api, [
      { type: 'tank', name: '배합', tip: '우유·설탕·원료를 섞습니다.', w: 2.4 },
      { type: 'tank', name: '살균', tip: '가열 살균 · 위생 기록', w: 2.4, opts: { color: '#d8dde0', h: 2.4 } },
      { type: 'freezer', name: '동결', tip: '아이스크림 믹스를 얼립니다.', w: 4, opts: { len: 4 } },
      { type: 'packer', name: '충진·포장', tip: '컵·바에 담고 포장합니다.', w: 3 },
      { type: 'freezer', name: '경화 터널', tip: '아주 낮은 온도에서 단단하게 굳힙니다.', w: 4, opts: { len: 4 } },
    ], { x0: -18, z: -5, colors: ['#f6e7cf', '#ffd1e1', '#ff9fbe', '#ff86b8'], speed: .03 });
    P.steamer(api, { x: 12, z: -5, tip: '호빵 라인 · 증숙기 (겨울 성수기)' }); api.label('호빵 증숙', { x: 12, y: 3.4, z: -5, size: .55 });
    const SI = window.SI3 || {}; const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
    api.box(31, .1, 4.6, '#20343b', { x: 0, y: .06, z: 4.4, shadow: false, tip: '냉동창고 · 월별 출하량(계절지수)' });
    api.label('냉동창고 · 월별 출하 = 계절지수', { x: -10, y: 5.6, z: 4.4, size: .6, border: '#82b8ff' });
    const stacks = [], labs = [];
    months.forEach((m, i) => { const x = -13.5 + i * 2.45; stacks.push(api.box(1.8, 1, 1.8, '#ff86b8', { x, z: 4.4, y: .5, tip: m })); labs.push(api.label('', { x, y: 1.5, z: 4.4, size: .5, bg: 'none' })); api.label(m, { x, y: .3, z: 6.1, size: .45, bg: 'none' }); });
    api.box(30, .05, .08, '#f1b646', { y: 2.2, z: 3.2, m: { emissive: '#f1b646', emissiveIntensity: .8 }, tip: '계절지수 1.00 = 평균적인 달' });
    function show(k) { const v = SI[k] || []; const col = { icecream: '#ff86b8', hoppang: '#f1b646', sweet_potato: '#c48a5a' }[k]; stacks.forEach((s, i) => { const h = Math.max(.08, (v[i] || 0) * 2.2); s.scale.y = h; s.position.y = h / 2; s.material = api.mat(col); s.userData.tip = `${months[i]} · 계절지수 ${(v[i] || 0).toFixed(2)}`; api.relabel(labs[i], (v[i] || 0).toFixed(2), { bg: 'none', size: .5 }); labs[i].position.y = h + .5; }); api.render(); }
    hudButtons(stage, ['아이스크림', '호빵', '군고구마'], i => show(['icecream', 'hoppang', 'sweet_potato'][i])); show('icecream');
    P.forklift(api, { x: 15, z: 1, path: [[14, 0], [17, 4]] });
    await api.chars([{ key: 'doctor', x: -15.5, z: 8.6, ry: .5, pose: 'explain' }, { key: 'haru', x: -13.8, z: 8.9, pose: 'hold' }, { key: 'jupanbot', x: -1, z: 8.8, pose: 'cheer' }, { key: 'fruitfly', x: -3, z: 8.6, pose: 'think' }, { key: 'sia', x: 6, z: 8.6, pose: 'idle' }, { key: 'moa', x: 7.6, z: 8.9, pose: 'cheer' }, ...crowd(11, 8.6)]);
  },

  // 4주차 · 판재 경화·검사 라인 (불량품 판정 데이터의 네 변수)
  async w04(api, stage) {
    wall(api, { title: '금속 판재 · 경화·재단·검사 라인', len: 46 });
    const STG = [2, 3, 4]; let on = [true, true, true]; const R = rng(4);
    const line = processLine(api, [
      { type: 'oven', name: '경화 오븐 180℃', tip: 'oven_temp_c · 평균 180℃ 안팎 (판정과 거의 무관했던 변수)', w: 5, opts: { len: 5 } },
      { type: 'cutter', name: '폭 300mm 재단', tip: 'with_mm · 정상 범위 약 297~302.4mm', w: 2.6, ly: 5.4 },
      { type: 'gate', name: '표면 거칠기', tip: 'surface_roughness_um · 4.9μm를 넘으면 이상', w: 2.4, ly: 5.4, opts: { color: '#f1b646' } },
      { type: 'gate', name: '초음파(UT)', tip: 'UT_dB · 27.5dB를 넘으면 내부 결함 의심', w: 2.4, opts: { color: '#82b8ff' } },
      { type: 'gate', name: '폭 측정', tip: '302.5mm를 넘으면 이상', w: 2.4, ly: 5.4, opts: { color: '#d672d6' } },
    ], { x0: -16, colors: ['#9aa5aa', '#b9c6c9', '#b9c6c9', '#b9c6c9'], speed: .03, items: 12, onItem: (m, px, k) => {
      if (m.userData.last == null || px < m.userData.last) m.userData.kind = R() < .18 ? Math.floor(R() * 3) : -1;
      m.userData.last = px;
      const kd = m.userData.kind, caught = kd >= 0 && on[kd] && k >= STG[kd];
      if (caught) m.material = api.mat('#f0604d');
      if (k >= 4) { const d = Math.min(2.6, (px - line.xs[4]) * 1.3); m.position.z = caught ? d : -d; }
    } });
    const X = line.xs[4] + 3.4;
    api.box(2.4, 1.2, 2.2, '#2a6b4a', { x: X, z: -2.8, tip: '정상 상자' }); api.label('정상', { x: X, y: 2, z: -2.8, size: .6 });
    api.box(2.4, 1.2, 2.2, '#7a2a24', { x: X, z: 2.8, tip: '불량 상자' }); api.label('불량', { x: X, y: 2, z: 2.8, size: .6 });
    hudButtons(stage, ['기준 셋 모두', '거칠기만', '초음파만', '폭만'], i => { on = i === 0 ? [true, true, true] : [i === 1, i === 2, i === 3]; });
    await api.chars([{ key: 'doctor', x: 6, z: 5.5, ry: -.3, pose: 'referee' }, { key: 'haru', x: -2, z: 5, pose: 'hold' }, { key: 'fruitfly', x: 2.5, z: -4.5, ry: Math.PI, pose: 'think' }, { key: 'jupanbot', x: .8, z: -4.6, ry: Math.PI, pose: 'cheer' }, { key: 'sia', x: X + 2.6, z: -2.4, ry: -1.4, pose: 'referee' }, { key: 'moa', x: X + 2.6, z: 3, ry: -1.6, pose: 'hold' }, ...crowd(-15, 6)]);
  },

  // 5주차 · CNC 가공 셀 (AI4I) + 작업지시서
  async w05(api, stage) {
    wall(api, { title: '기계 가공 · CNC 밀링 셀 — AI4I 2024', len: 44 });
    const M = window.M5 || []; const colors = { 정상: '#5ee39c', 주의: '#f1b646', 위험: '#f0604d' };
    const board = api.label('설비를 누르면 작업지시서 카드가 뜹니다', { x: 0, y: 8.4, z: -8.4, size: .8, border: '#2bb3a8' });
    processLine(api, [{ type: 'rack', name: '소재 투입', tip: '가공 전 소재', w: 3, opts: { n: 2, box: '#9aa5aa' } }, { type: 'gate', name: '치수 검사', tip: '가공 후 치수·표면 검사', w: 1.5, opts: { color: '#82b8ff' } }, { type: 'packer', name: '출하', tip: '가공품 출하', w: 3 }], { x0: -17, z: 1.4, colors: ['#9aa5aa', '#c9d6d8', '#5ee39c'], labels: true, num: false, speed: .025 });
    const showCard = m => { api.relabel(board, `${m.id} · ${m.label} · ${m.zone} → ${m.act}\n담당 ${m.who} · ${m.due}`, { border: colors[m.zone], size: .8 }); api.render(); if (window.SF_PICK) window.SF_PICK(m.id); };
    M.forEach((m, i) => {
      const x = -12 + (i % 3) * 8, z = -3.5 + Math.floor(i / 3) * 5.5;
      P.cnc(api, { x, z, tip: `<b>${m.id}</b> · ${m.label}<br>${m.zone} → ${m.act}`, onClick: () => showCard(m) });
      P.robot(api, { x: x + 2.6, z, ph: i, tip: '공작물 로딩 로봇' });
      const lamp = api.cyl(.28, .3, colors[m.zone], { x: x - .9, y: 2.6, z, m: { emissive: colors[m.zone], emissiveIntensity: 1 }, tip: `${m.id} · ${m.zone}`, onClick: () => showCard(m) });
      api.label(m.id, { x, y: 3.5, z, size: .55, bg: 'none' });
      api.tick(t => { lamp.material.emissiveIntensity = m.zone === '위험' ? .5 + .5 * Math.sin(t * 6) : 1; });
    });
    P.rack(api, { x: 13, z: 3, n: 3, tip: '공구 보관대 · 교체용 공구' }); api.label('공구 보관대', { x: 13, y: 3.6, z: 3, size: .5 });
    P.forklift(api, { x: 0, z: 6, path: [[-10, 6.5], [10, 6.5]] });
    await api.chars([{ key: 'doctor', x: 9, z: 7.8, ry: -.6, pose: 'explain' }, { key: 'haru', x: 7.3, z: 8, pose: 'hold' }, { key: 'fruitfly', x: -13, z: 7.6, ry: .4, pose: 'think' }, { key: 'jupanbot', x: -11.3, z: 8, pose: 'cheer' }, { key: 'sia', x: 2, z: 8.3, pose: 'referee' }, { key: 'moa', x: 3.7, z: 8.5, pose: 'idle', variant: 'suit' }, ...crowd(-5, 9)]);
  },

  // 6주차 · REVIEW · 면류 공장 라인 + 출하·물류
  async w06(api, stage) {
    wall(api, { title: '식품 · 면류 3사 — 냉면·콩국수·비빔면 여름 라인', len: 48, z: -12 });
    processLine(api, [
      { type: 'tank', name: '반죽 배합', tip: '밀가루·메밀·전분 + 물 (BOM 팩당 소요량)', w: 2.4 },
      { type: 'cutter', name: '제면', tip: '면을 뽑고 자릅니다. 라인당 시간당 850~1,100팩', w: 2 },
      { type: 'oven', name: '숙성·유탕', tip: '냉면은 숙성, 비빔면은 유탕(기름에 튀김)', w: 4, opts: { len: 4, color: '#7a5a3a' } },
      { type: 'freezer', name: '냉각', tip: '식힌 뒤 포장 대기', w: 3, opts: { len: 3 } },
      { type: 'gate', name: '금속검출', tip: '금속검출·중량·밀봉 검사 · 검사·출하대기 6~12시간', w: 1, opts: { color: '#5ee39c' } },
      { type: 'packer', name: '포장', tip: '박스입수 24~30팩', w: 3 },
    ], { x0: -20, z: -6, colors: ['#efe3c4', '#e8d39a', '#c98a4a', '#e0c79a'], speed: .03 });
    const D = [['수도권DC', -14, 5.5], ['중부DC', -5, 6.5], ['영남DC', 5, 6.5], ['호남DC', 14, 5.5]];
    D.forEach(d => { api.box(3, 1.4, 2.2, '#56506e', { x: d[1], z: d[2], tip: `<b>${d[0]}</b> · 물류센터` }); api.label(d[0], { x: d[1], y: 2.3, z: d[2], size: .5 }); });
    const dock = [15, -2]; api.box(4, .6, 3, '#3a3f4f', { x: dock[0], z: dock[1], tip: '출하 도크' }); api.label('출하 도크', { x: dock[0], y: 1.4, z: dock[1], size: .5, bg: 'none' });
    const trucks = D.map((d, i) => { const t = api.box(1.2, .8, .7, '#f1b646', { x: dock[0], z: dock[1], y: .5, tip: `출하 → ${d[0]}` }); t.userData.d = d; t.userData.o = i * .25; return t; });
    api.tick(t => trucks.forEach(k => { const u = (t * .1 + k.userData.o) % 1; const d = k.userData.d; k.position.x = dock[0] + (d[1] - dock[0]) * u; k.position.z = dock[1] + (d[2] - dock[1]) * u; }));
    api.label('2027 여름(6~8월) 생산계획 · REVIEW 종합 실습', { x: -2, y: 7.2, z: -11.5, size: .8, border: '#2bb3a8' });
    await api.chars([{ key: 'doctor', x: -12, z: 1.2, ry: .3, pose: 'explain' }, { key: 'haru', x: -10.4, z: 1.5, pose: 'wave' }, { key: 'fruitfly', x: -6.6, z: 1.2, pose: 'think' }, { key: 'jupanbot', x: -5, z: 1.5, pose: 'cheer' }, { key: 'sia', x: 0, z: 1.2, pose: 'idle' }, { key: 'moa', x: 1.6, z: 1.5, pose: 'cheer' }, ...crowd(6, 1.6)]);
  },

  // 부록 A · 공장 자재창고 = 데이터 창고
  async appA(api, stage) {
    wall(api, { title: '자재창고 — 수업 데이터 세트 보관', len: 40 });
    const S = window.DS || [];
    S.forEach((d, i) => {
      const x = -12 + (i % 5) * 6, z = -4 + Math.floor(i / 5) * 6;
      P.rack(api, { x, z, n: 2, box: d.color || '#2bb3a8', tip: `<b>${d.name}</b><br>${d.desc}` });
      api.box(2.8, .9, 1.4, d.color || '#2bb3a8', { x, z: z + 1.6, y: .45, tip: `<b>${d.name}</b><br>${d.desc}`, href: '#' + d.id });
      api.label(d.short, { x, y: 3.6, z, size: .5 });
    });
    P.forklift(api, { x: 0, z: 7, path: [[-12, 7.5], [12, 7.5]] });
    await api.chars([{ key: 'moa', x: -15, z: 8, pose: 'hold' }, { key: 'sia', x: -13.4, z: 8.2, pose: 'explain' }, { key: 'doctor', x: 14, z: 8, ry: -.5, pose: 'wave' }, { key: 'x3', x: 15.4, z: 8.4 }]);
  },
  // 부록 B · 공무실 프롬프트 공구함
  async appB(api, stage) {
    wall(api, { title: '공무실 — 프롬프트 공구함', len: 40 });
    const S = window.PB || [];
    api.box(26, 1.1, 3.6, '#5a3d2a', { z: -2, tip: '공구 작업대' });
    S.forEach((d, i) => {
      const x = -11.5 + i * (23 / Math.max(1, S.length - 1));
      api.box(1.4, 2 + (i % 3) * .5, .25, d.color || '#82b8ff', { x, z: -2, y: 2.1, tip: `<b>${d.name}</b><br>${d.desc}`, href: '#' + d.id });
      api.label(d.short, { x, y: 4 + (i % 3) * .5, z: -2, size: .45 });
    });
    P.cnc(api, { x: -12, z: 4, tip: '정비 중인 가공기' }); P.robot(api, { x: 12, z: 4, tip: '점검 중인 로봇' });
    await api.chars([{ key: 'haru', x: -6, z: 3.5, pose: 'hold' }, { key: 'jupanbot', x: -3, z: 3.8, pose: 'explain' }, { key: 'fruitfly', x: 3, z: 3.6, pose: 'think' }, { key: 'x1', x: 7, z: 4 }, { key: 'x2', x: 8.6, z: 4.2 }]);
  },
};
