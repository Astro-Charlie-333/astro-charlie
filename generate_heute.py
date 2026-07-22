# -*- coding: utf-8 -*-
"""Generiert taeglich die /heute/-Seite mit Mandys aktuellen Transiten.
Laeuft in GitHub Actions, ganz ohne manuelles Zutun."""
import swisseph as swe
import datetime, os, zoneinfo

F = swe.FLG_MOSEPH | swe.FLG_SPEED
S = ['Widder','Stier','Zwillinge','Krebs','Loewe','Jungfrau','Waage','Skorpion','Schuetze','Steinbock','Wassermann','Fische']
S_UML = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
GL = {'Sonne':'☉','Mond':'☽','Merkur':'☿','Venus':'♀','Mars':'♂','Jupiter':'♃','Saturn':'♄','Uranus':'♅','Neptun':'♆','Pluto':'♇','NK':'☊'}

def sp(d):
    dd=int(d%30); m=int((d%30-dd)*60)
    return f"{S_UML[int(d//30)]} {dd}°{m:02d}′"

# --- Mandys Natal-Chart (fest) ---
MANDY = {'Sonne':9.05,'Mond':18.53,'Merkur':341.55,'Venus':331.92,'Mars':55.70,
         'Jupiter':6.62,'Saturn':261.16,'Uranus':266.73,'Neptun':277.97,'Pluto':219.39,
         'NK':11.50,'ASC':67.97,'MC':302.77}
AI = int(MANDY['ASC']//30)
def house(d): return (int(d//30)-AI)%12+1

ASP = {0:('Konjunktion','☌'),60:('Sextil','⚹'),90:('Quadrat','□'),120:('Trigon','△'),180:('Opposition','☍')}

# --- Aktuelles Datum in Berlin ---
tz = zoneinfo.ZoneInfo("Europe/Berlin")
now = datetime.datetime.now(tz)
# UT aus Berliner Mittag
jd = swe.julday(now.year, now.month, now.day, 12.0 - (now.utcoffset().total_seconds()/3600))

WD = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']

# --- Himmel heute ---
TP = [('Sonne',swe.SUN),('Mond',swe.MOON),('Merkur',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),
      ('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Uranus',swe.URANUS),('Neptun',swe.NEPTUNE),('Pluto',swe.PLUTO)]
sky = {}
for n,pid in TP:
    r = swe.calc_ut(jd,pid,F); sky[n]=(r[0][0], r[0][3]<0)

# --- Transite zu Mandy ---
hits = []
for tn,(td,retro) in sky.items():
    for nn,nd in MANDY.items():
        diff = abs(td-nd)%360
        if diff>180: diff=360-diff
        for ang,(nm,g) in ASP.items():
            o = abs(diff-ang)
            lim = 3 if tn=='Mond' else 2
            if o<=lim:
                hits.append((o,tn,nm,g,nn,retro))
hits.sort()

# --- Deutungs-Snippets ---
def deute(tn,nm,nn):
    base = {
      'Sonne':'Fokus und Energie','Mond':'Gefühle und Stimmung','Merkur':'Denken und Austausch',
      'Venus':'Liebe und Werte','Mars':'Antrieb und Tatkraft','Jupiter':'Wachstum und Weite',
      'Saturn':'Struktur und Prüfung','Uranus':'Veränderung und Aufbruch','Neptun':'Sehnsucht und Auflösung','Pluto':'Tiefe und Wandlung'}
    nat = {
      'Sonne':'deinen Wesenskern','Mond':'dein Gefühlsleben','Merkur':'dein Denken','Venus':'deine Venus (Liebe/Werte)',
      'Mars':'deinen Antrieb','Jupiter':'deinen Jupiter (Wachstum)','Saturn':'deinen Saturn','Uranus':'deinen Uranus',
      'Neptun':'deinen Neptun','Pluto':'deinen Pluto','NK':'deine Wachstumsrichtung','ASC':'dein Auftreten','MC':'deine Berufung'}
    q = {'Konjunktion':'trifft und verstärkt','Sextil':'unterstützt sanft','Quadrat':'fordert heraus','Trigon':'fließt harmonisch zu','Opposition':'steht in Spannung zu'}
    return f"{base.get(tn,tn)} {q.get(nm,'berührt')} {nat.get(nn,nn)}."

# --- HTML bauen ---
CSS = """@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#FFF6F1;--card:#FCE4D6;--text:#3A1F14;--text-soft:#8A5A44;--indigo:#C1440E;--gold:#D9922E;--line:#F0CFB8;}
*{box-sizing:border-box;}body{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;padding:32px 20px 60px;}
.wrap{max-width:760px;margin:0 auto;}.sign-header{display:flex;align-items:center;gap:14px;margin-bottom:18px;}
.sign-glyph{width:44px;height:44px;border-radius:50%;background:var(--indigo);color:var(--bg);display:flex;align-items:center;justify-content:center;font-size:22px;}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:4px;}
.sub{font-size:14px;color:var(--text-soft);}h1{font-family:'Caveat',cursive;font-weight:700;font-size:44px;line-height:1.05;margin:0 0 8px;color:var(--indigo);}
.back-link{font-size:12.5px;color:var(--indigo);font-family:'JetBrains Mono',monospace;display:inline-block;margin-bottom:22px;}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold);margin:30px 0 14px;font-weight:700;}
.sky{font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.9;color:var(--text-soft);background:var(--card);border-radius:14px;padding:16px 20px;border:1px solid var(--line);margin-bottom:8px;}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 20px;margin-bottom:11px;}
.card.hl{border:2px solid var(--indigo);}
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:5px;flex-wrap:wrap;}
.card-title{font-weight:700;font-size:14.5px;}.card-orb{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold);}
.card p{margin:0;font-size:13.5px;line-height:1.5;color:var(--text-soft);}
.footer-note{margin-top:36px;padding-top:20px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--text-soft);line-height:1.6;}"""

sky_html = '<div class="sky">' + ' · '.join(
    f"{GL[n]} {sp(d)}{' R' if r else ''}" for n,(d,r) in sky.items()) + '</div>'

cards = []
for o,tn,nm,g,nn,retro in hits[:8]:
    hl = ' hl' if o<=0.5 else ''
    r = ' R' if retro else ''
    cards.append(f'<div class="card{hl}"><div class="card-head"><span class="card-title">{GL.get(tn,tn)} {tn}{r} {g} {nn}</span><span class="card-orb">Orb {o:.2f}°</span></div><p>{deute(tn,nm,nn)}</p></div>')
cards_html = '\n'.join(cards) if cards else '<div class="card"><p>Heute keine engen Transite - ein ruhiger Tag.</p></div>'

datum = f"{WD[now.weekday()]}, {now.day:02d}.{now.month:02d}.{now.year}"
html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Deine Transite heute</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="sign-header"><div class="sign-glyph">🌤️</div><div>
<div class="eyebrow">Astro Charlie · Heute</div><div class="sub">{datum} · Berlin</div></div></div>
<h1>Deine Transite heute.</h1>
<a class="back-link" href="../index.html">← zur Startseite</a>
<h2>Der Himmel heute</h2>
{sky_html}
<h2>Was auf dich wirkt</h2>
{cards_html}
<div class="footer-note">Automatisch berechnet mit Swiss Ephemeris für {datum}, Berlin · Whole Sign. Diese Seite aktualisiert sich täglich von selbst. Transite beschreiben Zeitqualitäten, keine festen Ereignisse.</div>
</div></body></html>"""

os.makedirs("heute", exist_ok=True)
with open("heute/index.html","w",encoding="utf-8") as f:
    f.write(html)
print(f"heute/index.html generiert fuer {datum} mit {len(hits)} Transiten")
