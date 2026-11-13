// 스마트 제조 연구실 · 3D 무대 모듈 (three.js 0.170, ES 모듈)
// 쓰는 법: import { mount } from '../assets/sf3d.js'; mount(stageEl, api => { api.box(...); api.chars([...]); }, {cam:[18,14,18]});
// 캐릭터 3D 모델: assets/lab3d.js (fruitfly-lab-expressions/chars3d/lab3d.js 복사본, 캐릭터 © 안상선)
import * as THREE from 'three';

const ROOT = document.body.getAttribute('data-root') || './';
const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function makeLabelTexture(text, o) {
  const lines = String(text).split('\n');
  const fs = (o.px || 44), pad = 18;
  const c = document.createElement('canvas'); const g = c.getContext('2d');
  g.font = `700 ${fs}px "IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif`;
  const w = Math.max(...lines.map(l => g.measureText(l).width)) + pad * 2, h = lines.length * fs * 1.25 + pad * 1.4;
  c.width = Math.ceil(w); c.height = Math.ceil(h);
  g.font = `700 ${fs}px "IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif`;
  if (o.bg !== 'none') { g.fillStyle = o.bg || 'rgba(12,26,32,.86)'; const r = 14; g.beginPath(); g.roundRect ? g.roundRect(0, 0, c.width, c.height, r) : g.rect(0, 0, c.width, c.height); g.fill(); if (o.border) { g.strokeStyle = o.border; g.lineWidth = 4; g.stroke(); } }
  g.fillStyle = o.color || '#e8f1f2'; g.textBaseline = 'top'; g.textAlign = 'center';
  lines.forEach((l, i) => g.fillText(l, c.width / 2, pad * .7 + i * fs * 1.25));
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return { tex: t, aspect: c.width / c.height };
}

export async function mount(stage, build, opts = {}) {
  const canvas = stage.querySelector('canvas') || stage.appendChild(document.createElement('canvas'));
  canvas.setAttribute('role', 'img');
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: !!opts.capture }); }
  catch (e) { stage.insertAdjacentHTML('beforeend', '<div class="fallback">이 브라우저에서는 3D 화면을 열 수 없습니다.<br>아래 글과 실험은 그대로 볼 수 있습니다.</div>'); return null; }
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(opts.bg || '#0c1a20');
  scene.fog = new THREE.Fog(opts.bg || '#0c1a20', 60, 140);
  const cam = new THREE.PerspectiveCamera(opts.fov || 38, 2, 0.1, 400);
  const C = opts.cam || [22, 18, 22]; cam.position.set(...C);
  const target = new THREE.Vector3(...(opts.target || [0, 1, 0]));
  let controls = null;
  try {
    const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
    controls = new OrbitControls(cam, canvas); controls.target.copy(target); controls.enableDamping = true;
    controls.maxPolarAngle = Math.PI * 0.47; controls.minDistance = opts.minD || 8; controls.maxDistance = opts.maxD || 80;
    controls.enablePan = opts.pan !== false; controls.update();
  } catch (e) { cam.lookAt(target); }
  scene.add(new THREE.HemisphereLight('#cfe9ff', '#1b2a2e', 1.1));
  const sun = new THREE.DirectionalLight('#ffffff', 1.6); sun.position.set(18, 30, 14); sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 30, bottom: -30, near: 1, far: 100 });
  scene.add(sun);
  const G = opts.ground || 60;
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(G, G * 0.75), new THREE.MeshStandardMaterial({ color: opts.floor || '#16282e', roughness: .95 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const grid = new THREE.GridHelper(G, G / 2, '#24404a', '#1c3238'); grid.position.y = 0.01; scene.add(grid);

  const ticks = [], hoverables = [];
  const mats = {};
  const mat = (c, o = {}) => { const k = c + JSON.stringify(o); return mats[k] || (mats[k] = new THREE.MeshStandardMaterial({ color: c, roughness: .6, metalness: .1, ...o })); };
  const place = (m, p = {}) => { m.position.set(p.x || 0, p.y || 0, p.z || 0); if (p.ry) m.rotation.y = p.ry; if (p.tip || p.href || p.onClick) { m.userData = { ...m.userData, tip: p.tip, href: p.href, onClick: p.onClick }; hoverables.push(m); } m.castShadow = p.shadow !== false; m.receiveShadow = true; (p.parent || scene).add(m); return m; };
  const api = {
    THREE, scene, cam, controls, mat,
    box(w, h, d, color, p = {}) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(color, p.m || {})); if (p.y == null) p.y = h / 2; return place(m, p); },
    cyl(r, h, color, p = {}) { const m = new THREE.Mesh(new THREE.CylinderGeometry(p.r2 ?? r, r, h, p.seg || 20), mat(color, p.m || {})); if (p.y == null) p.y = h / 2; return place(m, p); },
    group(p = {}) { const g = new THREE.Group(); g.position.set(p.x || 0, p.y || 0, p.z || 0); if (p.ry) g.rotation.y = p.ry; (p.parent || scene).add(g); return g; },
    label(text, p = {}) {
      const { tex, aspect } = makeLabelTexture(text, p); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: p.depthTest !== false, transparent: true }));
      const h = p.size || 1; s.scale.set(h * aspect, h, 1); s.position.set(p.x || 0, p.y || 2, p.z || 0); s.renderOrder = 5; (p.parent || scene).add(s);
      if (p.tip || p.href || p.onClick) { s.userData = { tip: p.tip, href: p.href, onClick: p.onClick }; hoverables.push(s); }
      return s;
    },
    relabel(sprite, text, p = {}) { const { tex, aspect } = makeLabelTexture(text, p); sprite.material.map.dispose(); sprite.material.map = tex; sprite.material.needsUpdate = true; const h = p.size || sprite.scale.y; sprite.scale.set(h * aspect, h, 1); },
    tick(fn) { ticks.push(fn); },
    hover(obj, tip, href, onClick) { obj.userData = { ...obj.userData, tip, href, onClick }; hoverables.push(obj); },
    async chars(list) {
      try {
        const mod = await import('./lab3d.js');
        const lab = mod.createLab3D(THREE, { outline: true, shadow: true });
        const out = [];
        for (const c of list) {
          const g = lab.build(c.key, { unit: c.unit || 1.75, pose: c.pose || 'idle', expr: c.expr || 'E13', variant: c.variant });
          g.position.set(c.x || 0, c.y || 0, c.z || 0); g.rotation.y = c.ry || 0; (c.parent || scene).add(g);
          g.traverse(o => { if (o.isMesh) o.castShadow = true; });
          if (c.tip) { g.traverse(o => { if (o.isMesh) { o.userData.tip = c.tip; hoverables.push(o); } }); }
          if (g.userData.update) ticks.push(t => g.userData.update(t));
          out.push(g);
        }
        api.render();
        return out;
      } catch (e) { console.warn('lab3d', e); return []; }
    },
    render: () => {},
  };

  // 툴팁 · 클릭
  const tip = document.createElement('div'); tip.className = 'tip3d'; stage.appendChild(tip);
  const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
  let hovered = null;
  function pick(ev) {
    const r = canvas.getBoundingClientRect(); mouse.x = ((ev.clientX - r.left) / r.width) * 2 - 1; mouse.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(mouse, cam); const hit = ray.intersectObjects(hoverables, false)[0];
    return hit ? hit.object : null;
  }
  canvas.addEventListener('pointermove', ev => {
    const o = pick(ev); hovered = o;
    if (o && o.userData.tip) { const r = stage.getBoundingClientRect(); tip.innerHTML = o.userData.tip; tip.style.display = 'block'; tip.style.left = Math.min(r.width - 250, ev.clientX - r.left + 14) + 'px'; tip.style.top = (ev.clientY - r.top + 14) + 'px'; }
    else tip.style.display = 'none';
    canvas.style.cursor = o && (o.userData.href || o.userData.onClick) ? 'pointer' : 'grab';
  });
  canvas.addEventListener('pointerleave', () => { tip.style.display = 'none'; });
  let downAt = null;
  canvas.addEventListener('pointerdown', ev => { downAt = [ev.clientX, ev.clientY]; });
  canvas.addEventListener('pointerup', ev => {
    if (!downAt || Math.hypot(ev.clientX - downAt[0], ev.clientY - downAt[1]) > 6) return;
    const o = pick(ev); if (!o) return;
    if (o.userData.onClick) o.userData.onClick(o); else if (o.userData.href) location.href = o.userData.href;
  });

  function size() { const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / Math.max(1, h); cam.updateProjectionMatrix(); }
  size(); window.addEventListener('resize', () => { size(); draw(0); });
  await build(api);
  let visible = true, last = performance.now(), t = 0;
  function draw(dt) { t += dt; ticks.forEach(f => f(t, dt)); if (controls) controls.update(); renderer.render(scene, cam); }
  api.render = () => draw(0);
  draw(0);
  if (controls) controls.addEventListener('change', () => { if (reduce || !visible) renderer.render(scene, cam); });
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(stage);
  function loop(now) { const dt = Math.min(0.05, (now - last) / 1000); last = now; if (visible && !reduce) draw(dt); requestAnimationFrame(loop); }
  requestAnimationFrame(loop);
  return api;
}

// 공장 소품
export function machine(api, p) {
  const g = api.group(p);
  api.box(p.w || 3, p.h || 2.2, p.d || 2.4, p.color || '#3b6f78', { parent: g, tip: p.tip, href: p.href });
  api.box((p.w || 3) * .5, .5, .1, p.screen || '#5ee39c', { parent: g, y: (p.h || 2.2) * .7, z: (p.d || 2.4) / 2 + .06, m: { emissive: p.screen || '#5ee39c', emissiveIntensity: .6 } });
  api.cyl(.18, .9, '#c9d6d8', { parent: g, x: (p.w || 3) * .35, y: (p.h || 2.2) + .45 });
  return g;
}
export function conveyor(api, p) {
  const g = api.group(p); const L = p.len || 12;
  api.box(L, .25, 1.4, '#2a3a40', { parent: g, y: .9 });
  for (let i = 0; i < 4; i++) api.box(.2, .9, 1.2, '#4a5a60', { parent: g, x: -L / 2 + .4 + i * (L - .8) / 3, y: .45 });
  return g;
}

// ── 공정 소품 라이브러리 ─────────────────────────────────────────
// 모든 소품: (api, p) → THREE.Group. p: {x,z,ry,tip,href,onClick,color,parent}
const sub = (api, p) => api.group(p);
export const P = {
  tank(api, p) { const g = sub(api, p); const r = p.r || 1.2, h = p.h || 3; api.cyl(r, h, p.color || '#b9c6c9', { parent: g, y: h / 2 + .6, tip: p.tip, m: { metalness: .6, roughness: .35 } }); api.cyl(r, .5, p.color || '#b9c6c9', { parent: g, y: h + .85, r2: .2, m: { metalness: .6, roughness: .35 } }); for (const a of [0, 2.1, 4.2]) api.cyl(.08, .6, '#55666a', { parent: g, x: Math.cos(a) * r * .8, z: Math.sin(a) * r * .8, y: .3 }); return g; },
  hopper(api, p) { const g = sub(api, p); api.cyl(.9, 1.4, p.color || '#c9a24a', { parent: g, y: 2.6, r2: .9, tip: p.tip }); api.cyl(.15, 1.0, p.color || '#c9a24a', { parent: g, y: 1.6, r2: .9 }); for (const s of [[-.6, -.6], [.6, -.6], [-.6, .6], [.6, .6]]) api.box(.1, 1.9, .1, '#55666a', { parent: g, x: s[0], z: s[1] }); return g; },
  injection(api, p) { const g = sub(api, p); api.box(5, 1.1, 1.6, '#d8dde0', { parent: g, y: .55, tip: p.tip, onClick: p.onClick }); api.box(2.2, 1.2, 1.4, '#3f7fb5', { parent: g, x: -1.2, y: 1.7 }); api.cyl(.35, 2, '#9aa5aa', { parent: g, x: .9, y: 1.7, ry: 0, r2: .35 }).rotation.z = Math.PI / 2; const mold = api.box(1, 1.3, 1.4, '#c9a24a', { parent: g, x: 2, y: 1.75 }); api.tick(t => { mold.position.x = 2 + Math.max(0, Math.sin(t * 1.5)) * .35; }); P.hopper(api, { parent: g, x: -1.6, y: 1.6, color: '#c9a24a' }).scale.setScalar(.55); return g; },
  robot(api, p) { const g = sub(api, p); api.cyl(.5, .5, '#e8a33d', { parent: g, tip: p.tip }); const s = api.group({ parent: g, y: .5 }); api.cyl(.22, 1.4, '#e8a33d', { parent: s, y: .7 }); const e = api.group({ parent: s, y: 1.4 }); api.box(1.6, .25, .25, '#e8a33d', { parent: e, x: .8, y: 0 }); api.box(.25, .5, .4, '#555', { parent: e, x: 1.6, y: -.25 }); api.tick(t => { s.rotation.y = Math.sin(t * .9 + (p.ph || 0)) * 1.2; e.rotation.z = -.2 + Math.sin(t * 1.8 + (p.ph || 0)) * .25; }); return g; },
  oven(api, p) { const g = sub(api, p); const L = p.len || 5; api.box(L, 1.8, 1.9, p.color || '#6d4b3a', { parent: g, y: 1.4, tip: p.tip, onClick: p.onClick }); api.box(L + .02, .25, 1.5, '#f0604d', { parent: g, y: .7, m: { emissive: '#f0604d', emissiveIntensity: .9 } }); api.cyl(.2, 1.2, '#55666a', { parent: g, x: L / 3, y: 2.9 }); return g; },
  freezer(api, p) { const g = sub(api, p); const L = p.len || 5; api.box(L, 2, 2, '#cfe3ef', { parent: g, y: 1.5, tip: p.tip }); api.box(L + .02, .25, 1.6, '#82b8ff', { parent: g, y: .7, m: { emissive: '#82b8ff', emissiveIntensity: .7 } }); for (let i = 0; i < 3; i++) api.cyl(.35, .2, '#9ab', { parent: g, x: -L / 3 + i * L / 3, y: 2.6 }); return g; },
  cutter(api, p) { const g = sub(api, p); api.box(.3, 2.4, 2, '#55666a', { parent: g, x: -.7, y: 1.2, tip: p.tip }); api.box(.3, 2.4, 2, '#55666a', { parent: g, x: .7, y: 1.2 }); api.box(1.7, .3, 2, '#55666a', { parent: g, y: 2.5 }); const bl = api.box(1.2, .1, 1.8, '#dfe6e8', { parent: g, y: 2, m: { metalness: .8, roughness: .2 } }); api.tick(t => { bl.position.y = 1.45 + Math.abs(Math.sin(t * 2.4)) * .6; }); return g; },
  gate(api, p) { const g = sub(api, p); const c = p.color || '#82b8ff'; api.box(.25, 2.6, .25, '#55666a', { parent: g, z: -1, y: 1.3, tip: p.tip, onClick: p.onClick }); api.box(.25, 2.6, .25, '#55666a', { parent: g, z: 1, y: 1.3 }); const bar = api.box(.3, .3, 2.2, c, { parent: g, y: 2.6, m: { emissive: c, emissiveIntensity: .8 }, tip: p.tip, onClick: p.onClick }); g.userData.bar = bar; return g; },
  cnc(api, p) { const g = sub(api, p); api.box(2.6, 2.4, 2.2, p.color || '#d8dde0', { parent: g, tip: p.tip, onClick: p.onClick }); api.box(1.4, 1, .05, '#1c3a48', { parent: g, y: 1.4, z: 1.11, m: { emissive: '#1c3a48', emissiveIntensity: .5 } }); const sp = api.cyl(.12, .7, '#9aa5aa', { parent: g, y: 1.7 }); api.box(.8, 1.5, .6, '#3f4a50', { parent: g, x: 1.7, y: .75 }); api.tick(t => { sp.rotation.y = t * 20; }); return g; },
  packer(api, p) { const g = sub(api, p); api.box(2.4, 1.8, 2, p.color || '#8a6f4e', { parent: g, y: .9, tip: p.tip }); for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) api.box(.7, .5, .6, '#c9a26a', { parent: g, x: 1.8 + i * .75, y: .25 + j * .52, z: -.3 }); return g; },
  steamer(api, p) { const g = sub(api, p); for (let i = 0; i < 3; i++) api.cyl(.9, .45, '#b0865a', { parent: g, y: .3 + i * .48, tip: p.tip }); api.cyl(.95, .2, '#8b6a46', { parent: g, y: 1.75 }); const st = []; for (let i = 0; i < 3; i++) st.push(api.cyl(.12, .5, '#ffffff', { parent: g, x: -.3 + i * .3, y: 2.2, m: { transparent: true, opacity: .35 } })); api.tick(t => st.forEach((s, i) => { s.position.y = 2.1 + ((t * .6 + i * .33) % 1) * 1.2; })); return g; },
  rack(api, p) { const g = sub(api, p); const n = p.n || 3; for (let i = 0; i < 3; i++) api.box(n * 1.4, .1, 1.4, '#e8a33d', { parent: g, y: .2 + i * 1.2 }); for (const x of [-n * .7, n * .7]) api.box(.1, 2.6, 1.4, '#3f6fa5', { parent: g, x, y: 1.3 }); for (let i = 0; i < n; i++) for (let j = 0; j < 2; j++) api.box(1.1, .7, 1.1, p.box || '#c9a26a', { parent: g, x: -n * .7 + .7 + i * 1.4, y: .6 + j * 1.2, tip: p.tip }); return g; },
  forklift(api, p) { const g = sub(api, p); api.box(1.4, .7, .9, '#e8a33d', { parent: g, y: .55, tip: p.tip || '지게차' }); api.box(.6, .8, .8, '#3f4a50', { parent: g, x: -.2, y: 1.3 }); api.box(.1, 1.6, .7, '#55666a', { parent: g, x: .8, y: .8 }); api.box(.8, .08, .6, '#55666a', { parent: g, x: 1.2, y: .3 }); if (p.path) api.tick(t => { const u = (Math.sin(t * .35 + (p.ph || 0)) + 1) / 2; g.position.x = p.path[0][0] + (p.path[1][0] - p.path[0][0]) * u; g.position.z = p.path[0][1] + (p.path[1][1] - p.path[0][1]) * u; }); return g; },
  panel(api, p) { const g = sub(api, p); api.box(.15, 1.6, 1, '#3f4a50', { parent: g, y: 1.4, tip: p.tip }); api.box(.05, 1.1, .8, p.screen || '#5ee39c', { parent: g, x: .1, y: 1.5, m: { emissive: p.screen || '#5ee39c', emissiveIntensity: .6 } }); api.box(.12, .7, .12, '#3f4a50', { parent: g, y: .35 }); return g; },
  sensor(api, p) { const g = sub(api, p); const c = p.color || '#5ee39c'; api.cyl(.08, 1.2, '#55666a', { parent: g, y: .6 }); const s = api.box(.35, .35, .35, c, { parent: g, y: 1.35, m: { emissive: c, emissiveIntensity: .8 }, tip: p.tip }); api.tick(t => { s.material.emissiveIntensity = .4 + .4 * Math.sin(t * 4 + (p.ph || 0)); }); return g; },
};

// 공정 라인: 소품을 차례로 놓고 컨베이어로 이은 뒤 제품을 흘린다.
// stations: [{type, name, tip, gap, opts}] · 반환: {pos:[x...], items, belt}
export function processLine(api, stations, o = {}) {
  const T = api.THREE; const z0 = o.z || 0, y0 = .95; let x = o.x0 ?? -14; const xs = [];
  stations.forEach((s, i) => {
    const w = s.w || 3;
    x += (i ? (s.gap ?? 1.6) : 0) + w / 2; xs.push(x);
    const prop = P[s.type] ? P[s.type](api, { x, z: z0 + (s.dz || 0), tip: s.tip ? `<b>${o.num === false ? '' : (i + 1) + '. '}${s.name}</b><br>${s.tip}` : null, onClick: s.onClick, ...(s.opts || {}) }) : null;
    if (s.name && o.labels !== false) api.label(`${o.num === false ? '' : (i + 1) + '. '}${s.name}`, { x, y: s.ly || 4.4, z: z0 + (s.dz || 0), size: s.ls || .85 });
    x += w / 2;
  });
  const x1 = xs[0] - 1, x2 = xs[xs.length - 1] + 1.5;
  const belt = api.box(x2 - x1, .2, 1.1, '#2a3a40', { x: (x1 + x2) / 2, y: y0 - .15, z: z0 + (o.beltDz || 0), shadow: false });
  for (let bx = x1 + .5; bx < x2; bx += 3) api.box(.15, .8, .9, '#4a5a60', { x: bx, y: .4, z: z0 + (o.beltDz || 0) });
  const items = []; const n = o.items || 10; const cols = o.colors || ['#d8c9a8', '#e8d39a', '#f1b646', '#5ee39c'];
  for (let i = 0; i < n; i++) {
    const m = (o.itemShape === 'cyl') ? api.cyl(.3, .3, cols[0], { y: y0 + .15 }) : api.box(.55, .35, .55, cols[0], { y: y0 + .17 });
    m.userData.u = i / n; m.castShadow = true; items.push(m);
  }
  const L = x2 - x1;
  api.tick((t, dt) => {
    items.forEach(m => {
      m.userData.u = (m.userData.u + dt * (o.speed || .035)) % 1; const px = x1 + L * m.userData.u; m.position.x = px; m.position.z = z0 + (o.beltDz || 0);
      let k = 0; xs.forEach((sx, j) => { if (px > sx) k = j; }); const c = cols[Math.min(cols.length - 1, Math.floor(k * cols.length / xs.length))];
      if (m.material.color.getHexString() !== c.slice(1)) m.material = api.mat(c);
      if (o.onItem) o.onItem(m, px, k);
    });
  });
  return { xs, items, x1, x2 };
}
export function wall(api, p) { // 공장 벽·기둥 (분위기용)
  const L = p.len || 40;
  api.box(L, 4.5, .3, '#1d3036', { x: p.x || 0, y: 2.25, z: p.z || -9, shadow: false });
  for (let x = -L / 2 + 2; x < L / 2; x += 8) api.box(.6, 6, .6, '#24404a', { x: (p.x || 0) + x, y: 3, z: (p.z || -9) + .4 });
  if (p.title) api.label(p.title, { x: p.x || 0, y: 5.6, z: (p.z || -9) + .5, size: 1, bg: 'rgba(43,179,168,.9)', color: '#06201d' });
}
