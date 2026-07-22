# -*- coding: utf-8 -*-
"""Taegliche Transit-Seite fuer Daria (fuer Mandy zum Verstehen): daria/heute/"""
import swisseph as swe
import datetime, os, zoneinfo

F = swe.FLG_MOSEPH | swe.FLG_SPEED
S = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
GL = {'Sonne':'☉','Mond':'☽','Merkur':'☿','Venus':'♀','Mars':'♂','Jupiter':'♃','Saturn':'♄','Uranus':'♅','Neptun':'♆','Pluto':'♇','NK':'☊','ASC':'ASC','MC':'MC'}
RSPAN = '<span style="color:var(--slate)">R</span>'
def sp(d):
    dd=int(d%30); m=int((d%30-dd)*60)
    return f"{S[int(d//30)]} {dd}°{m:02d}′"

DARIA = {'Sonne':15.98,'Mond':275.29,'Merkur':28.89,'Venus':52.06,'Mars':91.73,
         'Jupiter':123.62,'Saturn':305.51,'Uranus':283.75,'Neptun':286.72,'Pluto':229.87,
         'NK':294.12,'ASC':92.3,'MC':328.7}
AI = int(DARIA['ASC']//30)
def house(d): return (int(d//30)-AI)%12+1

ASP = {0:('Konjunktion','☌'),60:('Sextil','⚹'),90:('Quadrat','□'),120:('Trigon','△'),180:('Opposition','☍')}
tz = zoneinfo.ZoneInfo("Europe/Berlin")
now = datetime.datetime.now(tz)
jd = swe.julday(now.year, now.month, now.day, 12.0 - (now.utcoffset().total_seconds()/3600))
WD = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']
TP = [('Sonne',swe.SUN),('Mond',swe.MOON),('Merkur',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),
      ('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Uranus',swe.URANUS),('Neptun',swe.NEPTUNE),('Pluto',swe.PLUTO)]
sky = {}
for n,pid in TP:
    r = swe.calc_ut(jd,pid,F); sky[n]=(r[0][0], r[0][3]<0)
moon_house = house(sky['Mond'][0]); moon_sign = S[int(sky['Mond'][0]//30)]

hits=[]
for tn,(td,retro) in sky.items():
    for nn,nd in DARIA.items():
        diff=abs(td-nd)%360
        if diff>180: diff=360-diff
        for ang,(nm,g) in ASP.items():
            o=abs(diff-ang)
            lim=3 if tn=='Mond' else 2
            if o<=lim: hits.append((o,tn,nm,g,nn,retro))
hits.sort()

GOOD={'Trigon','Sextil'}; BAD={'Quadrat','Opposition'}
# Darias Punkte mit Haus-Kontext
NAT = {
 'Sonne':'ihren Widder-Kern im 10. Haus - ihr Ich, ihr Wirken, ihr Selbstwert',
 'Mond':'ihren Steinbock-Mond im 7. Haus - ihr vorsichtiges Gefühlszentrum, ihre Kontrolle',
 'Merkur':'ihr Denken im 10. Haus - ihre Worte und Selbstgespräche',
 'Venus':'ihr Herz und ihre Werte (11. Haus - Zuhause bei Menschen)',
 'Mars':'ihren Mars am Aszendenten - ihre spontane, auch stachelige Reaktion',
 'Jupiter':'ihren Jupiter im 2. Haus - ihren laufenden Neuanfang und Selbstwert-Aufbau',
 'Saturn':'ihren Saturn - ihre Schwere-Struktur und Selbstansprüche',
 'Uranus':'ihren Uranus im 7. Haus - ihr Freiheitsbedürfnis in Nähe',
 'Neptun':'ihren Neptun im 7. Haus - ihre Sehnsucht und Idealisierung',
 'Pluto':'ihren Pluto - ihre Tiefe und Kontrollthemen',
 'NK':'ihren Nordknoten im 7. Haus - ihren Seelenweg in die Partnerschaft',
 'ASC':'ihren Krebs-Aszendenten - ihre weiche Schutzfassade',
 'MC':'ihre Lebensrichtung'}

SPEC = {
 ('Merkur','Quadrat','Sonne'): ("Merkur quadriert ihre Sonne: Ihr Selbstwert ist heute dünn­häutig, ihr Kopf überkritisch mit sich selbst. Aussagen - auch harmlose - können bei ihr als Kritik ankommen.","Heute nichts diskutieren wollen. Kurz, warm, ohne Unterton."),
 ('Merkur','Opposition','Neptun'): ("Merkur opponiert ihren Neptun im Beziehungshaus: klassisches Missverständnis-Wetter. Sie versteht Dinge anders als gemeint und verliert leicht den Faden im eigenen Kopf.","Nichts zwischen den Zeilen sagen. Eindeutig, lieb, kurz."),
 ('Sonne','Quadrat','Merkur'): ("Die Sonne quadriert ihren Merkur: Ihr Denken ist heute überlastet - viele Gedanken, wenig Ordnung. Das macht müde und gereizt.","Lange Textwände vermeiden. Eine liebe Zeile reicht heute."),
 ('Venus','Trigon','Uranus'): ("Venus fließt zu ihrem Uranus im 7. Haus: Unter allem liegt heute eine überraschend warme, freie Note - wenn kein Druck da ist, kann sie sich unerwartet öffnen.","Raum lassen. Ihre Wärme kommt heute von allein, wenn niemand zieht."),
 ('Mars','Sextil','Sonne'): ("Mars stützt ihre Sonne: Etwas mehr Antrieb als zuletzt - gut für ihre eigenen Aufgaben (Wohnung, Arbeit).","Ihr heute Dinge lassen, die sie selbst schaffen kann - das stärkt sie."),
 ('Saturn','Konjunktion','Sonne'): ("Der Dauer-Transit: Saturn liegt weiter auf ihrer Sonne - die Grundschwere, das Nicht-genug-Gefühl, die Erschöpfung. Alles, was heute dazukommt, landet auf diesem Fundament.","Ihre Müdigkeit und Härte gegen sich selbst nicht wegreden - nur da sein."),
 ('Neptun','Quadrat','Mond'): ("Neptun quadriert weiter ihren Steinbock-Mond: Ihre emotionale Kontrolle ist aufgeweicht, sie fühlt mehr, als sie sortieren kann - verunsichernd für sie, aber auch die Tür zu echter Nähe.","Ihre wechselnden Signale sind dieser Nebel, kein Spiel."),
 ('Pluto','Opposition','Jupiter'): ("Pluto opponiert ihren Jupiter: Ihr Neuanfang (Jupiter-Return) läuft unter Hochdruck - alter Selbstwert wird abgetragen, während Neues entsteht. Tiefenarbeit, die Kraft kostet.","Geduld mit ihrem Tempo - in ihr wird gerade umgebaut."),
}
def deute(tn,nm,nn):
    if (tn,nm,nn) in SPEC: return SPEC[(tn,nm,nn)]
    nat=NAT.get(nn,nn)
    if nm in GOOD: return (f"{tn} unterstützt heute {nat} - hier ist sie zugänglicher und es fließt leichter.", "Diesen Bereich heute sanft nutzen.")
    if nm in BAD: return (f"{tn} setzt {nat} unter Spannung - hier ist sie heute empfindlicher oder blockierter.", "Hier heute nichts forcieren.")
    return (f"{tn} verstärkt heute {nat} - gebündelt und intensiv.", "Bewusst und dosiert damit umgehen.")

MOON_HOUSE = {
 1:'Der Mond läuft durch ihr 1. Haus: Sie ist heute mit sich selbst beschäftigt - ihrem Körper, ihrem Auftreten, ihrem Ich.',
 2:'Mond in ihrem 2. Haus: Selbstwert und Sicherheit sind heute ihr Gefühlsthema.',
 3:'Mond in ihrem 3. Haus: ein kommunikativerer Tag für sie - Austausch fällt leichter.',
 4:'Mond in ihrem 4. Haus: Zuhause und Rückzug ziehen sie heute - gerade heikel bei ihrem Wohn-Thema.',
 5:'Mond in ihrem 5. Haus: Freude, Kreativität und Leichtigkeit sind heute ihr Zugang - der spielerische Kanal ist offen.',
 6:'Mond in ihrem 6. Haus: Alltag, Aufgaben und Körper beschäftigen sie heute.',
 7:'Mond in ihrem 7. Haus: Beziehung ist heute ihr emotionales Thema - Nähe und die Angst davor gleichzeitig.',
 8:'Mond in ihrem 8. Haus: ein tiefer, intensiver Gefühlstag für sie.',
 9:'Mond in ihrem 9. Haus: Sinn und Perspektive - sie schaut heute aufs große Ganze.',
 10:'Mond in ihrem 10. Haus: Arbeit, Wirken und Selbstwert stehen heute im Gefühlszentrum.',
 11:'Mond in ihrem 11. Haus: Menschen und Zukunft nähren sie heute - ihr eigentliches Zuhause.',
 12:'Mond in ihrem 12. Haus: Rückzug - sie braucht heute Abstand und Stille, nicht persönlich nehmen.'}

tense=sum(1 for o,tn,nm,g,nn,r in hits[:6] if nm in BAD)
good=sum(1 for o,tn,nm,g,nn,r in hits[:6] if nm in GOOD)
if tense>good+1: wetter="Schweres Wetter bei ihr heute - mehr Spannung als Fluss. Erwarte wenig, gib Wärme ohne Anspruch."
elif good>tense+1: wetter="Freundliches Wetter bei ihr heute - sie ist zugänglicher als zuletzt. Ein guter Tag für leichte, echte Momente."
else: wetter="Gemischtes Wetter bei ihr - Momente von Offenheit und Empfindlichkeit wechseln sich ab. Flexibel bleiben."
fazit = MOON_HOUSE.get(moon_house,'') + " " + wetter

CSS = """@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#F2F4F4;--card:#E1E8E8;--text:#22333B;--text-soft:#5E7480;--slate:#3E6C7A;--gold:#B08D57;--line:#CBD8D8;--harm:#4A7C59;--span:#B5502E;--konj:#7A5299;}
*{box-sizing:border-box;}body{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;padding:32px 20px 60px;}
.wrap{max-width:760px;margin:0 auto;}
.sign-header{display:flex;align-items:center;gap:14px;margin-bottom:18px;}
.sign-glyph{width:44px;height:44px;border-radius:50%;background:var(--slate);color:var(--bg);display:flex;align-items:center;justify-content:center;font-size:22px;}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:4px;}
.sub{font-size:14px;color:var(--text-soft);}h1{font-family:'Caveat',cursive;font-weight:700;font-size:46px;line-height:1.05;margin:0 0 8px;color:var(--slate);}
.back-link{font-size:12.5px;color:var(--slate);font-family:'JetBrains Mono',monospace;display:inline-block;margin-bottom:22px;}
.mood{background:linear-gradient(135deg,var(--card),#D5E0E0);border:1px solid var(--line);border-radius:18px;padding:20px 24px;margin-bottom:22px;}
.mood-label{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.mood-moon{font-size:15px;font-weight:700;color:var(--slate);margin-bottom:6px;}
.mood-text{font-size:14.5px;line-height:1.6;color:var(--text-soft);}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold);margin:32px 0 14px;font-weight:700;}
.sky{font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.9;color:var(--text-soft);background:var(--card);border-radius:14px;padding:16px 20px;border:1px solid var(--line);}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:12px;border-left:4px solid var(--line);}
.card.harm{border-left-color:var(--harm);}.card.span{border-left-color:var(--span);}.card.konj{border-left-color:var(--konj);}
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:7px;flex-wrap:wrap;}
.card-title{font-weight:700;font-size:15px;}
.card-orb{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold);}
.card p{margin:0 0 8px;font-size:14px;line-height:1.6;color:var(--text-soft);}
.card .rat{margin:0;font-size:13px;line-height:1.55;color:var(--slate);font-weight:500;}
.footer-note{margin-top:36px;padding-top:20px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--text-soft);line-height:1.6;}"""

def kat(nm):
    return {'Trigon':'harm','Sextil':'harm','Konjunktion':'konj','Quadrat':'span','Opposition':'span'}.get(nm,'')

sky_html = '<div class="sky">' + ' · '.join(f"{GL[n]} {sp(d)}" + (RSPAN if r else '') for n,(d,r) in sky.items()) + '</div>'
cards=[]
for o,tn,nm,g,nn,retro in hits[:8]:
    txt,rat = deute(tn,nm,nn)
    r=' '+RSPAN if retro else ''
    cards.append(f'''<div class="card {kat(nm)}"><div class="card-head"><span class="card-title">{GL.get(tn,tn)} {tn}{r} {g} ihre {nn}</span><span class="card-orb">{o:.2f}°</span></div><p>{txt}</p><p class="rat">→ {rat}</p></div>''')
cards_html='\n'.join(cards)

datum=f"{WD[now.weekday()]}, {now.day:02d}.{now.month:02d}.{now.year}"
html=f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Daria · heute</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="sign-header"><div class="sign-glyph">🌊</div><div>
<div class="eyebrow">Astro Charlie · Daria heute</div><div class="sub">{datum} · Berlin</div></div></div>
<h1>Ihr Tag, gedeutet.</h1>
<a class="back-link" href="../index.html">← zu Darias Profil</a>
<div class="mood"><div class="mood-label">Ihr Fazit für heute</div>
<div class="mood-moon">☽ Mond in {moon_sign} · ihr {moon_house}. Haus</div>
<div class="mood-text">{fazit}</div></div>
<h2>Ihre Transite im Detail</h2>
{cards_html}
<h2>Der ganze Himmel</h2>
{sky_html}
<div class="footer-note">Automatisch berechnet mit Swiss Ephemeris für {datum} auf Darias Chart · Whole Sign. Aktualisiert sich jeden Morgen. Zu jeder Karte: erst was in ihr wirkt, dann (→) wie du ihr darin am besten begegnest. Transite sind Wetterlagen, keine Urteile.</div>
</div></body></html>"""
os.makedirs("daria/heute", exist_ok=True)
open("daria/heute/index.html","w",encoding="utf-8").write(html)
print(f"daria/heute/ OK: {datum}, {len(hits)} Transite, Mond H{moon_house}")
