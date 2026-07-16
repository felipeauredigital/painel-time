# -*- coding: utf-8 -*-
"""Gera o dashboard.html a partir de um model.json (estilo PBD: sidebar escura + accent dourado).
Uso: python render.py [model.json] [saida.html]   |   python render.py --demo"""
import json, os, sys, datetime, random

HERE = os.path.dirname(os.path.abspath(__file__))

def render(model):
    return HTML.replace("__MODEL__", json.dumps(model, ensure_ascii=False))

HTML = r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800&display=swap');
:root{
  --page:#f1ecfa; --side:#150d24; --side-2:#221636; --side-ink:#efe9fb; --side-muted:#a99cc4;
  --gold:#915fe3; --gold-2:#6f3fd0; --gold-soft:#efe6ff; --magenta:#bc3eff; --deep:#3d2661;
  --panel:#ffffff; --panel-2:#f7f3fe; --ink:#1e1630; --muted:#6d6683; --line:#ece6f8; --line-2:#ddd3ef;
  --good:#3fa36a; --blue:#3f7bc9; --crit:#e5484d; --high:#ef8f2e; --med:#e3b93d; --today:#948da6;
  --shadow-sm:0 1px 2px rgba(40,25,70,.05); --shadow:0 8px 26px rgba(50,30,90,.10);
  --r:18px; --r-sm:12px;
  --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --display:"Montserrat",var(--sans);
}
@media (prefers-color-scheme:dark){:root{
  --page:#0c0912; --side:#0a0612; --side-2:#170f26; --side-ink:#efe9fb; --side-muted:#9488ad;
  --gold:#a67ef0; --gold-2:#7d51d8; --gold-soft:#241a3c; --magenta:#c86bff; --deep:#2a1b45;
  --panel:#181024; --panel-2:#1f1530; --ink:#ece6f8; --muted:#9a90b0; --line:#282038; --line-2:#362b4a;
  --good:#5cb37b; --blue:#5b93da; --crit:#e9635f; --high:#eaa24c; --med:#e6cb5f; --today:#8f89a2;
  --shadow-sm:0 1px 2px rgba(0,0,0,.4); --shadow:0 10px 30px rgba(0,0,0,.5);
}}
:root[data-theme="light"]{--page:#f1ecfa;--side:#150d24;--side-2:#221636;--side-ink:#efe9fb;--side-muted:#a99cc4;--gold:#915fe3;--gold-2:#6f3fd0;--gold-soft:#efe6ff;--magenta:#bc3eff;--deep:#3d2661;--panel:#fff;--panel-2:#f7f3fe;--ink:#1e1630;--muted:#6d6683;--line:#ece6f8;--line-2:#ddd3ef;--good:#3fa36a;--blue:#3f7bc9;--crit:#e5484d;--high:#ef8f2e;--med:#e3b93d;--today:#948da6;--shadow-sm:0 1px 2px rgba(40,25,70,.05);--shadow:0 8px 26px rgba(50,30,90,.10);}
:root[data-theme="dark"]{--page:#0c0912;--side:#0a0612;--side-2:#170f26;--side-ink:#efe9fb;--side-muted:#9488ad;--gold:#a67ef0;--gold-2:#7d51d8;--gold-soft:#241a3c;--magenta:#c86bff;--deep:#2a1b45;--panel:#181024;--panel-2:#1f1530;--ink:#ece6f8;--muted:#9a90b0;--line:#282038;--line-2:#362b4a;--good:#5cb37b;--blue:#5b93da;--crit:#e9635f;--high:#eaa24c;--med:#e6cb5f;--today:#8f89a2;--shadow-sm:0 1px 2px rgba(0,0,0,.4);--shadow:0 10px 30px rgba(0,0,0,.5);}
*{box-sizing:border-box}
h1,h2,.brand b,.card-h h3,.acard h3,.stat .n,.donut .c b,.banner h2{font-family:var(--display)}
.wrap{font-family:var(--sans);background:var(--page);color:var(--ink);min-height:100vh;padding:16px;line-height:1.45;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.app{display:grid;grid-template-columns:236px 1fr;gap:16px;max-width:1360px;margin:0 auto;align-items:start}
@media(max-width:860px){.app{grid-template-columns:1fr}}

/* sidebar */
.side{background:var(--side);border-radius:22px;padding:18px 14px;position:sticky;top:16px;display:flex;flex-direction:column;gap:6px;min-height:calc(100vh - 32px)}
@media(max-width:860px){.side{position:static;min-height:0}}
.brand{display:flex;align-items:center;gap:10px;padding:8px 8px 18px;color:var(--side-ink)}
.brand .logo{display:inline-flex;flex-direction:column;align-items:flex-start;border:1.5px solid var(--gold);border-radius:9px;padding:4px 8px 3px;line-height:1;font-family:var(--display)}
.brand .logo .top{display:flex;align-items:flex-start;font-weight:800;font-size:17px;letter-spacing:-.02em}
.brand .logo .au{color:var(--side-ink)} .brand .logo .re{color:var(--gold)}
.brand .logo .dot{width:4px;height:4px;border-radius:50%;background:var(--gold);margin-left:2px;margin-top:2px}
.brand .logo .dig{font-family:var(--sans);font-size:6.5px;font-weight:700;letter-spacing:.34em;color:var(--gold);margin-top:2px;align-self:flex-end}
.brand .tag{font-size:12.5px;color:var(--side-muted);font-weight:700}
.navlbl{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--side-muted);font-weight:700;padding:12px 12px 6px}
.nav{background:transparent;border:0;width:100%;text-align:left;font-family:inherit;font-size:13.5px;font-weight:600;color:var(--side-muted);display:flex;align-items:center;gap:11px;padding:11px 12px;border-radius:12px;cursor:pointer}
.nav .ic{width:20px;text-align:center;font-size:15px;opacity:.9}
.nav:hover{color:var(--side-ink);background:var(--side-2)}
.nav[aria-current="true"]{background:linear-gradient(135deg,var(--gold),var(--magenta));color:#fff}
.tfilter{display:flex;gap:6px;padding:8px 6px 4px}
.tfilter button{flex:1;font-family:inherit;font-size:11.5px;font-weight:700;color:var(--side-muted);background:var(--side-2);border:0;border-radius:9px;padding:8px 4px;cursor:pointer}
.tfilter button[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2)}
:root[data-theme="dark"] .tfilter button[aria-pressed="true"]{color:var(--gold)}
.side-foot{margin-top:auto;display:flex;flex-direction:column;gap:10px;padding-top:12px}
.gen{font-size:11px;color:var(--side-muted);padding:0 12px}
.themetog{display:flex;background:var(--side-2);border-radius:11px;padding:4px;gap:4px}
.themetog button{flex:1;font-family:inherit;font-size:12px;font-weight:700;color:var(--side-muted);background:transparent;border:0;border-radius:8px;padding:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px}
.themetog button[aria-pressed="true"]{background:var(--gold);color:#fff}

/* main */
.main{display:flex;flex-direction:column;gap:16px;min-width:0}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.topbar h1{font-size:22px;font-weight:800;margin:0;letter-spacing:-.01em}
.content{display:grid;grid-template-columns:1fr 320px;gap:16px;align-items:start}
@media(max-width:1080px){.content{grid-template-columns:1fr}}
.col{display:flex;flex-direction:column;gap:16px;min-width:0}

/* banner */
.banner{background:linear-gradient(120deg,var(--gold) 0%,var(--magenta) 100%);border-radius:var(--r);padding:22px 24px;color:#fff;display:flex;justify-content:space-between;gap:18px;align-items:center;box-shadow:var(--shadow);position:relative;overflow:hidden}
.banner::after{content:"";position:absolute;right:-40px;top:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.12)}
.banner .bt{position:relative;z-index:1}
.banner h2{margin:0 0 6px;font-size:22px;font-weight:800;letter-spacing:-.01em}
.banner p{margin:0;font-size:13.5px;opacity:.9;max-width:52ch}
.banner .cta{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}
.banner .cta button{font-family:inherit;font-size:12.5px;font-weight:700;border:0;border-radius:10px;padding:9px 14px;cursor:pointer;background:#fff;color:var(--gold-2)}
.banner .cta button.ghost{background:rgba(255,255,255,.2);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.5)}
.avatar{width:74px;height:74px;border-radius:16px;background:rgba(255,255,255,.2);display:grid;place-items:center;font-size:24px;font-weight:800;color:#fff;position:relative;z-index:1;flex:none}

/* stat cards */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:14px 15px;box-shadow:var(--shadow-sm);display:flex;flex-direction:column;gap:8px}
.stat .ico{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;font-size:16px;background:var(--panel-2)}
.stat .n{font-size:24px;font-weight:800;line-height:1}
.stat .l{font-size:11.5px;color:var(--muted);font-weight:600}
.stat.crit .n{color:var(--crit)} .stat.crit .ico{background:color-mix(in srgb,var(--crit) 15%,transparent)}
.stat.gold .ico{background:var(--gold-soft)}

/* card */
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow-sm);overflow:hidden}
.card-h{padding:15px 18px;display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid var(--line)}
.card-h h3{margin:0;font-size:15px;font-weight:800}
.card-h .r{font-size:12.5px;color:var(--muted);font-weight:600;display:flex;gap:10px;align-items:center}
.linkish{font-family:inherit;font-size:12px;font-weight:700;color:var(--gold-2);background:transparent;border:0;cursor:pointer;padding:0}
:root[data-theme="dark"] .linkish{color:var(--gold)}
.pad{padding:16px 18px}

/* donut */
.donutwrap{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.donut{width:150px;height:150px;border-radius:50%;flex:none;display:grid;place-items:center;position:relative}
.donut::before{content:"";position:absolute;width:104px;height:104px;background:var(--panel);border-radius:50%}
.donut .c{position:relative;text-align:center}
.donut .c b{font-size:30px;font-weight:800;display:block;line-height:1}
.donut .c span{font-size:11px;color:var(--muted)}
.leg{flex:1;min-width:190px;display:flex;flex-direction:column;gap:12px}
.leg .row{display:grid;grid-template-columns:1fr auto;gap:4px 10px;align-items:center}
.leg .row .nm{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600}
.leg .row .nm .dot{width:11px;height:11px;border-radius:4px}
.leg .row .v{font-size:13px;font-weight:800}
.leg .track{grid-column:1/3;height:7px;border-radius:5px;background:var(--panel-2);overflow:hidden}
.leg .track span{display:block;height:100%;border-radius:5px}

/* activity rail */
.acard{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow-sm);padding:16px 16px}
.acard h3{margin:0 0 4px;font-size:14px;font-weight:800}
.acard .sub{font-size:11.5px;color:var(--muted);margin:0 0 12px}
.arow{display:flex;align-items:center;gap:11px;padding:9px 0;border-top:1px solid var(--line)}
.arow:first-of-type{border-top:0}
.ava{width:38px;height:38px;border-radius:11px;flex:none;display:grid;place-items:center;font-size:13px;font-weight:800;color:#fff}
.ava.E{background:linear-gradient(135deg,#915fe3,#6f3fd0)} .ava.F{background:linear-gradient(135deg,#bc3eff,#8f2bcf)}
.datebadge{width:42px;height:42px;border-radius:11px;background:var(--panel-2);display:grid;place-items:center;text-align:center;flex:none;line-height:1}
.datebadge b{font-size:15px;font-weight:800} .datebadge span{font-size:9px;color:var(--muted);text-transform:uppercase}
.arow .mid{flex:1;min-width:0}
.arow .mid b{font-size:13px;font-weight:700;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.arow .mid span{font-size:11.5px;color:var(--muted)}
.arow .end{font-size:14px;font-weight:800}
.arow .end.crit{color:var(--crit)} .arow .end.good{color:var(--good)}
.minibtn{font-family:inherit;font-size:11px;font-weight:700;color:var(--muted);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:5px 8px;cursor:pointer}
.minibtn:hover{color:var(--gold-2);border-color:var(--gold)}

/* people list (person mode rail) */
.plist{display:flex;flex-direction:column}
.pitem{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;width:100%;text-align:left;font-family:inherit;background:transparent;border:0;border-top:1px solid var(--line);padding:10px 0;cursor:pointer}
.pitem:first-child{border-top:0}
.pitem:hover .pn b{color:var(--gold-2)}
.pitem[aria-selected="true"]{background:linear-gradient(90deg,var(--gold-soft),transparent);border-radius:10px;padding-left:8px;padding-right:8px}
.pn{min-width:0}.pn b{font-size:13px;font-weight:700;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pn span{font-size:11px;color:var(--muted)}
.chipn{font-size:11px;font-weight:800;min-width:22px;text-align:center;padding:3px 6px;border-radius:8px;background:var(--panel-2)}
.chipn.crit{background:color-mix(in srgb,var(--crit) 16%,transparent);color:var(--crit)}

/* task rows */
.tasks{list-style:none;margin:0;padding:0}
.trow{display:grid;grid-template-columns:3px 1fr auto auto;gap:11px;padding:11px 16px 11px 0;border-top:1px solid var(--line);align-items:center}
.trow:first-child{border-top:0}
.stripe{width:3px;align-self:stretch;border-radius:0 3px 3px 0}
.s-crit{background:var(--crit)}.s-high{background:var(--high)}.s-med{background:var(--med)}.s-today{background:var(--today)}.s-none{background:var(--line-2)}
.tname{font-size:13.5px;font-weight:600;color:var(--ink);text-decoration:none;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tname:hover{color:var(--gold-2);text-decoration:underline}
.tmeta{display:flex;gap:6px;flex-wrap:wrap;margin-top:5px;align-items:center}
.pill{font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:6px;white-space:nowrap}
.pill.list{background:var(--panel-2);color:var(--muted);border:1px solid var(--line)}
.pill.proj{background:color-mix(in srgb,var(--gold) 15%,transparent);color:var(--gold-2);font-weight:700}
.pill.adi{background:color-mix(in srgb,var(--high) 18%,transparent);color:var(--high);font-weight:700}
:root[data-theme="dark"] .pill.proj{color:var(--gold)}
.pill.status{background:var(--gold-soft);color:var(--gold-2)}
:root[data-theme="dark"] .pill.status{color:var(--gold)}
.pill.status.camp{background:var(--panel-2);color:var(--muted);border:1px solid var(--line)}
.pill.warn{background:color-mix(in srgb,var(--high) 16%,transparent);color:var(--high)}
.pill.pr.urgent{color:#fff;background:var(--crit)} .pill.pr.high{color:var(--high);background:color-mix(in srgb,var(--high) 16%,transparent)}
.tright{text-align:right;white-space:nowrap}
.tdays{font-size:14.5px;font-weight:800} .tdays.crit{color:var(--crit)}.tdays.high{color:var(--high)}.tdays.med{color:var(--med)}.tdays.today{color:var(--today)}
.tdue{font-size:10.5px;color:var(--muted)}
.closebtn{font-family:inherit;font-size:11px;font-weight:700;color:var(--muted);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 9px;cursor:pointer;white-space:nowrap}
.closebtn:hover{color:var(--good);border-color:var(--good)}
.empty{padding:24px;text-align:center;color:var(--muted);font-size:13px}

/* comportamento */
.beh{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:640px){.beh{grid-template-columns:1fr}}
.beh h4{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0 0 12px;font-weight:700}
.spark{display:flex;align-items:flex-end;gap:3px;height:70px}
.spark .bar{flex:1;background:var(--gold);border-radius:3px 3px 0 0;min-height:2px;position:relative;opacity:.9}
.sparklbl{font-size:10px;color:var(--muted);margin-top:6px;display:flex;justify-content:space-between}
.brow{display:flex;justify-content:space-between;font-size:12.5px;padding:5px 0;border-bottom:1px dashed var(--line)}.brow:last-child{border-bottom:0}.brow b{font-weight:800}
.ranklist .arow .bar-mini{height:7px;border-radius:5px;background:var(--panel-2);overflow:hidden;margin-top:4px}
.foot{margin:6px 2px 0;color:var(--muted);font-size:11.5px}
.period{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:9px 14px;box-shadow:var(--shadow-sm);margin-bottom:16px}
.period .plabel{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.ppills{display:inline-flex;background:var(--panel-2);border:1px solid var(--line);border-radius:11px;padding:3px;gap:2px;flex-wrap:wrap}
.ppills button{font-family:inherit;font-size:12.5px;font-weight:600;color:var(--muted);background:transparent;border:0;border-radius:8px;padding:7px 13px;cursor:pointer;white-space:nowrap;transition:background .12s,color .12s}
.ppills button:hover{color:var(--ink)}
.ppills button[aria-pressed="true"]{background:linear-gradient(135deg,var(--gold),var(--magenta));color:#fff}
.ppills button:focus-visible,.applybtn:focus-visible,.pcustom input:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.pcustom{display:inline-flex;align-items:center;gap:7px;margin-left:auto}
.pcustom input[type=date]{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 9px;color-scheme:light dark}
.pcustom .arw{color:var(--muted);font-size:12px}
.pcustom .applybtn{font-family:inherit;font-size:12px;font-weight:700;color:#fff;background:var(--gold);border:0;border-radius:8px;padding:7px 14px;cursor:pointer}
.pcustom .applybtn:hover{filter:brightness(1.07)}
@media(max-width:620px){.pcustom{margin-left:0}}
.beh-ctrl{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.preset{font-family:inherit;font-size:11.5px;font-weight:700;color:var(--muted);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 10px;cursor:pointer}
.preset[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2);border-color:transparent}
:root[data-theme="dark"] .preset[aria-pressed="true"]{color:var(--gold)}
.beh-ctrl input[type=date]{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.applybtn{font-family:inherit;font-size:11.5px;font-weight:700;color:#fff;background:var(--gold);border:0;border-radius:8px;padding:7px 13px;cursor:pointer}
.applybtn:hover{filter:brightness(1.07)}
.ontime{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:22px}
.ontime .pct{font-family:var(--display);font-size:42px;font-weight:800;line-height:1;letter-spacing:-.02em}
.ontime-txt{display:flex;flex-direction:column;gap:2px}
.ontime-txt b{font-size:14px;font-weight:700}.ontime-txt span{font-size:12px;color:var(--muted)}
.otbar{flex:1 1 200px;min-width:180px;height:14px;border-radius:8px;background:var(--panel-2);overflow:hidden;display:flex}
.otbar span{height:100%}.otbar .g{background:var(--good)}.otbar .rd{background:var(--crit)}.otbar .nn{background:var(--line-2)}
.chart-h{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:2px 0 8px;flex-wrap:wrap}
.chart-h h4{font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0;font-weight:700}
.lgd{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:6px}
.lgd .d{width:10px;height:10px;border-radius:3px;display:inline-block}.lgd .d.g{background:var(--good)}.lgd .d.rd{background:var(--crit)}
.chart{display:flex;align-items:flex-end;gap:8px;min-height:184px;overflow-x:auto;padding:14px 2px 2px}
.colwrap{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:5px;flex:1;min-width:30px}
.coln{font-size:10.5px;color:var(--muted);font-weight:700}
.bar-col{width:26px;border-radius:6px 6px 4px 4px;overflow:hidden;display:flex;flex-direction:column-reverse;background:var(--panel-2)}
.bar-col .seg{width:100%}.bar-col .seg.ok{background:var(--good)}.bar-col .seg.late{background:var(--crit)}
.collbl{font-size:9.5px;color:var(--muted);white-space:nowrap}
.psum{display:flex;flex-wrap:wrap}
.psum>div{padding:14px 18px;border-right:1px solid var(--line);flex:1 1 120px}
.psum>div:last-child{border-right:0}
.psum>div b{font-family:var(--display);font-size:26px;font-weight:800;display:block;line-height:1}
.psum>div span{font-size:11.5px;color:var(--muted);font-weight:600;margin-top:4px;display:block}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.chip{background:var(--panel-2);border:1px solid var(--line);border-radius:11px;padding:9px 13px;font-size:11.5px;color:var(--muted);line-height:1.35}
.chip b{display:block;color:var(--ink);font-weight:800;font-size:17px;font-family:var(--display)}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--side);color:var(--side-ink);padding:11px 16px;border-radius:12px;font-size:13px;font-weight:600;box-shadow:var(--shadow);display:flex;gap:14px;align-items:center;z-index:60}
.toast button{font-family:inherit;font-weight:800;color:var(--gold);background:transparent;border:0;cursor:pointer;font-size:13px}
.toast[hidden]{display:none}
.daterange{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--muted)}
.daterange input{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.stepbtns{display:flex;gap:6px}
.btn{font-family:inherit;font-size:12px;font-weight:700;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:7px 11px;cursor:pointer}
.btn:hover{color:var(--ink);border-color:var(--line-2)}
.teamchip{font-size:10px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:rgba(255,255,255,.22);color:#fff}
</style>

<div class="wrap"><div class="app">
  <aside class="side">
    <div class="brand"><span class="logo"><span class="top"><span class="au">Au</span><span class="re">re</span><span class="dot"></span></span><span class="dig">DIGITAL</span></span><span class="tag">· Times</span></div>
    <div class="navlbl">Painel</div>
    <button class="nav" data-page="overview" aria-current="true"><span class="ic">▚</span> Visão geral</button>
    <button class="nav" data-page="person"><span class="ic">◉</span> Por pessoa</button>
    <div class="navlbl">Time</div>
    <div class="tfilter" id="tfilter">
      <button data-team="all" aria-pressed="true">Ambos</button>
      <button data-team="E-SCALE" aria-pressed="false">E‑SCALE</button>
      <button data-team="FENIX" aria-pressed="false">FENIX</button>
    </div>
    <div class="side-foot">
      <div class="gen" id="gen"></div>
      <div class="themetog" id="themetog">
        <button data-t="light" aria-pressed="false">☀ Light</button>
        <button data-t="dark" aria-pressed="false">☾ Dark</button>
      </div>
    </div>
  </aside>

  <main class="main">
    <div class="topbar"><h1 id="ptitle">Visão geral</h1><div id="topright"></div></div>
    <div class="period" title="Filtra conclusões, % no prazo e adiamentos. O atraso e as mal cadastradas são sempre o estado atual.">
      <span class="plabel">Período</span>
      <div class="ppills" id="periodpresets">
        <button data-preset="hoje">Hoje</button>
        <button data-preset="ontem">Ontem</button>
        <button data-preset="mes">Este mês</button>
        <button data-preset="30">30 dias</button>
        <button data-preset="90">90 dias</button>
        <button data-preset="all">Tudo</button>
      </div>
      <div class="pcustom">
        <input type="date" id="df"><span class="arw">→</span><input type="date" id="dt">
        <button class="applybtn" data-apply>Aplicar</button>
      </div>
    </div>
    <div id="root"></div>
    <div class="foot" id="foot"></div>
  </main>
</div></div>
<div class="toast" id="toast" hidden><span id="toastmsg"></span><button id="toastundo">Desfazer</button></div>

<script>
const MODEL = __MODEL__;
const MEM = {}; MODEL.members.forEach(m=>MEM[m.uid]=m);
const PPBYID = {}; (MODEL.postpones||[]).forEach(p=>{PPBYID[p.id]=p;});
const HKEY="clk_hidden_v1";
let page="overview", team="all", selUid=MODEL.members[0]?.uid, dFrom=MODEL.window.to, dTo=MODEL.window.to;  // abre em "Hoje"
const $=id=>document.getElementById(id);
const esc=s=>(s==null?"":String(s)).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sev=d=>d>30?"crit":d>7?"high":d>0?"med":"today";
const SEVC={crit:"var(--crit)",high:"var(--high)",med:"var(--med)",today:"var(--today)"};
const initials=n=>n.split(" ").filter(Boolean).slice(0,2).map(x=>x[0]).join("").toUpperCase();
function avaHTML(m,cls,style){
  const c=cls+" "+(m.team==="E-SCALE"?"E":"F"), st=style||"", ini=esc(initials(m.name||""));
  if(m.avatar) return `<span class="${c}" style="position:relative;overflow:hidden;${st}">${ini}<img src="${esc(m.avatar)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" onerror="this.remove()"></span>`;
  return `<span class="${c}" style="${st}">${ini}</span>`;
}
const hidden=()=>{try{return new Set(JSON.parse(localStorage.getItem(HKEY)||"[]"))}catch(e){return new Set()}};
const setHidden=s=>localStorage.setItem(HKEY,JSON.stringify([...s]));
const hideTask=id=>{const s=hidden();s.add(id);setHidden(s)};
const unhide=id=>{const s=hidden();s.delete(id);setHidden(s)};
const inTeam=uid=>team==="all"||MEM[uid].team===team;
const membersInTeam=()=>MODEL.members.filter(m=>team==="all"||m.team===team);

function overdueAll(){const h=hidden();return MODEL.overdue.filter(t=>!h.has(t.id)&&inTeam(t.uid));}
function overdueFor(uid){const h=hidden();return MODEL.overdue.filter(t=>t.uid===uid&&!h.has(t.id));}
function overdueForAll(uid){return MODEL.overdue.filter(t=>t.uid===uid);}
function malformedFor(uid){return MODEL.malformed.filter(t=>t.uid===uid);}
function eventsFor(uid){return MODEL.events.filter(e=>e.uid===uid&&e.day>=dFrom&&e.day<=dTo);}
function behavior(uid){
  const ev=eventsFor(uid),done=ev.filter(e=>e.kind==="done"),created=ev.filter(e=>e.kind==="created").length;
  const wd=done.filter(e=>!e.noDue),onTime=wd.filter(e=>!e.late).length,late=wd.filter(e=>e.late).length;
  const otRate=wd.length?Math.round(onTime/wd.length*100):null;
  const byDay={};done.forEach(e=>byDay[e.day]=(byDay[e.day]||0)+1);const pd=Object.values(byDay);
  return {doneN:done.length,created,onTime,late,noDue:done.length-wd.length,otRate,
    maxDay:pd.length?Math.max(...pd):0,bulkDays:pd.filter(n=>n>=5).length,avgDay:pd.length?done.length/pd.length:0,done};
}
// Adiamentos são cumulativos: mostramos SEMPRE o histórico total, independente do período.
// Tarefas "fechadas" (ocultadas) somem daqui também.
function postponesFor(uid){const h=hidden();
  return (MODEL.postpones||[]).filter(p=>(p.uids||[]).includes(uid)&&!h.has(p.id))
    .map(p=>({id:p.id,name:p.name,list:p.list,uids:p.uids||[],hist:p.history,inRange:p.history.length}))
    .sort((a,b)=>b.inRange-a.inRange);
}
function postponeCount(uid){const h=hidden();return (MODEL.postpones||[]).filter(p=>(p.uids||[]).includes(uid)&&!h.has(p.id))
  .reduce((s,p)=>s+p.history.length,0);}
const MO=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const p2=n=>String(n).padStart(2,"0");
const ymd=d=>d.getFullYear()+"-"+p2(d.getMonth()+1)+"-"+p2(d.getDate());
function timeline(done,from,to){ // linha do tempo CONTÍNUA e adaptativa: dia (≤31d), semana (≤100d) ou mês
  const start=new Date(from+"T00:00:00"), end=new Date(to+"T00:00:00"), days=(end-start)/864e5;
  const gran = days<=31 ? "day" : days<=100 ? "week" : "month";
  const buckets=[], idx={};
  const keyOf=d=>{
    if(gran==="month") return d.getFullYear()+"-"+p2(d.getMonth()+1);
    if(gran==="week"){ const m=new Date(d); m.setDate(d.getDate()-((d.getDay()+6)%7)); return ymd(m); }
    return ymd(d);
  };
  const push=(k,label)=>{ idx[k]=buckets.length; buckets.push({key:k,label,n:0,late:0}); };
  if(gran==="month"){ let d=new Date(start.getFullYear(),start.getMonth(),1);
    while(d<=end){ push(d.getFullYear()+"-"+p2(d.getMonth()+1), MO[d.getMonth()]+"/"+String(d.getFullYear()).slice(2)); d=new Date(d.getFullYear(),d.getMonth()+1,1); } }
  else if(gran==="week"){ let d=new Date(start); d.setDate(d.getDate()-((d.getDay()+6)%7));
    while(d<=end){ push(ymd(d), p2(d.getDate())+"/"+p2(d.getMonth()+1)); d=new Date(d); d.setDate(d.getDate()+7); } }
  else{ let d=new Date(start);
    while(d<=end){ push(ymd(d), p2(d.getDate())+"/"+p2(d.getMonth()+1)); d=new Date(d); d.setDate(d.getDate()+1); } }
  done.forEach(e=>{ const i=idx[keyOf(new Date(e.day+"T00:00:00"))]; if(i!=null){ buckets[i].n++; if(e.late)buckets[i].late++; } });
  return buckets;
}
function shiftDays(iso,n){const d=new Date(iso+"T00:00:00");d.setDate(d.getDate()+n);return d.toISOString().slice(0,10);}
const fmtBR=iso=>{const a=iso.split("-");return a[2]+"/"+a[1]+"/"+a[0].slice(2);};
function setPreset(p){
  const T=MODEL.window.to, W=MODEL.window.from;
  if(p==="all"){dFrom=W;dTo=T;}
  else if(p==="hoje"){dFrom=T;dTo=T;}
  else if(p==="ontem"){dFrom=dTo=shiftDays(T,-1);}
  else if(p==="mes"){dFrom=T.slice(0,8)+"01";dTo=T;}
  else{dTo=T;dFrom=shiftDays(T,-parseInt(p));}
  if(dFrom<W)dFrom=W;
}
function activePreset(){
  const T=MODEL.window.to, W=MODEL.window.from;
  if(dFrom===W&&dTo===T)return"all";
  if(dFrom===T&&dTo===T)return"hoje";
  const y=shiftDays(T,-1); if(dFrom===y&&dTo===y)return"ontem";
  if(dFrom===T.slice(0,8)+"01"&&dTo===T)return"mes";
  if(dTo===T&&dFrom===shiftDays(T,-30))return"30";
  if(dTo===T&&dFrom===shiftDays(T,-90))return"90";
  return"";
}
function segCount(ts){const c={crit:0,high:0,med:0,today:0};ts.forEach(t=>c[sev(t.days)]++);return c;}
function donutGrad(parts){ // parts: [{v,color}] -> conic-gradient
  let a=0,tot=parts.reduce((s,p)=>s+p.v,0)||1,out=[];
  parts.forEach(p=>{const b=a+p.v/tot*100;out.push(`${p.color} ${a}% ${b}%`);a=b;});
  return `conic-gradient(${out.join(",")})`;}

function taskRow(t,closable){
  const sv=sev(t.days),dl=t.days<=0?"hoje":t.days;
  const pr=(t.priority==="urgent"||t.priority==="high")?`<span class="pill pr ${t.priority}">${t.priority==="urgent"?"Urgente":"Alta"}</span>`:"";
  const adi=PPBYID[t.id]?`<span class="pill adi">↪ ${PPBYID[t.id].count}× adiada</span>`:"";
  const cb=closable?`<button class="closebtn" data-close="${t.id}" title="Ocultar (já concluída / cliente saiu)">✓ Fechar</button>`:"<span></span>";
  return `<li class="trow"><span class="stripe s-${sv}"></span>
    <div style="min-width:0"><a class="tname" href="https://app.clickup.com/t/${t.id}" target="_blank" rel="noopener">${esc(t.name)}</a>
    <div class="tmeta">${t.project?`<span class="pill proj">🏢 ${esc(t.project)}</span>`:""}<span class="pill list">${esc(t.list)}</span><span class="pill status ${t.bucket==="campanha"?"camp":""}">${esc(t.status)}</span>${pr}${adi}</div></div>
    <div class="tright"><div class="tdays ${sv}">${dl}${t.days>0?'<span style="font-size:9px"> d</span>':''}</div><div class="tdue">${esc(t.due)}</div></div>${cb}</li>`;
}

/* ---------------- OVERVIEW ---------------- */
function renderOverview(){
  $("ptitle").textContent="Visão geral";$("topright").innerHTML="";
  const od=overdueAll(),acao=od.filter(t=>t.bucket==="acao").length,crit=od.filter(t=>t.days>30).length;
  const mal=MODEL.malformed.filter(t=>t.uid==null||inTeam(t.uid)).length;
  const ppl=new Set(od.map(t=>t.uid)).size;
  const sc=segCount(od);
  const donut=donutGrad([{v:sc.crit,color:"var(--crit)"},{v:sc.high,color:"var(--high)"},{v:sc.med,color:"var(--med)"},{v:sc.today,color:"var(--today)"}]);
  const segRows=[["crit","+30 dias",sc.crit],["high","8–30 dias",sc.high],["med","1–7 dias",sc.med],["today","vence hoje",sc.today]];
  const segMax=Math.max(1,sc.crit,sc.high,sc.med,sc.today);
  // ranking
  const byM={};od.forEach(t=>(byM[t.uid]=byM[t.uid]||[]).push(t));
  const rank=Object.entries(byM).map(([u,ts])=>({uid:+u,n:ts.length,c:segCount(ts)})).sort((a,b)=>b.n-a.n);
  const rmax=Math.max(1,...rank.map(r=>r.n));
  // attention people (top overdue) & malformed & best on-time
  const attention=rank.slice(0,5);
  const malList=MODEL.malformed.filter(t=>t.uid==null||inTeam(t.uid)).slice(0,5);
  const best=membersInTeam().map(m=>({m,b:behavior(m.uid)})).filter(x=>x.b.onTime+x.b.late>=3)
    .sort((a,b)=>(b.b.otRate??-1)-(a.b.otRate??-1)).slice(0,4);
  const ppBoard=membersInTeam().map(m=>({m,n:postponeCount(m.uid)})).filter(x=>x.n>0).sort((a,b)=>b.n-a.n).slice(0,5);
  const tb=membersInTeam().reduce((a,m)=>{const bb=behavior(m.uid);a.done+=bb.doneN;a.onTime+=bb.onTime;a.late+=bb.late;a.created+=bb.created;return a;},{done:0,onTime:0,late:0,created:0});
  const tbOt=(tb.onTime+tb.late)?Math.round(tb.onTime/(tb.onTime+tb.late)*100):null;
  const tbOtColor=tbOt==null?"var(--muted)":tbOt>=80?"var(--good)":tbOt>=50?"var(--high)":"var(--crit)";
  const tbPP=membersInTeam().reduce((s,m)=>s+postponeCount(m.uid),0);
  const teamName=team==="all"?"E‑SCALE & FENIX":team;

  $("root").innerHTML=`<div class="content"><div class="col">
    <div class="banner"><div class="bt">
      <h2>Acompanhamento — ${teamName}</h2>
      <p>${od.length} tarefas em atraso, sendo ${acao} pendências de ação. ${crit} passaram de 30 dias. ${mal} tarefas mal cadastradas para revisar.</p>
      <div class="cta"><button data-goto-attention>Ver quem precisa de atenção</button><button class="ghost" data-page-go="person">Abrir por pessoa</button></div>
    </div><div class="avatar">📊</div></div>

    <div class="card"><div class="card-h"><h3>Conclusões no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${teamName}</div></div>
      <div class="psum">
        <div><b>${tb.done}</b><span>concluídas</span></div>
        <div><b style="color:${tbOtColor}">${tbOt==null?"—":tbOt+"%"}</b><span>no prazo</span></div>
        <div><b>${tb.created}</b><span>criadas</span></div>
        <div><b style="${tbPP?"color:var(--high)":""}">${tbPP}</b><span>adiamentos (total)</span></div>
      </div></div>

    <div class="stats">
      <div class="stat gold"><div class="ico">⏰</div><div class="n">${od.length}</div><div class="l">Em atraso</div></div>
      <div class="stat"><div class="ico">📋</div><div class="n">${acao}</div><div class="l">Pendências de ação</div></div>
      <div class="stat crit"><div class="ico">🔥</div><div class="n">${crit}</div><div class="l">Atraso +30 dias</div></div>
      <div class="stat"><div class="ico">⚠️</div><div class="n">${mal}</div><div class="l">Mal cadastradas</div></div>
      <div class="stat"><div class="ico">👤</div><div class="n">${ppl}</div><div class="l">Pessoas c/ atraso</div></div>
    </div>

    <div class="card"><div class="card-h"><h3>Atrasos por gravidade</h3><div class="r">${od.length} tarefas</div></div>
      <div class="pad"><div class="donutwrap">
        <div class="donut" style="background:${donut}"><div class="c"><b>${od.length}</b><span>em atraso</span></div></div>
        <div class="leg">${segRows.map(([k,lb,v])=>`<div class="row"><div class="nm"><span class="dot" style="background:${SEVC[k]}"></span>${lb}</div><div class="v">${v}</div><div class="track"><span style="width:${v/segMax*100}%;background:${SEVC[k]}"></span></div></div>`).join("")}</div>
      </div></div></div>

    <div class="card" id="rankcard"><div class="card-h"><h3>Ranking por pessoa</h3><div class="r">clique para abrir</div></div>
      <div class="pad ranklist">${rank.map(r=>{const c=r.c;return `<button class="arow" data-open="${r.uid}" style="width:100%;text-align:left;background:transparent;border:0;border-top:1px solid var(--line);font-family:inherit;cursor:pointer">
        ${avaHTML(MEM[r.uid],"ava","")}
        <div class="mid"><b>${esc(MEM[r.uid].name)}</b><div class="bar-mini"><span style="display:flex;height:100%;width:${r.n/rmax*100}%">${["crit","high","med","today"].map(k=>c[k]?`<span style="height:100%;width:${c[k]/r.n*100}%;background:${SEVC[k]}"></span>`:"").join("")}</span></div></div>
        <div class="end ${r.n>10?'crit':''}">${r.n}</div></button>`;}).join("")||'<div class="empty">Sem atrasos 🎉</div>'}</div></div>
  </div>

  <div class="col">
    <div class="acard" id="attentioncard"><h3>Precisam de atenção</h3><p class="sub">Maior volume de atraso</p>
      ${attention.map(r=>`<div class="arow">${avaHTML(MEM[r.uid],"ava","")}
        <div class="mid"><b>${esc(MEM[r.uid].name)}</b><span>${MEM[r.uid].team} · ${r.c.crit} crítica(s)</span></div>
        <button class="minibtn" data-open="${r.uid}">abrir</button></div>`).join("")||'<div class="empty">—</div>'}</div>

    <div class="acard"><h3>Mal cadastradas</h3><p class="sub">Sem responsável ou sem prazo</p>
      ${malList.map(t=>`<div class="arow"><div class="datebadge"><b>!</b><span>fix</span></div>
        <div class="mid"><b>${esc(t.name)}</b><span>${esc(t.list)}${t.account?" · "+esc(t.account):(t.gestor?" · "+esc(t.gestor):"")}</span></div>
        <a class="minibtn" href="https://app.clickup.com/t/${t.id}" target="_blank" rel="noopener">ver</a></div>`).join("")||'<div class="empty">Nenhuma 🎉</div>'}</div>

    <div class="acard"><h3>Melhores no prazo</h3><p class="sub">Janela ${dFrom} → ${dTo}</p>
      ${best.map(x=>`<div class="arow">${avaHTML(x.m,"ava","")}
        <div class="mid"><b>${esc(x.m.name)}</b><span>${x.b.onTime}/${x.b.onTime+x.b.late} no prazo</span></div>
        <div class="end good">${x.b.otRate}%</div></div>`).join("")||'<div class="empty">Rode o script p/ ver comportamento</div>'}</div>

    <div class="acard"><h3>Mais adiam prazo</h3><p class="sub">Total de adiamentos registrados</p>
      ${ppBoard.map(x=>`<button class="arow" data-open="${x.m.uid}" style="width:100%;text-align:left;background:transparent;border:0;font-family:inherit;cursor:pointer">
        ${avaHTML(x.m,"ava","")}
        <div class="mid"><b>${esc(x.m.name)}</b><span>${x.m.team}</span></div>
        <div class="end" style="color:var(--high)">${x.n}×</div></button>`).join("")||'<div class="empty">Sem adiamentos registrados ainda. Rode o painel com frequência para acumular.</div>'}</div>
  </div></div>`;
}

/* ---------------- PERSON ---------------- */
function renderPerson(){
  const inTeamList=membersInTeam();
  if(!inTeamList.some(m=>m.uid===selUid))selUid=inTeamList[0]?.uid;
  $("ptitle").textContent="Por pessoa";
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-step="-1">↑ Anterior</button><button class="btn" data-step="1">Próximo ↓</button></div>`;
  const m=MEM[selUid],od=overdueFor(selUid).sort((a,b)=>b.days-a.days),odAll=overdueForAll(selUid);
  const hiddenN=odAll.length-od.length,mal=malformedFor(selUid),b=behavior(selUid),crit=od.filter(t=>t.days>30).length;
  const tc=m.team==="E-SCALE"?"E":"F";
  const otColor=b.otRate==null?"var(--muted)":b.otRate>=80?"var(--good)":b.otRate>=50?"var(--high)":"var(--crit)";
  const doneTot=b.onTime+b.late+b.noDue;
  const pp=postponesFor(selUid), ppTotal=pp.reduce((s,x)=>s+x.inRange,0);
  const ppHidden=(MODEL.postpones||[]).filter(p=>(p.uids||[]).includes(selUid)&&hidden().has(p.id)).length;
  const tl=timeline(b.done,dFrom,dTo), tlMax=Math.max(1,...tl.map(x=>x.n));
  const lblStep=tl.length>14?Math.ceil(tl.length/8):1;   // afina os rótulos do eixo x quando há muitas barras
  const tlBars=tl.map((x,i)=>{const ot=x.n-x.late; const showLbl=(i%lblStep===0)||i===tl.length-1;
    return `<div class="colwrap"><div class="coln">${x.n||''}</div>
      <div class="bar-col" style="height:${Math.max(4,x.n/tlMax*140)}px" title="${x.label}: ${x.n} conclusões — ${ot} no prazo, ${x.late} em atraso">
        <div class="seg ok" style="flex:${ot}"></div><div class="seg late" style="flex:${x.late}"></div></div>
      <div class="collbl">${showLbl?x.label:''}</div></div>`;}).join("");
  // rail list
  const h=hidden();
  const rail=inTeamList.map(x=>{const n=MODEL.overdue.filter(t=>t.uid===x.uid&&!h.has(t.id)).length,ml=malformedFor(x.uid).length;
    return `<button class="pitem" data-uid="${x.uid}" aria-selected="${x.uid===selUid}">
      ${avaHTML(x,"ava","width:32px;height:32px;font-size:11px")}
      <span class="pn"><b>${esc(x.name)}</b><span>${x.role==="Gestor de Tráfego"?"Tráfego":x.role}</span></span>
      <span class="chipn ${n>10?'crit':''}">${n}</span></button>`;}).join("");

  $("root").innerHTML=`<div class="content"><div class="col">
    <div class="banner"><div class="bt">
      <h2>${esc(m.name)}</h2>
      <p>${esc(m.role)} · <span class="teamchip">${m.team}</span></p>
      <div class="cta"><button data-scroll="odsec">Ver ${od.length} em atraso</button>${mal.length?`<button class="ghost" data-scroll="malsec">${mal.length} mal cadastrada(s)</button>`:""}</div>
    </div>${avaHTML(m,"avatar","")}</div>

    <div class="stats">
      <div class="stat ${crit?'crit':'gold'}"><div class="ico">⏰</div><div class="n">${od.length}</div><div class="l">Em atraso${hiddenN?` · ${hiddenN} oculta(s)`:""}</div></div>
      <div class="stat"><div class="ico">⚠️</div><div class="n">${mal.length}</div><div class="l">Mal cadastradas</div></div>
      <div class="stat"><div class="ico">✅</div><div class="n" style="color:${otColor}">${b.otRate==null?"—":b.otRate+"%"}</div><div class="l">No prazo</div></div>
      <div class="stat"><div class="ico">📈</div><div class="n">${b.doneN}</div><div class="l">Concluídas</div></div>
      <div class="stat"><div class="ico">📦</div><div class="n">${b.maxDay}</div><div class="l">Check em lote/dia</div></div>
      <div class="stat"><div class="ico">✎</div><div class="n">${b.created}</div><div class="l">Criadas</div></div>
    </div>

    <div class="card" id="odsec"><div class="card-h"><h3>Em atraso</h3><div class="r"><span>${od.length} aberta(s)</span>${hiddenN?`<button class="linkish" id="showhidden">ver ${hiddenN} oculta(s)</button>`:""}</div></div>
      ${od.length?`<ul class="tasks" style="padding:4px 16px 8px">${od.map(t=>taskRow(t,true)).join("")}</ul>`:`<div class="empty">Sem tarefas em atraso 🎉</div>`}</div>

    ${mal.length?`<div class="card" id="malsec"><div class="card-h"><h3>Tarefas mal cadastradas</h3><div class="r">${mal.length} item(ns)</div></div>
      <ul class="tasks" style="padding:4px 16px 8px">${mal.map(t=>`<li class="trow"><span class="stripe s-none"></span>
        <div style="min-width:0"><a class="tname" href="https://app.clickup.com/t/${t.id}" target="_blank" rel="noopener">${esc(t.name)}</a>
        <div class="tmeta"><span class="pill list">${esc(t.list)}</span>${t.problems.map(p=>`<span class="pill warn">${p==="sem_responsavel"?"sem responsável":"sem prazo"}</span>`).join("")}
        <span class="pill list">provável → ${t.account?"Account: "+esc(t.account):""}${t.account&&t.gestor?" · ":""}${t.gestor?"Gestor: "+esc(t.gestor):""}${!t.account&&!t.gestor?"sem pista":""}</span></div></div>
        <div class="tright"><div class="tdue">${esc(t.created||"")}</div></div><span></span></li>`).join("")}</ul></div>`:""}

    <div class="card"><div class="card-h"><h3>Comportamento</h3>
      <div class="r">Período: <b>${fmtBR(dFrom)} → ${fmtBR(dTo)}</b> <span style="opacity:.7">· ajuste no topo</span></div></div>
      <div class="pad">
        <div class="ontime">
          <div class="pct" style="color:${otColor}">${b.otRate==null?"—":b.otRate+"%"}</div>
          <div class="ontime-txt"><b>das entregas no prazo</b>
            <span>${b.onTime} no prazo · ${b.late} em atraso${b.noDue?` · ${b.noDue} sem prazo`:""} — de ${doneTot} concluída(s)</span></div>
          <div class="otbar">${b.onTime?`<span class="g" style="flex:${b.onTime}"></span>`:""}${b.late?`<span class="rd" style="flex:${b.late}"></span>`:""}${b.noDue?`<span class="nn" style="flex:${b.noDue}"></span>`:""}</div>
        </div>
        <div class="chart-h"><h4>Conclusões ao longo do tempo</h4>
          <span class="lgd"><span class="d g"></span>no prazo <span class="d rd"></span>em atraso</span></div>
        ${b.doneN?`<div class="chart">${tlBars}</div>`:`<div class="empty">Sem conclusões nesse período. Toque em "Tudo" ou amplie as datas.</div>`}
        <div class="chips">
          <div class="chip"><b>${b.doneN}</b>concluídas no período</div>
          <div class="chip"><b>${b.created}</b>criadas por ela(e)</div>
          <div class="chip"><b>${b.maxDay}</b>máx. num único dia</div>
          <div class="chip"><b>${b.bulkDays}</b>dias com 5+ (check em lote)</div>
          <div class="chip"><b style="${ppTotal?'color:var(--high)':''}">${ppTotal}</b>adiamentos de prazo</div>
        </div>
      </div></div>

    <div class="card"><div class="card-h"><h3>Prazos adiados</h3>
      <div class="r">${ppTotal} adiamento(s) em ${pp.length} tarefa(s)${ppHidden?` · <button class="linkish" data-showpp>ver ${ppHidden} oculta(s)</button>`:" · histórico total"}</div></div>
      ${pp.length?`<ul class="tasks" style="padding:4px 16px 8px">${pp.map(p=>{const last=p.hist[p.hist.length-1];
        return `<li class="trow"><span class="stripe s-high"></span>
          <div style="min-width:0"><a class="tname" href="https://app.clickup.com/t/${p.id}" target="_blank" rel="noopener">${esc(p.name)}</a>
          <div class="tmeta"><span class="pill list">${esc(p.list)}</span><span class="pill warn">${p.inRange}× adiado</span>
          <span class="pill list">último: ${esc(last.from)} → ${esc(last.to)}</span></div></div>
          <div class="tright"><div class="tdays high">${p.inRange}×</div><div class="tdue">adiado</div></div>
          <button class="closebtn" data-close="${p.id}" title="Ocultar (já resolvida / não vai mais ser feita)">✓ Fechar</button></li>`;}).join("")}</ul>`
      :`<div class="empty">${(MODEL.postpones&&MODEL.postpones.length)?'Sem adiamentos registrados desta pessoa.':'Ainda sem adiamentos registrados — eles passam a ser contados a cada atualização do painel. Rode com frequência (ideal: 1×/dia) para acumular o histórico.'}</div>`}</div>
  </div>

  <div class="col"><div class="acard"><h3>Time ${team!=="all"?"· "+team:""}</h3><p class="sub">${inTeamList.length} pessoas · clique para abrir</p>
    <div class="plist">${rail}</div></div></div></div>`;
}

function render(){
  $("gen").textContent=`Atualizado ${MODEL.generated}`;
  $("foot").innerHTML=`Histórico ${MODEL.window.from} → ${MODEL.window.to}. "✓ Fechar" oculta tarefas já concluídas/cliente que saiu (salvo neste navegador, com desfazer). As datas em "Comportamento" filtram o histórico.`;
  [...$("tfilter").children].forEach(x=>x.setAttribute("aria-pressed",x.dataset.team===team));
  document.querySelectorAll(".nav").forEach(n=>n.setAttribute("aria-current",n.dataset.page===page));
  const cur=document.documentElement.getAttribute("data-theme");
  [...$("themetog").children].forEach(x=>x.setAttribute("aria-pressed",cur?x.dataset.t===cur:false));
  $("df").value=dFrom; $("dt").value=dTo;
  $("df").min=$("dt").min=MODEL.window.from; $("df").max=$("dt").max=MODEL.window.to;
  const apnow=activePreset();
  [...$("periodpresets").children].forEach(x=>x.setAttribute("aria-pressed",x.dataset.preset===apnow));
  if(page==="overview")renderOverview(); else renderPerson();
}
// events
document.addEventListener("click",e=>{
  const nav=e.target.closest(".nav"); if(nav){page=nav.dataset.page;render();window.scrollTo({top:0});return;}
  const tf=e.target.closest("#tfilter button"); if(tf){team=tf.dataset.team;render();return;}
  const pg=e.target.closest("[data-page-go]"); if(pg){page=pg.dataset.pageGo;render();window.scrollTo({top:0});return;}
  const op=e.target.closest("[data-open]"); if(op){selUid=+op.dataset.open;page="person";render();window.scrollTo({top:0});return;}
  const pi=e.target.closest(".pitem"); if(pi){selUid=+pi.dataset.uid;render();window.scrollTo({top:0});return;}
  const st=e.target.closest("[data-step]"); if(st){const L=membersInTeam();const i=L.findIndex(m=>m.uid===selUid);selUid=L[(i+ +st.dataset.step+L.length)%L.length].uid;render();window.scrollTo({top:0});return;}
  const cl=e.target.closest("[data-close]"); if(cl){hideTask(cl.dataset.close);window._last=cl.dataset.close;showToast("Tarefa ocultada.");render();return;}
  const sh=e.target.closest("#showhidden"); if(sh){const h=hidden();const od=MODEL.overdue.filter(t=>t.uid===selUid&&h.has(t.id));if(confirm(`Reexibir ${od.length} tarefa(s) ocultada(s)?`)){od.forEach(t=>unhide(t.id));render();}return;}
  const shp=e.target.closest("[data-showpp]"); if(shp){const h=hidden();const ids=(MODEL.postpones||[]).filter(p=>(p.uids||[]).includes(selUid)&&h.has(p.id)).map(p=>p.id);if(confirm(`Reexibir ${ids.length} tarefa(s) ocultada(s)?`)){ids.forEach(id=>unhide(id));render();}return;}
  const sc=e.target.closest("[data-scroll]"); if(sc){const el=$(sc.dataset.scroll);if(el)el.scrollIntoView({behavior:"smooth",block:"start"});return;}
  const at=e.target.closest("[data-goto-attention]"); if(at){$("attentioncard")?.scrollIntoView({behavior:"smooth"});return;}
  const tt=e.target.closest("#themetog button"); if(tt){document.documentElement.setAttribute("data-theme",tt.dataset.t);render();return;}
  const pr=e.target.closest("[data-preset]"); if(pr){setPreset(pr.dataset.preset);render();return;}
  const ap=e.target.closest("[data-apply]"); if(ap){const f=$("df").value,t=$("dt").value;if(f)dFrom=f;if(t)dTo=t;if(dFrom>dTo){const x=dFrom;dFrom=dTo;dTo=x;}render();return;}
});
document.addEventListener("change",e=>{if(e.target.id==="df"){dFrom=e.target.value;render();}if(e.target.id==="dt"){dTo=e.target.value;render();}});
function showToast(msg){$("toastmsg").textContent=msg;$("toast").hidden=false;clearTimeout(window._tt);window._tt=setTimeout(()=>$("toast").hidden=true,6000);}
$("toastundo").addEventListener("click",()=>{if(window._last){unhide(window._last);window._last=null;$("toast").hidden=true;render();}});
render();
</script>
"""

def _demo_model():
    random.seed(7)
    members=[(81464977,"Lucas Caldeira","E-SCALE","Head"),(55085676,"Carlos Barbosa","E-SCALE","Account"),
        (54912242,"Ray Junio","E-SCALE","Gestor de Tráfego"),(87447111,"Izabela Galdino","E-SCALE","Account"),
        (87413647,"Rafael Alves","E-SCALE","Gestor de Tráfego"),(206579907,"Thiago Zagnoli","FENIX","Head"),
        (87318381,"Vinicius Andrade","FENIX","Account"),(60944498,"Vitor Dumont","FENIX","Gestor de Tráfego"),
        (96672993,"Rafael Ramos","FENIX","Account"),(87448889,"Kaio Felipe","FENIX","Gestor de Tráfego"),
        (118026171,"Patrick Lima","FENIX","Account"),(87445783,"Carlos Nobre","FENIX","Gestor de Tráfego"),
        (96624276,"Tiago Lamêu","FENIX","Gestor de Tráfego")]
    M=[{"uid":u,"name":n,"team":t,"role":r} for u,n,t,r in members]
    lists=["Gestão de Projetos","Processos de Artes","Planejamento e Gestão de CRM","Envio de NPS","Otimização de Campanhas","Kickoff"]
    overdue=[];mal=[];events=[]
    for m in M:
        for i in range(random.randint(0,14)):
            overdue.append({"id":f"d{m['uid']}{i}","name":f"Tarefa exemplo {i} de {m['name'].split()[0]}","status":random.choice(["pendente","para fazer","em progresso"]),"priority":random.choice([None,"high","urgent"]),"list":random.choice(lists),"due":"01/07/26","days":random.choice([0,1,3,5,9,15,28,45,80]),"bucket":"acao","uid":m["uid"]})
        for i in range(random.randint(0,3)):
            mal.append({"id":f"m{m['uid']}{i}","name":f"Card sem cadastro {i} de {m['name'].split()[0]}","list":"Gestão de Projetos","problems":random.choice([["sem_responsavel"],["sem_prazo"]]),"uid":m["uid"],"account":m["name"] if m["role"]=="Account" else None,"gestor":"Ray Junio","team":m["team"],"created":"10/06/26"})
        base=datetime.date(2026,1,1)
        for _ in range(random.randint(25,120)):
            d=base+datetime.timedelta(days=random.randint(0,195));events.append({"uid":m["uid"],"kind":"done","day":d.isoformat(),"late":1 if random.random()<0.3 else 0,"noDue":1 if random.random()<0.1 else 0})
        for _ in range(random.randint(5,40)):
            d=base+datetime.timedelta(days=random.randint(0,195));events.append({"uid":m["uid"],"kind":"created","day":d.isoformat(),"late":0,"noDue":0})
    return {"generated":"14/07/2026","window":{"from":"2026-01-01","to":"2026-07-14"},"members":M,"overdue":overdue,"malformed":mal,"events":events}

if __name__=="__main__":
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    model=_demo_model() if "--demo" in sys.argv else json.load(open(args[0] if args else os.path.join(HERE,"model.json"),encoding="utf-8"))
    out=args[1] if len(args)>1 else os.path.join(HERE,"dashboard.html")
    open(out,"w",encoding="utf-8").write(render(model))
    print("Gerado:",out,"·",len(model["overdue"]),"atrasos ·",len(model["malformed"]),"mal cadastradas ·",len(model["events"]),"eventos")
