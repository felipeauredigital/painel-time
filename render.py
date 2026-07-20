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
.pill.okdone{background:color-mix(in srgb,var(--good) 16%,transparent);color:var(--good);font-weight:700}
.pill.badlate{background:color-mix(in srgb,var(--crit) 16%,transparent);color:var(--crit);font-weight:700}
.s-ok{background:var(--good)}
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

/* churn */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:15px 16px;box-shadow:var(--shadow-sm)}
.kpi .n{font-family:var(--display);font-size:25px;font-weight:800;line-height:1}
.kpi .l{font-size:11.5px;color:var(--muted);font-weight:600;margin-top:6px}
.kpi .s{font-size:11px;color:var(--muted);margin-top:3px}
.metabar{position:relative;height:13px;border-radius:7px;background:var(--panel-2);margin:9px 0}
.metabar.big{height:20px;border-radius:10px}
.metabar .mfill{position:absolute;left:0;top:0;height:100%;border-radius:7px;transition:width .3s}
.metabar .mtick{position:absolute;top:-3px;width:2px;height:19px;border-radius:2px}
.metabar.big .mtick{top:-4px;height:28px}
.metabar .mtick.sup{background:var(--good)}.metabar .mtick.meta{background:var(--high)}
.metabar .mlbl{position:absolute;top:22px;font-size:9.5px;font-weight:700;color:var(--muted);transform:translateX(-50%);white-space:nowrap}
.metabar.big .mlbl{top:30px}
.zbadge{font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;white-space:nowrap;display:inline-block}
.zbadge.super{background:color-mix(in srgb,var(--good) 18%,transparent);color:var(--good)}
.zbadge.meta{background:color-mix(in srgb,var(--med) 24%,transparent);color:var(--high)}
.zbadge.acima{background:color-mix(in srgb,var(--crit) 16%,transparent);color:var(--crit)}
.sqrow{display:grid;grid-template-columns:130px 1fr 82px;gap:16px;align-items:center;padding:15px 0;border-top:1px solid var(--line)}
.sqrow:first-child{border-top:0}
.sqrow .sqn{font-weight:800;font-size:14px}
.sqrow .sqmeta{font-size:11px;color:var(--muted);margin-top:3px}
.sqrow .sqpct{font-family:var(--display);font-size:22px;font-weight:800;text-align:right;line-height:1}
.sqrow .sqpct span{font-size:11px;font-weight:700}
@media(max-width:640px){.sqrow{grid-template-columns:1fr auto;gap:6px 12px}.sqrow .barcell{grid-column:1/3;order:3}}
.ctable{width:100%;border-collapse:collapse;font-size:12.5px}
.ctable th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:700;padding:9px 10px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--panel);z-index:1}
.ctable th.r,.ctable td.r{text-align:right}
.ctable td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
.ctable tr:last-child td{border-bottom:0}
.ctable tbody tr:hover td{background:var(--panel-2)}
.ctable .fee{font-weight:800;white-space:nowrap;font-variant-numeric:tabular-nums}
.ctable .cname{font-weight:700;color:var(--ink);text-decoration:none}
.ctable .cname:hover{color:var(--gold-2);text-decoration:underline}
.tblwrap{max-height:560px;overflow:auto;border-radius:0 0 var(--r) var(--r)}
.sqtag{font-size:10px;font-weight:800;padding:2px 7px;border-radius:6px;background:var(--panel-2);border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.metaedit{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}
.metaedit label{font-size:12px;font-weight:600;color:var(--muted);display:flex;flex-direction:column;gap:6px}
.metaedit input{font-family:inherit;font-size:16px;font-weight:800;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);border-radius:9px;padding:9px 12px;width:96px}
.sqtoggle{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.sqtoggle:first-child{border-top:0}
.switch{font-family:inherit;font-size:11.5px;font-weight:700;border:1px solid var(--line);background:var(--panel-2);color:var(--muted);border-radius:8px;padding:7px 12px;cursor:pointer}
.switch[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2);border-color:transparent}
:root[data-theme="dark"] .switch[aria-pressed="true"]{color:var(--gold)}
.note{background:var(--panel-2);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:10px;padding:12px 15px;font-size:12.5px;color:var(--muted);line-height:1.55}
.note b{color:var(--ink)}
.fbars{display:flex;align-items:flex-end;gap:5px;height:90px;overflow-x:auto;padding-top:8px}
.fbars .fb{flex:1;min-width:14px;background:linear-gradient(180deg,var(--gold),var(--gold-2));border-radius:4px 4px 0 0;min-height:3px;position:relative}
.fbars .fb .ft{position:absolute;top:-16px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--muted);white-space:nowrap}
.peoplemini{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.pmchip{display:flex;align-items:center;gap:7px;background:var(--panel-2);border:1px solid var(--line);border-radius:999px;padding:4px 11px 4px 4px;font-size:11.5px;font-weight:600}
</style>

<div class="wrap"><div class="app">
  <aside class="side">
    <div class="brand"><span class="logo"><span class="top"><span class="au">Au</span><span class="re">re</span><span class="dot"></span></span><span class="dig">DIGITAL</span></span><span class="tag">· Times</span></div>
    <div class="navlbl">Tarefas</div>
    <button class="nav" data-page="overview" aria-current="true"><span class="ic">▚</span> Visão geral</button>
    <button class="nav" data-page="person"><span class="ic">◉</span> Por pessoa</button>
    <div class="navlbl">Churn</div>
    <button class="nav" data-page="churn"><span class="ic">📉</span> Controle de churn</button>
    <button class="nav" data-page="times"><span class="ic">⚙</span> Times &amp; metas</button>
    <div id="teamfilterwrap">
      <div class="navlbl">Time</div>
      <div class="tfilter" id="tfilter">
        <button data-team="all" aria-pressed="true">Ambos</button>
        <button data-team="E-SCALE" aria-pressed="false">E‑SCALE</button>
        <button data-team="FENIX" aria-pressed="false">FENIX</button>
      </div>
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
    <div class="period" id="periodbar" title="Filtra conclusões/adiamentos (Tarefas) e saídas/histórico de fee (Churn). O churn atual é sempre o estado do momento.">
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
<input type="file" id="cfgfile" accept="application/json" hidden>

<script>
const MODEL = __MODEL__;
const MEM = {}; MODEL.members.forEach(m=>MEM[m.uid]=m);
const PPBYID = {}; (MODEL.postpones||[]).forEach(p=>{PPBYID[p.id]=p;});
const HKEY="clk_hidden_v1";
let page="overview", team="all", selUid=MODEL.members[0]?.uid, dFrom=MODEL.window.to, dTo=MODEL.window.to;  // abre em "Hoje"
let churnView="overview";  // navegação micro do churn: "overview" | "sq:NOME" | "pp:UID"
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
function todayFor(uid){const h=hidden();return (MODEL.today||[]).filter(t=>t.uid===uid&&!h.has(t.id));}
const inRng=day=>day>=dFrom&&day<=dTo;
function doneFor(uid){return (MODEL.done||[]).filter(e=>e.uid===uid&&inRng(e.day));}
function behavior(uid){
  const done=doneFor(uid);
  const created=(MODEL.created||[]).filter(e=>e.uid===uid&&inRng(e.day)).length;
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
  const hiddenN=odAll.length-od.length,mal=malformedFor(selUid),b=behavior(selUid),crit=od.filter(t=>t.days>30).length,td=todayFor(selUid);
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
      <div class="stat"><div class="ico">📅</div><div class="n">${td.length}</div><div class="l">Para fazer hoje</div></div>
      <div class="stat"><div class="ico">⚠️</div><div class="n">${mal.length}</div><div class="l">Mal cadastradas</div></div>
      <div class="stat"><div class="ico">✅</div><div class="n" style="color:${otColor}">${b.otRate==null?"—":b.otRate+"%"}</div><div class="l">No prazo</div></div>
      <div class="stat"><div class="ico">📈</div><div class="n">${b.doneN}</div><div class="l">Concluídas</div></div>
      <div class="stat"><div class="ico">📦</div><div class="n">${b.maxDay}</div><div class="l">Check em lote/dia</div></div>
      <div class="stat"><div class="ico">✎</div><div class="n">${b.created}</div><div class="l">Criadas</div></div>
    </div>

    <div class="card" id="odsec"><div class="card-h"><h3>Em atraso</h3><div class="r"><span>${od.length} aberta(s)</span>${hiddenN?`<button class="linkish" id="showhidden">ver ${hiddenN} oculta(s)</button>`:""}</div></div>
      ${od.length?`<ul class="tasks" style="padding:4px 16px 8px">${od.map(t=>taskRow(t,true)).join("")}</ul>`:`<div class="empty">Sem tarefas em atraso 🎉</div>`}</div>

    <div class="card" id="todaysec"><div class="card-h"><h3>Para fazer hoje</h3><div class="r">${td.length} tarefa(s) · vencem hoje</div></div>
      ${td.length?`<ul class="tasks" style="padding:4px 16px 8px">${td.map(t=>{const prb=(t.priority==="urgent"||t.priority==="high")?`<span class="pill pr ${t.priority}">${t.priority==="urgent"?"Urgente":"Alta"}</span>`:"";
        return `<li class="trow"><span class="stripe s-today"></span>
          <div style="min-width:0"><a class="tname" href="https://app.clickup.com/t/${t.id}" target="_blank" rel="noopener">${esc(t.name)}</a>
          <div class="tmeta">${t.project?`<span class="pill proj">🏢 ${esc(t.project)}</span>`:""}<span class="pill list">${esc(t.list)}</span><span class="pill status">${esc(t.status)}</span>${prb}</div></div>
          <div class="tright"><div class="tdue">vence hoje</div></div>
          <button class="closebtn" data-close="${t.id}" title="Ocultar">✓ Fechar</button></li>`;}).join("")}</ul>`
      :`<div class="empty">Nada com prazo para hoje.</div>`}</div>

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

    <div class="card"><div class="card-h"><h3>Concluídas</h3><div class="r">${b.doneN} no período · ${fmtBR(dFrom)} → ${fmtBR(dTo)}</div></div>
      ${b.doneN?`<ul class="tasks" style="padding:4px 16px 0">${b.done.slice().sort((a,c)=>a.day<c.day?1:-1).slice(0,40).map(e=>`<li class="trow"><span class="stripe ${e.late?'s-crit':(e.noDue?'s-today':'s-ok')}"></span>
        <div style="min-width:0"><a class="tname" href="https://app.clickup.com/t/${e.id}" target="_blank" rel="noopener">${esc(e.name)}</a>
        <div class="tmeta">${e.project?`<span class="pill proj">🏢 ${esc(e.project)}</span>`:""}<span class="pill list">${esc(e.list)}</span><span class="pill ${e.late?'badlate':(e.noDue?'list':'okdone')}">${e.late?'em atraso':(e.noDue?'sem prazo':'no prazo')}</span></div></div>
        <div class="tright"><div class="tdue">${fmtBR(e.day)}</div></div><span></span></li>`).join("")}</ul>${b.doneN>40?`<div style="padding:8px 16px 12px;font-size:12px;color:var(--muted)">Mostrando as 40 mais recentes de ${b.doneN}. Reduza o período para ver menos.</div>`:""}`
      :`<div class="empty">Nenhuma conclusão nesse período.</div>`}</div>

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

/* ---------------- CHURN ---------------- */
const BRL=n=>'R$ '+Math.round(n||0).toLocaleString('pt-BR');
const MKEY="clk_metas_v1";
function metas(){try{return Object.assign({meta:5,sup:3,hidden:[]},JSON.parse(localStorage.getItem(MKEY)||"{}"))}catch(e){return{meta:5,sup:3,hidden:[]}}}
function setMetas(m){localStorage.setItem(MKEY,JSON.stringify(m))}
function zoneOf(pct,m){return pct<=m.sup?"super":pct<=m.meta?"meta":"acima"}
const ZONEC={super:"var(--good)",meta:"var(--high)",acima:"var(--crit)"};
const ZONEL={super:"🟢 Super meta",meta:"🟡 Meta",acima:"🔴 Acima da meta"};
function attainBar(pct,m,big){
  const max=Math.max(m.meta*1.9,pct*1.12,8), z=zoneOf(pct,m), at=x=>Math.min(100,x/max*100);
  return `<div class="metabar${big?' big':''}">
    <div class="mfill" style="width:${at(pct)}%;background:${ZONEC[z]}"></div>
    <span class="mtick sup" style="left:${at(m.sup)}%"></span>${big?`<span class="mlbl" style="left:${at(m.sup)}%">super ${m.sup}%</span>`:''}
    <span class="mtick meta" style="left:${at(m.meta)}%"></span>${big?`<span class="mlbl" style="left:${at(m.meta)}%">meta ${m.meta}%</span>`:''}</div>`;
}
function avaChurn(p){const ini=esc(initials(p.name||"—"));
  const st="width:30px;height:30px;border-radius:9px;font-size:11px;background:linear-gradient(135deg,var(--gold),var(--gold-2));flex:none";
  if(p.avatar)return `<span class="ava" style="position:relative;overflow:hidden;${st}">${ini}<img src="${esc(p.avatar)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" onerror="this.remove()"></span>`;
  return `<span class="ava" style="${st}">${ini}</span>`;}
function exportCfg(){
  const cfg={metas:metas(),hiddenTasks:[...hidden()],exportedAt:new Date().toISOString()};
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(cfg,null,2)],{type:"application/json"}));
  a.download="painel-config.json";document.body.appendChild(a);a.click();a.remove();
}
function importCfg(file){const r=new FileReader();r.onload=()=>{try{const c=JSON.parse(r.result);
  if(c.metas)setMetas(c.metas); if(Array.isArray(c.hiddenTasks))setHidden(new Set(c.hiddenTasks));
  showToast("Config importada.");render();}catch(e){alert("Arquivo de config inválido.");}};r.readAsText(file);}

function renderChurn(){
  const C=MODEL.churn||{squads:[],people:[],clients:[],totals:{}}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  if(churnView.slice(0,3)==="sq:")return renderChurnSquad(churnView.slice(3),C,m,hiddenSq);
  if(churnView.slice(0,3)==="pp:")return renderChurnPerson(+churnView.slice(3),C,m,hiddenSq);
  $("ptitle").textContent="Controle de churn";
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-export-cfg>⭳ Exportar</button><button class="btn" data-import-cfg>⭱ Importar</button></div>`;
  const squads=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad));
  const tAtv=squads.reduce((s,x)=>s+x.feeAtivo,0), tAvi=squads.reduce((s,x)=>s+x.feeAviso,0);
  const tPct=(tAtv+tAvi)?+(tAvi/(tAtv+tAvi)*100).toFixed(2):0, z=zoneOf(tPct,m);
  const nAtivo=squads.reduce((s,x)=>s+x.nAtivo,0), nAviso=squads.reduce((s,x)=>s+x.nAviso,0);
  const avisoClients=(C.clients||[]).filter(c=>c.grp==="aviso"&&!hiddenSq.has(c.squad)).sort((a,b)=>b.fee-a.fee);
  const saidas=(C.clients||[]).filter(c=>c.grp==="churn"&&c.churnDate&&inRng(c.churnDate)&&!hiddenSq.has(c.squad)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const perdidoP=saidas.reduce((s,c)=>s+c.fee,0);
  const people=(C.people||[]).filter(p=>(p.nAtivo+p.nAviso)>0&&(p.squads||[]).some(s=>!hiddenSq.has(s))).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  const fh=Object.entries(MODEL.feeHistory||{}).filter(([d])=>inRng(d)).sort((a,b)=>a[0]<b[0]?-1:1);
  const fhMax=Math.max(1,...fh.map(([,v])=>v.feeAtivo||0));
  const squadRow=s=>{const zz=zoneOf(s.churnPct,m);return `<div class="sqrow" data-churn-open="sq:${esc(s.squad)}" style="cursor:pointer" title="Abrir ${esc(s.squad)}">
    <div><div class="sqn">${esc(s.squad)}</div><div class="sqmeta">${s.nAtivo} ativos · ${s.nAviso} em aviso</div></div>
    <div class="barcell">${attainBar(s.churnPct,m)}<div style="display:flex;justify-content:space-between;gap:8px;margin-top:5px;font-size:11px;color:var(--muted)">
      <span>${BRL(s.feeAtivo)} ativo</span><span class="zbadge ${zz}">${ZONEL[zz]}</span><span style="color:var(--crit)">${BRL(s.feeAviso)} aviso</span></div></div>
    <div class="sqpct" style="color:${ZONEC[zz]}">${s.churnPct}<span>%</span></div></div>`;};

  $("root").innerHTML=`<div class="col">
    <div class="banner"><div class="bt">
      <h2>Controle de churn — agência</h2>
      <p>${BRL(tAtv)} de fee ativo sob gestão · ${BRL(tAvi)} em aviso (${nAviso} cliente(s)) — churn de <b>${tPct}%</b> do faturamento. Meta ≤ ${m.meta}% · super meta ≤ ${m.sup}%.</p>
    </div><div class="avatar">📉</div></div>

    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(tAtv)}</div><div class="l">Fee ativo</div><div class="s">${nAtivo} clientes</div></div>
      <div class="kpi"><div class="n" style="color:var(--crit)">${BRL(tAvi)}</div><div class="l">Fee em aviso</div><div class="s">${nAviso} clientes</div></div>
      <div class="kpi"><div class="n" style="color:${ZONEC[z]}">${tPct}%</div><div class="l">Churn (faturamento)</div><div class="s"><span class="zbadge ${z}">${ZONEL[z]}</span></div></div>
      <div class="kpi"><div class="n">${BRL(perdidoP)}</div><div class="l">Saídas no período</div><div class="s">${saidas.length} cliente(s)</div></div>
    </div>

    <div class="card"><div class="card-h"><h3>Atingimento de meta — agência</h3><div class="r">churn ${tPct}% · meta ≤ ${m.meta}% · super ≤ ${m.sup}%</div></div>
      <div class="pad"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px">
        <b style="font-family:var(--display);font-size:30px;color:${ZONEC[z]}">${tPct}%</b><span class="zbadge ${z}">${ZONEL[z]}</span></div>
        ${attainBar(tPct,m,true)}<div style="height:26px"></div>
        <div class="note">A barra mostra o churn atual contra a <b>super meta (${m.sup}%)</b> e a <b>meta (${m.meta}%)</b>. Quanto <b>menor</b>, melhor. Edite as metas em <b>Times &amp; metas</b>.</div>
      </div></div>

    <div class="card"><div class="card-h"><h3>Por squad</h3><div class="r">${squads.length} squads · clique para abrir</div></div>
      <div class="pad">${squads.map(squadRow).join("")||'<div class="empty">Sem squads para mostrar.</div>'}</div></div>

    <div class="card"><div class="card-h"><h3>Por pessoa</h3><div class="r">carteira (Account + Gestor) · clique para abrir</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Pessoa</th><th>Squad</th><th class="r">Fee ativo</th><th class="r">Em aviso</th><th class="r">Churn</th><th style="width:120px">Meta</th></tr></thead>
      <tbody>${people.map(p=>{const zz=zoneOf(p.churnPct,m);return `<tr data-churn-open="pp:${p.uid}" style="cursor:pointer">
        <td><div style="display:flex;align-items:center;gap:9px">${avaChurn(p)}<span><b>${esc(p.name||"—")}</b><br><span style="font-size:10.5px;color:var(--muted)">${(p.roles||[]).map(r=>r==="Gestor de Tráfego"?"Gestor":r).join(" · ")}</span></span></div></td>
        <td>${(p.squads||[]).map(s=>`<span class="sqtag">${esc(s)}</span>`).join(" ")||"—"}</td>
        <td class="r fee">${BRL(p.feeAtivo)}</td><td class="r fee" style="color:${p.feeAviso?'var(--crit)':'var(--muted)'}">${p.feeAviso?BRL(p.feeAviso):"—"}</td>
        <td class="r"><b style="color:${ZONEC[zz]}">${p.churnPct}%</b></td><td>${attainBar(p.churnPct,m)}</td></tr>`;}).join("")||'<tr><td colspan="6" class="empty">Sem pessoas.</td></tr>'}</tbody></table></div></div>

    <div class="card"><div class="card-h"><h3>Clientes em aviso (risco de churn)</h3><div class="r">${avisoClients.length} · ${BRL(tAvi)}</div></div>
      ${avisoClients.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Aviso</th></tr></thead>
      <tbody>${avisoClients.map(c=>`<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td>
        <td><span class="sqtag">${esc(c.squad)}</span></td><td>${esc(c.account||"—")}</td><td>${esc(c.gestor||"—")}</td>
        <td class="r fee" style="color:var(--crit)">${BRL(c.fee)}</td><td class="r">${c.aviso?fmtBR(c.aviso):"—"}</td></tr>`).join("")}</tbody></table></div>`
      :'<div class="empty">Nenhum cliente em aviso 🎉</div>'}</div>

    <div class="card"><div class="card-h"><h3>Saídas no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${saidas.length} · ${BRL(perdidoP)}</div></div>
      ${saidas.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Account</th><th class="r">Fee</th><th class="r">Saída</th></tr></thead>
      <tbody>${saidas.map(c=>`<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td>
        <td><span class="sqtag">${esc(c.squad)}</span></td><td>${esc(c.account||"—")}</td>
        <td class="r fee">${BRL(c.fee)}</td><td class="r">${c.churnDate?fmtBR(c.churnDate):"—"}</td></tr>`).join("")}</tbody></table></div>`
      :'<div class="empty">Nenhuma saída nesse período. Ajuste o período no topo (ex.: "Este mês" ou "Tudo").</div>'}</div>

    <div class="card"><div class="card-h"><h3>Fee ativo ao longo do tempo</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)}</div></div>
      <div class="pad">${fh.length>1?`<div class="fbars">${fh.map(([d,v])=>`<div class="fb" style="height:${Math.max(3,(v.feeAtivo||0)/fhMax*82)}px" title="${fmtBR(d)}: ${BRL(v.feeAtivo||0)}"></div>`).join("")}</div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--muted)"><span>${fmtBR(fh[0][0])}</span><span>${fmtBR(fh[fh.length-1][0])}</span></div>`
      :`<div class="note">📅 O histórico de fee é gravado <b>1×/dia às 23h59</b> e começa a partir de hoje. Em alguns dias esta curva mostra a evolução do faturamento conforme clientes entram e saem.</div>`}</div></div>
  </div>`;
}

/* ---------------- CHURN · MICRO (por squad / por pessoa) ---------------- */
function churnPctCalc(atv,avi){return (atv+avi)?+(avi/(atv+avi)*100).toFixed(2):0;}
function bigAva(x){const nm=typeof x==="string"?x:((x&&x.name)||"—");const av=(x&&typeof x==="object")?x.avatar:null;const ini=esc(initials(nm));
  if(av)return `<span class="avatar" style="position:relative;overflow:hidden">${ini}<img src="${esc(av)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" onerror="this.remove()"></span>`;
  return `<div class="avatar">${ini}</div>`;}
function squadInitial(s){return esc(((s||"?").trim()[0]||"?").toUpperCase());}

function renderChurnSquad(name,C,m,hiddenSq){
  const squadsVis=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad));
  const s=squadsVis.find(x=>x.squad===name)||(C.squads||[]).find(x=>x.squad===name);
  if(!s){churnView="overview";return renderChurn();}
  const cls=(C.clients||[]).filter(c=>c.squad===name);
  const ativos=cls.filter(c=>c.grp==="ativo").sort((a,b)=>b.fee-a.fee);
  const aviso=cls.filter(c=>c.grp==="aviso").sort((a,b)=>b.fee-a.fee);
  const saidas=cls.filter(c=>c.grp==="churn"&&c.churnDate&&inRng(c.churnDate)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const perdido=saidas.reduce((x,c)=>x+c.fee,0), zz=zoneOf(s.churnPct,m);
  const PBYU={};(C.people||[]).forEach(p=>PBYU[p.uid]=p);
  const pmap={};
  cls.forEach(c=>{[["Account",c.accountUid],["Gestor de Tráfego",c.gestorUid]].forEach(([role,uid])=>{
    if(!uid)return;const p=pmap[uid]||(pmap[uid]={uid,name:(PBYU[uid]&&PBYU[uid].name)||"—",avatar:PBYU[uid]&&PBYU[uid].avatar,feeAtivo:0,feeAviso:0,nAtivo:0,nAviso:0,roles:new Set()});
    p.roles.add(role);if(c.grp==="ativo"){p.feeAtivo+=c.fee;p.nAtivo++;}else if(c.grp==="aviso"){p.feeAviso+=c.fee;p.nAviso++;}});});
  const ppl=Object.values(pmap).map(p=>({uid:p.uid,name:p.name,avatar:p.avatar,feeAtivo:p.feeAtivo,feeAviso:p.feeAviso,nAtivo:p.nAtivo,nAviso:p.nAviso,roles:[...p.roles],churnPct:churnPctCalc(p.feeAtivo,p.feeAviso)})).filter(p=>p.nAtivo+p.nAviso>0).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  const fh=Object.entries(MODEL.feeHistory||{}).filter(([d])=>inRng(d)).sort((a,b)=>a[0]<b[0]?-1:1).map(([d,v])=>[d,(v.bySquad&&v.bySquad[name])||0]);
  const fhMax=Math.max(1,...fh.map(([,x])=>x));
  $("ptitle").textContent="Churn · "+name;
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-churn-back>← Voltar</button><button class="btn" data-churn-step="-1">↑ Squad ant.</button><button class="btn" data-churn-step="1">Próx. squad ↓</button></div>`;
  const cRow=(c,dk)=>`<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td><td>${esc(c.account||"—")}</td><td>${esc(c.gestor||"—")}</td><td class="r fee"${c.grp==="aviso"?' style="color:var(--crit)"':''}>${BRL(c.fee)}</td>${dk?`<td class="r">${c[dk]?fmtBR(c[dk]):"—"}</td>`:''}</tr>`;
  $("root").innerHTML=`<div class="content"><div class="col">
    <div class="banner"><div class="bt"><h2>${esc(name)}</h2>
      <p>${BRL(s.feeAtivo)} de fee ativo · ${BRL(s.feeAviso)} em aviso (${s.nAviso} cliente(s)) — churn de <b>${s.churnPct}%</b>. Meta ≤ ${m.meta}% · super ≤ ${m.sup}%.</p>
      <div class="cta"><button class="ghost" data-churn-back>← Todos os squads</button></div>
    </div><div class="avatar">${squadInitial(name)}</div></div>
    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(s.feeAtivo)}</div><div class="l">Fee ativo</div><div class="s">${s.nAtivo} clientes</div></div>
      <div class="kpi"><div class="n" style="color:var(--crit)">${BRL(s.feeAviso)}</div><div class="l">Fee em aviso</div><div class="s">${s.nAviso} clientes</div></div>
      <div class="kpi"><div class="n" style="color:${ZONEC[zz]}">${s.churnPct}%</div><div class="l">Churn</div><div class="s"><span class="zbadge ${zz}">${ZONEL[zz]}</span></div></div>
      <div class="kpi"><div class="n">${BRL(perdido)}</div><div class="l">Saídas no período</div><div class="s">${saidas.length} cliente(s)</div></div>
    </div>
    <div class="card"><div class="card-h"><h3>Atingimento de meta — ${esc(name)}</h3><div class="r">churn ${s.churnPct}% · meta ≤ ${m.meta}% · super ≤ ${m.sup}%</div></div>
      <div class="pad"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px"><b style="font-family:var(--display);font-size:30px;color:${ZONEC[zz]}">${s.churnPct}%</b><span class="zbadge ${zz}">${ZONEL[zz]}</span></div>${attainBar(s.churnPct,m,true)}<div style="height:26px"></div></div></div>
    <div class="card"><div class="card-h"><h3>Pessoas do squad</h3><div class="r">${ppl.length} · clique para abrir</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Pessoa</th><th>Papel</th><th class="r">Fee ativo</th><th class="r">Em aviso</th><th class="r">Churn</th><th style="width:120px">Meta</th></tr></thead>
      <tbody>${ppl.map(p=>{const pz=zoneOf(p.churnPct,m);return `<tr data-churn-open="pp:${p.uid}" style="cursor:pointer">
        <td><div style="display:flex;align-items:center;gap:9px">${avaChurn(p)}<b>${esc(p.name)}</b></div></td>
        <td>${p.roles.map(r=>r==="Gestor de Tráfego"?"Gestor":r).join(" · ")}</td>
        <td class="r fee">${BRL(p.feeAtivo)}</td><td class="r fee" style="color:${p.feeAviso?'var(--crit)':'var(--muted)'}">${p.feeAviso?BRL(p.feeAviso):"—"}</td>
        <td class="r"><b style="color:${ZONEC[pz]}">${p.churnPct}%</b></td><td>${attainBar(p.churnPct,m)}</td></tr>`;}).join("")||'<tr><td colspan="6" class="empty">Sem pessoas vinculadas.</td></tr>'}</tbody></table></div></div>
    <div class="card"><div class="card-h"><h3>Clientes em aviso</h3><div class="r">${aviso.length} · ${BRL(aviso.reduce((x,c)=>x+c.fee,0))}</div></div>
      ${aviso.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Aviso</th></tr></thead><tbody>${aviso.map(c=>cRow(c,"aviso")).join("")}</tbody></table></div>`:'<div class="empty">Nenhum cliente em aviso 🎉</div>'}</div>
    <div class="card"><div class="card-h"><h3>Clientes ativos</h3><div class="r">${ativos.length} · ${BRL(ativos.reduce((x,c)=>x+c.fee,0))}</div></div>
      ${ativos.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th></tr></thead><tbody>${ativos.map(c=>cRow(c,null)).join("")}</tbody></table></div>`:'<div class="empty">—</div>'}</div>
    <div class="card"><div class="card-h"><h3>Saídas no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${saidas.length} · ${BRL(perdido)}</div></div>
      ${saidas.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Saída</th></tr></thead><tbody>${saidas.map(c=>cRow(c,"churnDate")).join("")}</tbody></table></div>`:'<div class="empty">Nenhuma saída nesse período.</div>'}</div>
    <div class="card"><div class="card-h"><h3>Fee ativo do squad ao longo do tempo</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)}</div></div>
      <div class="pad">${fh.length>1?`<div class="fbars">${fh.map(([d,x])=>`<div class="fb" style="height:${Math.max(3,x/fhMax*82)}px" title="${fmtBR(d)}: ${BRL(x)}"></div>`).join("")}</div><div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--muted)"><span>${fmtBR(fh[0][0])}</span><span>${fmtBR(fh[fh.length-1][0])}</span></div>`:'<div class="note">📅 O histórico por squad é gravado 1×/dia às 23h59 e começa a acumular a partir de agora.</div>'}</div></div>
  </div>
  <div class="col"><div class="acard"><h3>Squads</h3><p class="sub">${squadsVis.length} · clique para abrir</p>
    <div class="plist">${squadsVis.map(x=>{const xz=zoneOf(x.churnPct,m);return `<button class="pitem" data-churn-open="sq:${esc(x.squad)}" aria-selected="${x.squad===name}">
      <span class="ava" style="width:32px;height:32px;font-size:11px;border-radius:9px;background:linear-gradient(135deg,var(--gold),var(--gold-2));color:#fff;display:grid;place-items:center;font-weight:800">${squadInitial(x.squad)}</span>
      <span class="pn"><b>${esc(x.squad)}</b><span>${x.nAtivo} ativos · ${x.nAviso} aviso</span></span>
      <span class="chipn" style="color:${ZONEC[xz]}">${x.churnPct}<span style="font-size:9px">%</span></span></button>`;}).join("")}</div></div></div></div>`;
}

function renderChurnPerson(uid,C,m,hiddenSq){
  const PBYU={};(C.people||[]).forEach(p=>PBYU[p.uid]=p);
  const pref=PBYU[uid];
  const cls=(C.clients||[]).filter(c=>(c.accountUid===uid||c.gestorUid===uid)&&!hiddenSq.has(c.squad));
  if(!pref&&!cls.length){churnView="overview";return renderChurn();}
  const name=(pref&&pref.name)||(cls[0]&&(cls[0].accountUid===uid?cls[0].account:cls[0].gestor))||"—";
  const ativos=cls.filter(c=>c.grp==="ativo").sort((a,b)=>b.fee-a.fee);
  const aviso=cls.filter(c=>c.grp==="aviso").sort((a,b)=>b.fee-a.fee);
  const saidas=cls.filter(c=>c.grp==="churn"&&c.churnDate&&inRng(c.churnDate)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const feeAtv=ativos.reduce((x,c)=>x+c.fee,0), feeAvi=aviso.reduce((x,c)=>x+c.fee,0);
  const pct=churnPctCalc(feeAtv,feeAvi), zz=zoneOf(pct,m);
  const roleOf=c=>(c.accountUid===uid&&c.gestorUid===uid)?"Account + Gestor":c.accountUid===uid?"Account":"Gestor";
  const squadsList=[...new Set(cls.map(c=>c.squad))];
  const peopleVis=(C.people||[]).filter(pp=>(pp.nAtivo+pp.nAviso)>0&&(pp.squads||[]).some(x=>!hiddenSq.has(x))).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  $("ptitle").textContent="Churn · "+name;
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-churn-back>← Voltar</button><button class="btn" data-churn-step="-1">↑ Anterior</button><button class="btn" data-churn-step="1">Próximo ↓</button></div>`;
  const pRow=(c,dk)=>`<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td><td><span class="sqtag">${esc(c.squad)}</span></td><td>${roleOf(c)}</td><td class="r fee"${c.grp==="aviso"?' style="color:var(--crit)"':''}>${BRL(c.fee)}</td>${dk?`<td class="r">${c[dk]?fmtBR(c[dk]):"—"}</td>`:''}</tr>`;
  $("root").innerHTML=`<div class="content"><div class="col">
    <div class="banner"><div class="bt"><h2>${esc(name)}</h2>
      <p>Carteira de ${BRL(feeAtv+feeAvi)} · ${BRL(feeAvi)} em aviso — churn de <b>${pct}%</b>. ${squadsList.map(x=>`<span class="teamchip">${esc(x)}</span>`).join(" ")}</p>
      <div class="cta"><button class="ghost" data-churn-back>← Todas as pessoas</button></div>
    </div>${bigAva(pref||name)}</div>
    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(feeAtv)}</div><div class="l">Fee ativo</div><div class="s">${ativos.length} clientes</div></div>
      <div class="kpi"><div class="n" style="color:var(--crit)">${BRL(feeAvi)}</div><div class="l">Fee em aviso</div><div class="s">${aviso.length} clientes</div></div>
      <div class="kpi"><div class="n" style="color:${ZONEC[zz]}">${pct}%</div><div class="l">Churn (carteira)</div><div class="s"><span class="zbadge ${zz}">${ZONEL[zz]}</span></div></div>
      <div class="kpi"><div class="n">${BRL(saidas.reduce((x,c)=>x+c.fee,0))}</div><div class="l">Saídas no período</div><div class="s">${saidas.length} cliente(s)</div></div>
    </div>
    <div class="card"><div class="card-h"><h3>Atingimento de meta — ${esc(name)}</h3><div class="r">churn ${pct}% · meta ≤ ${m.meta}% · super ≤ ${m.sup}%</div></div>
      <div class="pad"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px"><b style="font-family:var(--display);font-size:30px;color:${ZONEC[zz]}">${pct}%</b><span class="zbadge ${zz}">${ZONEL[zz]}</span></div>${attainBar(pct,m,true)}<div style="height:26px"></div>
        <div class="note">Carteira consolidada como <b>Account</b> e <b>Gestor de Tráfego</b>. Cada cliente conta na carteira do seu Account e do seu Gestor.</div></div></div>
    <div class="card"><div class="card-h"><h3>Clientes em aviso</h3><div class="r">${aviso.length} · ${BRL(feeAvi)}</div></div>
      ${aviso.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th><th class="r">Aviso</th></tr></thead><tbody>${aviso.map(c=>pRow(c,"aviso")).join("")}</tbody></table></div>`:'<div class="empty">Nenhum cliente em aviso 🎉</div>'}</div>
    <div class="card"><div class="card-h"><h3>Clientes ativos</h3><div class="r">${ativos.length} · ${BRL(feeAtv)}</div></div>
      ${ativos.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th></tr></thead><tbody>${ativos.map(c=>pRow(c,null)).join("")}</tbody></table></div>`:'<div class="empty">—</div>'}</div>
    <div class="card"><div class="card-h"><h3>Saídas no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${saidas.length}</div></div>
      ${saidas.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th><th class="r">Saída</th></tr></thead><tbody>${saidas.map(c=>pRow(c,"churnDate")).join("")}</tbody></table></div>`:'<div class="empty">Nenhuma saída nesse período.</div>'}</div>
  </div>
  <div class="col"><div class="acard"><h3>Pessoas</h3><p class="sub">${peopleVis.length} · clique para abrir</p>
    <div class="plist">${peopleVis.map(x=>{const xz=zoneOf(x.churnPct,m);return `<button class="pitem" data-churn-open="pp:${x.uid}" aria-selected="${x.uid===uid}">
      ${avaChurn(x)}
      <span class="pn"><b>${esc(x.name||"—")}</b><span>${(x.squads||[]).join(", ")||"—"}</span></span>
      <span class="chipn" style="color:${ZONEC[xz]}">${x.churnPct}<span style="font-size:9px">%</span></span></button>`;}).join("")}</div></div></div></div>`;
}

function churnStep(d){
  const C=MODEL.churn||{}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  if(churnView.slice(0,3)==="sq:"){
    const list=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad));
    const i=list.findIndex(s=>s.squad===churnView.slice(3));
    if(i>=0&&list.length)churnView="sq:"+list[(i+d+list.length)%list.length].squad;
  }else if(churnView.slice(0,3)==="pp:"){
    const list=(C.people||[]).filter(pp=>(pp.nAtivo+pp.nAviso)>0&&(pp.squads||[]).some(s=>!hiddenSq.has(s))).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
    const uid=+churnView.slice(3), i=list.findIndex(pp=>pp.uid===uid);
    if(i>=0&&list.length)churnView="pp:"+list[(i+d+list.length)%list.length].uid;
  }
  render();window.scrollTo({top:0});
}

/* ---------------- TIMES & METAS ---------------- */
function renderTimes(){
  $("ptitle").textContent="Times & metas";
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-export-cfg>⭳ Exportar</button><button class="btn" data-import-cfg>⭱ Importar</button></div>`;
  const C=MODEL.churn||{squads:[],people:[]}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  const allSquads=(C.squads||[]).filter(s=>s.squad!=="—");
  const bySquad={};(C.people||[]).forEach(p=>(p.squads||[]).forEach(s=>{(bySquad[s]=bySquad[s]||[]).push(p);}));
  $("root").innerHTML=`<div class="col">
    <div class="note">⚙️ <b>Como funciona:</b> squads e pessoas vêm automaticamente do ClickUp (campo <b>Squad</b> + <b>Account</b>/<b>Gestor de Tráfego</b> na lista de Empresas). Ao cadastrar um cliente ou trocar alguém de squad no ClickUp, o painel se atualiza sozinho na próxima rodada — não precisa recadastrar aqui. Você edita as <b>metas</b> e escolhe quais squads acompanhar. <b>(Etapa que vamos refinar juntos.)</b></div>

    <div class="card"><div class="card-h"><h3>Metas de churn</h3><div class="r">valem para todos os squads e pessoas</div></div>
      <div class="pad"><div class="metaedit">
        <label>Meta — churn até (%)<input type="number" id="metaInput" value="${m.meta}" min="0" max="100" step="0.5"></label>
        <label>Super meta — churn até (%)<input type="number" id="supInput" value="${m.sup}" min="0" max="100" step="0.5"></label>
        <button class="applybtn" data-save-metas>Salvar metas</button>
      </div><div class="note" style="margin-top:14px">Até <b>${m.sup}%</b> = super meta 🟢 · até <b>${m.meta}%</b> = meta 🟡 · acima de <b>${m.meta}%</b> = fora da meta 🔴. Salvo neste navegador — use <b>Exportar</b> para compartilhar/backup.</div></div></div>

    <div class="card"><div class="card-h"><h3>Squads acompanhados</h3><div class="r">${allSquads.length-hiddenSq.size}/${allSquads.length} ativos</div></div>
      <div class="pad">${allSquads.map(s=>{const on=!hiddenSq.has(s.squad);return `<div class="sqtoggle">
        <div><b>${esc(s.squad)}</b><div style="font-size:11.5px;color:var(--muted)">${s.nAtivo} ativos · ${BRL(s.feeAtivo)} · churn ${s.churnPct}%</div></div>
        <button class="switch" data-toggle-squad="${esc(s.squad)}" aria-pressed="${on}">${on?"Acompanhando":"Oculto"}</button></div>`;}).join("")||'<div class="empty">—</div>'}</div></div>

    <div class="card"><div class="card-h"><h3>Pessoas por squad</h3><div class="r">automático do ClickUp</div></div>
      <div class="pad">${allSquads.filter(s=>!hiddenSq.has(s.squad)).map(s=>`<div style="padding:13px 0;border-top:1px solid var(--line)">
        <b>${esc(s.squad)}</b><div class="peoplemini">${(bySquad[s.squad]||[]).sort((a,b)=>b.feeAtivo-a.feeAtivo).map(p=>`<span class="pmchip">${avaChurn(p)}${esc(p.name||"—")}</span>`).join("")||'<span style="font-size:12px;color:var(--muted)">sem pessoas vinculadas</span>'}</div></div>`).join("")}</div></div>
  </div>`;
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
  $("teamfilterwrap").style.display=(page==="overview"||page==="person")?"":"none";
  $("periodbar").style.display=(page==="times")?"none":"";
  if(page==="overview")renderOverview();
  else if(page==="person")renderPerson();
  else if(page==="churn")renderChurn();
  else renderTimes();
}
// events
document.addEventListener("click",e=>{
  const nav=e.target.closest(".nav"); if(nav){page=nav.dataset.page;churnView="overview";render();window.scrollTo({top:0});return;}
  const tf=e.target.closest("#tfilter button"); if(tf){team=tf.dataset.team;render();return;}
  const pg=e.target.closest("[data-page-go]"); if(pg){page=pg.dataset.pageGo;render();window.scrollTo({top:0});return;}
  const cop=e.target.closest("[data-churn-open]"); if(cop){churnView=cop.dataset.churnOpen;page="churn";render();window.scrollTo({top:0});return;}
  const cbk=e.target.closest("[data-churn-back]"); if(cbk){churnView="overview";render();window.scrollTo({top:0});return;}
  const cst=e.target.closest("[data-churn-step]"); if(cst){churnStep(+cst.dataset.churnStep);return;}
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
  const ec=e.target.closest("[data-export-cfg]"); if(ec){exportCfg();return;}
  const ic=e.target.closest("[data-import-cfg]"); if(ic){$("cfgfile").click();return;}
  const sm=e.target.closest("[data-save-metas]"); if(sm){const mm=metas();mm.meta=parseFloat($("metaInput").value);mm.sup=parseFloat($("supInput").value);if(!(mm.meta>=0))mm.meta=5;if(!(mm.sup>=0))mm.sup=3;setMetas(mm);showToast("Metas salvas.");render();return;}
  const ts=e.target.closest("[data-toggle-squad]"); if(ts){const mm=metas();mm.hidden=mm.hidden||[];const s=ts.dataset.toggleSquad,i=mm.hidden.indexOf(s);if(i>=0)mm.hidden.splice(i,1);else mm.hidden.push(s);setMetas(mm);render();return;}
});
document.addEventListener("change",e=>{
  if(e.target.id==="df"){dFrom=e.target.value;render();}
  if(e.target.id==="dt"){dTo=e.target.value;render();}
  if(e.target.id==="cfgfile"&&e.target.files[0]){importCfg(e.target.files[0]);e.target.value="";}
});
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
