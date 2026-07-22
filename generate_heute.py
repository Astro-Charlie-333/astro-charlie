# -*- coding: utf-8 -*-
"""Generiert taeglich die /heute/-Seite mit Mandys aktuellen Transiten.
Reiche, spezifische Deutungen basierend auf ihrem Chart. Laeuft in GitHub Actions."""
import swisseph as swe
import datetime, os, zoneinfo

F = swe.FLG_MOSEPH | swe.FLG_SPEED
S = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
GL = {'Sonne':'☉','Mond':'☽','Merkur':'☿','Venus':'♀','Mars':'♂','Jupiter':'♃','Saturn':'♄','Uranus':'♅','Neptun':'♆','Pluto':'♇','NK':'☊','ASC':'ASC','MC':'MC'}

def sp(d):
    dd=int(d%30); m=int((d%30-dd)*60)
    return f"{S[int(d//30)]} {dd}°{m:02d}′"

MANDY = {'Sonne':9.05,'Mond':18.53,'Merkur':341.55,'Venus':331.92,'Mars':55.70,
         'Jupiter':6.62,'Saturn':261.16,'Uranus':266.73,'Neptun':277.97,'Pluto':219.39,
         'NK':11.50,'ASC':67.97,'MC':302.77}
AI = int(MANDY['ASC']//30)
def house(d): return (int(d//30)-AI)%12+1

ASP = {0:('Konjunktion','☌'),60:('Sextil','⚹'),90:('Quadrat','□'),120:('Trigon','△'),180:('Opposition','☍')}

tz = zoneinfo.ZoneInfo("Europe/Berlin")
now = datetime.datetime.now(tz)
jd = swe.julday(now.year, now.month, now.day, 12.0 - (now.utcoffset().total_seconds()/3600))
WD = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']

# Himmel heute
TP = [('Sonne',swe.SUN),('Mond',swe.MOON),('Merkur',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),
      ('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Uranus',swe.URANUS),('Neptun',swe.NEPTUNE),('Pluto',swe.PLUTO)]
sky = {}
for n,pid in TP:
    r = swe.calc_ut(jd,pid,F); sky[n]=(r[0][0], r[0][3]<0)

moon_house = house(sky['Mond'][0])
moon_sign = S[int(sky['Mond'][0]//30)]

# Transite
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

# ===== REICHE DEUTUNGS-BIBLIOTHEK =====
# Was der Transit-Planet HEUTE bringt (Verb + Farbe)
TP_MEAN = {
 'Sonne':('beleuchtet','bringt Energie und Fokus'),
 'Mond':('berührt','färbt heute die Stimmung'),
 'Merkur':('verbindet sich mit','bringt Gedanken und Gespräche'),
 'Venus':('umschmeichelt','bringt Wärme, Liebe und Wert'),
 'Mars':('befeuert','bringt Antrieb und Tatkraft'),
 'Jupiter':('weitet','bringt Wachstum und Zuversicht'),
 'Saturn':('prüft','bringt Ernst und Struktur'),
 'Uranus':('elektrisiert','bringt Überraschung und Aufbruch'),
 'Neptun':('umnebelt','bringt Sehnsucht und Auflösung'),
 'Pluto':('durchdringt','bringt Tiefe und Wandlung'),
}
# Was der natale Punkt in DIR ist (mit Haus-Kontext)
NAT_MEAN = {
 'Sonne':'deinen Wesenskern und deine Lebenskraft (11. Haus: Zukunft & Gemeinschaft)',
 'Mond':'dein Gefühlsleben und deine Bedürfnisse (11. Haus: dein Umfeld nährt dich)',
 'Merkur':'dein Denken und Sprechen (10. Haus: dein Ausdruck nach außen, deine Berufung)',
 'Venus':'deine Venus - dein Lieben und Werten (10. Haus: sichtbar in deinem Wirken)',
 'Mars':'deinen Antrieb (12. Haus: deine stille, im Verborgenen wirkende Kraft)',
 'Jupiter':'deinen Jupiter - Wachstum und Sinn (11. Haus, Herrscher deines 7. - deine Liebe & Zukunft)',
 'Saturn':'deinen Saturn im 7. Haus - dein Thema von Verbindlichkeit und Reife in Beziehung',
 'Uranus':'deinen Uranus im 7. Haus - dein Bedürfnis nach Freiheit in Bindung',
 'Neptun':'deinen Neptun im 8. Haus - Tiefe, Intimität, das Verborgene',
 'Pluto':'deinen Pluto im 6. Haus - Alltag, Körper, Wandlung im Kleinen',
 'NK':'deine Wachstumsrichtung (11. Haus: dein Weg über Gemeinschaft & Zukunft)',
 'ASC':'dein Auftreten und deine Ausstrahlung',
 'MC':'deine Berufung und Lebensrichtung (Wassermann-MC)',
}
# Aspekt-Qualität als Ton
ASP_TONE = {
 'Konjunktion':'verschmilzt damit - die Energien wirken heute als Einheit, kraftvoll und direkt',
 'Sextil':'reicht ihm sanft die Hand - eine leichte Chance, wenn du sie ergreifst',
 'Quadrat':'reibt sich daran - eine Spannung, die dich zum Handeln oder Nachjustieren bewegt',
 'Trigon':'fließt mühelos dazu - hier geht heute etwas leicht und wie von selbst',
 'Opposition':'stellt sich gegenüber - eine Polarität, die nach Balance verlangt, oft über andere gespiegelt',
}
def deute(tn,nm,nn,orb):
    verb, farbe = TP_MEAN.get(tn,('berührt','wirkt'))
    nat = NAT_MEAN.get(nn,nn)
    tone = ASP_TONE.get(nm,'verbindet sich')
    txt = f"Transit-{tn} {farbe} und {tone}. Es trifft {nat}."
    if orb<=0.5:
        txt += " Dieser Aspekt ist heute besonders exakt - du spürst ihn deutlich."
    return txt

# Kategorie & Farbe je Aspekt
def kat(nm):
    return {'Trigon':('Fluss','harm'),'Sextil':('Chance','harm'),'Konjunktion':('Verstärkung','konj'),
            'Quadrat':('Reibung','span'),'Opposition':('Spannung','span')}.get(nm,('',''))

# Mond-Haus-Deutung (Tagesstimmung)
MOON_HOUSE = {
 1:'Heute geht es um dich - dein Auftreten, dein Körper, dein Ich steht im Vordergrund.',
 2:'Heute liegt der Fokus auf Körper, Werten und dem, was dir Sicherheit gibt.',
 3:'Ein kommunikativer Tag - Austausch, kurze Wege, Gedanken und Gespräche.',
 4:'Ein Kokon-Tag - Zuhause, Rückzug, Wurzeln und emotionale Geborgenheit.',
 5:'Ein Tag für Freude, Kreativität, Spiel und alles, was das Herz leuchten lässt.',
 6:'Ein Tag für Alltag, Körper, Ordnung und die kleinen Dinge, die guttun.',
 7:'Beziehung und Begegnung stehen heute im Zentrum - das bewusste Du.',
 8:'Ein tiefer Tag - Intimität, das Verborgene, echte Nähe statt Oberfläche.',
 9:'Ein weiter Tag - Sinn, das große Ganze, Ausblick und Perspektive.',
 10:'Berufung und Sichtbarkeit rücken heute in den Blick - dein Wirken nach außen.',
 11:'Dein Umfeld, Freundschaften und deine Zukunftsvisionen nähren dich heute.',
 12:'Ein Rückzugstag - Ruhe, Träume, das Unbewusste, sanft zu dir sein.',
}
tages_stimmung = MOON_HOUSE.get(moon_house,'')

# ===== HTML =====
CSS = """@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#FFF6F1;--card:#FCE4D6;--text:#3A1F14;--text-soft:#8A5A44;--indigo:#C1440E;--gold:#D9922E;--line:#F0CFB8;--harm:#4A7C59;--span:#B5502E;--konj:#7A5299;}
*{box-sizing:border-box;}body{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;padding:32px 20px 60px;}
.wrap{max-width:760px;margin:0 auto;}
.sign-header{display:flex;align-items:center;gap:14px;margin-bottom:18px;}
.sign-glyph{width:44px;height:44px;border-radius:50%;background:var(--indigo);color:var(--bg);display:flex;align-items:center;justify-content:center;font-size:22px;}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:4px;}
.sub{font-size:14px;color:var(--text-soft);}h1{font-family:'Caveat',cursive;font-weight:700;font-size:46px;line-height:1.05;margin:0 0 8px;color:var(--indigo);}
.back-link{font-size:12.5px;color:var(--indigo);font-family:'JetBrains Mono',monospace;display:inline-block;margin-bottom:22px;}
.mood{background:linear-gradient(135deg,var(--card),#F8D9C4);border:1px solid var(--line);border-radius:18px;padding:20px 24px;margin-bottom:26px;}
.mood-label{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.mood-moon{font-size:15px;font-weight:700;color:var(--indigo);margin-bottom:6px;}
.mood-text{font-size:14.5px;line-height:1.6;color:var(--text-soft);}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold);margin:32px 0 14px;font-weight:700;}
.sky{font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.9;color:var(--text-soft);background:var(--card);border-radius:14px;padding:16px 20px;border:1px solid var(--line);margin-bottom:8px;}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:12px;border-left:4px solid var(--line);}
.card.harm{border-left-color:var(--harm);}.card.span{border-left-color:var(--span);}.card.konj{border-left-color:var(--konj);}
.card.exact{box-shadow:0 2px 12px rgba(193,68,14,.12);}
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:7px;flex-wrap:wrap;}
.card-title{font-weight:700;font-size:15.5px;}
.card-meta{display:flex;gap:8px;align-items:center;flex-shrink:0;}
.kat{font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:20px;color:#fff;}
.kat.harm{background:var(--harm);}.kat.span{background:var(--span);}.kat.konj{background:var(--konj);}
.card-orb{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold);}
.card p{margin:0;font-size:14px;line-height:1.6;color:var(--text-soft);}
.footer-note{margin-top:36px;padding-top:20px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--text-soft);line-height:1.6;}
.empty{background:var(--card);border-radius:16px;padding:24px;text-align:center;color:var(--text-soft);font-size:14.5px;}"""

sky_html = '<div class="sky">' + ' · '.join(
    f"{GL[n]} {sp(d)}{' <span style=\"color:var(--indigo)\">R</span>' if r else ''}" for n,(d,r) in sky.items()) + '</div>'

# Mond separat hervorheben in Stimmungsbox
mood_html = f'''<div class="mood">
<div class="mood-label">Die Stimmung heute</div>
<div class="mood-moon">☽ Mond in {moon_sign} · dein {moon_house}. Haus</div>
<div class="mood-text">{tages_stimmung}</div></div>'''

cards = []
for o,tn,nm,g,nn,retro in hits[:8]:
    katname,katcls = kat(nm)
    exact = ' exact' if o<=0.5 else ''
    r = ' <span style="color:var(--indigo)">R</span>' if retro else ''
    katbadge = f'<span class="kat {katcls}">{katname}</span>' if katname else ''
    cards.append(f'''<div class="card {katcls}{exact}">
<div class="card-head"><span class="card-title">{GL.get(tn,tn)} {tn}{r} {g} {GL.get(nn,nn)} {nn}</span>
<span class="card-meta">{katbadge}<span class="card-orb">{o:.2f}°</span></span></div>
<p>{deute(tn,nm,nn,o)}</p></div>''')
cards_html = '\n'.join(cards) if cards else '<div class="empty">Heute keine engen Transite - ein ruhiger, offener Tag ohne besonderen kosmischen Druck. Genieß die Leichtigkeit.</div>'

datum = f"{WD[now.weekday()]}, {now.day:02d}.{now.month:02d}.{now.year}"
html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Deine Transite heute</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="sign-header"><div class="sign-glyph">🌤️</div><div>
<div class="eyebrow">Astro Charlie · Heute</div><div class="sub">{datum} · Berlin</div></div></div>
<h1>Deine Transite heute.</h1>
<a class="back-link" href="../index.html">← zur Startseite</a>
{mood_html}
<h2>Was heute auf dich wirkt</h2>
{cards_html}
<h2>Der ganze Himmel</h2>
{sky_html}
<div class="footer-note">Automatisch berechnet mit Swiss Ephemeris für {datum}, Berlin · Whole Sign. Diese Seite aktualisiert sich jeden Morgen von selbst. Farben zeigen die Aspekt-Qualität: <span style="color:var(--harm)">grün = Fluss/Chance</span>, <span style="color:var(--span)">rot = Reibung/Spannung</span>, <span style="color:var(--konj)">violett = Verstärkung</span>. Transite beschreiben Zeitqualitäten, keine festen Ereignisse.</div>
</div></body></html>"""

os.makedirs("heute", exist_ok=True)
with open("heute/index.html","w",encoding="utf-8") as f:
    f.write(html)
print(f"heute/index.html generiert fuer {datum}: {len(hits)} Transite, Mond in {moon_sign} (H{moon_house})")
