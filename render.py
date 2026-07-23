# -*- coding: utf-8 -*-
"""Gera o dashboard.html a partir de um model.json (estilo PBD: sidebar escura + accent dourado).
Uso: python render.py [model.json] [saida.html]   |   python render.py --demo"""
import json, os, sys, datetime, random

HERE = os.path.dirname(os.path.abspath(__file__))

def render(model):
    return HTML.replace("__MODEL__", json.dumps(model, ensure_ascii=False))

HTML = r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root{
  --page:#f6f3fc; --side:#1c1030; --side-2:rgba(255,255,255,.09); --side-ink:#f3eefb; --side-muted:#a99cc6;
  --gold:#7c3aed; --gold-2:#6d28d9; --gold-soft:#f1e9fd; --magenta:#7c3aed; --deep:#160b28; --accent:#7c3aed; --side-accent:#b98cf5;
  --panel:#ffffff; --panel-2:#f6f3fc; --ink:#1b1230; --ink-2:#3a3350; --muted:#6a6284; --line:#e9e2f5; --line-2:#dccff0;
  --good:#22c55e; --blue:#3f7bc9; --crit:#e5484d; --high:#f59e0b; --med:#f2b90c; --today:#94a3b8; --gd-ink:#15803d; --hi-ink:#b45309; --cr-ink:#c0392b;
  --shadow-sm:0 1px 2px rgba(60,30,110,.05); --shadow:0 3px 12px rgba(70,35,130,.07);
  --r:15px; --r-sm:11px;
  --sans:"Manrope",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --display:var(--sans);
}
@media (prefers-color-scheme:dark){:root{
  --page:#120e1c; --side:#0d0a16; --side-2:rgba(255,255,255,.08); --side-ink:#f2eefb; --side-muted:#a99cc6;
  --gold:#a67ef0; --gold-2:#b98cf5; --gold-soft:#241a3c; --magenta:#a67ef0; --deep:#160b28; --accent:#a67ef0; --side-accent:#b98cf5;
  --panel:#1a1428; --panel-2:#211934; --ink:#f0ecfa; --ink-2:#cfc7e2; --muted:#9a90b5; --line:#2c2440; --line-2:#392c52;
  --good:#3fbe80; --blue:#5b93da; --crit:#f0635e; --high:#e6a544; --med:#d8b84e; --today:#8a80a5; --gd-ink:#4ade80; --hi-ink:#fbbf24; --cr-ink:#f87171;
  --shadow-sm:0 1px 2px rgba(0,0,0,.4); --shadow:0 10px 30px rgba(0,0,0,.5);
}}
:root[data-theme="light"]{--page:#f6f3fc;--side:#1c1030;--side-2:rgba(255,255,255,.09);--side-ink:#f3eefb;--side-muted:#a99cc6;--gold:#7c3aed;--gold-2:#6d28d9;--gold-soft:#f1e9fd;--magenta:#7c3aed;--deep:#160b28;--accent:#7c3aed;--side-accent:#b98cf5;--panel:#fff;--panel-2:#f6f3fc;--ink:#1b1230;--ink-2:#3a3350;--muted:#6a6284;--line:#e9e2f5;--line-2:#dccff0;--good:#22c55e;--blue:#3f7bc9;--crit:#e5484d;--high:#f59e0b;--med:#f2b90c;--today:#94a3b8;--gd-ink:#15803d;--hi-ink:#b45309;--cr-ink:#c0392b;--shadow-sm:0 1px 2px rgba(60,30,110,.05);--shadow:0 3px 12px rgba(70,35,130,.07);}
:root[data-theme="dark"]{--page:#120e1c;--side:#0d0a16;--side-2:rgba(255,255,255,.08);--side-ink:#f2eefb;--side-muted:#a99cc6;--gold:#a67ef0;--gold-2:#b98cf5;--gold-soft:#241a3c;--magenta:#a67ef0;--deep:#160b28;--accent:#a67ef0;--side-accent:#b98cf5;--panel:#1a1428;--panel-2:#211934;--ink:#f0ecfa;--ink-2:#cfc7e2;--muted:#9a90b5;--line:#2c2440;--line-2:#392c52;--good:#3fbe80;--blue:#5b93da;--crit:#f0635e;--high:#e6a544;--med:#d8b84e;--today:#8a80a5;--gd-ink:#4ade80;--hi-ink:#fbbf24;--cr-ink:#f87171;--shadow-sm:0 1px 2px rgba(0,0,0,.4);--shadow:0 10px 30px rgba(0,0,0,.5);}
*{box-sizing:border-box}
h1,h2,.brand b,.card-h h3,.acard h3,.stat .n,.donut .c b,.banner h2{font-family:var(--display)}
.wrap{font-family:var(--sans);background:var(--page);color:var(--ink);min-height:100vh;padding:0;line-height:1.5;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.app{display:grid;grid-template-columns:86px 1fr;gap:0;max-width:none;margin:0;align-items:start}
@media(max-width:860px){.wrap{padding:0}.app{grid-template-columns:1fr;gap:0}.main{padding:16px}}

/* rail de ícones (Opção B): navegação compacta, rótulos em tooltip */
.side{background:linear-gradient(185deg,#28154a,#160b28);border-radius:0;padding:14px 0;position:sticky;top:0;display:flex;flex-direction:column;align-items:center;gap:6px;min-height:100vh;box-shadow:2px 0 18px rgba(40,20,80,.07)}
@media(max-width:860px){.side{position:static;min-height:0;flex-direction:row;padding:8px 12px;justify-content:center}}
.rbrand{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#8b5cf6,#6d28d9);display:grid;place-items:center;font-family:var(--display);font-weight:800;font-size:16px;color:#fff;margin-bottom:12px}
@media(max-width:860px){.rbrand{margin-bottom:0;margin-right:8px}}
.nav{background:transparent;border:0;width:74px;font-family:inherit;color:var(--side-muted);display:flex;flex-direction:column;align-items:center;gap:5px;padding:9px 2px 8px;border-radius:11px;cursor:pointer;transition:background .12s,color .12s;position:relative}
.nav .ic{display:inline-flex;align-items:center;justify-content:center}
.nav .ic svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.nav .nlbl{font-size:9.5px;font-weight:700;letter-spacing:.02em;line-height:1.15;text-align:center}
.nav:hover{color:#fff;background:var(--side-2)}
.nav[aria-current="true"]{background:rgba(255,255,255,.14);color:#fff}
.nav[aria-current="true"]::before{content:"";position:absolute;left:-6px;top:50%;transform:translateY(-50%);width:3.5px;height:26px;border-radius:3px;background:var(--side-accent)}
@media(max-width:860px){.nav[aria-current="true"]::before{left:50%;top:-6px;transform:translateX(-50%);width:22px;height:3.5px}}
.raildot{position:absolute;top:6px;right:20px;width:8px;height:8px;border-radius:50%;background:#f43f5e;border:2px solid #241447}
.side .sp{flex:1}
/* filtro de time: pílulas claras no topo da página */
#teamfilterwrap{display:flex;min-width:0}
.tfilter{display:flex;flex-direction:row;gap:2px;background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:3px;flex-wrap:wrap}
.tfilter button{display:flex;align-items:center;gap:7px;font-family:inherit;font-size:12px;font-weight:700;color:var(--muted);background:transparent;border:0;border-radius:8px;padding:6px 10px;cursor:pointer}
.tfilter button:hover{color:var(--ink);background:var(--panel-2)}
.tfilter button[aria-pressed="true"]{background:var(--gold);color:#fff}
.tfilter .tdot{width:9px;height:9px;border-radius:3px;flex:none}
.tfilter button[aria-pressed="true"] .tdot{box-shadow:0 0 0 2px rgba(255,255,255,.35)}
.tfilter .tct{font-size:10px;font-weight:700;color:var(--muted);background:var(--panel-2);border-radius:999px;padding:1px 6px;min-width:18px;text-align:center}
.tfilter button[aria-pressed="true"] .tct{color:#fff;background:rgba(255,255,255,.2)}
.gen{font-size:11px;color:var(--muted)}
.themetog{display:flex;flex-direction:column;background:var(--side-2);border-radius:10px;padding:3px;gap:3px;margin-top:6px}
@media(max-width:860px){.themetog{flex-direction:row;margin-top:0;margin-left:8px}}
.themetog button{font-family:inherit;font-size:13px;font-weight:600;color:var(--side-muted);background:transparent;border:0;border-radius:7px;padding:7px 9px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.themetog button[aria-pressed="true"]{background:var(--side-accent);color:#1c1030}

/* main */
.main{display:flex;flex-direction:column;gap:22px;min-width:0;padding:24px 40px 44px;max-width:1380px;margin-inline:auto;width:100%}
.topbar{display:flex;justify-content:space-between;align-items:flex-end;gap:14px;flex-wrap:wrap}
.topctl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.topbar h1{font-size:22px;font-weight:800;margin:0;letter-spacing:-.015em}
.crumbs{display:flex;flex-direction:column;gap:5px;margin:0}
.eyebrow{font-family:var(--sans);font-size:11px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--accent);background:transparent;border:0;padding:0;cursor:pointer;text-align:left}
.eyebrow:hover{opacity:.72}
.pagetitle{font-family:var(--sans);font-size:30px;font-weight:800;letter-spacing:-.022em;line-height:1.04;margin:0;color:var(--ink)}
@media(max-width:860px){.pagetitle{font-size:24px}}
.crumbs .cr{background:transparent;border:0;font:inherit;color:var(--muted);cursor:pointer;padding:0;line-height:1.1}
.crumbs .cr:hover{color:var(--ink)}
.crumbs .sep{color:var(--muted);opacity:.5;font-weight:500;font-size:17px}
.crumbs .cur{color:var(--ink)}
.content{display:grid;grid-template-columns:1fr 310px;gap:22px;align-items:start}
@media(max-width:1080px){.content{grid-template-columns:1fr}}
.col{display:flex;flex-direction:column;gap:20px;min-width:0}

/* banner -> cabecalho de pagina limpo, texto escuro de alto contraste */
.banner{background:transparent;border:0;border-bottom:1px solid var(--line);border-radius:0;padding:0 0 20px;color:var(--ink);display:flex;justify-content:space-between;gap:18px;align-items:flex-start;box-shadow:none;position:static;overflow:visible}
.banner::after{display:none}
.banner .bt{position:relative;z-index:1}
.banner h2{margin:0 0 7px;font-size:23px;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.banner p{margin:0;font-size:13.5px;color:var(--muted);max-width:64ch;line-height:1.55}
.banner p b{color:var(--ink-2);font-weight:700}
.banner .cta{display:flex;gap:9px;margin-top:15px;flex-wrap:wrap}
.banner .cta button{font-family:inherit;font-size:12.5px;font-weight:700;border:1px solid var(--line-2);border-radius:9px;padding:9px 15px;cursor:pointer;background:var(--gold);color:#fff}
.banner .cta button:hover{filter:brightness(1.06)}
.banner .cta button.ghost{background:var(--panel);color:var(--ink);border-color:var(--line-2)}
.banner .cta button.ghost:hover{border-color:var(--accent);color:var(--accent);filter:none}
.avatar{width:48px;height:48px;border-radius:13px;background:var(--gold-soft);display:grid;place-items:center;font-size:16px;font-weight:800;color:var(--gold-2);position:relative;z-index:1;flex:none}

/* stat cells */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:11px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:15px 16px;display:flex;flex-direction:column;gap:7px;box-shadow:var(--shadow-sm)}
.stat .ico{width:32px;height:32px;border-radius:9px;display:grid;place-items:center;background:var(--gold-soft)}
.stat .ico svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;color:var(--gold-2)}
.stat.crit .ico{background:color-mix(in srgb,var(--crit) 12%,transparent)} .stat.crit .ico svg{color:var(--crit)}
.stat .n{font-size:25px;font-weight:800;line-height:1;letter-spacing:-.02em;white-space:nowrap;color:var(--ink)}
.stat .l{font-size:11.5px;color:var(--muted);font-weight:600;line-height:1.3}
.stat.crit .n{color:var(--crit)}

/* card */
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow-sm);overflow:hidden}
.card-h{padding:16px 20px;display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid var(--line)}
.card-h h3{margin:0;font-size:15px;font-weight:800;letter-spacing:-.01em}
.card-h .r{font-size:12px;color:var(--muted);font-weight:600;display:flex;gap:10px;align-items:center}
.linkish{font-family:inherit;font-size:12px;font-weight:700;color:var(--accent);background:transparent;border:0;cursor:pointer;padding:0}
.pad{padding:18px 20px}

/* donut */
.donutwrap{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.donut{width:150px;height:150px;border-radius:50%;flex:none;display:grid;place-items:center;position:relative}
.donut::before{content:"";position:absolute;width:106px;height:106px;background:var(--panel);border-radius:50%}
.donut .c{position:relative;text-align:center}
.donut .c b{font-size:30px;font-weight:800;display:block;line-height:1;color:var(--ink)}
.donut .c span{font-size:11px;color:var(--muted)}
.leg{flex:1;min-width:190px;display:flex;flex-direction:column;gap:12px}
.leg .row{display:grid;grid-template-columns:1fr auto;gap:4px 10px;align-items:center}
.leg .row .nm{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600}
.leg .row .nm .dot{width:10px;height:10px;border-radius:3px}
.leg .row .v{font-size:13px;font-weight:800}
.leg .track{grid-column:1/3;height:6px;border-radius:4px;background:var(--panel-2);overflow:hidden}
.leg .track span{display:block;height:100%;border-radius:4px}

/* activity rail */
.acard{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow-sm);padding:18px 18px}
.acard h3{margin:0 0 4px;font-size:14px;font-weight:800}
.acard .sub{font-size:11.5px;color:var(--muted);margin:0 0 12px}
.arow{display:flex;align-items:center;gap:11px;padding:10px 0;border-top:1px solid var(--line)}
.arow:first-of-type{border-top:0}
.ava{width:37px;height:37px;border-radius:10px;flex:none;display:grid;place-items:center;font-size:12.5px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#6d28d9)}
.ava.E{background:linear-gradient(135deg,#8b5cf6,#6d28d9)} .ava.F{background:linear-gradient(135deg,#a855f7,#7c2fd6)}
.datebadge{width:42px;height:42px;border-radius:10px;background:var(--panel-2);display:grid;place-items:center;text-align:center;flex:none;line-height:1;border:1px solid var(--line)}
.datebadge b{font-size:15px;font-weight:800} .datebadge span{font-size:9px;color:var(--muted);text-transform:uppercase}
.arow .mid{flex:1;min-width:0}
.arow .mid b{font-size:13px;font-weight:700;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.arow .mid span{font-size:11.5px;color:var(--muted)}
.arow .end{font-size:14px;font-weight:800}
.arow .end.crit{color:var(--crit)} .arow .end.good{color:var(--good)}
.minibtn{font-family:inherit;font-size:11px;font-weight:600;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 9px;cursor:pointer}
.minibtn:hover{color:var(--accent);border-color:var(--accent)}

/* people list */
.plist{display:flex;flex-direction:column}
.pitem{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;width:100%;text-align:left;font-family:inherit;background:transparent;border:0;border-top:1px solid var(--line);padding:10px 0;cursor:pointer}
.pitem:first-child{border-top:0}
.pitem:hover .pn b{color:var(--accent)}
.pitem[aria-selected="true"]{background:var(--gold-soft);border-radius:10px;padding-left:10px;padding-right:10px}
.pn{min-width:0}.pn b{font-size:13px;font-weight:700;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pn span{font-size:11px;color:var(--muted)}
.chipn{font-size:11px;font-weight:800;min-width:22px;text-align:center;padding:3px 6px;border-radius:7px;background:var(--panel-2);color:var(--muted)}
.chipn.crit{background:color-mix(in srgb,var(--crit) 13%,transparent);color:var(--crit)}

/* task rows */
.tasks{list-style:none;margin:0;padding:0}
.trow{display:grid;grid-template-columns:3px 1fr auto auto;gap:11px;padding:11px 16px 11px 0;border-top:1px solid var(--line);align-items:center}
.trow:first-child{border-top:0}
.stripe{width:3px;align-self:stretch;border-radius:0 3px 3px 0}
.s-crit{background:var(--crit)}.s-high{background:var(--high)}.s-med{background:var(--med)}.s-today{background:var(--today)}.s-none{background:var(--line-2)}
.tname{font-size:13.5px;font-weight:600;color:var(--ink);text-decoration:none;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tname:hover{color:var(--accent);text-decoration:underline}
.tmeta{display:flex;gap:6px;flex-wrap:wrap;margin-top:5px;align-items:center}
.pill{font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:6px;white-space:nowrap}
.pill.list{background:var(--panel-2);color:var(--muted);border:1px solid var(--line)}
.pill.proj{background:var(--gold-soft);color:var(--gold-2);font-weight:700}
.pill.adi{background:color-mix(in srgb,var(--high) 15%,transparent);color:var(--high);font-weight:700}
.pill.okdone{background:color-mix(in srgb,var(--good) 14%,transparent);color:var(--good);font-weight:700}
.pill.badlate{background:color-mix(in srgb,var(--crit) 13%,transparent);color:var(--crit);font-weight:700}
.s-ok{background:var(--good)}
.pill.status{background:var(--gold-soft);color:var(--gold-2)}
.pill.status.camp{background:var(--panel-2);color:var(--muted);border:1px solid var(--line)}
.pill.warn{background:color-mix(in srgb,var(--high) 14%,transparent);color:var(--high)}
.pill.pr.urgent{color:#fff;background:var(--crit)} .pill.pr.high{color:var(--high);background:color-mix(in srgb,var(--high) 15%,transparent)}
.tright{text-align:right;white-space:nowrap}
.tdays{font-size:14.5px;font-weight:800} .tdays.crit{color:var(--cr-ink)}.tdays.high{color:var(--hi-ink)}.tdays.med{color:var(--hi-ink)}.tdays.today{color:var(--today)}
.tdue{font-size:10.5px;color:var(--muted)}
.closebtn{font-family:inherit;font-size:11px;font-weight:600;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 9px;cursor:pointer;white-space:nowrap}
.closebtn:hover{color:var(--good);border-color:var(--good)}
.empty{padding:26px;text-align:center;color:var(--muted);font-size:13px}

/* comportamento */
.beh{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:640px){.beh{grid-template-columns:1fr}}
.beh h4{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0 0 12px;font-weight:700}
.spark{display:flex;align-items:flex-end;gap:3px;height:70px}
.spark .bar{flex:1;background:var(--gold);border-radius:3px 3px 0 0;min-height:2px;position:relative;opacity:.9}
.sparklbl{font-size:10px;color:var(--muted);margin-top:6px;display:flex;justify-content:space-between}
.brow{display:flex;justify-content:space-between;font-size:12.5px;padding:6px 0;border-bottom:1px solid var(--line)}.brow:last-child{border-bottom:0}.brow b{font-weight:800}
.ranklist .arow .bar-mini{height:6px;border-radius:4px;background:var(--panel-2);overflow:hidden;margin-top:4px}
.foot{margin:8px 2px 0;color:var(--muted);font-size:11.5px;line-height:1.5}
.period{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:9px 14px;box-shadow:var(--shadow-sm);margin-bottom:2px}
.period .plabel{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.ppills{display:inline-flex;background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:3px;gap:2px;flex-wrap:wrap}
.ppills button{font-family:inherit;font-size:12.5px;font-weight:600;color:var(--muted);background:transparent;border:0;border-radius:7px;padding:7px 12px;cursor:pointer;white-space:nowrap;transition:background .12s,color .12s}
.ppills button:hover{color:var(--ink)}
.ppills button[aria-pressed="true"]{background:var(--gold);color:#fff}
.ppills button:focus-visible,.applybtn:focus-visible,.pcustom input:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.pcustom{display:inline-flex;align-items:center;gap:7px;margin-left:auto}
.pcustom input[type=date]{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 9px;color-scheme:light dark}
.pcustom .arw{color:var(--muted);font-size:12px}
.pcustom .applybtn{font-family:inherit;font-size:12px;font-weight:700;color:#fff;background:var(--gold);border:0;border-radius:8px;padding:7px 14px;cursor:pointer}
.pcustom .applybtn:hover{filter:brightness(1.06)}
@media(max-width:620px){.pcustom{margin-left:0}}
.beh-ctrl{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.preset{font-family:inherit;font-size:11.5px;font-weight:600;color:var(--muted);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 10px;cursor:pointer}
.preset[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2);border-color:transparent}
.beh-ctrl input[type=date]{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.applybtn{font-family:inherit;font-size:11.5px;font-weight:700;color:#fff;background:var(--gold);border:0;border-radius:8px;padding:7px 13px;cursor:pointer}
.applybtn:hover{filter:brightness(1.06)}
.ontime{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:22px}
.ontime .pct{font-family:var(--display);font-size:42px;font-weight:800;line-height:1;letter-spacing:-.03em}
.ontime-txt{display:flex;flex-direction:column;gap:2px}
.ontime-txt b{font-size:14px;font-weight:700}.ontime-txt span{font-size:12px;color:var(--muted)}
.otbar{flex:1 1 200px;min-width:180px;height:13px;border-radius:7px;background:var(--panel-2);overflow:hidden;display:flex}
.otbar span{height:100%}.otbar .g{background:var(--good)}.otbar .rd{background:var(--crit)}.otbar .nn{background:var(--line-2)}
.chart-h{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:2px 0 8px;flex-wrap:wrap}
.chart-h h4{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0;font-weight:700}
.lgd{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:6px}
.lgd .d{width:10px;height:10px;border-radius:3px;display:inline-block}.lgd .d.g{background:var(--good)}.lgd .d.rd{background:var(--crit)}
.chart{display:flex;align-items:flex-end;gap:8px;min-height:184px;overflow-x:auto;padding:14px 2px 2px}
.colwrap{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:5px;flex:1;min-width:30px}
.coln{font-size:10.5px;color:var(--muted);font-weight:700}
.bar-col{width:25px;border-radius:6px 6px 4px 4px;overflow:hidden;display:flex;flex-direction:column-reverse;background:var(--panel-2)}
.bar-col .seg{width:100%}.bar-col .seg.ok{background:var(--good)}.bar-col .seg.late{background:var(--crit)}
.collbl{font-size:9.5px;color:var(--muted);white-space:nowrap}
.psum{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr))}
.psum>div{padding:14px 18px;border-right:1px solid var(--line)}
.psum>div:last-child{border-right:0}
.psum>div b{font-family:var(--display);font-size:25px;font-weight:800;display:block;line-height:1;letter-spacing:-.02em}
.psum>div span{font-size:11.5px;color:var(--muted);font-weight:600;margin-top:5px;display:block}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.chip{background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:9px 13px;font-size:11.5px;color:var(--muted);line-height:1.35}
.chip b{display:block;color:var(--ink);font-weight:800;font-size:17px;font-family:var(--display)}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:#241243;color:#f3eefb;padding:11px 16px;border-radius:11px;font-size:13px;font-weight:600;box-shadow:0 12px 34px rgba(20,10,45,.34);display:flex;gap:14px;align-items:center;z-index:60}
.toast button{font-family:inherit;font-weight:800;color:var(--side-accent);background:transparent;border:0;cursor:pointer;font-size:13px}
.toast[hidden]{display:none}
.daterange{display:flex;gap:6px;align-items:center;font-size:12px;color:var(--muted)}
.daterange input{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.stepbtns{display:flex;gap:6px}
.btn{font-family:inherit;font-size:12px;font-weight:600;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:7px 11px;cursor:pointer}
.btn:hover{color:var(--ink);border-color:var(--line-2)}
.teamchip{font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--gold-soft);color:var(--gold-2)}

/* churn */
.cnav{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:2px}
.cbtn{font-family:inherit;font-size:12px;font-weight:600;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:7px 12px;cursor:pointer}
.cbtn:hover{color:var(--ink);border-color:var(--line-2)}
.cbtn[aria-pressed="true"]{background:var(--gold);color:#fff;border-color:transparent}
.cbtn.sec{background:transparent;border-color:transparent;color:var(--muted);padding:7px 8px}
.cbtn.sec:hover{color:var(--accent);background:var(--panel-2)}
.cbtn.sec[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2);border-color:transparent}
.cnav .sp{flex:1}
.cnav .csecwrap{display:inline-flex;gap:2px;align-items:center;padding-left:8px;margin-left:2px;border-left:1px solid var(--line)}
.cbase{display:inline-flex;gap:4px;align-items:center;font-size:11.5px;color:var(--muted);font-weight:600}
.cscope{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:var(--gold-2);background:var(--gold-soft);border:1px solid transparent;border-radius:8px;padding:6px 8px 6px 12px;margin-right:2px}
.cscope .cx{border:0;background:transparent;color:inherit;cursor:pointer;font-weight:800;font-size:13px;line-height:1;padding:0 2px;opacity:.7}
.cscope .cx:hover{opacity:1}
.hmatrix{width:100%;border-collapse:collapse;font-size:12px}
.hmatrix th,.hmatrix td{padding:8px 9px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}
.hmatrix th:first-child,.hmatrix td:first-child{text-align:left;font-weight:800;position:sticky;left:0;background:var(--panel)}
.hmatrix thead th{font-size:10px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);font-weight:700;position:sticky;top:0;background:var(--panel);z-index:1}
.hmatrix tbody tr:hover td{background:var(--panel-2)}
.hcell{font-weight:700;border-radius:6px;padding:3px 6px;display:inline-block;min-width:44px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:11px;align-items:stretch}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:var(--r-sm);padding:16px 18px;box-shadow:var(--shadow-sm);display:flex;flex-direction:column;justify-content:center;min-height:88px;min-width:0}
.kpi .n{font-family:var(--display);font-size:23px;font-weight:800;line-height:1.12;letter-spacing:-.02em;white-space:nowrap;color:var(--ink)}
.kpi .l{font-size:11.5px;color:var(--muted);font-weight:700;margin-top:8px;line-height:1.3}
.kpi .s{font-size:11px;color:var(--muted);margin-top:3px;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.metabar{position:relative;height:11px;border-radius:6px;background:var(--panel-2);margin:9px 0}
.metabar.big{height:17px;border-radius:9px}
.metabar .mfill{position:absolute;left:0;top:0;height:100%;border-radius:6px;transition:width .3s}
.metabar .mtick{position:absolute;top:-3px;width:2px;height:17px;border-radius:2px}
.metabar.big .mtick{top:-4px;height:25px}
.metabar .mtick.sup{background:var(--good)}.metabar .mtick.meta{background:var(--high)}
.metabar .mlbl{position:absolute;top:21px;font-size:9.5px;font-weight:600;color:var(--muted);transform:translateX(-50%);white-space:nowrap}
.metabar.big .mlbl{top:27px}
.zbadge{font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;white-space:nowrap;display:inline-block}
.zbadge.super{background:color-mix(in srgb,var(--good) 20%,transparent);color:var(--gd-ink)}
.zbadge.meta{background:color-mix(in srgb,var(--med) 34%,transparent);color:var(--hi-ink)}
.zbadge.acima{background:color-mix(in srgb,var(--crit) 18%,transparent);color:var(--cr-ink)}
.sqrow{display:grid;grid-template-columns:130px 1fr 82px;gap:16px;align-items:center;padding:16px 0;border-top:1px solid var(--line)}
.sqrow:first-child{border-top:0}
.sqrow .sqn{font-weight:800;font-size:14px}
.sqrow .sqmeta{font-size:11px;color:var(--muted);margin-top:3px}
.sqrow .sqpct{font-family:var(--display);font-size:23px;font-weight:800;text-align:right;line-height:1;letter-spacing:-.02em}
.sqrow .sqpct span{font-size:11px;font-weight:700}
@media(max-width:640px){.sqrow{grid-template-columns:1fr auto;gap:6px 12px}.sqrow .barcell{grid-column:1/3;order:3}}
.ctable{width:100%;border-collapse:collapse;font-size:12.5px}
.ctable th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:700;padding:10px 12px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--panel);z-index:1}
.ctable th.r,.ctable td.r{text-align:right}
.ctable td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
.ctable tr:last-child td{border-bottom:0}
.ctable tbody tr:hover td{background:var(--panel-2)}
.ctable .fee{font-weight:800;white-space:nowrap;font-variant-numeric:tabular-nums}
.ctable .cname{font-weight:700;color:var(--ink);text-decoration:none}
.ctable .cname:hover{color:var(--accent);text-decoration:underline}
.tblwrap{max-height:560px;overflow:auto;border-radius:0 0 var(--r) var(--r)}
.sqtag{font-size:10px;font-weight:700;padding:2px 7px;border-radius:6px;background:var(--panel-2);border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.metaedit{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}
.metaedit label{font-size:12px;font-weight:600;color:var(--muted);display:flex;flex-direction:column;gap:6px}
.metaedit input{font-family:inherit;font-size:16px;font-weight:800;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);border-radius:9px;padding:9px 12px;width:96px}
.metaedit .lancin{font-size:13px;font-weight:600;width:auto;min-width:150px;color-scheme:light dark}
.metaedit select.lancin{cursor:pointer;min-width:120px}
.sqtoggle{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 0;border-top:1px solid var(--line)}
.sqtoggle:first-child{border-top:0}
.switch{font-family:inherit;font-size:11.5px;font-weight:600;border:1px solid var(--line);background:var(--panel-2);color:var(--muted);border-radius:8px;padding:7px 12px;cursor:pointer}
.switch[aria-pressed="true"]{background:var(--gold-soft);color:var(--gold-2);border-color:transparent}
.note{background:var(--panel-2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:13px 16px;font-size:12.5px;color:var(--muted);line-height:1.6}
.note b{color:var(--ink)}
.fbars{display:flex;align-items:flex-end;gap:5px;height:90px;overflow-x:auto;padding-top:8px}
.fbars .fb{flex:1;min-width:14px;background:linear-gradient(180deg,var(--gold),var(--gold-2));border-radius:4px 4px 0 0;min-height:3px;position:relative}
.fbars .fb .ft{position:absolute;top:-16px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--muted);white-space:nowrap}
.peoplemini{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.pmchip{display:flex;align-items:center;gap:7px;background:var(--panel-2);border:1px solid var(--line);border-radius:999px;padding:4px 11px 4px 4px;font-size:11.5px;font-weight:600}

/* --- KPIs com contexto: delta vs mês anterior, anel de meta, sparkline --- */
.delta{display:inline-flex;align-items:center;gap:4px;font-size:10.5px;font-weight:800;padding:2px 8px;border-radius:999px;width:fit-content;white-space:nowrap}
.delta.up{background:color-mix(in srgb,var(--crit) 12%,transparent);color:var(--cr-ink)}
.delta.dn{background:color-mix(in srgb,var(--good) 14%,transparent);color:var(--gd-ink)}
.kspark{margin-top:4px;display:block}
.kpi .delta{margin-top:6px;margin-right:4px}
.kring{display:flex;align-items:center;gap:11px}
.ring{width:46px;height:46px;border-radius:50%;flex:none;display:grid;place-items:center;position:relative}
.ring::before{content:"";position:absolute;width:34px;height:34px;background:var(--panel);border-radius:50%}
/* busca dentro do card + mini avatar de pessoa na tabela */
.tsearch{font-family:inherit;font-size:12px;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);border-radius:8px;padding:6px 10px;min-width:150px}
.tsearch::placeholder{color:var(--muted)}
.avmini{width:21px;height:21px;border-radius:50%;background:var(--gold-soft);color:var(--gold-2);display:inline-grid;place-items:center;font-size:8.5px;font-weight:800;flex:none}
.pcell{display:inline-flex;align-items:center;gap:6px}
.ctable tfoot td{background:var(--panel-2);font-weight:800;border-top:1.5px solid var(--line-2)}

/* --- identificação de usuário (telemetria de uso) --- */
.identov{position:fixed;inset:0;background:rgba(22,11,40,.78);backdrop-filter:blur(3px);z-index:60;display:grid;place-items:center;padding:20px}
.identov[hidden]{display:none}
.identcard{background:var(--panel);border-radius:18px;box-shadow:0 24px 80px rgba(0,0,0,.4);padding:28px 30px;max-width:660px;width:100%;max-height:86vh;overflow:auto}
.identcard h2{font-size:21px;font-weight:800;letter-spacing:-.02em;margin:0 0 6px}
.identcard p{font-size:13px;color:var(--muted);margin:0 0 18px;line-height:1.5}
.identgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.identgrid button{font-family:inherit;display:flex;align-items:center;gap:9px;background:var(--panel-2);border:1px solid var(--line);border-radius:11px;padding:9px 11px;cursor:pointer;text-align:left;font-size:12.5px;font-weight:700;color:var(--ink)}
.identgrid button:hover{border-color:var(--accent);background:var(--gold-soft)}
.identgrid .tm{display:block;font-size:10px;font-weight:600;color:var(--muted)}
/* página Uso */
.uscore{display:inline-flex;align-items:center;gap:7px}
.uscore .bar{width:70px;height:7px;border-radius:5px;background:var(--panel-2);overflow:hidden}
.uscore .bar i{display:block;height:100%;border-radius:5px}
.uscore b{font-size:13px;min-width:24px;text-align:right}
.upill{font-size:10.5px;font-weight:800;padding:2.5px 9px;border-radius:999px;white-space:nowrap}
.upill.g{background:color-mix(in srgb,var(--good) 14%,transparent);color:var(--gd-ink)}
.upill.w{background:color-mix(in srgb,var(--high) 14%,transparent);color:var(--hi-ink)}
.upill.c{background:color-mix(in srgb,var(--crit) 12%,transparent);color:var(--cr-ink)}

/* --- acessibilidade: foco de teclado + alvos de clique --- */
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px}
.nav:focus-visible,.themetog button:focus-visible{outline-color:var(--side-accent)}
.cx{min-width:26px;min-height:26px;display:inline-grid;place-items:center;padding:2px}
.minibtn,.closebtn{min-height:28px}
</style>

<div class="wrap"><div class="app">
  <aside class="side">
    <div class="rbrand" title="Aure Digital · Times">A</div>
    <button class="nav" data-page="overview" aria-current="true"><span class="ic"><svg aria-hidden="true" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></span><span class="nlbl">Visão geral</span></button>
    <button class="nav" data-page="person"><span class="ic"><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.6"/><path d="M5 20c0-3.6 3.2-5.6 7-5.6s7 2 7 5.6"/></svg></span><span class="nlbl">Pessoas</span></button>
    <button class="nav" data-page="churn"><span class="ic"><svg aria-hidden="true" viewBox="0 0 24 24"><polyline points="3 6 10 13 14 9 21 17"/><polyline points="21 12 21 17 16 17"/></svg></span><span class="nlbl">Churn</span><span class="raildot" id="raildot" hidden></span></button>
    <button class="nav" data-page="uso" id="navuso" hidden><span class="ic"><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v4.8l3 1.8"/></svg></span><span class="nlbl">Uso</span></button>
    <div class="sp"></div>
    <button class="nav" data-page="times"><span class="ic"><svg aria-hidden="true" viewBox="0 0 24 24"><line x1="4" y1="8" x2="20" y2="8"/><circle cx="9" cy="8" r="2.4"/><line x1="4" y1="16" x2="20" y2="16"/><circle cx="15" cy="16" r="2.4"/></svg></span><span class="nlbl">Ajustes</span></button>
    <div class="themetog" id="themetog">
      <button data-t="light" aria-pressed="false" title="Tema claro" aria-label="Tema claro">☀</button>
      <button data-t="dark" aria-pressed="false" title="Tema escuro" aria-label="Tema escuro">☾</button>
    </div>
  </aside>

  <main class="main">
    <div class="topbar"><nav class="crumbs" id="ptitle" aria-label="Navegação"></nav>
      <div class="topctl">
        <div id="teamfilterwrap"><div class="tfilter" id="tfilter"><!-- times montados dinamicamente --></div></div>
        <div id="topright"></div>
      </div>
    </div>
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
    <div class="gen" id="gen"></div>
    <div class="foot" id="foot"></div>
  </main>
</div></div>
<div class="identov" id="identov" hidden><div class="identcard">
  <h2>Quem está usando o painel?</h2>
  <p>Acesso restrito aos <b>heads de squad</b>. Escolha seu nome e digite seu PIN — usamos a identificação para entender o uso da ferramenta. Dá para trocar em <b>Ajustes</b>.</p>
  <div class="identgrid" id="identgrid"></div>
</div></div>
<div class="toast" id="toast" hidden><span id="toastmsg"></span><button id="toastundo">Desfazer</button></div>
<input type="file" id="cfgfile" accept="application/json" hidden>

<script>
const MODEL = __MODEL__;
const MEM = {}; MODEL.members.forEach(m=>MEM[m.uid]=m);
const PPBYID = {}; (MODEL.postpones||[]).forEach(p=>{PPBYID[p.id]=p;});
const HKEY="clk_hidden_v1";
let page="overview", team="all", selUid=MODEL.members[0]?.uid, dFrom=MODEL.window.to, dTo=MODEL.window.to;  // abre em "Hoje"
let churnScope="all";      // onde estou no churn: "all" | "sq:NOME" | "pp:UID"
let churnTab="overview";   // qual aba: "overview" | "history" | "projection" | "bonus" | "insights"
let churnBase="fee";       // base de cálculo: "fee" | "var" (Fee + Variável)
let churnYear="all";       // filtro do histórico: "all" | "2025" | "2026" | ...
let churnPmYear=null;      // ano exibido no filtro de meses do churn (default: ano atual)
const $=id=>document.getElementById(id);
const esc=s=>(s==null?"":String(s)).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sev=d=>d>30?"crit":d>7?"high":d>0?"med":"today";
const SEVC={crit:"var(--crit)",high:"var(--high)",med:"var(--med)",today:"var(--today)"};
const initials=n=>n.split(" ").filter(Boolean).slice(0,2).map(x=>x[0]).join("").toUpperCase();
const TEAMGRAD={"E-SCALE":"linear-gradient(135deg,#915fe3,#6f3fd0)","FENIX":"linear-gradient(135deg,#bc3eff,#8f2bcf)",
  "ADFORCE":"linear-gradient(135deg,#3a86c8,#255e9a)","G.O.A.T":"linear-gradient(135deg,#b06bd8,#8a3fc0)",
  "BULLS":"linear-gradient(135deg,#3aa88f,#248069)","COMERCIAL":"linear-gradient(135deg,#d0a24a,#b07f2c)",
  "BACKOFFICE":"linear-gradient(135deg,#7a80d8,#565cc0)"};
const TEAMDOT={"ADFORCE":"#3a86c8","G.O.A.T":"#a259d8","BULLS":"#2fa78d","E-SCALE":"#8a5cf0","FENIX":"#c23dff","COMERCIAL":"#d0a24a","BACKOFFICE":"#7a80d8"};
const TEAMPAL=["#915fe3","#3a86c8","#3aa88f","#d0a24a","#c8506a","#7a80d8","#b06bd8","#5aa06a"];
function teamGrad(t){ if(TEAMGRAD[t])return TEAMGRAD[t];
  let h=0; for(let i=0;i<(t||"").length;i++)h=(h*31+t.charCodeAt(i))>>>0;
  const c=TEAMPAL[h%TEAMPAL.length]; return "linear-gradient(135deg,"+c+","+c+"cc)"; }
function avaHTML(m,cls,style){
  const st=(style?style+";":"")+"background:"+teamGrad(m.team), ini=esc(initials(m.name||""));
  if(m.avatar) return `<span class="${cls}" style="position:relative;overflow:hidden;${st}">${ini}<img src="${esc(m.avatar)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" onerror="this.remove()"></span>`;
  return `<span class="${cls}" style="${st}">${ini}</span>`;
}
const mTeams=m=>(m&&m.teams&&m.teams.length)?m.teams:(m&&m.team?[m.team]:[]);
const hidden=()=>{try{return new Set(JSON.parse(localStorage.getItem(HKEY)||"[]"))}catch(e){return new Set()}};
const setHidden=s=>localStorage.setItem(HKEY,JSON.stringify([...s]));
const hideTask=id=>{const s=hidden();s.add(id);setHidden(s)};
const unhide=id=>{const s=hidden();s.delete(id);setHidden(s)};
const inTeam=uid=>team==="all"||(MEM[uid]&&mTeams(MEM[uid]).includes(team));
const membersInTeam=()=>MODEL.members.filter(m=>team==="all"||mTeams(m).includes(team));

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
function monthEnd(k){const y=+k.slice(0,4),mo=+k.slice(5,7);const last=new Date(y,mo,0).getDate();let e=k+"-"+p2(last);if(e>MODEL.window.to)e=MODEL.window.to;return e;}
function setPreset(p){
  const T=MODEL.window.to, W=MODEL.window.from;
  if(p.slice(0,2)==="m:"){const k=p.slice(2);dFrom=k+"-01";dTo=monthEnd(k);return;}   // mês inteiro (churn)
  if(p==="all"){dFrom=W;dTo=T;}
  else if(p==="hoje"){dFrom=T;dTo=T;}
  else if(p==="ontem"){dFrom=dTo=shiftDays(T,-1);}
  else if(p==="mes"){dFrom=T.slice(0,8)+"01";dTo=T;}
  else{dTo=T;dFrom=shiftDays(T,-parseInt(p));}
  if(dFrom<W)dFrom=W;
}
function activePreset(){
  const T=MODEL.window.to, W=MODEL.window.from;
  if(/^\d{4}-\d{2}-01$/.test(dFrom)&&dTo===monthEnd(dFrom.slice(0,7)))return"m:"+dFrom.slice(0,7);
  if(dFrom===W&&dTo===T)return"all";
  if(dFrom===T&&dTo===T)return"hoje";
  const y=shiftDays(T,-1); if(dFrom===y&&dTo===y)return"ontem";
  if(dFrom===T.slice(0,8)+"01"&&dTo===T)return"mes";
  if(dTo===T&&dFrom===shiftDays(T,-30))return"30";
  if(dTo===T&&dFrom===shiftDays(T,-90))return"90";
  return"";
}
function dayPresetsHTML(){return `<button data-preset="hoje">Hoje</button><button data-preset="ontem">Ontem</button><button data-preset="mes">Este mês</button><button data-preset="30">30 dias</button><button data-preset="90">90 dias</button><button data-preset="all">Tudo</button>`;}
function monthPresetsHTML(){
  const curY=+MODEL.window.to.slice(0,4);
  if(churnPmYear==null)churnPmYear=curY;
  const ys=new Set([curY]); Object.keys((MODEL.churnHistory&&MODEL.churnHistory.meses)||{}).forEach(k=>ys.add(+k.slice(0,4)));
  const years=[...ys].sort((a,b)=>a-b);
  let lastMo=(churnPmYear===curY)?+MODEL.window.to.slice(5,7):12;   // ano atual: até o mês corrente...
  if(churnPmYear===curY){   // ...estendido p/ incluir meses futuros que já têm churn (projeção)
    ((MODEL.churn&&MODEL.churn.projection)||[]).forEach(p=>{const k=p.mes||"";if(k.slice(0,4)==String(curY)){const mo=+k.slice(5,7);if(mo>lastMo)lastMo=mo;}});
  }
  let out=[];
  for(let mo=1;mo<=lastMo;mo++){const k=churnPmYear+"-"+p2(mo);out.push(`<button data-preset="m:${k}">${monthLbl(k)}</button>`);}  // crescente
  out.push('<button data-preset="all">Tudo</button>');
  const yearNav=years.length>1?`<span style="display:inline-flex;gap:2px;margin-right:8px;padding-right:8px;border-right:1px solid var(--line)">${years.map(y=>`<button data-churn-pmyear="${y}" aria-pressed="${y===churnPmYear}">${y}</button>`).join('')}</span>`:'';
  return yearNav+out.join("");
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
  const mal=MODEL.malformed.filter(t=>t.uid==null?team==="all":inTeam(t.uid)).length;   // sem responsável só conta em "Todos"
  const ppl=new Set(od.map(t=>t.uid)).size;
  const sc=segCount(od);
  const donut=donutGrad([{v:sc.crit,color:"var(--crit)"},{v:sc.high,color:"var(--high)"},{v:sc.med,color:"var(--med)"},{v:sc.today,color:"var(--today)"}]);
  const segRows=[["crit","+30 dias",sc.crit],["high","8–30 dias",sc.high],["med","1–7 dias",sc.med],["today","vence hoje",sc.today]];
  const segMax=Math.max(1,sc.crit,sc.high,sc.med,sc.today);
  // ranking
  const byM={};od.forEach(t=>(byM[t.uid]=byM[t.uid]||[]).push(t));
  const rank=Object.entries(byM).map(([u,ts])=>({uid:+u,n:ts.length,c:segCount(ts)})).sort((a,b)=>b.n-a.n);
  const rmax=Math.max(1,...rank.map(r=>r.n));
  // attention people (top overdue) & best on-time  (mal cadastradas ficou só na visão Por pessoa)
  const attention=rank.slice(0,5);
  const best=membersInTeam().map(m=>({m,b:behavior(m.uid)})).filter(x=>x.b.onTime+x.b.late>=3)
    .sort((a,b)=>(b.b.otRate??-1)-(a.b.otRate??-1)).slice(0,4);
  const ppBoard=membersInTeam().map(m=>({m,n:postponeCount(m.uid)})).filter(x=>x.n>0).sort((a,b)=>b.n-a.n).slice(0,5);
  const tb=membersInTeam().reduce((a,m)=>{const bb=behavior(m.uid);a.done+=bb.doneN;a.onTime+=bb.onTime;a.late+=bb.late;a.created+=bb.created;return a;},{done:0,onTime:0,late:0,created:0});
  const tbOt=(tb.onTime+tb.late)?Math.round(tb.onTime/(tb.onTime+tb.late)*100):null;
  const tbOtColor=tbOt==null?"var(--muted)":tbOt>=80?"var(--good)":tbOt>=50?"var(--high)":"var(--crit)";
  const tbPP=membersInTeam().reduce((s,m)=>s+postponeCount(m.uid),0);
  const teamName=team==="all"?"Todos os times":team;

  $("root").innerHTML=`<div class="content"><div class="col">
    <div class="banner"><div class="bt">
      <h2>Acompanhamento — ${teamName}</h2>
      <p>${od.length} tarefas em atraso, sendo ${acao} pendências de ação. ${crit} passaram de 30 dias. ${mal} tarefas mal cadastradas para revisar.</p>
      <div class="cta"><button data-goto-attention>Ver quem precisa de atenção</button><button class="ghost" data-page-go="person">Abrir por pessoa</button></div>
    </div></div>

    <div class="card"><div class="card-h"><h3>Conclusões no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${teamName}</div></div>
      <div class="psum">
        <div><b>${tb.done}</b><span>concluídas</span></div>
        <div><b style="color:${tbOtColor}">${tbOt==null?"—":tbOt+"%"}</b><span>no prazo</span></div>
        <div><b>${tb.created}</b><span>criadas</span></div>
        <div><b style="${tbPP?"color:var(--high)":""}">${tbPP}</b><span>adiamentos (total)</span></div>
      </div></div>

    <div class="stats">
      <div class="stat gold"><div class="ico">${ICON.clock}</div><div class="n">${od.length}</div><div class="l">Em atraso</div></div>
      <div class="stat"><div class="ico">${ICON.list}</div><div class="n">${acao}</div><div class="l">Pendências de ação</div></div>
      <div class="stat crit"><div class="ico">${ICON.alert}</div><div class="n">${crit}</div><div class="l">Atraso +30 dias</div></div>
      <div class="stat"><div class="ico">${ICON.warn}</div><div class="n">${mal}</div><div class="l">Mal cadastradas</div></div>
      <div class="stat"><div class="ico">${ICON.user}</div><div class="n">${ppl}</div><div class="l">Pessoas c/ atraso</div></div>
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
        <div class="end ${r.n>10?'crit':''}">${r.n}</div></button>`;}).join("")||'<div class="empty">Sem atrasos</div>'}</div></div>
  </div>

  <div class="col">
    <div class="acard" id="attentioncard"><h3>Precisam de atenção</h3><p class="sub">Maior volume de atraso</p>
      ${attention.map(r=>`<div class="arow">${avaHTML(MEM[r.uid],"ava","")}
        <div class="mid"><b>${esc(MEM[r.uid].name)}</b><span>${MEM[r.uid].team} · ${r.c.crit} crítica(s)</span></div>
        <button class="minibtn" data-open="${r.uid}">abrir</button></div>`).join("")||'<div class="empty">—</div>'}</div>

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
      <p>${esc(m.role)} · ${mTeams(m).map(t=>`<span class="teamchip">${esc(t)}</span>`).join(" ")}</p>
      <div class="cta"><button data-scroll="odsec">Ver ${od.length} em atraso</button>${mal.length?`<button class="ghost" data-scroll="malsec">${mal.length} mal cadastrada(s)</button>`:""}</div>
    </div>${avaHTML(m,"avatar","")}</div>

    <div class="stats">
      <div class="stat ${crit?'crit':'gold'}"><div class="ico">${ICON.clock}</div><div class="n">${od.length}</div><div class="l">Em atraso${hiddenN?` · ${hiddenN} oculta(s)`:""}</div></div>
      <div class="stat"><div class="ico">${ICON.calendar}</div><div class="n">${td.length}</div><div class="l">Para fazer hoje</div></div>
      <div class="stat"><div class="ico">${ICON.warn}</div><div class="n">${mal.length}</div><div class="l">Mal cadastradas</div></div>
      <div class="stat"><div class="ico">${ICON.check}</div><div class="n" style="color:${otColor}">${b.otRate==null?"—":b.otRate+"%"}</div><div class="l">No prazo</div></div>
      <div class="stat"><div class="ico">${ICON.up}</div><div class="n">${b.doneN}</div><div class="l">Concluídas</div></div>
      <div class="stat"><div class="ico">${ICON.list}</div><div class="n">${b.maxDay}</div><div class="l">Check em lote/dia</div></div>
      <div class="stat"><div class="ico">${ICON.check}</div><div class="n">${b.created}</div><div class="l">Criadas</div></div>
    </div>

    <div class="card" id="odsec"><div class="card-h"><h3>Em atraso</h3><div class="r"><span>${od.length} aberta(s)</span>${hiddenN?`<button class="linkish" id="showhidden">ver ${hiddenN} oculta(s)</button>`:""}</div></div>
      ${od.length?`<ul class="tasks" style="padding:4px 16px 8px">${od.map(t=>taskRow(t,true)).join("")}</ul>`:`<div class="empty">Sem tarefas em atraso</div>`}</div>

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
  // fonte de variável/reduções agora é a PLANILHA (já vem calculada no backend). Sem pending local.
  const C=MODEL.churn||{squads:[],people:[],clients:[],totals:{}}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  const teamOk=s=>team==="all"||s===team;                                     // filtro de time da sidebar vale no churn
  const effScope=(churnScope==="all"&&team!=="all")?("sq:"+team):churnScope;   // sem drill: o time vira escopo de squad p/ as abas
  if(churnTab!=="overview"){
    if(churnTab==="history")return renderChurnHistory(C,m,effScope);
    if(churnTab==="projection")return renderChurnProjection(C,m,hiddenSq,effScope);
    if(churnTab==="bonus")return renderChurnBonus(C,m,hiddenSq,effScope);
    if(churnTab==="insights")return renderChurnInsights(C,m,hiddenSq,effScope);
  }
  if(churnScope.slice(0,3)==="sq:")return renderChurnSquad(churnScope.slice(3),C,m,hiddenSq);
  if(churnScope.slice(0,3)==="pp:")return renderChurnPerson(+churnScope.slice(3),C,m,hiddenSq);
  $("ptitle").textContent="Controle de churn";
  // lançamentos são feitos direto na planilha — aqui só o atalho p/ abrir
  $("topright").innerHTML=`<button class="btn" onclick="window.open('${PLANILHA_URL}','_blank')" title="Os lançamentos de churn, variável e bonificação são feitos na planilha">📄 Abrir planilha</button>`;
  const useVar=churnBase==="var";
  const FA=x=>useVar&&x.feeAtivoVar!=null?x.feeAtivoVar:x.feeAtivo;
  const CP=x=>useVar&&x.churnPctVar!=null?x.churnPctVar:x.churnPct;
  // --- o MÊS selecionado no topo pilota o churn (atribuído pela Data de Saída) ---
  const selMes=(activePreset().slice(0,2)==="m:")?activePreset().slice(2):null;   // null = "Tudo" (todos os meses)
  const mesLbl=selMes?projMesLbl(selMes):"todos os meses";
  const CHURN_GRP=new Set(["aviso","futuro","saiu"]);
  const churnCli=(C.clients||[]).filter(c=>c.saidaMes&&CHURN_GRP.has(c.grp)&&(selMes?c.saidaMes===selMes:true)&&!hiddenSq.has(c.squad)&&teamOk(c.squad));
  const aviBySq={},nAviBySq={},aviByUid={},nByUid={};
  churnCli.forEach(c=>{aviBySq[c.squad]=(aviBySq[c.squad]||0)+c.fee;nAviBySq[c.squad]=(nAviBySq[c.squad]||0)+1;
    new Set([...(c.accountUids||[]),...(c.gestorUids||[])]).forEach(u=>{aviByUid[u]=(aviByUid[u]||0)+c.fee;nByUid[u]=(nByUid[u]||0)+1;});});
  const pctOf=(base,avi)=>(base+avi)?+(avi/(base+avi)*100).toFixed(2):0;
  const squads=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad)&&teamOk(s.squad)).map(s=>{
    const avi=+(aviBySq[s.squad]||0).toFixed(2);
    return Object.assign({},s,{feeAviso:avi,nAviso:nAviBySq[s.squad]||0,
      churnPct:pctOf(s.feeAtivo,avi),churnPctVar:pctOf(s.feeAtivoVar!=null?s.feeAtivoVar:s.feeAtivo,avi)});});
  const tFee=squads.reduce((s,x)=>s+x.feeAtivo,0), tVar=squads.reduce((s,x)=>s+(x.variavel||0),0);
  const tAtv=squads.reduce((s,x)=>s+FA(x),0), tAvi=squads.reduce((s,x)=>s+x.feeAviso,0);
  const tPct=(tAtv+tAvi)?+(tAvi/(tAtv+tAvi)*100).toFixed(2):0, z=zoneOf(tPct,m);
  const nAtivo=squads.reduce((s,x)=>s+x.nAtivo,0), nAviso=squads.reduce((s,x)=>s+x.nAviso,0);
  const avisoClients=churnCli.slice().sort((a,b)=>b.fee-a.fee);
  const saidas=(C.clients||[]).filter(c=>c.grp==="saiu"&&c.churnDate&&inRng(c.churnDate)&&!hiddenSq.has(c.squad)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const perdidoP=saidas.reduce((s,c)=>s+c.fee,0);
  const people=(C.people||[]).filter(p=>(p.squads||[]).some(s=>!hiddenSq.has(s)&&teamOk(s))).map(p=>{
    const avi=+(aviByUid[p.uid]||0).toFixed(2);
    return Object.assign({},p,{feeAviso:avi,nAviso:nByUid[p.uid]||0,
      churnPct:pctOf(p.feeAtivo,avi),churnPctVar:pctOf(p.feeAtivoVar!=null?p.feeAtivoVar:p.feeAtivo,avi)});
  }).filter(p=>(p.nAtivo+p.nAviso)>0).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  const fh=Object.entries(MODEL.feeHistory||{}).filter(([d])=>inRng(d)).sort((a,b)=>a[0]<b[0]?-1:1);
  const fhMax=Math.max(1,...fh.map(([,v])=>v.feeAtivo||0));
  // --- contexto p/ os KPIs: mês anterior (delta) + histórico p/ sparkline + anel de meta ---
  const prevMes=selMes?(mm=>{const y=+mm.slice(0,4),mo=+mm.slice(5,7);return mo===1?(y-1)+"-12":y+"-"+p2(mo-1);})(selMes):null;
  const prevCli=prevMes?(C.clients||[]).filter(c=>c.saidaMes===prevMes&&CHURN_GRP.has(c.grp)&&!hiddenSq.has(c.squad)&&teamOk(c.squad)):[];
  const pAvi=prevCli.reduce((s,c)=>s+c.fee,0), pN=prevCli.length;
  const dAvi=tAvi-pAvi, dN=nAviso-pN, prevLbl=prevMes?projMesLbl(prevMes):"";
  const deltaChip=(v,fmt)=>!prevMes?"":v===0?`<span class="delta dn">= igual a ${prevLbl}</span>`:
    `<span class="delta ${v>0?'up':'dn'}">${v>0?'▲ +':'▼ −'}${fmt(Math.abs(v))} vs ${prevLbl}</span>`;
  const fhAll=Object.entries(MODEL.feeHistory||{}).sort((a,b)=>a[0]<b[0]?-1:1).slice(-30);
  let kspark="";
  if(fhAll.length>1){const vs=fhAll.map(([,v])=>v.feeAtivo||0),mn=Math.min(...vs),mx=Math.max(...vs),rg=(mx-mn)||1;
    const pts=vs.map((v,i)=>`${(i/(vs.length-1)*116).toFixed(1)},${(22-(v-mn)/rg*18).toFixed(1)}`).join(" ");
    kspark=`<svg class="kspark" width="120" height="26" viewBox="0 0 120 26" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="var(--gold)" stroke-width="2"/><circle cx="116" cy="${(22-(vs[vs.length-1]-mn)/rg*18).toFixed(1)}" r="2.6" fill="var(--gold)"/></svg>`;}
  const ringFrac=Math.min(1,tPct/Math.max(m.meta*2,tPct*1.08,.01));
  const ringHTML=`<span class="ring" style="background:conic-gradient(${ZONEC[z]} 0 ${(ringFrac*100).toFixed(1)}%,var(--panel-2) ${(ringFrac*100).toFixed(1)}% 100%)" aria-hidden="true"><b style="position:relative;font-size:10.5px;font-weight:800;color:${ZONEC[z]}">${Math.round(tPct*10)/10}%</b></span>`;
  const squadRow=s=>{const zz=zoneOf(CP(s),m);return `<div class="sqrow" data-churn-open="sq:${esc(s.squad)}" style="cursor:pointer" title="Abrir ${esc(s.squad)}">
    <div><div class="sqn">${esc(s.squad)}</div><div class="sqmeta">${s.nAtivo} ativos · ${s.nAviso} em aviso</div></div>
    <div class="barcell">${attainBar(CP(s),m)}<div style="display:flex;justify-content:space-between;gap:8px;margin-top:5px;font-size:11px;color:var(--muted)">
      <span>${BRL(s.feeAtivo)} fee${s.variavel?` · <span style="color:var(--gold-2)">${BRL(s.variavel)} var</span>`:''}</span><span class="zbadge ${zz}">${ZONEL[zz]}</span><span style="color:var(--crit)">${BRL(s.feeAviso)} aviso</span></div></div>
    <div class="sqpct" style="color:${ZONEC[zz]}">${CP(s)}<span>%</span></div></div>`;};

  $("root").innerHTML=`<div class="col">
    ${churnNav()}
    <div class="banner"><div class="bt">
      <h2>Controle de churn — ${team==="all"?"agência":esc(team)}</h2>
      <p>${BRL(tAtv)} de ${useVar?'fee + variável':'fee ativo'} sob gestão · <b>${BRL(tAvi)}</b> de churn em ${mesLbl} (${nAviso} cliente(s)) — <b>${tPct}%</b> do faturamento. O mês do churn vem da Data de Saída. Troque o mês no topo. Meta ≤ ${m.meta}% · super meta ≤ ${m.sup}%.</p>
    </div></div>
    ${(C.semDataSaida||[]).length?`<div class="note" style="border-left-color:var(--crit)"><b>${C.semDataSaida.length} cliente(s) em status de churn sem Data de Saída</b> — sem a data não dá pra saber em que mês o churn entra, então ficam de fora da conta. Preencha a Data de Saída no ClickUp: ${C.semDataSaida.slice(0,8).map(c=>esc(c.name)+" ("+esc(c.status)+")").join(" · ")}${C.semDataSaida.length>8?" …":""}.</div>`:''}

    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(tFee)}</div><div class="l">Fee ativo</div><div class="s">${nAtivo} clientes</div>${kspark}</div>
      <div class="kpi"><div class="n" style="color:var(--gold-2)">${BRL(tVar)}</div><div class="l">Variável</div><div class="s">comissão do mês</div></div>
      <div class="kpi"><div class="n">${BRL(tFee+tVar)}</div><div class="l">Fee + Variável</div><div class="s">base total</div></div>
      <div class="kpi"><div class="n" style="color:var(--crit)">${BRL(tAvi)}</div><div class="l">Churn de ${mesLbl}</div><div class="s">${nAviso} cliente(s) saindo</div>${deltaChip(dAvi,v=>BRL(v))}${prevMes?` ${deltaChip(dN,v=>v+" cliente(s)")}`:""}</div>
      <div class="kpi"><div class="kring">${ringHTML}<div><div class="n" style="color:${ZONEC[z]};font-size:20px">${tPct}%</div><div class="l">Churn (${useVar?'fee+var':'fee'}) · meta ≤ ${m.meta}%</div><div class="s"><span class="zbadge ${z}">${ZONEL[z]}</span></div></div></div></div>
    </div>

    <div class="card"><div class="card-h"><h3>Atingimento de meta — ${team==="all"?"agência":esc(team)}</h3><div class="r">churn ${tPct}% · meta ≤ ${m.meta}% · super ≤ ${m.sup}%</div></div>
      <div class="pad"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px">
        <b style="font-family:var(--display);font-size:30px;color:${ZONEC[z]}">${tPct}%</b><span class="zbadge ${z}">${ZONEL[z]}</span></div>
        ${attainBar(tPct,m,true)}<div style="height:26px"></div>
        <div class="note">A barra mostra o churn atual contra a <b>super meta (${m.sup}%)</b> e a <b>meta (${m.meta}%)</b>. Quanto <b>menor</b>, melhor. Edite as metas em <b>Times &amp; metas</b>.</div>
      </div></div>

    <div class="card"><div class="card-h"><h3>Por squad</h3><div class="r">${squads.length} squads · clique para abrir</div></div>
      <div class="pad">${squads.map(squadRow).join("")||'<div class="empty">Sem squads para mostrar.</div>'}</div></div>

    <div class="card"><div class="card-h"><h3>Por pessoa</h3><div class="r">carteira (Account + Gestor) · clique para abrir</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Pessoa</th><th>Squad</th><th class="r">Fee ativo</th><th class="r">Variável</th><th class="r">Em aviso</th><th class="r">Churn</th><th style="width:110px">Meta</th></tr></thead>
      <tbody>${people.map(p=>{const zz=zoneOf(CP(p),m);return `<tr data-churn-open="pp:${p.uid}" style="cursor:pointer">
        <td><div style="display:flex;align-items:center;gap:9px">${avaChurn(p)}<span><b>${esc(p.name||"—")}</b><br><span style="font-size:10.5px;color:var(--muted)">${(p.roles||[]).map(r=>r==="Gestor de Tráfego"?"Gestor":r).join(" · ")}</span></span></div></td>
        <td>${(p.squads||[]).map(s=>`<span class="sqtag">${esc(s)}</span>`).join(" ")||"—"}</td>
        <td class="r fee">${BRL(p.feeAtivo)}</td><td class="r fee" style="color:${p.variavel?'var(--gold-2)':'var(--muted)'}">${p.variavel?BRL(p.variavel):"—"}</td><td class="r fee" style="color:${p.feeAviso?'var(--crit)':'var(--muted)'}">${p.feeAviso?BRL(p.feeAviso):"—"}</td>
        <td class="r"><b style="color:${ZONEC[zz]}">${CP(p)}%</b></td><td>${attainBar(CP(p),m)}</td></tr>`;}).join("")||'<tr><td colspan="7" class="empty">Sem pessoas.</td></tr>'}</tbody></table></div></div>

    <div class="card"><div class="card-h"><h3>Churn de ${mesLbl}</h3><div class="r"><span>${avisoClients.length} · ${BRL(tAvi)}</span><input type="search" class="tsearch" id="clisearch" placeholder="filtrar cliente…" aria-label="Filtrar cliente"></div></div>
      ${avisoClients.length?`<div class="tblwrap"><table class="ctable" id="chtbl"><thead><tr><th>Cliente</th><th>Squad</th><th>Status</th><th>Account</th><th>Gestor</th><th class="r">Fee</th></tr></thead>
      <tbody>${avisoClients.map(c=>`<tr data-n="${esc((c.name||"").toLowerCase())}"><td>${c.id?`<a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a>`:`<span class="cname">${esc(c.name)}</span>`}</td>
        <td><span class="sqtag">${esc(c.squad)}</span></td><td>${esc(c.status||"—")}</td>
        <td>${c.account?`<span class="pcell"><span class="avmini">${esc(initials(c.account))}</span>${esc(c.account.split(" ").slice(0,2).join(" "))}</span>`:"—"}</td>
        <td>${c.gestor?`<span class="pcell"><span class="avmini">${esc(initials(c.gestor))}</span>${esc(c.gestor.split(" ").slice(0,2).join(" "))}</span>`:"—"}</td>
        <td class="r fee" style="color:var(--crit)">${BRL(c.fee)}</td></tr>`).join("")}</tbody>
      <tfoot><tr><td colspan="5">Total · ${avisoClients.length} cliente(s)</td><td class="r fee" style="color:var(--crit)">${BRL(tAvi)}</td></tr></tfoot></table></div>`
      :`<div class="empty">Nenhum churn com Data de Saída em ${mesLbl}</div>`}</div>

    <div class="card"><div class="card-h"><h3>Fee ativo ao longo do tempo</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)}</div></div>
      <div class="pad">${fh.length>1?`<div class="fbars">${fh.map(([d,v])=>`<div class="fb" style="height:${Math.max(3,(v.feeAtivo||0)/fhMax*82)}px" title="${fmtBR(d)}: ${BRL(v.feeAtivo||0)}"></div>`).join("")}</div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--muted)"><span>${fmtBR(fh[0][0])}</span><span>${fmtBR(fh[fh.length-1][0])}</span></div>`
      :`<div class="note">O histórico de fee é gravado <b>1×/dia às 23h59</b> e começa a partir de hoje. Em alguns dias esta curva mostra a evolução do faturamento conforme clientes entram e saem.</div>`}</div></div>
  </div>`;
}

/* ---------------- CHURN · MICRO (por squad / por pessoa) ---------------- */
function churnPctCalc(atv,avi){return (atv+avi)?+(avi/(atv+avi)*100).toFixed(2):0;}
// pessoa vinculada ao cliente: usa TODOS os account/gestor (não só o 1o), p/ casar com o ranking
function cIsAcc(c,uid){return (c.accountUids&&c.accountUids.length?c.accountUids:[c.accountUid]).indexOf(uid)>=0;}
function cIsGes(c,uid){return (c.gestorUids&&c.gestorUids.length?c.gestorUids:[c.gestorUid]).indexOf(uid)>=0;}
function cInvolves(c,uid){return cIsAcc(c,uid)||cIsGes(c,uid);}
function projMesLbl(k){return k==="sem-data"?"sem data prevista":monthLbl(k);}
function bigAva(x){const nm=typeof x==="string"?x:((x&&x.name)||"—");const av=(x&&typeof x==="object")?x.avatar:null;const ini=esc(initials(nm));
  if(av)return `<span class="avatar" style="position:relative;overflow:hidden">${ini}<img src="${esc(av)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" onerror="this.remove()"></span>`;
  return `<div class="avatar">${ini}</div>`;}
function squadInitial(s){return esc(((s||"?").trim()[0]||"?").toUpperCase());}

function renderChurnSquad(name,C,m,hiddenSq){
  const squadsVis=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad));
  const s=squadsVis.find(x=>x.squad===name)||(C.squads||[]).find(x=>x.squad===name);
  if(!s){churnScope="all";churnTab="overview";return renderChurn();}
  const cls=(C.clients||[]).filter(c=>c.squad===name);
  const ativos=cls.filter(c=>c.grp==="ativo").sort((a,b)=>b.fee-a.fee);
  const aviso=cls.filter(c=>c.grp==="aviso").sort((a,b)=>b.fee-a.fee);
  const saidas=cls.filter(c=>c.grp==="saiu"&&c.churnDate&&inRng(c.churnDate)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const perdido=saidas.reduce((x,c)=>x+c.fee,0), zz=zoneOf(s.churnPct,m);
  const PBYU={};(C.people||[]).forEach(p=>PBYU[p.uid]=p);
  const pmap={};
  cls.forEach(c=>{
    const addp=(uid,role)=>{if(!uid)return;const p=pmap[uid]||(pmap[uid]={uid,name:(PBYU[uid]&&PBYU[uid].name)||"—",avatar:PBYU[uid]&&PBYU[uid].avatar,feeAtivo:0,feeAviso:0,nAtivo:0,nAviso:0,roles:new Set()});
      p.roles.add(role);if(c.grp==="ativo"){p.feeAtivo+=c.fee;p.nAtivo++;}else if(c.grp==="aviso"){p.feeAviso+=c.fee;p.nAviso++;}};
    (c.accountUids&&c.accountUids.length?c.accountUids:[c.accountUid]).forEach(u=>addp(u,"Account"));
    (c.gestorUids&&c.gestorUids.length?c.gestorUids:[c.gestorUid]).forEach(u=>addp(u,"Gestor de Tráfego"));});
  const ppl=Object.values(pmap).map(p=>({uid:p.uid,name:p.name,avatar:p.avatar,feeAtivo:p.feeAtivo,feeAviso:p.feeAviso,nAtivo:p.nAtivo,nAviso:p.nAviso,roles:[...p.roles],churnPct:churnPctCalc(p.feeAtivo,p.feeAviso)})).filter(p=>p.nAtivo+p.nAviso>0).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  const fh=Object.entries(MODEL.feeHistory||{}).filter(([d])=>inRng(d)).sort((a,b)=>a[0]<b[0]?-1:1).map(([d,v])=>[d,(v.bySquad&&v.bySquad[name])||0]);
  const fhMax=Math.max(1,...fh.map(([,x])=>x));
  $("ptitle").textContent="Churn · "+name;
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-churn-step="-1">↑ Squad ant.</button><button class="btn" data-churn-step="1">Próx. squad ↓</button></div>`;
  const vr=s.feeAtivo>0?(s.variavel||0)/s.feeAtivo:0;   // variável do último mês, rateada por fee
  const cRow=(c,dk)=>`<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td><td>${esc(c.account||"—")}</td><td>${esc(c.gestor||"—")}</td><td class="r fee"${c.grp==="aviso"?' style="color:var(--crit)"':''}>${BRL(c.fee)}</td><td class="r fee" style="color:var(--gold-2)">${BRL(c.fee*vr)}</td><td class="r fee">${BRL(c.fee*(1+vr))}</td>${dk?`<td class="r">${c[dk]?fmtBR(c[dk]):"—"}</td>`:''}</tr>`;
  $("root").innerHTML=`${churnNav('Squad: '+name)}<div class="content"><div class="col">
    <div class="banner"><div class="bt"><h2>${esc(name)}</h2>
      <p>${BRL(s.feeAtivo)} de fee ativo · ${BRL(s.feeAviso)} em aviso (${s.nAviso} cliente(s)) — churn de <b>${s.churnPct}%</b>. Meta ≤ ${m.meta}% · super ≤ ${m.sup}%.</p>
    </div><div class="avatar">${squadInitial(name)}</div></div>
    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(s.feeAtivo)}</div><div class="l">Fee ativo</div><div class="s">${s.nAtivo} clientes</div></div>
      <div class="kpi"><div class="n" style="color:var(--gold-2)">${BRL(s.variavel||0)}</div><div class="l">Variável</div><div class="s">Fee+Var ${BRL(s.feeAtivoVar!=null?s.feeAtivoVar:s.feeAtivo)}</div></div>
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
      ${aviso.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th><th class="r">Aviso</th></tr></thead><tbody>${aviso.map(c=>cRow(c,"aviso")).join("")}</tbody></table></div>`:'<div class="empty">Nenhum cliente em aviso</div>'}</div>
    <div class="card"><div class="card-h"><h3>Clientes ativos</h3><div class="r">${ativos.length} · ${BRL(ativos.reduce((x,c)=>x+c.fee,0))}</div></div>
      ${ativos.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th></tr></thead><tbody>${ativos.map(c=>cRow(c,null)).join("")}</tbody></table></div>`:'<div class="empty">—</div>'}</div>
    <div class="card"><div class="card-h"><h3>Saídas no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${saidas.length} · ${BRL(perdido)}</div></div>
      ${saidas.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Account</th><th>Gestor</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th><th class="r">Saída</th></tr></thead><tbody>${saidas.map(c=>cRow(c,"churnDate")).join("")}</tbody></table></div>`:'<div class="empty">Nenhuma saída nesse período.</div>'}</div>
    <div class="card"><div class="card-h"><h3>Fee ativo do squad ao longo do tempo</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)}</div></div>
      <div class="pad">${fh.length>1?`<div class="fbars">${fh.map(([d,x])=>`<div class="fb" style="height:${Math.max(3,x/fhMax*82)}px" title="${fmtBR(d)}: ${BRL(x)}"></div>`).join("")}</div><div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--muted)"><span>${fmtBR(fh[0][0])}</span><span>${fmtBR(fh[fh.length-1][0])}</span></div>`:'<div class="note">O histórico por squad é gravado 1×/dia às 23h59 e começa a acumular a partir de agora.</div>'}</div></div>
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
  const cls=(C.clients||[]).filter(c=>cInvolves(c,uid)&&!hiddenSq.has(c.squad));
  if(!pref&&!cls.length){churnScope="all";churnTab="overview";return renderChurn();}
  const name=(pref&&pref.name)||(cls[0]&&(cIsAcc(cls[0],uid)?cls[0].account:cls[0].gestor))||"—";
  const ativos=cls.filter(c=>c.grp==="ativo").sort((a,b)=>b.fee-a.fee);
  const aviso=cls.filter(c=>c.grp==="aviso").sort((a,b)=>b.fee-a.fee);
  const saidas=cls.filter(c=>c.grp==="saiu"&&c.churnDate&&inRng(c.churnDate)).sort((a,b)=>a.churnDate<b.churnDate?1:-1);
  const feeAtv=ativos.reduce((x,c)=>x+c.fee,0), feeAvi=aviso.reduce((x,c)=>x+c.fee,0);
  const pct=churnPctCalc(feeAtv,feeAvi), zz=zoneOf(pct,m);
  const roleOf=c=>(cIsAcc(c,uid)&&cIsGes(c,uid))?"Account + Gestor":cIsAcc(c,uid)?"Account":"Gestor";
  const squadsList=[...new Set(cls.map(c=>c.squad))];
  const ratioBySquad={}; (C.squads||[]).forEach(s=>ratioBySquad[s.squad]=s.feeAtivo>0?(s.variavel||0)/s.feeAtivo:0);
  const rOf=c=>ratioBySquad[c.squad]||0;
  let accBase=0,gesBase=0;
  ativos.forEach(c=>{const b=c.fee*(1+rOf(c)); if(cIsAcc(c,uid))accBase+=b; if(cIsGes(c,uid))gesBase+=b;});
  const carteiraVar=accBase+gesBase, bMeta=accBase*0.01*0.65+gesBase*0.01*0.35, bSup=accBase*0.02*0.65+gesBase*0.02*0.35;
  const peopleVis=(C.people||[]).filter(pp=>(pp.nAtivo+pp.nAviso)>0&&(pp.squads||[]).some(x=>!hiddenSq.has(x))).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
  $("ptitle").textContent="Churn · "+name;
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-churn-step="-1">↑ Anterior</button><button class="btn" data-churn-step="1">Próximo ↓</button></div>`;
  const pRow=(c,dk)=>{const r=rOf(c);return `<tr><td><a class="cname" href="https://app.clickup.com/t/${c.id}" target="_blank" rel="noopener">${esc(c.name)}</a></td><td><span class="sqtag">${esc(c.squad)}</span></td><td>${roleOf(c)}</td><td class="r fee"${c.grp==="aviso"?' style="color:var(--crit)"':''}>${BRL(c.fee)}</td><td class="r fee" style="color:var(--gold-2)">${BRL(c.fee*r)}</td><td class="r fee">${BRL(c.fee*(1+r))}</td>${dk?`<td class="r">${c[dk]?fmtBR(c[dk]):"—"}</td>`:''}</tr>`;};
  $("root").innerHTML=`${churnNav('Pessoa: '+name)}<div class="content"><div class="col">
    <div class="banner"><div class="bt"><h2>${esc(name)}</h2>
      <p>Carteira de ${BRL(feeAtv+feeAvi)} · ${BRL(feeAvi)} em aviso — churn de <b>${pct}%</b>. ${squadsList.map(x=>`<span class="teamchip">${esc(x)}</span>`).join(" ")}</p>
    </div>${bigAva(pref||name)}</div>
    <div class="kpis">
      <div class="kpi"><div class="n">${BRL(feeAtv)}</div><div class="l">Fee ativo</div><div class="s">${ativos.length} clientes</div></div>
      <div class="kpi"><div class="n" style="color:var(--gold-2)">${BRL((pref&&pref.variavel)||0)}</div><div class="l">Variável</div><div class="s">Fee+Var ${BRL(feeAtv+((pref&&pref.variavel)||0))}</div></div>
      <div class="kpi"><div class="n" style="color:var(--crit)">${BRL(feeAvi)}</div><div class="l">Fee em aviso</div><div class="s">${aviso.length} clientes</div></div>
      <div class="kpi"><div class="n" style="color:${ZONEC[zz]}">${pct}%</div><div class="l">Churn (carteira)</div><div class="s"><span class="zbadge ${zz}">${ZONEL[zz]}</span></div></div>
      <div class="kpi"><div class="n">${BRL(saidas.reduce((x,c)=>x+c.fee,0))}</div><div class="l">Saídas no período</div><div class="s">${saidas.length} cliente(s)</div></div>
    </div>
    <div class="card"><div class="card-h"><h3>Atingimento de meta — ${esc(name)}</h3><div class="r">churn ${pct}% · meta ≤ ${m.meta}% · super ≤ ${m.sup}%</div></div>
      <div class="pad"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2px"><b style="font-family:var(--display);font-size:30px;color:${ZONEC[zz]}">${pct}%</b><span class="zbadge ${zz}">${ZONEL[zz]}</span></div>${attainBar(pct,m,true)}<div style="height:26px"></div>
        <div class="note">Carteira consolidada como <b>Account</b> e <b>Gestor de Tráfego</b>. Cada cliente conta na carteira do seu Account e do seu Gestor.</div></div></div>
    <div class="card"><div class="card-h"><h3>Bonificação de ${esc(name)}</h3><div class="r">quanto recebe se bater a meta</div></div>
      <div class="pad"><div class="chips">
        <div class="chip"><b style="color:var(--high)">${BRL(bMeta)}</b>se bater a meta 🟡 (1%)</div>
        <div class="chip"><b style="color:var(--good)">${BRL(bSup)}</b>se bater a super meta 🟢 (2%)</div>
        <div class="chip"><b>${BRL(carteiraVar)}</b>carteira Fee + Variável (ativa)</div>
      </div><div class="note">Bônus = 1% (meta) ou 2% (super meta) da carteira <b>Fee + Variável</b>. Você recebe <b>65%</b> onde é Account e <b>35%</b> onde é Gestor. Depende do churn do seu squad no mês.</div></div></div>
    <div class="card"><div class="card-h"><h3>Clientes em aviso</h3><div class="r">${aviso.length} · ${BRL(feeAvi)}</div></div>
      ${aviso.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th><th class="r">Aviso</th></tr></thead><tbody>${aviso.map(c=>pRow(c,"aviso")).join("")}</tbody></table></div>`:'<div class="empty">Nenhum cliente em aviso</div>'}</div>
    <div class="card"><div class="card-h"><h3>Clientes ativos</h3><div class="r">${ativos.length} · ${BRL(feeAtv)}</div></div>
      ${ativos.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th></tr></thead><tbody>${ativos.map(c=>pRow(c,null)).join("")}</tbody></table></div>`:'<div class="empty">—</div>'}</div>
    <div class="card"><div class="card-h"><h3>Saídas no período</h3><div class="r">${fmtBR(dFrom)} → ${fmtBR(dTo)} · ${saidas.length}</div></div>
      ${saidas.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th>Papel</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Fee+Var</th><th class="r">Saída</th></tr></thead><tbody>${saidas.map(c=>pRow(c,"churnDate")).join("")}</tbody></table></div>`:'<div class="empty">Nenhuma saída nesse período.</div>'}</div>
  </div>
  <div class="col"><div class="acard"><h3>Pessoas</h3><p class="sub">${peopleVis.length} · clique para abrir</p>
    <div class="plist">${peopleVis.map(x=>{const xz=zoneOf(x.churnPct,m);return `<button class="pitem" data-churn-open="pp:${x.uid}" aria-selected="${x.uid===uid}">
      ${avaChurn(x)}
      <span class="pn"><b>${esc(x.name||"—")}</b><span>${(x.squads||[]).join(", ")||"—"}</span></span>
      <span class="chipn" style="color:${ZONEC[xz]}">${x.churnPct}<span style="font-size:9px">%</span></span></button>`;}).join("")}</div></div></div></div>`;
}

function churnStep(d){
  const C=MODEL.churn||{}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  if(churnScope.slice(0,3)==="sq:"){
    const list=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad));
    const i=list.findIndex(s=>s.squad===churnScope.slice(3));
    if(i>=0&&list.length)churnScope="sq:"+list[(i+d+list.length)%list.length].squad;
  }else if(churnScope.slice(0,3)==="pp:"){
    const list=(C.people||[]).filter(pp=>(pp.nAtivo+pp.nAviso)>0&&(pp.squads||[]).some(s=>!hiddenSq.has(s))).sort((a,b)=>b.churnPct-a.churnPct||b.feeAviso-a.feeAviso);
    const uid=+churnScope.slice(3), i=list.findIndex(pp=>pp.uid===uid);
    if(i>=0&&list.length)churnScope="pp:"+list[(i+d+list.length)%list.length].uid;
  }
  render();window.scrollTo({top:0});
}

/* ---------------- CHURN · sub-navegação + Histórico / Projeção / Bonificação ---------------- */
const MLBL=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const monthLbl=k=>{const a=k.split('-');return MLBL[+a[1]-1]+'/'+a[0].slice(2);};
function scopeLabel(scope,C){
  if(scope.slice(0,3)==="sq:")return "Squad: "+scope.slice(3);
  if(scope.slice(0,3)==="pp:"){const p=(C.people||[]).find(x=>x.uid===+scope.slice(3));return "Pessoa: "+((p&&p.name)||"—");}
  return "";
}
function churnNav(label){
  const T=(k,l)=>`<button class="cbtn" data-churn-tab="${k}" aria-pressed="${churnTab===k}">${l}</button>`;
  const S=(k,l)=>`<button class="cbtn sec" data-churn-tab="${k}" aria-pressed="${churnTab===k}">${l}</button>`;
  const showBase=(churnTab==="insights")||(churnTab==="overview"&&churnScope==="all");
  const base=!showBase?'':`<span class="cbase">Base:</span>
    <button class="cbtn" data-churn-base="fee" aria-pressed="${churnBase==='fee'}">Fee</button>
    <button class="cbtn" data-churn-base="var" aria-pressed="${churnBase==='var'}">Fee + Variável</button>`;
  const chip=label?`<span class="cscope">${esc(label)}<button class="cx" data-churn-back title="Ver a agência toda">✕</button></span>`:'';
  return `<div class="cnav">${chip}${T('overview','Resumo')}${T('history','Histórico')}${T('projection','Projeção')}${T('bonus','Bonificação')}<span class="csecwrap">${S('insights','Insights')}</span><span class="sp"></span>${base}</div>`;
}

function renderChurnHistory(C,m,scope){
  $("ptitle").textContent="Churn · Histórico";
  $("topright").innerHTML="";
  const H=MODEL.churnHistory||{}; const allMeses=Object.keys(H.meses||{}).sort();
  const anos=[...new Set(allMeses.map(k=>k.slice(0,4)))];
  const meses=churnYear==="all"?allMeses:allMeses.filter(k=>k.startsWith(churnYear));
  const allSquads=(H.squads||["TOTAL"]).filter(s=>s!=="—");
  const curMes=(MODEL.window&&MODEL.window.to||"").slice(0,7);
  const zc=v=>v==null?'var(--muted)':v<=m.sup?'var(--good)':v<=m.meta?'var(--high)':'var(--crit)';
  const cell=v=>v==null?'<span style="color:var(--muted)">—</span>':`<span class="hcell" style="background:color-mix(in srgb,${zc(v)} 16%,transparent);color:${zc(v)}">${v.toFixed(1).replace('.',',')}%</span>`;
  const squadSeries=s=>(k=>H.meses&&H.meses[k]?(H.meses[k][s]??null):null);
  // define as linhas conforme o escopo — a 1a linha é a "principal" (vira o gráfico)
  let rows=[], primaryLabel="agência (TOTAL)", scopedMissing=false, isPerson=false, personNote=false;
  if(scope.slice(0,3)==="pp:"){
    isPerson=true;
    const p=(C.people||[]).find(x=>x.uid===+scope.slice(3));
    const pUid=String(p?p.uid:scope.slice(3)), pName=(p&&p.name)||"pessoa";
    const pLive=p?p.churnPct:null;   // churn real da pessoa no mês corrente (ao vivo)
    const pSquads=allSquads.filter(s=>p&&(p.squads||[]).includes(s));
    // série da PESSOA: mês corrente = valor ao vivo; meses passados = histórico por pessoa (— se não houver)
    const personSeries=k=>(k===curMes&&pLive!=null)?pLive:((H.pessoas&&H.pessoas[k])?(H.pessoas[k][pUid]??null):null);
    rows.push({label:pName,series:personSeries,me:true});
    pSquads.forEach(s=>rows.push({label:s+" · squad",series:squadSeries(s)}));
    rows.push({label:"TOTAL agência",series:squadSeries("TOTAL")});
    primaryLabel=pName; personNote=true;
  }else if(scope.slice(0,3)==="sq:"){
    const sn=scope.slice(3); primaryLabel=sn;
    if(allSquads.includes(sn)){rows.push({label:sn,series:squadSeries(sn)});rows.push({label:"TOTAL",series:squadSeries("TOTAL")});}
    else{rows.push({label:"TOTAL",series:squadSeries("TOTAL")});scopedMissing=true;}
  }else{
    allSquads.filter(s=>s!=="TOTAL").forEach(s=>rows.push({label:s,series:squadSeries(s)}));
    rows.push({label:"TOTAL",series:squadSeries("TOTAL")});
  }
  const primary=rows[0]||{label:"TOTAL",series:squadSeries("TOTAL")};
  const totVals=meses.map(k=>[k,primary.series(k)]).filter(([,v])=>v!=null);
  const maxV=Math.max(m.meta*1.5,...totVals.map(([,v])=>v),8);
  const batidas=row=>{let hit=0,tot=0;meses.forEach(k=>{const v=row.series(k);if(v!=null){tot++;if(v<=m.meta)hit++;}});return tot?hit+'/'+tot:'—';};
  const yrBtn=(y,l)=>`<button class="cbtn" data-churn-year="${y}" aria-pressed="${churnYear===y}">${l}</button>`;
  const hasData=meses.length>0;
  $("root").innerHTML=`<div class="col">
    ${churnNav(scopeLabel(scope,C))}
    <div class="banner"><div class="bt"><h2>Histórico de churn${scope!=="all"?' — '+esc(primaryLabel):''}</h2>
      <p>Churn % por mês. Verde ≤ super (${m.sup}%) · amarelo ≤ meta (${m.meta}%) · vermelho acima.</p>
      <div class="cta" style="gap:6px">${yrBtn('all','Todos')}${anos.map(y=>yrBtn(y,y)).join('')}</div></div><div class="avatar">📚</div></div>
    ${personNote?`<div class="note">Série do churn <b>da pessoa</b> (não do squad). O mês corrente vem ao vivo da carteira dela; meses anteriores só existem de <b>${monthLbl(curMes)}</b> em diante — antes o painel guardava histórico só por squad, então aparecem como <b>—</b>. A linha do squad fica logo abaixo, como contexto.</div>`:''}
    ${scopedMissing?`<div class="card"><div class="pad"><div class="note"><b>${esc(primaryLabel)}</b> ainda não tem série histórica (a planilha base importada tinha só ADFORCE, G.O.A.T, BULLS e E-SCALE). A partir de agora o painel grava o churn deste squad a cada fechamento mensal.</div></div></div>`:(!hasData?'<div class="note">Sem histórico ainda.</div>':`
    <div class="card"><div class="card-h"><h3>Evolução — ${esc(primaryLabel)}</h3><div class="r">${monthLbl(meses[0])} → ${monthLbl(meses[meses.length-1])}</div></div>
      <div class="pad">${totVals.length?`<div class="chart" style="min-height:150px">${totVals.map(([k,v])=>`<div class="colwrap"><div class="coln">${v.toFixed(1).replace('.',',')}</div><div class="bar-col" style="height:${Math.max(4,v/maxV*130)}px;background:transparent"><div class="seg" style="flex:1;background:${zc(v)}"></div></div><div class="collbl">${monthLbl(k)}</div></div>`).join('')}</div>`:'<div class="empty">Ainda sem meses com dado para esta série.</div>'}
        <div class="note">Cada barra é o churn no mês. Cor pela zona de meta (super ${m.sup}% / meta ${m.meta}%).</div></div></div>
    <div class="card"><div class="card-h"><h3>Matriz churn % — ${isPerson?'pessoa e squad':'squad'} × mês</h3><div class="r">meta batidas na última coluna</div></div>
      <div class="tblwrap"><table class="hmatrix"><thead><tr><th>${isPerson?'Linha':'Squad'}</th>${meses.map(k=>`<th>${monthLbl(k)}</th>`).join('')}<th>Batidas</th></tr></thead>
      <tbody>${rows.map(r=>`<tr${r.me?' style="background:color-mix(in srgb,var(--brand) 8%,transparent)"':''}><td>${r.me?'<b>':''}${esc(r.label)}${r.me?'</b>':''}</td>${meses.map(k=>`<td>${cell(r.series(k))}</td>`).join('')}<td><b>${batidas(r)}</b></td></tr>`).join('')}</tbody></table></div></div>`)}
  </div>`;
}

function renderChurnProjection(C,m,hiddenSq,scope){
  $("ptitle").textContent="Churn · Projeção";
  $("topright").innerHTML="";
  const sqName=scope.slice(0,3)==="sq:"?scope.slice(3):null, uid=scope.slice(0,3)==="pp:"?+scope.slice(3):null;
  const inScope=c=>!hiddenSq.has(c.squad)&&(!sqName||c.squad===sqName)&&(uid==null||cInvolves(c,uid));
  const proj=(C.projection||[]).map(p=>{const cl=(p.clients||[]).filter(inScope);return {mes:p.mes,clients:cl,n:cl.length,fee:cl.reduce((s,c)=>s+c.fee,0)};}).filter(p=>p.n);
  const totalN=proj.reduce((s,p)=>s+p.n,0), totalFee=proj.reduce((s,p)=>s+p.fee,0);
  $("root").innerHTML=`<div class="col">
    ${churnNav(scopeLabel(scope,C))}
    <div class="banner"><div class="bt"><h2>Projeção de churn${scope!=="all"?' — '+esc(scopeLabel(scope,C).replace(/^(Squad|Pessoa): /,'')):''}</h2>
      <p>Cada cliente em churn entra no mês da sua <b>Data de Saída</b>. Projeção: <b>${totalN}</b> cliente(s) · <b>${BRL(totalFee)}</b> saindo do mês atual em diante.</p></div></div>
    <div class="kpis">${proj.map(p=>`<div class="kpi"><div class="n" style="color:var(--crit)">${p.n}</div><div class="l">Churn projetado · ${projMesLbl(p.mes)}</div><div class="s">${BRL(p.fee)}</div></div>`).join('')||'<div class="kpi"><div class="n">0</div><div class="l">Nada projetado</div><div class="s">Sem clientes em aviso</div></div>'}</div>
    ${proj.map(p=>`<div class="card"><div class="card-h"><h3>Projeção ${projMesLbl(p.mes)}</h3><div class="r">${p.n} cliente(s) · ${BRL(p.fee)}</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Squad</th><th class="r">Fee</th><th class="r">Sai em</th></tr></thead>
      <tbody>${p.clients.slice().sort((a,b)=>b.fee-a.fee).map(c=>`<tr><td>${esc(c.name)}</td><td><span class="sqtag">${esc(c.squad)}</span></td><td class="r fee" style="color:var(--crit)">${BRL(c.fee)}</td><td class="r">${c.churnEm?fmtBR(c.churnEm):'—'}</td></tr>`).join('')}</tbody></table></div></div>`).join('')}
    <div class="note">Modelo: cada cliente em status de churn (aviso, rescisão, pendência adm, inadimplente, finalizado) é atribuído ao <b>mês da sua Data de Saída</b>. Status + Data de Saída definem o churn.</div>
  </div>`;
}

function renderChurnBonus(C,m,hiddenSq,scope){
  const CPV=x=>(x.churnPctVar!=null?x.churnPctVar:x.churnPct);
  $("ptitle").textContent="Churn · Bonificação";
  $("topright").innerHTML="";
  const sqName=scope.slice(0,3)==="sq:"?scope.slice(3):null, uid=scope.slice(0,3)==="pp:"?+scope.slice(3):null;
  const pPerson=uid!=null?(C.people||[]).find(x=>x.uid===uid):null, pSquads=pPerson?new Set(pPerson.squads||[]):null;
  const squads=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad)&&(!sqName||s.squad===sqName)&&(!pSquads||pSquads.has(s.squad)));
  const AC=0.65,GE=0.35, bonusPct=cp=>cp<=m.sup?2:cp<=m.meta?1:0;
  const bb=C.bonusBase||{disponivel:false,bySquad:{},byPerson:{},varBySquad:{},mes:""}, usaSnap=!!bb.disponivel;
  const varSq=bb.varBySquad||{}, r2=x=>Math.round(x*100)/100;
  const feeSquad=s=>(usaSnap&&bb.bySquad[s.squad]!=null)?bb.bySquad[s.squad]:s.feeAtivo;   // fee do fechamento; senão carteira atual
  const baseSquad=s=>feeSquad(s)+(varSq[s.squad]||0);   // base = fee do fechamento + variável do mês anterior (planilha)
  const accGes=p=>usaSnap?(bb.byPerson[String(p.uid)]||{acc:0,ges:0}):{acc:(p.accFee||0),ges:(p.gesFee||0)};
  const temVar=Object.keys(varSq).length>0;
  const baseLbl=(usaSnap?("fee da carteira ativa no fechamento de "+projMesLbl(bb.mes)):"carteira ativa atual (ainda sem fechamento do mês passado)")+(temVar?" + variável de "+projMesLbl(bb.mes):"");
  const rows=squads.map(s=>{const cp=CPV(s),bp=bonusPct(cp),base=baseSquad(s),pool=base*bp/100;
    return {s,cp,bp,base,fee:feeSquad(s),vari:(varSq[s.squad]||0),pool,meta1:base*0.01,sup2:base*0.02};});
  const totPool=rows.reduce((a,r)=>a+r.pool,0), totBase=rows.reduce((a,r)=>a+r.base,0);
  const people=(C.people||[]).filter(p=>(p.nAtivo+p.nAviso)>0&&(p.squads||[]).some(s=>!hiddenSq.has(s))&&(!sqName||(p.squads||[]).includes(sqName))&&(uid==null||p.uid===uid));
  const ppl0=people.map(p=>{const b=accGes(p), fee=(b.acc||0)*AC+(b.ges||0)*GE, roles=[];
    if((b.acc||0)>0)roles.push("Account"); if((b.ges||0)>0)roles.push("Gestor");
    return {uid:p.uid,name:p.name,avatar:p.avatar,squads:p.squads||[],roles,fee};
  }).filter(p=>p.fee>0);
  // rateia a variável do squad (mês anterior) entre as pessoas, proporcional ao fee ponderado de cada uma no squad
  const sqFeeTot={}; ppl0.forEach(p=>(p.squads||[]).forEach(s=>{sqFeeTot[s]=(sqFeeTot[s]||0)+p.fee;}));
  const ppl=ppl0.map(p=>{let v=0;(p.squads||[]).forEach(s=>{if(varSq[s]&&sqFeeTot[s])v+=varSq[s]*(p.fee/sqFeeTot[s]);});
    const carteira=r2(p.fee+v); return Object.assign({},p,{vari:r2(v),carteira,meta:carteira*0.01,sup:carteira*0.02});}).sort((a,b)=>b.sup-a.sup);
  const totMeta=ppl.reduce((a,p)=>a+p.meta,0), totSup=ppl.reduce((a,p)=>a+p.sup,0);
  $("root").innerHTML=`<div class="col">
    ${churnNav(scopeLabel(scope,C))}
    <div class="banner"><div class="bt"><h2>Bonificação</h2>
      <p>Bônus = % da carteira (<b>fee${temVar?' + variável':''}</b>) pela meta de churn: <b>super meta ⇒ 2%</b> · <b>meta ⇒ 1%</b> · acima ⇒ 0%. Account 65% / Gestor 35%.${temVar?' A variável vem da planilha, do mês anterior.':''}</p></div><div class="avatar">🏆</div></div>
    <div class="note"${usaSnap?'':' style="border-left-color:var(--high)"'}>Base do bônus: <b>${baseLbl}</b>, só projetos ativos.${usaSnap?'':' Assim que existir o fechamento do mês passado (o painel tira o retrato sozinho todo dia às 23h59), a base troca automaticamente.'}</div>

    <div class="card"><div class="card-h"><h3>Quanto cada pessoa recebe</h3><div class="r">se bater meta (1%) × super meta (2%)</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Pessoa</th><th>Papel</th><th>Squad</th><th class="r">Base ponderada</th><th class="r">Se meta 🟡 (1%)</th><th class="r">Se super 🟢 (2%)</th></tr></thead>
      <tbody>${ppl.map(p=>`<tr><td><div style="display:flex;align-items:center;gap:9px">${avaChurn(p)}<b>${esc(p.name||"—")}</b></div></td>
        <td>${p.roles.join(" · ")||"—"}</td><td>${(p.squads||[]).map(s=>`<span class="sqtag">${esc(s)}</span>`).join(" ")}</td>
        <td class="r fee">${BRL(p.carteira)}</td><td class="r fee" style="color:var(--high)">${BRL(p.meta)}</td><td class="r fee" style="color:var(--good)">${BRL(p.sup)}</td></tr>`).join("")||'<tr><td colspan="6" class="empty">Sem pessoas.</td></tr>'}
      <tr style="border-top:2px solid var(--line-2)"><td><b>Total</b></td><td></td><td></td><td class="r fee">${BRL(ppl.reduce((a,p)=>a+p.carteira,0))}</td><td class="r fee" style="color:var(--high)"><b>${BRL(totMeta)}</b></td><td class="r fee" style="color:var(--good)"><b>${BRL(totSup)}</b></td></tr></tbody></table></div>
      <div style="padding:10px 16px"><div class="note">Cada cliente entra na carteira do seu <b>Account</b> (65%) e do seu <b>Gestor</b> (35%). "Base ponderada" = fee do fechamento × peso do papel${temVar?' + a variável do mês anterior (planilha), rateada por fee no squad':''}. <b>Se meta</b> = 1% · <b>Se super</b> = 2%. O que cada um leva no mês depende do churn do squad dele.</div></div></div>

    <div class="card"><div class="card-h"><h3>Bônus por squad</h3><div class="r">pela meta batida</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Squad</th><th class="r">Churn</th><th>Faixa</th><th class="r">Base (fechamento)</th><th class="r">Bônus atual</th><th class="r">Se meta 1%</th><th class="r">Se super 2%</th></tr></thead>
      <tbody>${rows.map(r=>{const zz=zoneOf(r.cp,m);return `<tr><td><b>${esc(r.s.squad)}</b></td><td class="r"><b style="color:${ZONEC[zz]}">${r.cp}%</b></td>
        <td><span class="zbadge ${zz}">${r.bp?r.bp+'%':'—'}</span></td><td class="r fee">${BRL(r.base)}</td>
        <td class="r fee"${r.pool?' style="color:var(--good)"':''}>${r.pool?BRL(r.pool):'—'}</td><td class="r" style="color:var(--high)">${BRL(r.meta1)}</td><td class="r" style="color:var(--good)">${BRL(r.sup2)}</td></tr>`;}).join('')}
      <tr style="border-top:2px solid var(--line-2)"><td><b>Total</b></td><td></td><td></td><td class="r fee">${BRL(totBase)}</td><td class="r fee"><b>${BRL(totPool)}</b></td><td class="r">${BRL(totBase*0.01)}</td><td class="r">${BRL(totBase*0.02)}</td></tr></tbody></table></div></div>
    <div class="note">Regra: <b>super meta</b> (churn ≤ ${m.sup}%) ⇒ <b>2%</b> · <b>meta</b> (churn ≤ ${m.meta}%) ⇒ <b>1%</b> · acima ⇒ 0%. Base = ${esc(baseLbl)}. Split Account 65% / Gestor 35%. Metas em <b>Times &amp; metas</b>.</div>
  </div>`;
}

function renderChurnInsights(C,m,hiddenSq,scope){
  $("ptitle").textContent="Churn · Insights";
  $("topright").innerHTML="";
  const sqName=scope.slice(0,3)==="sq:"?scope.slice(3):null, uid=scope.slice(0,3)==="pp:"?+scope.slice(3):null;
  const pPerson=uid!=null?(C.people||[]).find(x=>x.uid===uid):null, pSquads=pPerson?new Set(pPerson.squads||[]):null;
  const squads=(C.squads||[]).filter(s=>s.squad!=="—"&&!hiddenSq.has(s.squad)&&(!sqName||s.squad===sqName)&&(!pSquads||pSquads.has(s.squad)));
  const people=(C.people||[]).filter(p=>(p.nAtivo+p.nAviso)>0&&(p.squads||[]).some(s=>!hiddenSq.has(s))&&(!sqName||(p.squads||[]).includes(sqName))&&(uid==null||p.uid===uid));
  const useVar=churnBase==="var";
  const CPV=x=>useVar&&x.churnPctVar!=null?x.churnPctVar:x.churnPct;   // respeita o toggle Fee/Fee+Variável
  const FAV=x=>useVar&&x.feeAtivoVar!=null?x.feeAtivoVar:x.feeAtivo;
  const bonusPct=cp=>cp<=m.sup?2:cp<=m.meta?1:0;
  const sqSorted=[...squads].sort((a,b)=>CPV(a)-CPV(b));
  const best=sqSorted[0], worst=sqSorted[sqSorted.length-1];
  const nSuper=squads.filter(s=>CPV(s)<=m.sup).length, nMeta=squads.filter(s=>CPV(s)>m.sup&&CPV(s)<=m.meta).length, nFora=squads.filter(s=>CPV(s)>m.meta).length;
  const tAtv=squads.reduce((a,s)=>a+s.feeAtivo,0), tAvi=squads.reduce((a,s)=>a+s.feeAviso,0), tVar=squads.reduce((a,s)=>a+(s.variavel||0),0);
  const tPct=(tAtv+tVar+tAvi)?+(tAvi/(tAtv+tVar+tAvi)*100).toFixed(2):0;
  const projList=(C.projection||[]).map(p=>{const cl=(p.clients||[]).filter(c=>!hiddenSq.has(c.squad)&&(!sqName||c.squad===sqName)&&(uid==null||cInvolves(c,uid)));return {mes:p.mes,n:cl.length,fee:cl.reduce((s,c)=>s+c.fee,0)};}).filter(p=>p.n);
  const proj=projList[0];
  const bigCart=[...people].sort((a,b)=>FAV(b)-FAV(a))[0];
  const avisoBig=(C.clients||[]).filter(c=>c.grp==="aviso"&&!hiddenSq.has(c.squad)&&(!sqName||c.squad===sqName)&&(uid==null||cInvolves(c,uid))).sort((a,b)=>b.fee-a.fee)[0];
  const bonusPot=squads.reduce((a,s)=>a+FAV(s)*0.02,0);   // se todos batessem super meta
  const rk=[...people].sort((a,b)=>CPV(a)-CPV(b)||FAV(b)-FAV(a));
  const medal=i=>i===0?"🥇":i===1?"🥈":i===2?"🥉":`<span style="color:var(--muted)">${i+1}º</span>`;
  const bySquadBest=squads.map(s=>{const ppl=people.filter(p=>(p.squads||[]).includes(s.squad)).sort((a,b)=>CPV(a)-CPV(b));return {s,best:ppl[0]};});
  const insight=(ic,val,lbl,color)=>`<div class="kpi"><div class="n" style="${color?`color:${color}`:''};font-size:20px">${val}</div><div class="l">${lbl}</div></div>`;
  $("root").innerHTML=`<div class="col">
    ${churnNav(scopeLabel(scope,C))}
    <div class="banner"><div class="bt"><h2>Insights & Ranking</h2>
      <p>Panorama do churn da agência: quem está batendo meta, melhores e piores squads, faturamento em risco e projeção. Base ${churnBase==="var"?'Fee + Variável':'Fee'}.</p></div><div class="avatar">💡</div></div>
    <div class="kpis">
      ${best?insight('🏆',esc(best.squad),`Melhor squad · ${CPV(best)}%`,'var(--good)'):''}
      ${worst?insight('⚠️',esc(worst.squad),`Precisa atenção · ${CPV(worst)}%`,'var(--crit)'):''}
      ${insight('✅',`${nSuper+nMeta}/${squads.length}`,`Squads na meta (${nSuper} super)`,'var(--gold-2)')}
      ${insight('💸',BRL(tAvi),`Em risco · ${tPct}% churn`,'var(--crit)')}
      ${insight('📅',proj?`${proj.n}`:'0',`Churn projetado ${proj?projMesLbl(proj.mes):'—'}`,'var(--high)')}
      ${bigCart?insight('👑',esc((bigCart.name||'—').split(' ')[0]),`Maior carteira · ${BRL(FAV(bigCart))}`,''):''}
    </div>

    <div class="card"><div class="card-h"><h3>Ranking geral — quem está batendo meta</h3><div class="r">${rk.length} pessoas · menor churn primeiro</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>#</th><th>Pessoa</th><th>Squad</th><th class="r">Carteira</th><th class="r">Churn</th><th>Situação</th></tr></thead>
      <tbody>${rk.map((p,i)=>{const zz=zoneOf(CPV(p),m);return `<tr data-churn-open="pp:${p.uid}" style="cursor:pointer"><td style="font-weight:800;font-size:15px">${medal(i)}</td>
        <td><div style="display:flex;align-items:center;gap:9px">${avaChurn(p)}<b>${esc(p.name||"—")}</b></div></td>
        <td>${(p.squads||[]).map(s=>`<span class="sqtag">${esc(s)}</span>`).join(" ")}</td>
        <td class="r fee">${BRL(FAV(p))}</td><td class="r"><b style="color:${ZONEC[zz]}">${CPV(p)}%</b></td>
        <td><span class="zbadge ${zz}">${ZONEL[zz]}</span></td></tr>`;}).join("")||'<tr><td colspan="6" class="empty">Sem pessoas.</td></tr>'}</tbody></table></div></div>

    <div class="card"><div class="card-h"><h3>Ranking por squad</h3><div class="r">menor churn primeiro</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>#</th><th>Squad</th><th class="r">Fee</th><th class="r">Variável</th><th class="r">Churn</th><th>Faixa bônus</th><th>Situação</th></tr></thead>
      <tbody>${sqSorted.map((s,i)=>{const zz=zoneOf(CPV(s),m),bp=bonusPct(CPV(s));return `<tr data-churn-open="sq:${esc(s.squad)}" style="cursor:pointer"><td style="font-weight:800;font-size:15px">${medal(i)}</td>
        <td><b>${esc(s.squad)}</b></td><td class="r fee">${BRL(s.feeAtivo)}</td><td class="r fee" style="color:var(--gold-2)">${BRL(s.variavel||0)}</td>
        <td class="r"><b style="color:${ZONEC[zz]}">${CPV(s)}%</b></td><td><span class="zbadge ${zz}">${bp?bp+'%':'—'}</span></td><td><span class="zbadge ${zz}">${ZONEL[zz]}</span></td></tr>`;}).join("")}</tbody></table></div></div>

    <div class="card"><div class="card-h"><h3>Destaque de cada time</h3><div class="r">menor churn por squad</div></div>
      <div class="pad"><div class="peoplemini" style="gap:12px">${bySquadBest.filter(x=>x.best).map(x=>`<span class="pmchip" style="padding:8px 14px 8px 6px">${avaChurn(x.best)}<span><b style="display:block">${esc((x.best.name||'—'))}</b><span style="font-size:10.5px;color:var(--muted)">${esc(x.s.squad)} · ${CPV(x.best)}%</span></span></span>`).join("")||'<span style="color:var(--muted)">—</span>'}</div></div></div>

    <div class="card"><div class="card-h"><h3>Insights rápidos</h3></div>
      <div class="pad"><div class="chips">
        <div class="chip"><b>${BRL(bonusPot)}</b>bônus potencial se todos batessem super meta</div>
        <div class="chip"><b style="${nFora?'color:var(--crit)':''}">${nFora}</b>squad(s) acima da meta</div>
        ${avisoBig?`<div class="chip"><b style="color:var(--crit)">${esc(avisoBig.name)}</b>maior cliente em aviso · ${BRL(avisoBig.fee)}</div>`:''}
        ${proj?`<div class="chip"><b>${BRL(proj.fee)}</b>fee saindo em ${projMesLbl(proj.mes)} (projeção)</div>`:''}
        <div class="chip"><b>${BRL(tVar)}</b>variável do mês (todas as carteiras)</div>
      </div></div></div>
  </div>`;
}

/* ---------------- CHURN · LANÇAMENTOS (redução + variável, avulsos) ---------------- */
const LKEY="clk_lanc_v1";
function lancLocal(){try{return Object.assign({variaveis:[],reducoes:[]},JSON.parse(localStorage.getItem(LKEY)||"{}"))}catch(e){return{variaveis:[],reducoes:[]}}}
function setLancLocal(l){localStorage.setItem(LKEY,JSON.stringify(l))}
/* ---- Salvar automático no GitHub (o painel commita sozinho o lancamentos.json) ---- */
const GHKEY="clk_gh_token_v1";
const GH_OWNER="felipeauredigital", GH_REPO="painel-time", GH_BRANCH="main", GH_PATH="data/lancamentos.json";
function ghToken(){return (localStorage.getItem(GHKEY)||"").trim();}
function setGhToken(t){t?localStorage.setItem(GHKEY,t.trim()):localStorage.removeItem(GHKEY);}
function newLancId(){return Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,8);}
function b64encU(s){return btoa(unescape(encodeURIComponent(s)));}
function b64decU(b){return decodeURIComponent(escape(atob(String(b).replace(/\n/g,""))));}
// tira do navegador os lançamentos que já entraram no arquivo commitado (dedup por id) — evita contar em dobro
function pruneCommittedLanc(){
  const com=MODEL.lancamentos||{variaveis:[],reducoes:[]}, loc=lancLocal();
  const ids=new Set([...(com.variaveis||[]),...(com.reducoes||[])].map(e=>e&&e.id).filter(Boolean));
  if(!ids.size)return; let ch=false;
  ["variaveis","reducoes"].forEach(k=>{const b=loc[k].length; loc[k]=loc[k].filter(e=>!(e&&e.id&&ids.has(e.id))); if(loc[k].length!==b)ch=true;});
  if(ch)setLancLocal(loc);
}
async function ghApi(method,url,body){
  const r=await fetch(url,{method,headers:{"Authorization":"Bearer "+ghToken(),"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"},body:body?JSON.stringify(body):undefined});
  if(!r.ok){let t="";try{t=(await r.json()).message||"";}catch(e){} throw new Error("GitHub "+r.status+(t?" — "+t:""));}
  return r.json();
}
// lê o arquivo atual no repo, mescla as pendências (por id) que faltam e grava de volta
async function pushLancToGitHub(){
  if(!ghToken())throw new Error("sem token");
  const url="https://api.github.com/repos/"+GH_OWNER+"/"+GH_REPO+"/contents/"+encodeURIComponent(GH_PATH).replace(/%2F/g,"/");
  let cur=null;
  try{cur=await ghApi("GET",url+"?ref="+GH_BRANCH);}catch(e){if(!/GitHub 404/.test(e.message))throw e;}
  let doc={variaveis:[],reducoes:[]};
  if(cur&&cur.content){try{doc=JSON.parse(b64decU(cur.content));}catch(e){}}
  doc.variaveis=doc.variaveis||[]; doc.reducoes=doc.reducoes||[];
  const has=(arr,id)=>arr.some(e=>e&&e.id===id);
  const loc=lancLocal(); let added=0;
  ["variaveis","reducoes"].forEach(k=>loc[k].forEach(e=>{if(e&&e.id&&!has(doc[k],e.id)){doc[k].push(e);added++;}}));
  if(!added)return {added:0};
  doc._doc="Lancamentos avulsos (variaveis=comissao + reducoes=desconto/servico) — data/lancamentos.json. Editado pelo painel.";
  const body={message:"Lancamentos: +"+added+" via painel",content:b64encU(JSON.stringify(doc,null,2)),branch:GH_BRANCH};
  if(cur&&cur.sha)body.sha=cur.sha;
  await ghApi("PUT",url,body);
  return {added};
}
// aplica os lançamentos PENDENTES (localStorage) ao churn ao vivo, para o efeito aparecer na hora
function applyPendingLanc(C){
  const loc=lancLocal(); if(!(loc.reducoes.length||loc.variaveis.length))return C;
  const mes=(MODEL.lancamentos&&MODEL.lancamentos.mesAtual)||MODEL.window.to.slice(0,7);
  const redBy={},varBy={};
  loc.reducoes.forEach(e=>{if((e.mes||mes)===mes)redBy[e.squad]=(redBy[e.squad]||0)+(+e.valor||0);});
  loc.variaveis.forEach(e=>{if((e.mes||mes)===mes)varBy[e.squad]=(varBy[e.squad]||0)+(+e.valor||0);});
  const cp=(atv,avi)=>(atv+avi)?+((avi/(atv+avi))*100).toFixed(2):0, r2=x=>Math.round(x*100)/100;
  const squads=(C.squads||[]).map(s=>{const pr=redBy[s.squad]||0,pv=varBy[s.squad]||0; if(!pr&&!pv)return s;
    const red=(s.reducao||0)+pr, vari=(s.variavel||0)+pv;
    return Object.assign({},s,{reducao:r2(red),variavel:r2(vari),feeAtivoVar:r2(s.feeAtivo+vari),
      churnPct:cp(s.feeAtivo,s.feeAviso+red),churnPctVar:cp(s.feeAtivo+vari,s.feeAviso+red)});});
  const tAtv=squads.reduce((a,s)=>a+s.feeAtivo,0),tAvi=squads.reduce((a,s)=>a+s.feeAviso,0),
        tVar=squads.reduce((a,s)=>a+(s.variavel||0),0),tRed=squads.reduce((a,s)=>a+(s.reducao||0),0);
  const totals=Object.assign({},C.totals,{variavel:r2(tVar),reducao:r2(tRed),feeAtivoVar:r2(tAtv+tVar),
    churnPct:cp(tAtv,tAvi+tRed),churnPctVar:cp(tAtv+tVar,tAvi+tRed)});
  return Object.assign({},C,{squads,totals,_pending:loc.reducoes.length+loc.variaveis.length});
}
function addLancFromForm(tipo){
  const l=lancLocal(), mes=(MODEL.lancamentos&&MODEL.lancamentos.mesAtual)||MODEL.window.to.slice(0,7);
  if(tipo==="reducao"){
    const sq=$("redSquad").value, cli=($("redCli").value||"").trim(), val=parseFloat($("redVal").value), mot=($("redMot").value||"").trim(), data=$("redData").value;
    if(!cli||!(val>0)){alert("Preencha o cliente e um valor maior que zero.");return;}
    l.reducoes.push({id:newLancId(),cliente:cli,squad:sq,valor:val,motivo:mot,data:data,mes:(data?data.slice(0,7):mes)});
  }else{
    const sq=$("varSquad").value, cli=($("varCli").value||"").trim(), val=parseFloat($("varVal").value);
    if(!cli||!(val>0)){alert("Preencha o cliente e um valor maior que zero.");return;}
    l.variaveis.push({id:newLancId(),cliente:cli,squad:sq,valor:val,mes:mes});
  }
  setLancLocal(l); render();  // aplica na hora aqui no painel (localStorage)
  if(ghToken()){
    showToast("Salvando no repositório…");
    pushLancToGitHub().then(r=>showToast("✓ Salvo no repositório. Já aplicado aqui na hora; no ar para toda a equipe em ~10 min."))
      .catch(err=>showToast("⚠️ Não salvou no GitHub ("+err.message+"). Ficou pendente neste navegador — confira o token em Salvar automático."));
  }else{
    showToast("Aplicado aqui na hora (pendente). Ligue o Salvar automático (token) para valer para todos sozinho, ou baixe o arquivo.");
  }
}
function exportLanc(){
  const base=MODEL.lancamentos||{variaveis:[],reducoes:[]}, loc=lancLocal();
  const clean=a=>(a||[]).map(e=>{const o=Object.assign({},e);delete o._i;return o;});
  const merged={_doc:"Lancamentos avulsos: variaveis (comissao) + reducoes (desconto/servico). Colocar em data/lancamentos.json.",
    variaveis:[...clean(base.variaveis),...clean(loc.variaveis)],reducoes:[...clean(base.reducoes),...clean(loc.reducoes)]};
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(merged,null,2)],{type:"application/json"}));
  a.download="lancamentos.json";document.body.appendChild(a);a.click();a.remove();
  showToast("Arquivo baixado. Me envie (ou faça commit em data/lancamentos.json) para valer para todos.");
}
const PLANILHA_URL="https://docs.google.com/spreadsheets/d/10M2woH8TCalSE5qqXKZH9sg3JSOqGdPc6zjWwKB8P9g/edit";  // [Controle] Churns e Bonificações
function renderChurnLanc(C,m,hiddenSq){
  $("ptitle").textContent="Churn · Lançamentos";
  $("topright").innerHTML="";
  const L=MODEL.lancamentos||{variaveis:[],reducoes:[],mesAtual:"",mesPrev:""};
  const mes=L.mesAtual||MODEL.window.to.slice(0,7), mesPrev=L.mesPrev||"";
  const red=(L.reducoes||[]).filter(e=>!hiddenSq.has(e.squad)).sort((a,b)=>(a.mes<b.mes?1:-1)||b.valor-a.valor);
  const var_=(L.variaveis||[]).filter(e=>!hiddenSq.has(e.squad)).sort((a,b)=>(a.mes<b.mes?1:-1)||b.valor-a.valor);
  const redMes=red.filter(e=>e.mes===mes), varPrev=var_.filter(e=>e.mes===mesPrev);
  const redRow=e=>`<tr><td><b>${esc(e.cliente||'—')}</b></td><td><span class="sqtag">${esc(e.squad||'—')}</span></td><td>${esc(e.motivo||'—')}</td><td class="r fee" style="color:var(--crit)">${BRL(e.valor||0)}</td><td class="r">${esc(e.mes||'—')}</td></tr>`;
  const varRow=e=>`<tr><td><b>${esc(e.cliente||'—')}</b></td><td><span class="sqtag">${esc(e.squad||'—')}</span></td><td class="r fee" style="color:var(--gold-2)">${BRL(e.valor||0)}</td><td class="r">${esc(e.mes||'—')}</td></tr>`;
  $("root").innerHTML=`<div class="col">
    ${churnNav('')}
    <div class="banner"><div class="bt"><h2>Lançamentos — da planilha</h2>
      <p>Variável e reduções vêm da <b>planilha compartilhada</b>. O time preenche lá; o painel <b>lê sozinho</b> a cada rodada. Esta tela é só espelho (leitura).</p>
      <div class="cta"><button onclick="window.open('${PLANILHA_URL}','_blank')">📄 Abrir a planilha</button></div></div><div class="avatar">📄</div></div>

    <div class="note">Como funciona: <b>Churn</b> (abas "{Time} - Churn") entra no churn do mês da coluna Mês. <b>Variável</b> (abas "{Time} - Variável", coluna Valor da Comissão) entra na <b>meta do mês seguinte</b> — por isso a bonificação de agora usa a variável de <b>${mesPrev?projMesLbl(mesPrev):'—'}</b>. Não precisa baixar nem importar nada.</div>

    <div class="card"><div class="card-h"><h3>Reduções — ${projMesLbl(mes)}</h3><div class="r">aplicadas no churn do mês: ${BRL((C.totals&&C.totals.reducao)||0)}</div></div>
      ${redMes.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Time</th><th>Motivo</th><th class="r">Valor</th><th class="r">Mês</th></tr></thead>
      <tbody>${redMes.map(redRow).join('')}</tbody></table></div>`:'<div class="empty">Nenhuma redução na planilha para este mês.</div>'}</div>

    <div class="card"><div class="card-h"><h3>Variável — ${mesPrev?projMesLbl(mesPrev):'mês anterior'} (vale na meta de ${projMesLbl(mes)})</h3><div class="r">${varPrev.length} lançamento(s)</div></div>
      ${varPrev.length?`<div class="tblwrap"><table class="ctable"><thead><tr><th>Cliente</th><th>Time</th><th class="r">Comissão</th><th class="r">Mês</th></tr></thead>
      <tbody>${varPrev.map(varRow).join('')}</tbody></table></div>`:'<div class="empty">Nenhuma variável na planilha para o mês anterior.</div>'}</div>

    ${(red.length||var_.length)?`<div class="card"><div class="card-h"><h3>Tudo que está na planilha</h3><div class="r">todos os meses · ${red.length} reduções · ${var_.length} variáveis</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Tipo</th><th>Cliente</th><th>Time</th><th class="r">Valor</th><th class="r">Mês</th></tr></thead>
      <tbody>${red.map(e=>`<tr><td><span class="pill">redução</span></td><td>${esc(e.cliente||'—')}</td><td><span class="sqtag">${esc(e.squad)}</span></td><td class="r fee" style="color:var(--crit)">${BRL(e.valor||0)}</td><td class="r">${esc(e.mes)}</td></tr>`).join('')}${var_.map(e=>`<tr><td><span class="pill">variável</span></td><td>${esc(e.cliente||'—')}</td><td><span class="sqtag">${esc(e.squad)}</span></td><td class="r fee" style="color:var(--gold-2)">${BRL(e.valor||0)}</td><td class="r">${esc(e.mes)}</td></tr>`).join('')}</tbody></table></div></div>`:''}
  </div>`;
}

/* ---------------- TIMES & METAS ---------------- */
function renderTimes(){
  $("ptitle").textContent="Times & metas";
  $("topright").innerHTML=`<div class="stepbtns"><button class="btn" data-export-cfg>⭳ Exportar</button><button class="btn" data-import-cfg>⭱ Importar</button></div>`;
  const C=MODEL.churn||{squads:[],people:[]}, m=metas(), hiddenSq=new Set(m.hidden||[]);
  const allSquads=(C.squads||[]).filter(s=>s.squad!=="—");
  const bySquad={};(C.people||[]).forEach(p=>(p.squads||[]).forEach(s=>{(bySquad[s]=bySquad[s]||[]).push(p);}));
  $("root").innerHTML=`<div class="col">
    <div class="note"><b>Como funciona:</b> squads e pessoas vêm automaticamente do ClickUp (campo <b>Squad</b> + <b>Account</b>/<b>Gestor de Tráfego</b> na lista de Empresas). Ao cadastrar um cliente ou trocar alguém de squad no ClickUp, o painel se atualiza sozinho na próxima rodada — não precisa recadastrar aqui. Você edita as <b>metas</b> e escolhe quais squads acompanhar. <b>(Etapa que vamos refinar juntos.)</b></div>

    ${usoOn()?`<div class="card"><div class="card-h"><h3>Identificação</h3><div class="r">usada na medição de uso do painel</div></div>
      <div class="pad" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
        <span style="font-size:13px">${ident()?`Você está identificado como <b>${esc(ident().name)}</b>.`:"Você ainda não se identificou."}</span>
        <button class="btn" data-ident-reset>${ident()?"Trocar usuário":"Identificar-se"}</button>
      </div></div>`:""}

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

const ICON={
  clock:'<svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v4.8l3 1.8"/></svg>',
  list:'<svg aria-hidden="true" viewBox="0 0 24 24"><line x1="8" y1="7" x2="20" y2="7"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="8" y1="17" x2="20" y2="17"/><circle cx="4" cy="7" r=".6"/><circle cx="4" cy="12" r=".6"/><circle cx="4" cy="17" r=".6"/></svg>',
  alert:'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3.5 2.5 20.5h19L12 3.5z"/><line x1="12" y1="10" x2="12" y2="14"/><line x1="12" y1="17" x2="12" y2="17"/></svg>',
  warn:'<svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><line x1="12" y1="7.5" x2="12" y2="13"/><line x1="12" y1="16.5" x2="12" y2="16.5"/></svg>',
  user:'<svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.6"/><path d="M5 20c0-3.6 3.2-5.6 7-5.6s7 2 7 5.6"/></svg>',
  calendar:'<svg aria-hidden="true" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><line x1="3.5" y1="9.5" x2="20.5" y2="9.5"/><line x1="8" y1="3" x2="8" y2="6.5"/><line x1="16" y1="3" x2="16" y2="6.5"/></svg>',
  check:'<svg aria-hidden="true" viewBox="0 0 24 24"><polyline points="4 12.5 9.5 18 20 6.5"/></svg>',
  up:'<svg aria-hidden="true" viewBox="0 0 24 24"><polyline points="3 17 10 10 14 14 21 6"/><polyline points="21 11 21 6 16 6"/></svg>'
};
const CTABLBL={overview:"Resumo",history:"Histórico",projection:"Projeção",bonus:"Bonificação",lanc:"Lançamentos",insights:"Insights"};
function setCrumbs(){
  let el="",ec=null,title="";
  if(page==="overview"){el="Tarefas";ec="overview";title="Visão geral";}
  else if(page==="person"){el="Tarefas";ec="overview";title="Por pessoa";}
  else if(page==="times"){el="Ajustes";title="Times & metas";}
  else if(page==="uso"){el="Adoção";title="Uso do painel";}
  else if(page==="churn"){
    if(churnScope.slice(0,3)==="sq:"){el="Churn";ec="churn";title=churnScope.slice(3);}
    else if(churnScope.slice(0,3)==="pp:"){const u=+churnScope.slice(3);const pe=((MODEL.churn||{}).people||[]).find(x=>x.uid===u);el="Churn";ec="churn";title=pe?pe.name:"Pessoa";}
    else {el="Churn";ec="churn";title=CTABLBL[churnTab]||"Resumo";}
  }
  const eye=ec?`<button class="eyebrow" data-crumb="${ec}">${esc(el)}</button>`:`<span class="eyebrow">${esc(el)}</span>`;
  $("ptitle").innerHTML=eye+`<h1 class="pagetitle">${esc(title)}</h1>`;
}
function render(){
  $("gen").textContent=`Atualizado ${MODEL.generated}`;
  $("foot").innerHTML=`Histórico ${MODEL.window.from} → ${MODEL.window.to}. "✓ Fechar" oculta tarefas já concluídas/cliente que saiu (salvo neste navegador, com desfazer). As datas em "Comportamento" filtram o histórico.`;
  [...$("tfilter").children].forEach(x=>x.setAttribute("aria-pressed",x.dataset.team===team));
  document.querySelectorAll(".nav").forEach(n=>n.setAttribute("aria-current",n.dataset.page===page));
  const _ct=(MODEL.churn||{}).totals||{};                          // alerta no rail: churn acima da meta
  $("raildot").hidden=!((_ct.churnPct||0)>metas().meta);
  const cur=document.documentElement.getAttribute("data-theme");
  [...$("themetog").children].forEach(x=>x.setAttribute("aria-pressed",cur?x.dataset.t===cur:false));
  $("df").value=dFrom; $("dt").value=dTo;
  $("df").min=$("dt").min=MODEL.window.from; $("df").max=$("dt").max=MODEL.window.to;
  $("periodpresets").innerHTML=(page==="churn")?monthPresetsHTML():dayPresetsHTML();   // churn filtra por MÊS
  const apnow=activePreset();
  [...$("periodpresets").children].forEach(x=>{if(x.dataset.preset!=null)x.setAttribute("aria-pressed",x.dataset.preset===apnow);});
  $("teamfilterwrap").style.display=(page==="overview"||page==="person"||page==="churn")?"":"none";
  const churnNoPeriod=(page==="churn"&&(churnTab==="history"||churnTab==="projection"||churnTab==="bonus"));
  $("periodbar").style.display=(page==="times"||page==="uso"||churnNoPeriod)?"none":"";
  $("navuso").hidden=!usoOn()||!(ident()&&ident().adm);   // página Uso: só o admin vê (e ainda pede PIN)
  if(window._lastPage!==page){window._lastPage=page;track("page",page);}
  if(page==="overview")renderOverview();
  else if(page==="person")renderPerson();
  else if(page==="churn")renderChurn();
  else if(page==="uso")renderUso();
  else renderTimes();
  setCrumbs();
}
// events
document.addEventListener("click",e=>{
  const nav=e.target.closest(".nav"); if(nav){page=nav.dataset.page;churnScope="all";churnTab="overview";if(page==="churn"&&activePreset().slice(0,2)!=="m:")setPreset("m:"+MODEL.window.to.slice(0,7));render();window.scrollTo({top:0});return;}
  const cr=e.target.closest("[data-crumb]"); if(cr){const c=cr.dataset.crumb;if(c==="overview")page="overview";else if(c==="person")page="person";else if(c==="churn"){page="churn";churnScope="all";churnTab="overview";}else if(c==="times")page="times";render();window.scrollTo({top:0});return;}
  const tf=e.target.closest("#tfilter button"); if(tf){team=tf.dataset.team;if(page==="churn")churnScope="all";render();return;}
  const pg=e.target.closest("[data-page-go]"); if(pg){page=pg.dataset.pageGo;render();window.scrollTo({top:0});return;}
  const ctab=e.target.closest("[data-churn-tab]"); if(ctab){churnTab=ctab.dataset.churnTab;page="churn";render();window.scrollTo({top:0});return;}
  const cop=e.target.closest("[data-churn-open]"); if(cop){const v=cop.dataset.churnOpen;churnScope=(v==="overview"||v==="all")?"all":v;churnTab="overview";page="churn";render();window.scrollTo({top:0});return;}
  const cbk=e.target.closest("[data-churn-back]"); if(cbk){churnScope="all";churnTab="overview";render();window.scrollTo({top:0});return;}
  const la=e.target.closest("[data-lanc-add]"); if(la){addLancFromForm(la.dataset.lancAdd);return;}
  const ld=e.target.closest("[data-lanc-del]"); if(ld){const p=ld.dataset.lancDel.split(":");const l=lancLocal();if(l[p[0]])l[p[0]].splice(+p[1],1);setLancLocal(l);render();return;}
  const lx=e.target.closest("[data-lanc-export]"); if(lx){exportLanc();return;}
  const gsv=e.target.closest("[data-gh-save]"); if(gsv){const t=($("ghTok").value||"").trim(); if(!t){alert("Cole o token do GitHub.");return;} setGhToken(t);
    showToast("Testando o token…"); pushLancToGitHub().then(r=>showToast(r.added?("✓ Conectado. "+r.added+" pendência(s) enviada(s) ao repositório."):"✓ Conectado ao GitHub. Salvar automático ligado."))
      .catch(err=>{showToast("⚠️ Token não funcionou: "+err.message+". Confira as permissões (Contents: Read and write no repo painel-time).");}); render(); return;}
  const gcl=e.target.closest("[data-gh-clear]"); if(gcl){setGhToken(""); showToast("Token removido deste navegador."); render(); return;}
  const grt=e.target.closest("[data-gh-retry]"); if(grt){showToast("Salvando no repositório…"); pushLancToGitHub().then(r=>showToast(r.added?("✓ "+r.added+" lançamento(s) salvo(s) no repositório."):"✓ Já estava tudo salvo no repositório.")).catch(err=>showToast("⚠️ Não salvou: "+err.message)); return;}
  const cst=e.target.closest("[data-churn-step]"); if(cst){churnStep(+cst.dataset.churnStep);return;}
  const cbs=e.target.closest("[data-churn-base]"); if(cbs){churnBase=cbs.dataset.churnBase;render();return;}
  const cyr=e.target.closest("[data-churn-year]"); if(cyr){churnYear=cyr.dataset.churnYear;render();return;}
  const pmy=e.target.closest("[data-churn-pmyear]"); if(pmy){churnPmYear=+pmy.dataset.churnPmyear;render();return;}
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
document.addEventListener("input",e=>{
  if(e.target.id==="clisearch"){const q=e.target.value.trim().toLowerCase();
    document.querySelectorAll("#chtbl tbody tr").forEach(tr=>{tr.style.display=(tr.dataset.n||"").includes(q)?"":"none";});}
});
document.addEventListener("change",e=>{
  if(e.target.id==="df"){dFrom=e.target.value;render();}
  if(e.target.id==="dt"){dTo=e.target.value;render();}
  if(e.target.id==="cfgfile"&&e.target.files[0]){importCfg(e.target.files[0]);e.target.value="";}
});
function showToast(msg){$("toastmsg").textContent=msg;$("toast").hidden=false;clearTimeout(window._tt);window._tt=setTimeout(()=>$("toast").hidden=true,6000);}
$("toastundo").addEventListener("click",()=>{if(window._last){unhide(window._last);window._last=null;$("toast").hidden=true;render();}});
/* ---------------- TELEMETRIA DE USO (identificação + eventos + página Uso) ---------------- */
const USO_URL="";                    // URL /exec do Apps Script — vazio = recurso desligado
const ADMIN_PIN="2026";              // PIN p/ abrir a página Uso (troque quando quiser)
// Acesso: SOMENTE os heads de squad (+ adm). match = início do nome no ClickUp (p/ achar avatar/uid).
const HEADS=[
  {match:"pedro henrique", label:"Pedro Henrique", squad:"G.O.A.T",        pin:"4172"},
  {match:"thulio",         label:"Thulio",         squad:"BULLS/SPARTANS", pin:"8305"},
  {match:"thiago zagnoli", label:"Thiago Zagnoli", squad:"FENIX",          pin:"6941"},
  {match:"lucas caldeira", label:"Lucas Caldeira", squad:"E-SCALE",        pin:"2537"},
  {match:"matheus augusto",label:"Matheus Augusto",squad:"ADFORCE",        pin:"9814"},
  {match:"__adm",          label:"Felipe",         squad:"Aure Digital · Adm", pin:"2026"},
];
const _nrmJs=n=>(n||"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"");
const headMember=h=>MODEL.members.find(m=>_nrmJs(m.name).startsWith(h.match))||null;
const headUid=h=>{const m=headMember(h);if(m)return m.uid;let x=0;for(let i=0;i<h.match.length;i++)x=(x*31+h.match.charCodeAt(i))>>>0;return 900000+x%100000;};
const IDKEY="clk_ident_v1", TQKEY="clk_tq_v1";
const usoUrl=()=>USO_URL||localStorage.getItem("clk_uso_url")||"";
const usoOn=()=>!!usoUrl();
function ident(){try{return JSON.parse(localStorage.getItem(IDKEY)||"null")}catch(e){return null}}
let SID=null;
function track(type,detail){ if(!usoOn()||!ident())return;
  try{ const q=JSON.parse(localStorage.getItem(TQKEY)||"[]");
    q.push({ts:new Date().toISOString(),uid:ident().uid,name:ident().name,type:type,page:page,detail:detail||"",sid:SID});
    localStorage.setItem(TQKEY,JSON.stringify(q.slice(-600)));
  }catch(e){}
}
function flushT(useBeacon){ if(!usoOn())return;
  try{ const q=JSON.parse(localStorage.getItem(TQKEY)||"[]"); if(!q.length)return;
    const body=JSON.stringify({events:q});
    if(useBeacon&&typeof navigator!=="undefined"&&navigator.sendBeacon){ if(navigator.sendBeacon(usoUrl(),body))localStorage.setItem(TQKEY,"[]"); return; }
    if(typeof fetch==="undefined")return;
    fetch(usoUrl(),{method:"POST",body:body}).then(()=>localStorage.setItem(TQKEY,"[]")).catch(()=>{});
  }catch(e){}
}
function showIdent(){ if(!usoOn()||ident())return;
  $("identgrid").innerHTML=HEADS.map((h,i)=>{const m=headMember(h);
    const av=m?avaHTML(m,"ava","width:30px;height:30px;border-radius:9px;font-size:11px")
      :`<span class="ava" style="width:30px;height:30px;border-radius:9px;font-size:11px;background:linear-gradient(135deg,#8b5cf6,#6d28d9)">${esc(initials(h.label))}</span>`;
    return `<button data-ident-pick="${i}">${av}<span>${esc(h.label)}<span class="tm">${esc(h.squad)}</span></span></button>`;}).join("");
  $("identov").hidden=false;
}
function startT(){ if(!usoOn()||!ident())return;
  SID="s"+Date.now().toString(36)+Math.random().toString(36).slice(2,7);
  track("session");track("page",page);
  if(typeof setInterval==="function"){
    setInterval(()=>{if(typeof document!=="undefined"&&document.visibilityState==="visible")track("hb");},60000);
    setInterval(()=>flushT(),90000);
  }
  if(typeof document!=="undefined"&&document.addEventListener){
    document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="hidden")flushT(true);});
  }
  if(typeof window!=="undefined"&&window.addEventListener)window.addEventListener("pagehide",()=>flushT(true));
}
document.addEventListener("click",e=>{ // ações que contam p/ "qualidade de uso" (fase de captura, não interfere)
  const ip=e.target.closest("[data-ident-pick]");
  if(ip){ const h=HEADS[+ip.dataset.identPick]; if(!h)return;
    const p=prompt("PIN de "+h.label+":");
    if(p!==h.pin){ if(p!=null)alert("PIN incorreto."); return; }
    localStorage.setItem(IDKEY,JSON.stringify({uid:headUid(h),name:h.label,team:h.squad,adm:h.match==="__adm"}));
    $("identov").hidden=true;startT();render(); return; }
  const ir=e.target.closest("[data-ident-reset]");
  if(ir){ localStorage.removeItem(IDKEY); showIdent(); return; }
  if(!usoOn()||!ident())return;
  const a=e.target.closest('a[href*="app.clickup.com"]'); if(a){track("action","abrir tarefa");return;}
  if(e.target.closest("[data-close]"))track("action","fechar tarefa");
  else if(e.target.closest("#tfilter button"))track("action","filtro de time");
  else if(e.target.closest("[data-preset]"))track("action","filtro de período");
  else if(e.target.closest("[data-churn-open]"))track("action","abrir squad/pessoa");
  else if(e.target.closest("[data-churn-tab]"))track("action","aba do churn");
},true);
const fmtMin=n=>{n=Math.round(n);return n>=60?Math.floor(n/60)+"h "+String(n%60).padStart(2,"0")+"m":n+"m";};
function renderUso(){
  if(ADMIN_PIN&&!window._usoOk){ const p=prompt("PIN de acesso à página Uso:");
    if(p!==ADMIN_PIN){page="overview";render();return;} window._usoOk=true; }
  $("topright").innerHTML="";
  $("root").innerHTML='<div class="col"><div class="empty">Carregando dados de uso…</div></div>';
  const cache=window._usoCache;
  if(cache&&Date.now()-cache.at<300000)return drawUso(cache.evts);
  if(typeof fetch==="undefined")return drawUso([]);
  fetch(usoUrl()+"?days=15").then(r=>r.json()).then(d=>{window._usoCache={at:Date.now(),evts:d.events||[]};if(page==="uso")drawUso(d.events||[]);})
    .catch(()=>{if(page==="uso")$("root").innerHTML='<div class="col"><div class="empty">Não consegui ler os dados de uso agora. Tente de novo em instantes.</div></div>';});
}
function drawUso(evts){
  const WIN=15;
  const byU={},pages={},byDay={};
  evts.forEach(ev=>{ const u=byU[ev.uid]=byU[ev.uid]||{uid:+ev.uid,name:ev.name,hb:0,days:{},sids:{},acts:0};
    const day=String(ev.ts).slice(0,10);
    if(ev.type==="hb"){u.hb++;u.days[day]=1;byDay[day]=(byDay[day]||0)+1;}
    if(ev.sid)u.sids[ev.sid]=1;
    if(ev.type==="action")u.acts++;
    if(ev.type==="page"&&ev.detail)pages[ev.detail]=(pages[ev.detail]||0)+1; });
  const roster=HEADS.filter(h=>h.match!=="__adm").map(h=>{const m=headMember(h);
    return {uid:headUid(h),name:h.label,team:h.squad,teams:[h.squad],avatar:m?m.avatar:null};});
  const rows=roster.map(m=>{ const u=byU[m.uid]||{hb:0,days:{},sids:{},acts:0};
    const days=Object.keys(u.days).length, sess=Object.keys(u.sids).length, aps=sess?u.acts/sess:0;
    const score=u.hb?Math.round(100*(0.5*Math.min(1,days/(WIN*0.8))+0.3*Math.min(1,aps/6)+0.2*Math.min(1,u.hb/180))):0;
    return {m:m,hb:u.hb,days:days,sess:sess,aps:aps,score:score}; }).sort((a,b)=>b.score-a.score||b.hb-a.hb);
  const lbl=r=>!r.hb?["nunca abriu","c"]:r.score>=70?["usa todo dia","g"]:r.score>=40?["em formação","w"]:r.aps<1?["só olha, não age","w"]:["quase não usa","c"];
  const used=rows.filter(r=>r.hb>0), totMin=rows.reduce((s,r)=>s+r.hb,0), totSess=rows.reduce((s,r)=>s+r.sess,0);
  const avgScore=Math.round(rows.reduce((s,r)=>s+r.score,0)/Math.max(1,rows.length));
  // uso × resultado: cruza dias de uso com atrasos reais do painel
  const odByUid={}; (MODEL.overdue||[]).forEach(t=>odByUid[t.uid]=(odByUid[t.uid]||0)+1);
  const hi=rows.filter(r=>r.days>=8), lo=rows.filter(r=>r.days<8);
  const avgOd=g=>g.length?(g.reduce((s,r)=>s+(odByUid[r.m.uid]||0),0)/g.length).toFixed(1):"—";
  const never=rows.filter(r=>!r.hb);
  const nevBy={}; never.forEach(r=>{const t=r.m.team||"—";nevBy[t]=(nevBy[t]||0)+1;});
  const nevTop=Object.entries(nevBy).sort((a,b)=>b[1]-a[1])[0];
  // barras por dia (últimos 15)
  const dayKeys=[]; for(let i=WIN-1;i>=0;i--){const d=new Date(Date.now()-i*864e5);dayKeys.push(ymd(d));}
  const dayMax=Math.max(1,...dayKeys.map(k=>byDay[k]||0));
  const pageTot=Object.values(pages).reduce((a,b)=>a+b,0)||1;
  const PLBL={overview:"Visão geral",person:"Pessoas",churn:"Churn",times:"Ajustes",uso:"Uso"};
  const topPages=Object.entries(pages).sort((a,b)=>b[1]-a[1]).slice(0,5);
  $("root").innerHTML=`<div class="col">
    <div class="kpis">
      <div class="kpi"><div class="n">${fmtMin(totMin)}</div><div class="l">Tempo ativo do time</div><div class="s">últimos ${WIN} dias</div></div>
      <div class="kpi"><div class="n">${used.length} <span style="font-size:14px;color:var(--muted)">/ ${rows.length}</span></div><div class="l">Pessoas que usaram</div><div class="s">${never.length} nunca abriram</div></div>
      <div class="kpi"><div class="n">${totSess?fmtMin(totMin/totSess):"—"}</div><div class="l">Sessão média</div><div class="s">${totSess} sessões</div></div>
      <div class="kpi"><div class="n" style="color:${avgScore>=60?'var(--gd-ink)':avgScore>=35?'var(--hi-ink)':'var(--cr-ink)'}">${avgScore}</div><div class="l">Engajamento do time</div><div class="s">score 0–100</div></div>
    </div>
    <div class="card"><div class="card-h"><h3>Uso × resultado</h3><div class="r">o painel muda comportamento?</div></div>
      <div class="pad" style="display:flex;flex-direction:column;gap:10px">
        <div class="note">Quem usou o painel <b>8+ dias</b> no período tem em média <b>${avgOd(hi)}</b> tarefa(s) em atraso. Quem usou menos: <b>${avgOd(lo)}</b>.</div>
        ${never.length?`<div class="note" style="border-left-color:var(--crit)"><b>${never.length} pessoa(s) nunca abriram o painel</b>${nevTop?` — ${nevTop[1]} do ${esc(nevTop[0])}`:""}. Vale um alinhamento.</div>`:""}
      </div></div>
    <div class="card"><div class="card-h"><h3>Por pessoa</h3><div class="r">últimos ${WIN} dias</div></div>
      <div class="tblwrap"><table class="ctable"><thead><tr><th>Pessoa</th><th>Time</th><th class="r">Tempo ativo</th><th class="r">Dias</th><th class="r">Ações/sessão</th><th>Score</th><th></th></tr></thead>
      <tbody>${rows.map(r=>{const L=lbl(r);const sc=r.score>=70?"var(--good)":r.score>=40?"var(--high)":"var(--crit)";
        return `<tr><td><div style="display:flex;align-items:center;gap:9px">${avaHTML(r.m,"ava","width:28px;height:28px;border-radius:9px;font-size:10px")}<b>${esc(r.m.name)}</b></div></td>
        <td>${mTeams(r.m).map(t=>`<span class="sqtag">${esc(t)}</span>`).join(" ")}</td>
        <td class="r">${r.hb?`<b>${fmtMin(r.hb)}</b>`:"—"}</td><td class="r">${r.days}/${WIN}</td><td class="r">${r.sess?r.aps.toFixed(1):"—"}</td>
        <td><span class="uscore"><span class="bar"><i style="width:${Math.max(3,r.score)}%;background:${sc}"></i></span><b style="color:${sc}">${r.score}</b></span></td>
        <td><span class="upill ${L[1]}">${L[0]}</span></td></tr>`;}).join("")}</tbody></table></div></div>
    <div class="card"><div class="card-h"><h3>Uso ao longo dos dias</h3><div class="r">minutos ativos do time por dia</div></div>
      <div class="pad">${evts.length?`<div class="fbars">${dayKeys.map(k=>`<div class="fb" style="height:${Math.max(3,(byDay[k]||0)/dayMax*82)}px" title="${fmtBR(k)}: ${fmtMin(byDay[k]||0)}"></div>`).join("")}</div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--muted)"><span>${fmtBR(dayKeys[0])}</span><span>${fmtBR(dayKeys[dayKeys.length-1])}</span></div>`
      :'<div class="empty">Ainda sem eventos registrados — os dados começam a aparecer assim que o time usar o painel.</div>'}</div></div>
    <div class="card"><div class="card-h"><h3>Páginas mais usadas</h3><div class="r">participação nas visitas</div></div>
      ${topPages.length?`<div class="tblwrap"><table class="ctable"><tbody>${topPages.map(([p,n])=>`<tr><td>${esc(PLBL[p]||p)}</td><td class="r"><b>${Math.round(n/pageTot*100)}%</b></td></tr>`).join("")}</tbody></table></div>`:'<div class="empty">Sem visitas registradas ainda.</div>'}</div>
  </div>`;
}
function buildTeamFilter(){
  const set=new Set(), cnt={}; MODEL.members.forEach(m=>mTeams(m).forEach(t=>{set.add(t);cnt[t]=(cnt[t]||0)+1;}));
  const CANON=["ADFORCE","G.O.A.T","BULLS","E-SCALE","FENIX"];
  const ordered=CANON.filter(t=>set.has(t)).concat([...set].filter(t=>!CANON.includes(t)).sort());
  const dot=v=>`<span class="tdot" style="background:${v==="all"?"var(--side-accent)":(TEAMDOT[v]||"var(--side-accent)")}"></span>`;
  const btn=(v,l,c)=>`<button data-team="${esc(v)}" aria-pressed="${team===v}">${dot(v)}<span>${esc(l)}</span><span class="tct">${c}</span></button>`;
  $("tfilter").innerHTML=btn("all","Todos",MODEL.members.length)+ordered.map(t=>btn(t,t,cnt[t]||0)).join("");
}
buildTeamFilter();
render();
if(usoOn()){ showIdent(); if(ident())startT(); }
</script>
"""

def _demo_model():
    random.seed(7)
    members=[(81464977,"Lucas Caldeira","E-SCALE","Head",["E-SCALE"]),(55085676,"Carlos Barbosa","E-SCALE","Account",["E-SCALE"]),
        (54912242,"Ray Junio","E-SCALE","Gestor de Tráfego",["E-SCALE"]),(87447111,"Izabela Galdino","E-SCALE","Account",["E-SCALE","ADFORCE"]),
        (87413647,"Rafael Alves","E-SCALE","Gestor de Tráfego",["E-SCALE"]),(206579907,"Thiago Zagnoli","FENIX","Head",["FENIX"]),
        (87318381,"Vinicius Andrade","FENIX","Account",["FENIX"]),(60944498,"Vitor Dumont","FENIX","Gestor de Tráfego",["FENIX","G.O.A.T"]),
        (96672993,"Rafael Ramos","FENIX","Account",["FENIX"]),(87448889,"Kaio Felipe","FENIX","Gestor de Tráfego",["FENIX"]),
        (118026171,"Patrick Lima","FENIX","Account",["FENIX"]),(87445783,"Carlos Nobre","FENIX","Gestor de Tráfego",["FENIX"]),
        (96624276,"Tiago Lamêu","FENIX","Gestor de Tráfego",["FENIX"]),
        (300001,"Gabriel Marcuci","G.O.A.T","Account",["G.O.A.T"]),(300002,"Pedro Reis","G.O.A.T","Gestor de Tráfego",["G.O.A.T"]),
        (300003,"Bianca Alves","ADFORCE","Account",["ADFORCE"]),(300004,"Rodrigo Sá","ADFORCE","Gestor de Tráfego",["ADFORCE"]),
        (300005,"Marina Costa","BULLS","Account",["BULLS"]),(300006,"Igor Nunes","BULLS","Gestor de Tráfego",["BULLS"])]
    M=[{"uid":u,"name":n,"team":t,"role":r,"teams":ts} for u,n,t,r,ts in members]
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
