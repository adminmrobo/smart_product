/* 스마트 제조 연구실 · 공용 스크립트 (외부 라이브러리 없음)
   Cast(캐릭터 그림) · Gloss(용어 말풍선) · Quiz · 복사 버튼 · 진행 막대 · 작은 SVG 차트 · 위젯 등록 */
(function(){
  'use strict';
  var ROOT = document.body.getAttribute('data-root') || './';
  var $ = function(s, el){ return (el||document).querySelector(s); };
  var $$ = function(s, el){ return Array.prototype.slice.call((el||document).querySelectorAll(s)); };
  window.LAB = { ROOT: ROOT, $: $, $$: $$ };

  /* ---------- 캐릭터 그림 ---------- */
  var HAS = { x1:1, x2:1, x3:1 };
  var XOK = ['e01','e02','e03','e04','e09','e13','e15','e16','e24'];
  function charSrc(who, mood){
    mood = (mood || 'e13').toLowerCase();
    if (HAS[who] && XOK.indexOf(mood) < 0) mood = 'e13';
    return ROOT + 'assets/char/' + who + '/' + who + '_' + mood + '.webp';
  }
  window.Cast = {
    src: charSrc,
    fill: function(){
      $$('img[data-who]').forEach(function(img){
        if (img.getAttribute('data-filled')) return;
        img.setAttribute('data-filled','1');
        var who = img.getAttribute('data-who');
        img.onerror = function(){ img.onerror = null; img.src = charSrc(who, 'e13'); };
        img.src = charSrc(who, img.getAttribute('data-mood'));
      });
    },
    set: function(img, who, mood){ img.style.opacity = .2; img.src = charSrc(who, mood); setTimeout(function(){ img.style.opacity = 1; }, 200); }
  };

  /* ---------- 용어 말풍선 ---------- */
  function initGloss(){
    var GL = window.GL || {};
    var tip = document.createElement('div'); tip.id = 'tip'; tip.setAttribute('role','tooltip'); document.body.appendChild(tip);
    function show(el){
      var k = el.getAttribute('data-t'); var g = GL[k]; if (!g) return;
      tip.innerHTML = '<b>' + g[0] + '</b> · <span style="color:var(--muted)">' + g[1] + '</span><br>' + g[2];
      tip.style.display = 'block';
      var r = el.getBoundingClientRect(); var w = Math.min(300, window.innerWidth - 20);
      var x = Math.max(10, Math.min(window.innerWidth - w - 10, r.left));
      tip.style.left = x + 'px'; tip.style.top = (r.bottom + 8) + 'px';
      var tr = tip.getBoundingClientRect(); if (tr.bottom > window.innerHeight - 8) tip.style.top = (r.top - tr.height - 8) + 'px';
    }
    function hide(){ tip.style.display = 'none'; }
    $$('.jt').forEach(function(el){
      el.setAttribute('tabindex','0');
      el.addEventListener('pointerenter', function(){ show(el); });
      el.addEventListener('pointerleave', hide);
      el.addEventListener('focus', function(){ show(el); });
      el.addEventListener('blur', hide);
      el.addEventListener('click', function(e){ e.stopPropagation(); show(el); });
    });
    document.addEventListener('click', hide);
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') hide(); });
  }

  /* ---------- 확인 퀴즈 ---------- */
  function initQuiz(){
    $$('.quiz[data-q]').forEach(function(box){
      var Q; try { Q = JSON.parse(box.getAttribute('data-q')); } catch(e){ return; }
      var html = '<div class="qh">확인 퀴즈</div>';
      Q.forEach(function(q, i){
        html += '<div class="q"><p>' + (i+1) + '. ' + q.q + '</p><div class="opts">' +
          q.o.map(function(o, j){ return '<button class="bt" data-i="'+i+'" data-j="'+j+'">' + o + '</button>'; }).join('') +
          '</div><div class="fb" aria-live="polite"></div></div>';
      });
      box.innerHTML = html;
      $$('button', box).forEach(function(b){
        b.addEventListener('click', function(){
          var i = +b.getAttribute('data-i'), j = +b.getAttribute('data-j'), q = Q[i];
          var wrap = b.parentNode, fb = wrap.nextElementSibling;
          $$('button', wrap).forEach(function(x){ x.classList.remove('ok','no'); });
          if (j === q.a){ b.classList.add('ok'); fb.innerHTML = '✔ 맞습니다. ' + q.why; }
          else { b.classList.add('no'); fb.innerHTML = '✘ 다시 생각해 볼까요? ' + (q.hint || q.why); }
        });
      });
    });
  }

  /* ---------- 복사 버튼 ---------- */
  function initCopy(){
    $$('.prompt').forEach(function(p){
      var b = document.createElement('button'); b.className = 'bt copy'; b.type = 'button'; b.textContent = '복사';
      b.addEventListener('click', function(){
        var t = p.getAttribute('data-raw') || p.innerText.replace(/^복사\n?/, '');
        function done(){ b.textContent = '복사됨'; setTimeout(function(){ b.textContent = '복사'; }, 1500); }
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function(){ fallback(t); done(); });
        else { fallback(t); done(); }
      });
      p.appendChild(b);
    });
    function fallback(t){ var a = document.createElement('textarea'); a.value = t; document.body.appendChild(a); a.select(); try { document.execCommand('copy'); } catch(e){} a.remove(); }
  }

  /* ---------- 진행 막대 · 내비 강조 ---------- */
  function initProg(){
    var bar = $('#prog'); if (!bar) return;
    var links = $$('nav.top .links a[href^="#"]');
    function on(){
      var h = document.documentElement; var p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
      bar.style.width = (p * 100).toFixed(1) + '%';
      var cur = null;
      links.forEach(function(a){ var t = document.getElementById(a.getAttribute('href').slice(1)); if (t && t.getBoundingClientRect().top < 120) cur = a; });
      links.forEach(function(a){ a.classList.toggle('on', a === cur); });
    }
    window.addEventListener('scroll', on, { passive: true }); on();
  }

  /* ---------- 작은 SVG 차트 ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent){ var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function nice(v){ var a = Math.abs(v); if (a >= 1e6) return (v/1e6).toFixed(a >= 1e7 ? 0 : 1) + 'M'; if (a >= 1e4) return (v/1e3).toFixed(0) + 'k'; if (a >= 100) return Math.round(v).toLocaleString('ko-KR'); return (+v.toFixed(2)).toString(); }
  /* series: [{name, color, values:[...], dash}] ; labels: [...] */
  function line(svg, o){
    svg.innerHTML = ''; var W = o.w || 640, H = o.h || 260, L = 52, R = 14, T = 16, B = 30;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('class', 'chart');
    var all = []; o.series.forEach(function(s){ s.values.forEach(function(v){ if (v != null && isFinite(v)) all.push(v); }); });
    if (o.band) o.band.forEach(function(b){ all.push(b[0], b[1]); });
    var lo = o.min != null ? o.min : Math.min.apply(null, all), hi = o.max != null ? o.max : Math.max.apply(null, all);
    if (lo === hi){ lo -= 1; hi += 1; } var pad = (hi - lo) * .06; if (o.min == null) lo -= pad; if (o.max == null) hi += pad;
    var n = o.labels.length, X = function(i){ return L + (W - L - R) * (n === 1 ? .5 : i / (n - 1)); }, Y = function(v){ return T + (H - T - B) * (1 - (v - lo) / (hi - lo)); };
    for (var g = 0; g <= 4; g++){ var v = lo + (hi - lo) * g / 4, y = Y(v); el('line', { x1: L, x2: W - R, y1: y, y2: y, stroke: '#363a52', 'stroke-width': 1 }, svg); el('text', { x: L - 6, y: y + 4, 'text-anchor': 'end' }, svg).textContent = nice(v); }
    var step = Math.max(1, Math.ceil(n / (o.ticks || 8)));
    o.labels.forEach(function(lb, i){ if (i % step === 0 || i === n - 1) el('text', { x: X(i), y: H - 10, 'text-anchor': 'middle' }, svg).textContent = lb; });
    if (o.ref != null){ var yr = Y(o.ref); el('line', { x1: L, x2: W - R, y1: yr, y2: yr, stroke: '#f1b646', 'stroke-dasharray': '4 4' }, svg); }
    if (o.vline) o.vline.forEach(function(v){ el('line', { x1: X(v), x2: X(v), y1: T, y2: H - B, stroke: '#f0604d', 'stroke-dasharray': '3 3' }, svg); });
    if (o.band){ var pts = o.band.map(function(b, i){ return X(i) + ',' + Y(b[1]); }).concat(o.band.map(function(b, i){ return [i, b]; }).reverse().map(function(p){ return X(p[0]) + ',' + Y(p[1][0]); })); el('polygon', { points: pts.join(' '), fill: 'rgba(130,184,255,.15)' }, svg); }
    o.series.forEach(function(s){
      var d = ''; s.values.forEach(function(v, i){ if (v == null || !isFinite(v)) return; d += (d ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(v).toFixed(1); });
      el('path', { d: d, fill: 'none', stroke: s.color, 'stroke-width': s.width || 2, 'stroke-dasharray': s.dash || '', 'stroke-linejoin': 'round' }, svg);
      if (s.dots) s.values.forEach(function(v, i){ if (v != null) el('circle', { cx: X(i), cy: Y(v), r: 3, fill: s.color }, svg); });
    });
    var lx = L + 6; o.series.forEach(function(s){ if (!s.name) return; el('rect', { x: lx, y: T - 2, width: 12, height: 3, fill: s.color }, svg); var t = el('text', { x: lx + 16, y: T + 3 }, svg); t.textContent = s.name; lx += 26 + s.name.length * 11; });
    return { X: X, Y: Y };
  }
  function bars(svg, o){
    svg.innerHTML = ''; var W = o.w || 640, H = o.h || 240, L = 46, R = 10, T = 18, B = 30;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('class', 'chart');
    var k = o.series.length, n = o.labels.length; var all = [0]; o.series.forEach(function(s){ all = all.concat(s.values); });
    var lo = o.min != null ? o.min : Math.min.apply(null, all), hi = o.max != null ? o.max : Math.max.apply(null, all) * 1.08;
    var Y = function(v){ return T + (H - T - B) * (1 - (v - lo) / (hi - lo)); };
    for (var g = 0; g <= 4; g++){ var v = lo + (hi - lo) * g / 4, y = Y(v); el('line', { x1: L, x2: W - R, y1: y, y2: y, stroke: '#363a52' }, svg); el('text', { x: L - 6, y: y + 4, 'text-anchor': 'end' }, svg).textContent = nice(v); }
    if (o.ref != null){ var yr = Y(o.ref); el('line', { x1: L, x2: W - R, y1: yr, y2: yr, stroke: '#f1b646', 'stroke-dasharray': '4 4' }, svg); }
    var bw = (W - L - R) / n;
    o.labels.forEach(function(lb, i){
      o.series.forEach(function(s, j){
        var v = s.values[i], x = L + bw * i + bw * .12 + (bw * .76 / k) * j, y0 = Y(Math.max(lo, 0)), y = Y(v);
        var r = el('rect', { x: x, y: Math.min(y, y0), width: bw * .76 / k - 1, height: Math.abs(y0 - y), fill: (s.colorAt ? s.colorAt(v, i) : s.color), rx: 2 }, svg);
        var tt = el('title', {}, r); tt.textContent = lb + ' · ' + (s.name || '') + ' ' + nice(v);
        if (o.values) el('text', { x: x + (bw * .76 / k) / 2, y: (v >= 0 ? y - 4 : y + 12), 'text-anchor': 'middle', style: 'fill:#eceaf3' }, svg).textContent = o.fmt ? o.fmt(v) : nice(v);
      });
      el('text', { x: L + bw * i + bw / 2, y: H - 10, 'text-anchor': 'middle' }, svg).textContent = lb;
    });
    var lx = L + 6; o.series.forEach(function(s){ if (!s.name) return; el('rect', { x: lx, y: 4, width: 10, height: 10, fill: s.color }, svg); el('text', { x: lx + 14, y: 13 }, svg).textContent = s.name; lx += 24 + s.name.length * 11; });
  }
  window.Chart = { line: line, bars: bars, nice: nice };

  /* ---------- 위젯 등록 ---------- */
  window.W = window.W || {};
  function initWidgets(){
    $$('[data-w]').forEach(function(box){
      var f = window.W[box.getAttribute('data-w')];
      if (f) { try { f(box); } catch(e){ console.error('widget', box.getAttribute('data-w'), e); box.insertAdjacentHTML('beforeend', '<p class="lim">이 실험은 지금 열리지 않습니다. 새로고침해 보세요.</p>'); } }
    });
  }
  window.rng = function(seed){ var s = seed >>> 0 || 1; return function(){ s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 1e6) / 1e6; }; };

  function boot(){ Cast.fill(); initGloss(); initQuiz(); initCopy(); initProg(); initWidgets(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
