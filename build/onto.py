#!/usr/bin/env python3
"""챕터·실습 리포트 페이지에 지식 색인(#kg)·꾸러미(#export)를 붙인다 (ai-lab-retrofit 도구 사용).
  python3 build/onto.py <retrofit 도구 폴더>
"""
import json, os, re, subprocess, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TOOLS = sys.argv[1]
sys.path.insert(0, HERE)
import build as B
DATE = '2026-11-13'; SITE = B.SITE
strip = lambda s: re.sub(r'<[^>]+>', '', s or '').strip()
first = lambda s: (re.split(r'(?<=[.다요])\s', strip(s)) or [''])[0][:160]


def node(i, t, ko, page, anchor, level=2, definition=None, conf='high', dom=('ai', 'mfg'), **kw):
    n = {'id': i, 'type': t, 'label': {'ko': ko[:120], 'en': ''}, 'page': page, 'anchor': anchor, 'level': level, 'status': 'known',
         'confidence': conf, 'coverage': 'explained', 'match': []}
    if t not in ('Work', 'QuizItem', 'Topic', 'Area'): n['domain'] = list(dom)
    if definition: n['definition'] = {'ko': definition}
    n.update(kw); return n


def edge(s, p, o, anchor, conf='high'):
    return {'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': anchor, 'confidence': conf}


def ref(rid, title, typ='report', note='author'):
    return {'id': rid, 'type': typ, 'title': title, 'author': [{'family': '안', 'given': '상선'}], 'issued': {'date-parts': [[2026]]},
            'lab': {'work': 'lab:work/' + rid, 'role': 'primary', 'supports': [], 'locs': [], 'verified': {'title': True, 'author': True, 'year': True, 'container': False, 'pages': False, 'doi': False},
                    'checkedBy': '저자 강의 자료', 'checkedSource': note}}


def meta(title, number, about, basis, typ='interactive explainer', url=''):
    return {'title': title, 'number': number, 'series': '스마트 제조 연구실', 'about': about, 'basedOn': basis, 'educationalLevel': '입문',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': DATE, 'version': '1.0',
            'language': ['ko'], 'license': '', 'url': url, 'registry': 'KG_00_registry 0.2', 'learningResourceType': typ, 'seeAlso': '',
            'suggestedCitation': f'안상선 (2026). {title}. 스마트 제조 연구실 {number}, v1.0.'}


def chapter_kg(m, slug):
    CH = m.CH; page = slug; topic = f'lab:topic/smart-manufacturing-{slug}'
    rid = f'ahn2026sm{slug}'
    N, E = [], []
    N.append(node(f'lab:work/{rid}', 'Work', f'안상선 (2026) 스마트 제조 {CH["num"]} 강의 자료', page, '#kgx'))
    prev = None
    for k, s in enumerate(CH['subs']):
        cid = f'lab:concept/sm-{slug}-{k + 1:02d}'
        body = ' '.join(x for x in s.get('body', []) if not x.startswith('<div'))
        N.append(node(cid, 'Concept', strip(s['title']), page, '#' + s['id'], 2, first(body) or strip(s['title'])))
        E.append(edge(cid, 'broader', topic, '#' + s['id']))
        if k == 0: E.append(edge(cid, 'derivedFrom', f'lab:work/{rid}', '#' + s['id']))
        if prev: E.append(edge(prev, 'prerequisiteOf', cid, '#' + s['id'], 'medium'))
        if s.get('limit'):
            lid = f'lab:limit/sm-{slug}-{k + 1:02d}'
            N.append(node(lid, 'Limitation', strip(s['limit'])[:80], page, '#' + s['id'], 3, strip(s['limit'])[:200]))
            E.append(edge(cid, 'hasLimitation', lid, '#' + s['id']))
        for j, q in enumerate(s.get('quiz') or []):
            qid = f'lab:quiz/sm-{slug}-{k + 1:02d}-{j + 1}'
            N.append(node(qid, 'QuizItem', strip(q['q']), page, '#q-' + s['id']))
            E.append(edge(qid, 'assesses', cid, '#q-' + s['id']))
        prev = cid
    if CH.get('duel'):
        sid = f'lab:sim/sm-{slug}-duel'
        N.append(node(sid, 'Simulation', '대결 — ' + strip(CH['duel']['q']), page, '#duel', 2, strip(CH['duel']['q'])))
        E.append(edge(f'lab:concept/sm-{slug}-01', 'demonstratedBy', sid, '#duel', 'medium'))
    refs = [ref(rid, f'스마트 제조 {CH["num"]} 강의 교안·수업 자료')]
    mt = meta(strip(CH['title']), CH['num'], [f'lab:concept/sm-{slug}-01'], [rid], url=SITE + f'weeks/{slug}/index.html')
    return {'version': '1.0', 'page': page, 'nodes': N, 'edges': E}, refs, mt


def report_kg(m, slug):
    RP = m.RP; page = slug + '-practice'; rid = f'ahn2026sm{slug}r'; did = f'lab:dataset/sm-{slug}'
    sec = [s['id'] for s in RP['sections']]
    N = [node(f'lab:work/{rid}', 'Work', f'안상선 (2026) 스마트 제조 {slug} 실습 계산', page, '#refs'),
         node(f'lab:claim/sm-{slug}-finding', 'Claim', strip(RP['summary']['finding']), page, '#summary', 4, strip(RP['summary']['finding']), source=[{'ref': rid, 'loc': 'Summary'}]),
         node(did, 'Dataset', '수업 데이터 (가상)', page, '#' + sec[2], 2, '이 리포트가 계산에 쓴 수업용 데이터'),
         node(f'lab:method/sm-{slug}', 'Method', '방법 — ' + strip(RP['sections'][2]['title']), page, '#' + sec[2], 2, strip(RP['sections'][2]['title'])),
         node(f'lab:limit/sm-{slug}', 'Limitation', '의의와 한계', page, '#' + sec[-1], 3, '가상 데이터·작은 표본 등 리포트가 밝힌 한계'),
         node(f'lab:question/sm-{slug}', 'Question', '추측·후속 과제', page, '#' + sec[-2], 3, '반론과 다른 설명 장의 추측'),
         node(f'lab:claim/sm-{slug}-alt', 'Claim', '반론과 다른 설명', page, '#' + sec[-2], 3, '같은 결과를 달리 설명하는 길', conf='medium')]
    E = [edge(f'lab:claim/sm-{slug}-finding', 'assertedIn', f'lab:work/{rid}', '#summary'),
         edge(f'lab:method/sm-{slug}', 'evaluatedOn', did, '#' + sec[2]),
         edge(f'lab:method/sm-{slug}', 'supports', f'lab:claim/sm-{slug}-finding', '#' + sec[3]),
         edge(f'lab:claim/sm-{slug}-finding', 'hasLimitation', f'lab:limit/sm-{slug}', '#' + sec[-1]),
         edge(f'lab:claim/sm-{slug}-finding', 'raises', f'lab:question/sm-{slug}', '#' + sec[-2]),
         edge(f'lab:claim/sm-{slug}-alt', 'contrastsWith', f'lab:claim/sm-{slug}-finding', '#' + sec[-2], 'medium'),
         edge(f'lab:method/sm-{slug}', 'broader', f'lab:topic/smart-manufacturing-{slug}', '#' + sec[2])]
    for k, ev in enumerate(RP['summary']['evidence']):
        kind = 'high' if '사실' in ev else 'medium'
        cid = f'lab:claim/sm-{slug}-ev{k + 1}'
        N.append(node(cid, 'Claim', strip(ev).replace('사실 ', '').replace('해석 ', '')[:120], page, '#summary', 3, strip(ev)[:220], conf=kind, source=[{'ref': rid, 'loc': 'Summary'}]))
        E.append(edge(cid, 'supports', f'lab:claim/sm-{slug}-finding', '#summary', kind))
    refs = [ref(rid, f'스마트 제조 {slug} 실습 리포트 계산 (analysis/)', 'dataset')]
    mt = meta(strip(RP['title']), slug + '-R', [f'lab:claim/sm-{slug}-finding'], [rid], 'finding report', SITE + f'weeks/{slug}/practice.html')
    return {'version': '1.0', 'page': page, 'nodes': N, 'edges': E}, refs, mt


def run(page_rel, kg, refs, mt, tag):
    d = os.path.join(ROOT, 'onto', tag); os.makedirs(d, exist_ok=True)
    for n, o in (('kg.json', kg), ('refs.json', refs), ('meta.json', mt)):
        json.dump(o, open(os.path.join(d, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    page = os.path.join(ROOT, page_rel); orig = os.path.join(d, 'orig.html')
    open(orig, 'w', encoding='utf-8').write(open(page, encoding='utf-8').read())
    subprocess.run([sys.executable, os.path.join(TOOLS, 'retrofit.py'), orig, '--kg', os.path.join(d, 'kg.json'), '--refs', os.path.join(d, 'refs.json'),
                    '--meta', os.path.join(d, 'meta.json'), '--js', '../../assets/kgx.js', '-o', page], check=True, cwd=TOOLS, stdout=subprocess.DEVNULL)
    r = subprocess.run([sys.executable, os.path.join(TOOLS, 'check.py'), orig, page, '--report', os.path.join(d, 'check_report.md')], cwd=TOOLS, capture_output=True, text=True)
    os.remove(orig)
    print(tag, 'nodes', len(kg['nodes']), 'edges', len(kg['edges']), '| check exit', r.returncode, (r.stdout.strip().splitlines() or [''])[-1][:120])


if __name__ == '__main__':
    for slug, num, title, sec, st in B.CHAPTERS:
        if st != 'built': continue
        m = B.load(slug)
        run(f'weeks/{slug}/index.html', *chapter_kg(m, slug), slug)
        if hasattr(m, 'RP'): run(f'weeks/{slug}/practice.html', *report_kg(m, slug), slug + '-practice')
