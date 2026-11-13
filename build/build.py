#!/usr/bin/env python3
"""스마트 제조 연구실 사이트 빌더.
content/*.py 의 CH(챕터)·RP(실습 리포트) 사전을 읽어 정적 HTML을 만든다.
  python3 build/build.py          → 저장소 루트에 weeks/…/index.html, practice.html 생성
"""
import html, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://adminmrobo.github.io/smart_product/'
AUTHOR = '글 · 안상선 (<a href="https://www.ahnboat.xyz">www.ahnboat.xyz</a>) · (주)M-Robo 대표'
WHO = {'doc': '박사', 'asst': '조수(하루)', 'fly': '초파리 연구원', 'robo': '주판봇', 'sia': '인턴 시아', 'moa': '인턴 모아',
       'x1': '미공개 X1', 'x2': '미공개 X2', 'x3': '미공개 X3'}
ROLE = {'doc': '해설과 판정. 판단은 데이터대로 합니다.', 'asst': '꼼꼼한 조수. 처음 배우는 사람의 눈높이로 묻고 숫자를 발표합니다.',
        'fly': '의심하는 연구원. "그 숫자, 정말 맞아?"를 맡습니다.', 'robo': '확신하는 계산 로봇. 빠르지만 가끔 성급합니다.',
        'sia': '인턴 · 조수1. 순서를 정리하고 안내합니다.', 'moa': '인턴 · 조수2. 기록을 모으고 응원합니다.',
        'x1': '미공개 식구 · 리본', 'x2': '미공개 식구 · 모자', 'x3': '미공개 식구 · 꼬마'}
E = html.escape

# ── 장(챕터) 목록: 15주 + 부록 2 = 17 ─────────────────────────────
CHAPTERS = [
    ('w01', '01', '오리엔테이션 & 스마트 제조란', 'SECTION 1 · 준비', 'built'),
    ('w02', '02', '생성형 AI 원리 & 프롬프트 기초', 'SECTION 1 · 준비', 'built'),
    ('w03', '03', '생산실적 추세 분석 — 시계열의 원리', 'SECTION 2 · 데이터', 'built'),
    ('w04', '04', '분류와 회귀 — 데이터에 말 걸기', 'SECTION 2 · 데이터', 'built'),
    ('w05', '05', '작업지시서와 한 페이지 앱', 'SECTION 2 · 데이터', 'built'),
    ('w06', '06', 'REVIEW — 1~5주 다시 보기', 'REVIEW', 'built'),
    ('w07', '07', '불량 분석 ① 어디서 터지는가', 'SECTION 3 · 분석', 'built'),
    ('w08', '08', '중간 점검 — 보고서 주제 카드', '중간 점검', 'built'),
    ('w09', '09', '불량 분석 ② 왜 터지는가', 'SECTION 3 · 분석', 'slot'),
    ('w10', '10', '설비 효율(OEE) 분석', 'SECTION 3 · 분석', 'slot'),
    ('w11', '11', '시각화 & 1페이지 대시보드', 'SECTION 3 · 분석', 'slot'),
    ('w12', '12', '문서 자동화 ① 생산일보·점검일지', 'SECTION 4 · 자동화', 'slot'),
    ('w13', '13', '문서 자동화 ② 품질보고서·시정조치', 'SECTION 4 · 자동화', 'slot'),
    ('w14', '14', '작업지시서·SOP 자동 생성', 'SECTION 4 · 자동화', 'slot'),
    ('w15', '15', 'REVIEW — 공정 자동화와 기말 제출', 'REVIEW', 'slot'),
    ('appA', 'A', '부록 A · 데이터 창고', '부록', 'built'),
    ('appB', 'B', '부록 B · 프롬프트 공구함', '부록', 'built'),
]
SLOT_PLAN = {
    'w07': '불량 유형 집계, 파레토, 공정·설비 분포',
    'w08': '개인별 제출물 — 문제 정의 → 현황 분석 → 원인 규명 → 자동화 구상 → 기대효과·90일 계획',
    'w09': '4M 관점 요인 분해, 가설 5개 생성',
    'w10': '가동률 × 성능 × 양품률, 자동 계산 시트',
    'w11': '경영진용 vs 현장 게시용, 목적별 차트 선택',
    'w12': '회사 양식 프롬프트 이식, 나만의 AI 비서',
    'w13': '8D 구조화, 고객 제출용 문체',
    'w14': '숙련자 암묵지 인터뷰, 신입 교육용 요약',
    'w15': '7~14주 다시 보기 + 공정 자동화 워크플로우(트리거 → AI 처리 → 전달), 자동 리포트 발송 흐름 제출',
}


def load(name):
    p = os.path.join(HERE, 'content', name + '.py')
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def head(title, desc, root, og=None, three=False, extra=''):
    og = og or SITE + 'img/cover.webp'
    im = ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",'
          '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>') if three else ''
    return f'''<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{og}">
<meta name="author" content="안상선">
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/lab.css">
{im}{extra}
</head>'''


def nav(root, links, title='스마트 제조 <b>연구실</b>'):
    a = ''.join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top" aria-label="이 페이지 목차"><a class="logo" href="{root}index.html">{title}</a><div class="links">{a}</div></nav><div id="prog"></div>'


def say(who, mood, text):
    name = WHO[who]
    return (f'<div class="say" data-who="{who}"><img class="who" data-who="{who}" data-mood="{mood}" alt="" aria-hidden="true">'
            f'<div class="bub"><b class="name">{name}</b><p>{text}</p></div></div>')


def talk(lines):
    return '<div class="talk">' + ''.join(say(*l) for l in lines) + '</div>' if lines else ''


def quiz(qs, qid):
    return f"<div class=\"quiz\" id=\"{qid}\" data-q='{E(json.dumps(qs, ensure_ascii=False))}'></div>" if qs else ''


class Gl:
    """용어 밑줄: 페이지에서 처음 나오는 곳 한 번만"""
    def __init__(self, gl): self.gl = gl; self.done = set()
    def __call__(self, s):
        for k in sorted(self.gl, key=len, reverse=True):
            if k in self.done: continue
            # 태그 밖 글자에서만 찾는다
            parts = re.split(r'(<[^>]+>)', s); found = False
            for i, p in enumerate(parts):
                if p.startswith('<') or found: continue
                j = p.find(k)
                if j >= 0:
                    parts[i] = p[:j] + f'<span class="jt" data-t="{E(k)}">{k}</span>' + p[j + len(k):]; found = True
            if found: self.done.add(k); s = ''.join(parts)
        return s


def paras(lst, g):
    out = []
    for p in lst:
        if p.startswith('<'): out.append(g(p))
        else: out.append('<p>' + g(p) + '</p>')
    return ''.join(out)


def render_sub(s, g, n):
    h = [f'<article class="lvl" id="{s["id"]}">',
         f'<div class="lvl-head"><div class="hex" aria-hidden="true">{s["no"]}</div><div><h3 style="margin:.1em 0">{s["title"]}</h3>'
         f'<div class="tags">' + ''.join(f'<span class="tag t">{E(t)}</span>' for t in s.get('tags', [])) + '</div></div></div>']
    if s.get('pair'):
        lt, ltx, rt, rtx = s['pair']
        h.append(f'<div class="pair"><div><h4>{lt}</h4><p style="margin:0">{g(ltx)}</p></div><div><h4>{rt}</h4><p style="margin:0">{g(rtx)}</p></div></div>')
    if s.get('why') or s.get('fx'):
        h.append('<div class="wf">')
        if s.get('why'):
            w = s['why']
            h.append(f'<div class="why"><h4>왜 이 방법을 쓰나</h4><p>{g(w["problem"])}</p><p>{g(w["limit"])}</p><p>{g(w["solve"])}</p><div class="easy">쉽게 말하면 — {w["easy"]}</div></div>')
        if s.get('fx'):
            f = s['fx']
            rows = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in f['rows'])
            h.append(f'<div class="fx"><h4>수학 수식을 어려워하는 조수가 대신 물어봅니다</h4>'
                     + say('asst', 'e04', f['q']) +
                     f'<p style="font-size:14px;color:var(--muted);margin:8px 0 2px">학교 수학으로 보면 · {f["school"]}</p>'
                     f'<div class="eq">{f["eq"]}</div><table>{rows}</table>'
                     f'<p><b style="color:var(--amber)">숫자로 한 번 해 보기</b> — {f["calc"]}</p>' + say('asst', 'e10', f['comment']) + '</div>')
        h.append('</div>')
    if s.get('body'): h.append(paras(s['body'], g))
    h.append(talk(s.get('talk', [])))
    if s.get('widget'):
        name, inner = s['widget']
        h.append(f'<div class="panel" data-w="{name}" id="w-{s["id"]}">{inner}</div>')
    if s.get('explain'):
        h.append('<div class="explain"><h4>풀이</h4>' + paras(s['explain'], g) + '</div>')
    if s.get('limit'): h.append(f'<p class="lim"><b>이 칸의 한계</b> — {s["limit"]}</p>')
    if s.get('bridge'): h.append(f'<div class="bridge"><h4>{s["bridge"][0]}</h4><p style="margin:0">{s["bridge"][1]}</p></div>')
    if s.get('code'):
        rows = ''.join(f'<tr><td><code>{E(c)}</code></td><td>{m}</td></tr>' for c, m in s['code'])
        h.append(f'<details><summary>교안의 파이썬 코드로 보면 (몰라도 됩니다)</summary><div class="tw"><table class="tb">{rows}</table></div></details>')
    h.append(quiz(s.get('quiz'), 'q-' + s['id']))
    h.append('</article>')
    return ''.join(h)


def footer(sources, notes, prev=None, nxt=None, root='../../'):
    src = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in sources)
    pn = '<div class="navpn">' + (f'<a href="{prev[0]}">← {prev[1]}</a>' if prev else '<span></span>') + (f'<a href="{nxt[0]}">{nxt[1]} →</a>' if nxt else '') + '</div>'
    return (f'<footer><div class="wrap">{pn}<h3 style="margin-top:0">출처와 표기</h3><table>{src}</table>'
            f'<p>예시값·설명용 모형: {notes}</p>'
            f'<p>{AUTHOR}<br>캐릭터 이름·설정·그림 © 안상선 (<a href="https://github.com/adminmrobo/fruitfly-lab-expressions">fruitfly-lab-expressions</a>). 허락 없이 쓸 수 없습니다. 3D 화면은 three.js(MIT)를 씁니다.</p>'
            f'<p><a href="{root}index.html">스마트 제조 연구실 첫 화면</a></p></div></footer>')


def chapter_links(slug):
    i = [c[0] for c in CHAPTERS].index(slug)
    def link(j):
        c = CHAPTERS[j]; return (f'../{c[0]}/index.html', (f'{c[1]}주차 ' if c[1].isdigit() else '') + c[2])
    return (link(i - 1) if i > 0 else None), (link(i + 1) if i < len(CHAPTERS) - 1 else None)


def render_chapter(CH):
    root = '../../'
    g = Gl(CH.get('glossary', {}))
    subs = CH['subs']
    for k, s in enumerate(subs, 1): s['no'] = s.get('no') or f'{CH["num"]}.{k}'
    links = [('#three', '3줄'), ('#cast', '등장인물'), ('#why', '왜'), ('#map', '큰 그림'), ('#' + subs[0]['id'], '본문')]
    if CH.get('duel'): links.append(('#duel', '대결'))
    links += [('#sum', '정리'), ('#outro', '마무리'), ('#kgx', '색인')]
    if CH.get('practice'): links.append((CH['practice'][0], '실습 리포트'))
    title = f'{CH["num"]}주차 · {CH["title"]} — 스마트 제조 연구실' if CH['num'].isdigit() else f'{CH["title"]} — 스마트 제조 연구실'
    out = [head(title, CH['desc'], root, og=SITE + 'img/' + CH['slug'] + '.webp', three=True), f'<body data-root="{root}">', nav(root, links)]
    # 히어로
    kp = ''.join(f'<div class="kpi {c}"><b>{v}</b><span>{l}</span></div>' for v, l, c in CH.get('kpis', []))
    out.append(f'''<header class="hero"><div class="wrap">
<span class="eyebrow">{E(CH["eyebrow"])}</span>
<h1>{CH["title"]}</h1>
<p class="lead"><b>핵심 질문</b> — {CH["q"]}</p>
<p class="lead" style="font-size:16px">{CH["lead"]}</p>
<div class="stage" id="stage" aria-label="{E(CH["scene_alt"])}"><canvas></canvas><div class="hud">{CH["scene_hud"]}</div><div class="hud2" id="hud2"></div></div>
<p style="font-size:13px;color:var(--muted);margin-top:-6px">끌어서 돌리고, 휠·두 손가락으로 확대합니다. 물체에 손을 올리면 설명이 뜹니다.</p>
<div class="kpis">{kp}</div>
{talk(CH.get("hero_talk", []))}
</div></header><main>''')
    # 3줄
    t = CH['three']; ab = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in CH.get('abbr', []))
    out.append(f'''<section class="first" id="three"><div class="wrap narrow"><div class="three">
<h2 style="font-size:22px">처음 오신 분께 — 이 페이지를 3줄로</h2>
<ol><li><b>무엇을</b> — {t[0]}</li><li><b>왜 중요한가</b> — {t[1]}</li><li><b>업무에서는</b> — {t[2]}</li></ol>
<p class="nocode">코드·수식을 몰라도 됩니다. 이 과목은 노코딩으로 설계되어 있습니다.</p>
{f'<details><summary>이 페이지에 나오는 영어 약어 풀이</summary><div class="tw"><table class="tb"><tr><th>약어</th><th>풀어 쓰면</th><th>뜻</th></tr>{ab}</table></div></details>' if ab else ''}
</div></div></section>''')
    # 등장인물
    cast = ''.join(f'<div class="c{" secret" if w.startswith("x") else ""}"><img data-who="{w}" data-mood="{"e13" if w.startswith("x") else "e01"}" alt="{WHO[w]}"><div><b>{WHO[w]}</b><span>{CH.get("roles", {}).get(w, ROLE[w])}</span></div></div>'
                   for w in ['doc', 'asst', 'fly', 'robo', 'sia', 'moa', 'x1', 'x2', 'x3'])
    toc = ''.join(f'<a href="#{s["id"]}"><i>{s["no"]}</i>{re.sub("<[^>]+>", "", s["title"])}</a>' for s in subs)
    out.append(f'''<section id="cast"><div class="wrap"><h2>등장인물과 이 페이지 사용법</h2>
<div class="cast">{cast}</div>
<p style="margin-top:14px">점선 밑줄이 있는 말은 누르면 뜻이 나옵니다. 칸마다 실험 패널과 확인 퀴즈가 있습니다. 미공개 식구 X1~X3는 말 대신 소리로만 등장합니다.</p>
{CH.get("prev_note", "")}
<h3>세부 챕터 {len(subs)}개</h3><div class="toc">{toc}</div>
{f'<p><a class="bt primary" style="text-decoration:none;display:inline-block" href="{CH["practice"][0]}">실습 리포트 열기 — {CH["practice"][1]}</a></p>' if CH.get("practice") else ""}
</div></section>''')
    # 왜 · 큰 그림
    why = ''.join(f'<div><b>{a}</b><p style="margin:6px 0 0">{g(b)}</p></div>' for a, b in CH['why'])
    big = ''.join(f'<div><b>{a}</b><p style="margin:6px 0 0">{g(b)}</p></div>' for a, b in CH['big'])
    out.append(f'<section id="why"><div class="wrap"><h2>왜 이 주제인가</h2><div class="steps">{why}</div></div></section>')
    out.append(f'<section id="map"><div class="wrap"><h2>큰 그림</h2><p>{CH.get("big_lead", "")}</p><div class="steps big" style="--n:{len(CH["big"])}">{big}</div>{CH.get("big_extra", "")}</div></section>')
    # 본문 칸
    out.append('<section id="body"><div class="wrap"><h2>본문</h2>' + ''.join(render_sub(s, g, i) for i, s in enumerate(subs)) + '</div></section>')
    # 대결
    if CH.get('duel'):
        d = CH['duel']
        out.append(f'''<section id="duel"><div class="wrap"><h2>대결 — {d["q"]}</h2>
{talk(d.get("intro", []))}
<div class="duel"><div class="side">{say("fly", "e09", d["fly"])}</div><div class="vs">VS</div><div class="side">{say("robo", "e16", d["robo"])}</div></div>
<div class="panel" data-w="{d["widget"]}" id="w-duel">{d.get("panel", "")}</div>
<div class="verdict" id="verdict" aria-live="polite">{say("doc", "e10", d["verdict"])}</div>
{talk(d.get("after", []))}
</div></section>''')
    # 정리
    sm = CH['summary']
    rows = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in sm['rows'])
    head_ = ''.join(f'<th>{c}</th>' for c in sm['head'])
    lims = ''.join(f'<li>{x}</li>' for x in sm.get('limits', []))
    out.append(f'''<section id="sum"><div class="wrap"><h2>정리</h2><div class="tw"><table class="tb"><tr>{head_}</tr>{rows}</table></div>
<div class="explain"><h4>비유와 이 페이지의 한계</h4><ul>{lims}</ul></div>{sm.get("extra", "")}</div></section>''')
    out.append(f'<section id="outro"><div class="wrap"><h2>마무리</h2>{talk(CH["outro"])}</div></section>')
    out.append('<section id="kgx"><div class="wrap"><p style="color:var(--muted)">아래는 이 페이지의 지식 색인과 내려받기 꾸러미입니다.</p></div></section>')
    out.append('</main>')
    prev, nxt = chapter_links(CH['slug'])
    out.append(footer(CH['sources'], CH['notes'], prev, nxt))
    gl = json.dumps(CH.get('glossary', {}), ensure_ascii=False).replace('</', '<\\/')
    out.append(f'<script>window.GL={gl};</script>')
    if CH.get('js'): out.append('<script>var W=window.W=window.W||{};\n' + CH['js'] + '\n</script>')
    out.append(f'<script src="{root}assets/lab.js"></script>')
    out.append(f'''<script type="module">
import {{ mount }} from '{root}assets/sf3d.js';
import {{ scenes }} from '{root}assets/scenes.js';
const st = document.getElementById('stage');
mount(st, api => scenes['{CH["slug"]}'](api, st), {json.dumps(CH.get("scene_opts", {}))});
</script>''')
    out.append('</body></html>')
    return '\n'.join(out)


# ── 실습 리포트 (발견편 형식) ──────────────────────────────────────
def memo(mood, text):
    return f'<div class="memo"><img data-who="doc" data-mood="{mood}" alt="" aria-hidden="true"><div><b>박사의 메모</b><p style="margin:4px 0 0">{text}</p></div></div>'


def render_block(b):
    k = b[0]
    if k == 'p': return f'<p>{b[1]}</p>'
    if k == 'key': return f'<p class="key">{b[1]}</p>'
    if k == 'html': return b[1]
    if k == 'memo': return memo(b[1], b[2])
    if k == 'prompt': return f'<div class="prompt" data-raw="{E(b[1])}">{E(b[1])}</div>'
    if k == 'fig':
        f = b[1]
        return (f'<figure class="fig" id="{f["id"]}" style="margin:16px 0"><div class="cap">{f["cap"]}</div>'
                f'<div class="cwrap"><svg data-w="{f["w"]}" role="img" aria-label="{E(f["alt"])}"></svg></div>'
                f'{f.get("ctrl", "")}<div class="src">{f["src"]}</div></figure>')
    if k == 'table':
        t = b[1]
        hd = ''.join(f'<th>{c}</th>' for c in t['head'])
        rows = ''.join('<tr>' + ''.join(f'<td{" class=n" if isinstance(c, (int, float)) or (isinstance(c, str) and re.fullmatch(r"[−\-+]?[\d,.]+%?", c)) else ""}>{c}</td>' for c in r) + '</tr>' for r in t['rows'])
        return (f'<div class="fig" id="{t["id"]}"><div class="cap">{t["cap"]}</div><div class="tw"><table class="tb"><tr>{hd}</tr>{rows}</table></div>'
                f'<div class="src">{t["src"]}</div></div>')
    if k == 'widget': return f'<div class="panel" data-w="{b[1]}" id="{b[2]}">{b[3] if len(b) > 3 else ""}</div>'
    raise ValueError(k)


def render_report(RP):
    root = '../../'
    secs = RP['sections']
    links = [('#summary', 'Summary')] + [('#' + s['id'], s['nav']) for s in secs] + [('#kgx', '색인')]
    out = [head(RP['title'] + ' — 스마트 제조 연구실 실습 리포트', RP['desc'], root, og=SITE + 'img/' + RP.get('slug', 'cover') + '.webp'), f'<body data-root="{root}" class="report">', nav(root, links)]
    sm = RP['summary']
    ev = ''.join(f'<li>{x}</li>' for x in sm['evidence'])
    out.append(f'''<header class="hero"><div class="wrap">
<span class="eyebrow">{E(RP["eyebrow"])}</span>
<h1>{RP["title"]}</h1>
<p class="lead">{RP["lead"]}</p>
<div style="display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap">
<img data-who="doc" data-mood="{RP.get("cover_mood", "e07")}" alt="자료를 펼쳐 설명하는 박사" style="width:140px;height:140px;border-radius:16px;border:2px solid var(--c-doc);background:var(--panel2)">
<p style="color:var(--muted);font-size:14px;max-width:560px">이 리포트는 박사 혼자 안내합니다. 숫자는 모두 수업용 가상 데이터를 직접 계산한 값이며, 실제 기업·공장 수치가 아닙니다.<br>표시: <span class="fact">사실</span>데이터에서 확인 · <span class="interp">해석</span>박사가 읽는 방식 · <span class="guess">추측</span>아직 검증하지 않은 것</p>
</div></div></header>
<main class="wrap"><div class="rlayout"><nav class="rtoc" aria-label="장 목차"><a href="#summary">Summary</a>{"".join(f'<a href="#{s["id"]}">{s["nav"]}</a>' for s in secs)}<a href="{RP["back"][0]}">← {RP["back"][1]}</a></nav><div>
<section class="first" id="summary"><h2>Summary</h2><p class="key">{sm["finding"]}</p><ul>{ev}</ul>{render_block(sm["fig"]) if sm.get("fig") else ""}</section>''')
    for s in secs:
        out.append(f'<section id="{s["id"]}"><h2>{s["title"]}</h2>' + ''.join(render_block(b) for b in s['blocks']) + '</section>')
    refs = ''.join(f'<li>{r}</li>' for r in RP['refs'])
    out.append(f'<section id="refs"><h2>참고 문헌 · 데이터 출처</h2><ol>{refs}</ol></section>')
    out.append('<section id="kgx"><p style="color:var(--muted)">아래는 이 리포트의 지식 색인과 내려받기 꾸러미입니다.</p></section></div></div></main>')
    out.append(footer(RP['sources'], RP['notes'], RP['back'], RP.get('next')))
    out.append('<script>window.GL={};</script>')
    if RP.get('js'): out.append('<script>var W=window.W=window.W||{};\n' + RP['js'] + '\n</script>')
    out.append(f'<script src="{root}assets/lab.js"></script></body></html>')
    return '\n'.join(out)


def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f: f.write(text)
    print('wrote', rel, len(text.encode()) // 1024, 'KB')


def main(only=None):
    for slug, num, title, sec, st in CHAPTERS:
        if only and slug not in only: continue
        if st == 'built':
            m = load(slug)
            if hasattr(m, 'CH'): write(f'weeks/{slug}/index.html', render_chapter(m.CH))
            if hasattr(m, 'PAGE'): write(f'weeks/{slug}/index.html', m.PAGE(sys.modules[__name__]))
            if hasattr(m, 'RP'): m.RP['slug'] = slug; write(f'weeks/{slug}/practice.html', render_report(m.RP))
        else:
            write(f'weeks/{slug}/index.html', render_slot(slug, num, title, sec))


def render_slot(slug, num, title, sec):
    root = '../../'
    prev, nxt = chapter_links(slug)
    rev = slug == 'w15'
    body = f'''{head(f"{num}주차 · {title} — 스마트 제조 연구실 (준비 중)", f"스마트 제조 {num}주차 {title} — 준비 중인 빈 슬롯", root)}
<body data-root="{root}">{nav(root, [])}
<header class="hero"><div class="wrap narrow"><span class="eyebrow">{num}주차 · {sec}</span><h1>{title}</h1>
<div class="slotbox"><p style="font-size:18px;margin:0 0 6px">이 챕터는 아직 비어 있는 슬롯입니다.</p>
<p style="margin:0">강의계획서에 적힌 내용: <b style="color:var(--text)">{SLOT_PLAN[slug]}</b></p>
<p style="margin:10px 0 0;font-size:14px">{"REVIEW 챕터로, 7~14주 챕터가 채워진 뒤 함께 만듭니다." if rev else "강의 자료가 준비되는 대로 1~6주와 같은 형식(세부 챕터 8~15개, 3D 장면, 실습 리포트)으로 채웁니다."}</p></div>
{talk([("doc", "e09", "이 방은 아직 공사 중입니다. 기계가 들어오면 불을 켤게요."), ("sia", "e07", "순서대로 채워 가겠습니다."), ("x2", "e09", "(…)")])}
</div></header>
{footer([("강의계획", "스마트 제조(AI212) 2026-2학기 OT 교안 · 주차별 계획")], "없음 (준비 중)", prev, nxt)}
<script src="{root}assets/lab.js"></script></body></html>'''
    return body




FACTORY = {'w01': '사출성형 A라인', 'w02': '케이블 하네스 조립', 'w03': '빙과·호빵 식품 공장', 'w04': '금속 판재 경화·검사', 'w05': 'CNC 밀링 가공 셀', 'w06': '면류 공장·물류',
           'w07': '기어 가공 라인', 'w08': 'SMT 전자부품 실장 라인', 'w09': '(준비 중)', 'w10': '(준비 중)', 'w11': '(준비 중)', 'w12': '(준비 중)', 'w13': '(준비 중)', 'w14': '(준비 중)', 'w15': '(준비 중)',
           'appA': '자재창고', 'appB': '공무실'}
SHORT = {'w01': 'OT·스마트 제조', 'w02': '생성형 AI·프롬프트', 'w03': '생산실적 추세', 'w04': '분류·회귀', 'w05': '작업지시서·앱', 'w06': 'REVIEW 1~5주',
         'w07': '불량 ① 어디서', 'w08': '중간 점검·주제 카드', 'w09': '불량 ② 왜', 'w10': 'OEE', 'w11': '대시보드', 'w12': '생산일보', 'w13': '품질보고서', 'w14': 'SOP', 'w15': 'REVIEW·기말',
         'appA': '데이터 창고', 'appB': '프롬프트 공구함'}


def render_hub():
    root = './'
    chaps = []
    cards = []
    for slug, num, title, sec, st in CHAPTERS:
        nsub, prac = 0, None
        if st == 'built':
            m = load(slug); nsub = len(m.CH['subs']); prac = getattr(m, 'RP', None) is not None
        status = 'app' if slug.startswith('app') else st
        review = 'REVIEW' in title
        stko = {'built': '공개', 'slot': '빈 슬롯 · 준비 중', 'app': '부록'}[status] + (' · REVIEW' if review else '')
        href = f'weeks/{slug}/index.html'
        chaps.append({'slug': slug, 'num': num, 'title': title, 'short': SHORT[slug], 'factory': FACTORY[slug], 'status': status, 'review': review, 'statusKo': stko, 'href': href})
        tag = '<span class="tag t">' + stko + '</span>'
        meta = f'세부 챕터 {nsub}개' if nsub else '세부 챕터는 자료가 오면 채움'
        pr = f' · <a href="weeks/{slug}/practice.html">실습 리포트</a>' if prac else ''
        cards.append(f'<div class="panel" style="margin:0;{"opacity:.6" if status == "slot" else ""}"><div style="display:flex;gap:10px;align-items:center"><div class="hex" style="width:44px;height:50px;font-size:14px;{"background:#4a4f63;color:#ccc" if status == "slot" else "background:#f1b646" if review else "background:#82b8ff" if status == "app" else ""}">{num}</div><div><b><a href="{href}" style="color:var(--text);text-decoration:none">{title}</a></b><div style="font-size:13px;color:var(--muted)">{sec} · {FACTORY[slug]}</div></div></div><p style="margin:8px 0 0;font-size:14px">{tag} {meta}{pr}</p></div>')
    goals = ''.join(f'<li><b>{a}</b> — {b}</li>' for a, b in [('데이터 이해', '생산일보·품질 데이터의 구조를 읽고, 생산량·불량률·OEE의 의미를 설명합니다.'), ('AI 분석', '엑셀 파일을 AI에 올려 정제·집계·추세·원인분석까지 대화만으로 수행합니다.'), ('시각화', '자연어 지시로 차트와 1페이지 대시보드를 만들고, 보고 목적에 맞는 차트를 고릅니다.'), ('문서 자동화', '생산일보·품질보고서·작업지시서·SOP를 표준 프롬프트로 자동 생성합니다.'), ('공정 자동화', '데이터 수집 → AI 분석 → 보고서 발송까지 이어지는 자동 흐름을 1개 구축합니다.'), ('현장 적용', '자신의 공정에 맞는 개선 과제를 정의하고 90일 실행계획으로 제안합니다.')])
    html_ = f'''{head("스마트 제조 연구실 — 3D로 보는 15주", "스마트 제조(AI212) 15주 강의를 차시마다 다른 3D 공장과 연구실 식구들이 안내하는 해설 사이트. 1~8주 공개, 9~15주 준비 중.", root, three=True)}
<body data-root="{root}">{nav(root, [("#campus", "캠퍼스"), ("#course", "강좌 개요"), ("#chapters", "17개 챕터"), ("#cast", "등장인물")])}
<header class="hero"><div class="wrap">
<span class="eyebrow">AI212 · 2026-2학기 · 스마트 제조 · 노코딩</span>
<h1>스마트 제조 연구실 — 3D로 보는 15주</h1>
<p class="lead">코딩 없이 생성형 AI로 공장 데이터를 분석하고 현장 문서를 자동화합니다. 주차마다 다른 공장(사출·하네스·식품·판재·CNC·면류·기어·SMT)이 3D로 서 있고, 연구실 식구들이 그 공정 위에서 안내합니다.</p>
<div class="stage" id="campus" aria-label="15주 공장 캠퍼스 3D. 주차별 작업장 17개가 컨베이어로 이어져 있고, 1~8주는 불이 켜져 있으며 9~15주는 준비 중이다. 작업장을 누르면 해당 챕터로 이동한다."><canvas></canvas><div class="hud">3D · 작업장을 누르면 그 주차로 들어갑니다 · 초록 컨베이어 = 공개된 주차</div><div class="hud2" id="hud2"></div></div>
<p style="font-size:13px;color:var(--muted);margin-top:-6px">끌어서 돌리고, 휠·두 손가락으로 확대합니다. 청록 = 공개 · 노랑 = REVIEW · 회색 = 빈 슬롯 · 파랑 = 부록</p>
<div class="kpis"><div class="kpi g"><b>8 / 15</b><span>공개된 주차 (9~15주 준비 중)</span></div><div class="kpi a"><b>17</b><span>챕터 (15주 + 부록 2)</span></div><div class="kpi m"><b>{sum(1 for c in chaps if c["status"] != "slot")}</b><span>공개 챕터</span></div><div class="kpi r"><b>7</b><span>실습 리포트 (2~8주)</span></div></div>
{talk([("doc", "e08", "어서 오세요. 스마트 제조 연구실입니다. 주차마다 공장이 하나씩 서 있습니다."), ("asst", "e01", "1주 사출성형 라인부터 8주 SMT 라인까지 열려 있어요!"), ("fly", "e09", "9주부터는 아직 불이 꺼져 있어. 자료가 오면 하나씩 켤 거야."), ("robo", "e16", "저는 컨베이어 끝까지 달려가겠습니다!")])}
</div></header><main>
<section id="course"><div class="wrap"><h2>강좌 개요</h2>
<p>이 강좌는 IoT, AI, 빅데이터 등 첨단 기술을 활용해 제조업의 효율성과 생산성을 높이는 방법을 배웁니다. 스마트 팩토리 시스템을 구축하고 운영하는 데 필요한 기술과 전략을 다룹니다. 센서·자동화·데이터 분석으로 실시간 모니터링과 예측 유지보수를 구현하는 방법을 배우고, 산업 현장의 스마트 기술 적용 사례와 최신 제조 기술 동향을 학습합니다.</p>
<h3>학습 목표</h3><ol>{goals}</ol>
<div class="steps big" style="--n:4"><div><b>SECTION 1 · 준비</b><p style="margin:6px 0 0">1~2주 · AI에게 말 거는 법</p></div><div><b>SECTION 2 · 데이터</b><p style="margin:6px 0 0">3~5주 · 읽고, 청소하고, 물어보기</p></div><div><b>SECTION 3 · 분석</b><p style="margin:6px 0 0">6~11주 · 6주 REVIEW, 8주 중간 제출</p></div><div><b>SECTION 4 · 자동화</b><p style="margin:6px 0 0">12~15주 · 15주 REVIEW·기말 제출</p></div></div>
<p style="font-size:14px;color:var(--muted)">시험일자는 학교 학사 일정 등에 따라 달라질 수 있습니다. 이 사이트의 주차 배정은 실제 진행 자료(1~8주 교안)를 따랐고, 9~15주 제목은 OT 교안의 주차별 계획에서 가져왔습니다.</p>
</div></section>
<section id="chapters"><div class="wrap"><h2>17개 챕터</h2><div class="toc" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr))">{"".join(cards)}</div></div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2><div class="cast">{"".join(f'<div class="c"><img data-who="{w}" data-mood="{"e13" if w.startswith("x") else "e01"}" alt="{WHO[w]}"><div><b>{WHO[w]}</b><span>{ROLE[w]}</span></div></div>' for w in ["doc", "asst", "fly", "robo", "sia", "moa", "x1", "x2", "x3"])}</div>
<p style="font-size:14px;color:var(--muted)">인턴 시아·모아가 조수1·조수2 자리를 맡습니다. 미공개 X1~X3는 말 대신 소리로만 등장합니다.</p></div></section>
</main>
<footer><div class="wrap"><p>{AUTHOR}</p><p>모든 공장은 교육용 가상 공장입니다. 데이터는 수업용 가상값이며 실제 기업·공장 수치가 아닙니다(면류 검색지수 제외).</p>
<p>캐릭터 이름·설정·그림 © 안상선 (<a href="https://github.com/adminmrobo/fruitfly-lab-expressions">fruitfly-lab-expressions</a>). 3D 화면은 three.js(MIT). 참고 사례: <a href="https://adminmrobo.github.io/smart_factory_world/">스마트 팩토리 World</a></p></div></footer>
<script>window.CHAPS={json.dumps(chaps, ensure_ascii=False)};</script>
<script src="{root}assets/lab.js"></script>
<script type="module">
import {{ mount }} from './assets/sf3d.js';
import {{ scenes }} from './assets/scenes.js';
const st = document.getElementById('campus');
mount(st, api => scenes.hub(api, st), {{ cam: [0, 25, 37], target: [0, 0, 1.5], ground: 70, maxD: 90 }});
</script></body></html>'''
    write('index.html', html_)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or 'hub' in args: render_hub()
    rest = [a for a in args if a != 'hub']
    if not args or rest: main(rest or None)
