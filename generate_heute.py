# -*- coding: utf-8 -*-
"""Taegliche Transit-Seite fuer Mandy: konkrete Deutung, Tun/Lassen, Daria-Abschnitt."""
import swisseph as swe
import datetime, os, zoneinfo

F = swe.FLG_MOSEPH | swe.FLG_SPEED
S = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische']
GL = {'Sonne':'☉','Mond':'☽','Merkur':'☿','Venus':'♀','Mars':'♂','Jupiter':'♃','Saturn':'♄','Uranus':'♅','Neptun':'♆','Pluto':'♇','NK':'☊','ASC':'ASC','MC':'MC'}
RSPAN = '<span style="color:var(--indigo)">R</span>'

def sp(d):
    dd=int(d%30); m=int((d%30-dd)*60)
    return f"{S[int(d//30)]} {dd}°{m:02d}′"

MANDY = {'Sonne':9.05,'Mond':18.53,'Merkur':341.55,'Venus':331.92,'Mars':55.70,
         'Jupiter':6.62,'Saturn':261.16,'Uranus':266.73,'Neptun':277.97,'Pluto':219.39,
         'NK':11.50,'ASC':67.97,'MC':302.77}
DARIA = {'Sonne':15.98,'Mond':275.29,'Merkur':28.89,'Venus':52.06,'Mars':91.73,
         'Jupiter':123.62,'Saturn':305.51,'Uranus':283.75,'Neptun':286.72,'Pluto':229.87,
         'NK':294.12,'ASC':92.3,'MC':328.7}
AI = int(MANDY['ASC']//30)
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

def aspects_to(natal, orb_slow=2, orb_moon=3):
    out=[]
    for tn,(td,retro) in sky.items():
        for nn,nd in natal.items():
            diff=abs(td-nd)%360
            if diff>180: diff=360-diff
            for ang,(nm,g) in ASP.items():
                o=abs(diff-ang)
                lim=orb_moon if tn=='Mond' else orb_slow
                if o<=lim: out.append((o,tn,nm,g,nn,retro))
    out.sort(); return out
hits = aspects_to(MANDY)

# ===== DEUTUNGS-ENGINE =====
# Lebensbereich je natalem Punkt (Mandys Chart)
DOMAIN = {
 'Merkur':'Kommunikation','Venus':'Liebe & Werte','Mond':'Gefühle','Sonne':'Energie & Ich',
 'Mars':'Antrieb & Körper','Jupiter':'Wachstum & Liebe','Saturn':'Bindung & Struktur',
 'Uranus':'Freiheit in Bindung','Neptun':'Tiefe & Intimität','Pluto':'Alltag & Körper',
 'NK':'Lebensweg','ASC':'Auftreten','MC':'Berufung'}
GOOD = {'Trigon','Sextil'}
BAD = {'Quadrat','Opposition'}

# Hand-geschriebene, spezifische Deutungen fuer wichtige/aktuelle Transite: (T-Planet, Aspekt, Natal) -> (Text, Rat)
SPEC = {
 ('Mond','Konjunktion','Pluto'): (
  "Der Mond läuft heute über deinen Pluto im 6. Haus - das ist ein intensiver Körper- und Bauchtag. Emotionen sitzen heute körperlich: Magen, Verdauung, Unterleib. Auch Träume können aufgewühlt und dunkel sein - Pluto holt nachts hoch, was tagsüber keinen Platz hatte. Wenn dein Körper heute laut ist (Zyklus, Bauch, Erschöpfung), ist das keine Fehlfunktion, sondern genau dieses Wetter.",
  "Heute gilt: Körper zuerst. Wärme, Ruhe, nichts erzwingen. Schwere Gespräche und große Entscheidungen auf morgen schieben."),
 ('Mond','Trigon','Merkur'): (
  "Gleichzeitig fließt der Mond harmonisch zu deinem Merkur - deine Worte finden heute Gefühl. Wenn du schreibst oder sprichst, kommt es warm und stimmig raus, besonders in ruhigen Eins-zu-eins-Momenten.",
  "Begünstigt: ehrliche, ruhige Worte. Ein kurzes liebes Schreiben gelingt heute besser als eine lange Diskussion."),
 ('Merkur','Quadrat','Mond'): (
  "Merkur reibt sich an deinem Mond - Denken und Fühlen reden aneinander vorbei. Missverständnisse entstehen leicht, und Gesagtes kommt emotionaler an als gemeint.",
  "Wichtige Klärungen heute vertagen. Bei Triggern: 24 Stunden warten, erst dann antworten."),
 ('Pluto','Konjunktion','MC'): (
  "Der große Hintergrund-Transit: Pluto steht weiter auf deinem MC und baut deine Lebensrichtung tiefgreifend um. Das arbeitet leise, kostet aber täglich Kraft - wie ein Update, das im Hintergrund läuft.",
  "Nicht wundern, wenn die Energie schneller leer ist als sonst. Das ist Tiefenarbeit, kein Versagen."),
 ('Jupiter','Opposition','MC'): (
  "Jupiter spannt sich weiter gegen deinen MC - Möglichkeiten und Weite zerren an deiner Berufungsachse. Ideen wollen größer werden, während Pluto gleichzeitig das Alte abträgt.",
  "Ideen notieren, aber nicht heute umsetzen müssen. Sammeln reicht."),
 ('Uranus','Trigon','MC'): (
  "Uranus fließt harmonisch zu deinem MC - Erneuerung deiner Richtung geht gerade leicht, in kleinen Aha-Momenten und plötzlichen Einfällen.",
  "Wenn heute ein überraschender Gedanke zu deinem Weg auftaucht: aufschreiben. Das sind die echten."),
 ('Neptun','Sextil','MC'): (
  "Neptun schenkt deiner Berufung leise Inspiration - Visionen entstehen gerade im Ruhen und Träumen, nicht am Schreibtisch.",
  "Tagträume zulassen. Was im Halbschlaf oder unter der Dusche kommt, ist heute wertvoller als jede To-do-Liste."),
 ('Jupiter','Trigon','Jupiter'): (
  "Jupiter im Trigon zu deinem Jupiter - dein Wachstums- und Liebesplanet (Herrscher deines 7. Hauses) wird sanft geweitet. Ein wohlwollender Grundton unter allem, auch wenn der Tag schwer ist: Es wächst trotzdem etwas.",
  "Vertrauen. Auch ein Blob-Tag zahlt auf dein Wachstum ein."),
 ('Mars','Sextil','Mond'): (
  "Mars reicht deinem Mond die Hand - trotz allem ist heute ein Rest Kraft für das Nötigste da, dosiert und ruhig einsetzbar.",
  "Eine kleine Sache erledigen reicht. Nicht die Liste - eine Sache."),
 ('Uranus','Sextil','Jupiter'): (
  "Uranus unterstützt deinen Jupiter - Überraschendes kann heute Türen öffnen, gerade über Menschen und dein Umfeld.",
  "Offen bleiben für Unerwartetes von Freundinnen oder Kontakten."),
}

def generic_text(tn,nm,nn):
    dom = DOMAIN.get(nn,nn)
    if nm in GOOD:
        return (f"{tn} unterstützt heute dein Thema {dom} - hier läuft es leichter als sonst.",
                f"Begünstigt: alles rund um {dom} heute bewusst nutzen.")
    if nm in BAD:
        return (f"{tn} setzt dein Thema {dom} unter Spannung - hier hakt oder reibt es heute leichter.",
                f"Achtung bei {dom}: heute lieber nichts forcieren, Reibung nicht persönlich nehmen.")
    return (f"{tn} verstärkt heute dein Thema {dom} - die Energie ist gebündelt und direkt spürbar.",
            f"{dom} ist heute intensiviert - bewusst und dosiert damit umgehen.")

def deute(tn,nm,nn):
    if (tn,nm,nn) in SPEC: return SPEC[(tn,nm,nn)]
    return generic_text(tn,nm,nn)

# Tun/Lassen-Listen aus den Aspekten bauen
tun=[]; lassen=[]
for o,tn,nm,g,nn,retro in hits[:9]:
    txt,rat = deute(tn,nm,nn)
    if nm in GOOD and len(tun)<4: tun.append(rat)
    elif nm in BAD and len(lassen)<4: lassen.append(rat)
# Merkur-Status
merc_retro = sky['Merkur'][1]
if merc_retro:
    lassen.insert(0,"Merkur ist rückläufig: keine Verträge, keine endgültigen Klärungen, Missverständnis-Gefahr erhöht.")

# ===== DARIA-ABSCHNITT: heutiges Beziehungswetter =====
dhits = []
for tn,(td,retro) in sky.items():
    if tn=='Mond': lim=3
    else: lim=1.5
    for nn,nd in DARIA.items():
        diff=abs(td-nd)%360
        if diff>180: diff=360-diff
        for ang,(nm,g) in ASP.items():
            o=abs(diff-ang)
            if o<=lim: dhits.append((o,tn,nm,g,nn,retro))
dhits.sort()

# Beziehungs-relevante Deutungen fuer Darias Tages-Transite
DSPEC = {
 ('Merkur','Quadrat','Sonne'): "Merkur steht im Quadrat zu ihrer Sonne: Ihr Selbstwert ist heute leicht kratzbar, Worte treffen sie schneller als gemeint. Diskussionen eskalieren heute aus dem Nichts - nicht weil ihr nicht passt, sondern weil ihr Empfang gestört ist.",
 ('Merkur','Opposition','Neptun'): "Merkur opponiert ihren Neptun: Sie versteht heute leicht etwas anderes, als du sagst - und du liest vielleicht Dinge in ihre Worte, die nicht drin sind. Klassisches Missverständnis-Wetter.",
 ('Venus','Trigon','Uranus'): "Venus fließt zu ihrem Uranus im Beziehungshaus: Unter dem Nebel liegt heute eine überraschend warme, freie Note - ein unerwartet liebes Wort von ihr ist möglich, wenn kein Druck herrscht.",
 ('Mars','Sextil','Sonne'): "Mars stützt ihre Sonne: Sie hat heute etwas mehr Antrieb als zuletzt - gut für ihre eigenen Dinge, nicht unbedingt für Beziehungsklärung.",
 ('Sonne','Quadrat','Merkur'): "Die Sonne quadriert ihren Merkur: Ihr Kopf ist heute überlastet, Denken und Formulieren fällt ihr schwer. Kurze Nachrichten kommen besser an als lange.",
}
def ddeute(tn,nm,nn):
    if (tn,nm,nn) in DSPEC: return DSPEC[(tn,nm,nn)]
    dom={'Sonne':'ihren Kern','Mond':'ihr Gefühl','Merkur':'ihr Denken','Venus':'ihr Herz','Saturn':'ihre Schwere','Jupiter':'ihren Neuanfang','ASC':'ihr Auftreten','MC':'ihre Richtung','Neptun':'ihre Sehnsucht','Uranus':'ihren Freiraum','Pluto':'ihre Tiefe','NK':'ihren Weg','Mars':'ihren Antrieb'}.get(nn,nn)
    if nm in GOOD: return f"{tn} unterstützt heute {dom} - hier ist sie zugänglicher."
    if nm in BAD: return f"{tn} setzt {dom} unter Spannung - hier ist sie heute empfindlicher."
    return f"{tn} verstärkt heute {dom}."

daria_cards=[]
rat_daria=""
tense_count=sum(1 for o,tn,nm,g,nn,r in dhits[:5] if nm in BAD)
good_count=sum(1 for o,tn,nm,g,nn,r in dhits[:5] if nm in GOOD)
for o,tn,nm,g,nn,retro in dhits[:3]:
    daria_cards.append(f'<div class="dcard"><div class="dcard-head">{GL.get(tn,tn)} {tn} {g} ihre {nn} <span class="card-orb">{o:.2f}°</span></div><p>{ddeute(tn,nm,nn)}</p></div>')
if tense_count>=2:
    rat_daria="<b>Dein Umgang heute:</b> Ihr Empfang ist gestört - das ist Wetter, nicht ihr Herz. Diskussionen heute nicht vertiefen, nichts Grundsätzliches klären, kurz und warm bleiben. Ein einzelner lieber Satz wirkt heute mehr als jedes Klärungsgespräch. Wenn sie stichelt oder wirr wirkt: nicht persönlich nehmen, ruhiger Pol bleiben."
elif good_count>=2:
    rat_daria="<b>Dein Umgang heute:</b> Sie ist heute zugänglicher als zuletzt - ein guter Tag für Wärme, Leichtigkeit und echte Momente. Kein Druck nötig, einfach da sein."
else:
    rat_daria="<b>Dein Umgang heute:</b> Gemischtes Wetter bei ihr - warm bleiben, wenig erwarten, nichts forcieren. Was heute nicht klärbar ist, klärt sich an einem besseren Tag."

# ===== TAGES-FAZIT oben =====
MOON_HOUSE = {
 1:'Heute dreht sich alles um dich selbst - Auftreten, Körper, dein Ich.',
 2:'Fokus auf Körper, Sicherheit und das, was dir wirklich wichtig ist.',
 3:'Kommunikativer Tag: Austausch, Wege, Gespräche.',
 4:'Kokon-Tag: Zuhause, Rückzug, emotionale Basis.',
 5:'Tag für Freude, Spiel, Kreativität und Herz.',
 6:'Körper- und Alltagstag: Routinen, Gesundheit, die kleinen Dinge. Dein System verarbeitet heute viel körperlich.',
 7:'Beziehungstag: das Du steht im Zentrum.',
 8:'Tiefer Tag: Intimität, das Verborgene, intensive Gefühle und Träume.',
 9:'Weiter Blick: Sinn, Perspektive, das große Ganze.',
 10:'Berufung und Sichtbarkeit im Fokus.',
 11:'Freundinnen, Umfeld und Zukunft nähren dich heute.',
 12:'Rückzugstag: Ruhe, Träume, das Unbewusste ist laut.'}
strongest = hits[0] if hits else None
fazit = MOON_HOUSE.get(moon_house,'')
if strongest and strongest[0]<=1.5:
    o,tn,nm,g,nn,retro = strongest
    t,_ = deute(tn,nm,nn)
    fazit += " Der stärkste Aspekt heute: " + t.split(' - ')[0] + "."

# ===== HTML =====
CSS = """@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#FFF6F1;--card:#FCE4D6;--text:#3A1F14;--text-soft:#8A5A44;--indigo:#C1440E;--gold:#D9922E;--line:#F0CFB8;--harm:#4A7C59;--span:#B5502E;--konj:#7A5299;--slate:#3E6C7A;--slatebg:#E1E8E8;}
*{box-sizing:border-box;}body{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;padding:32px 20px 60px;}
.wrap{max-width:760px;margin:0 auto;}
.sign-header{display:flex;align-items:center;gap:14px;margin-bottom:18px;}
.sign-glyph{width:44px;height:44px;border-radius:50%;background:var(--indigo);color:var(--bg);display:flex;align-items:center;justify-content:center;font-size:22px;}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:4px;}
.sub{font-size:14px;color:var(--text-soft);}h1{font-family:'Caveat',cursive;font-weight:700;font-size:46px;line-height:1.05;margin:0 0 8px;color:var(--indigo);}
.back-link{font-size:12.5px;color:var(--indigo);font-family:'JetBrains Mono',monospace;display:inline-block;margin-bottom:22px;}
.mood{background:linear-gradient(135deg,var(--card),#F8D9C4);border:1px solid var(--line);border-radius:18px;padding:20px 24px;margin-bottom:22px;}
.mood-label{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.mood-moon{font-size:15px;font-weight:700;color:var(--indigo);margin-bottom:6px;}
.mood-text{font-size:14.5px;line-height:1.6;color:var(--text-soft);}
.dolass{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:8px;}
@media(max-width:560px){.dolass{grid-template-columns:1fr;}}
.dobox{background:var(--card);border-radius:16px;padding:16px 18px;border-top:4px solid var(--harm);}
.lassbox{background:var(--card);border-radius:16px;padding:16px 18px;border-top:4px solid var(--span);}
.dobox h3,.lassbox h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;}
.dobox h3{color:var(--harm);}.lassbox h3{color:var(--span);}
.dobox ul,.lassbox ul{margin:0;padding-left:18px;font-size:13.5px;line-height:1.6;color:var(--text-soft);}
.dobox li,.lassbox li{margin-bottom:8px;}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold);margin:32px 0 14px;font-weight:700;}
.sky{font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.9;color:var(--text-soft);background:var(--card);border-radius:14px;padding:16px 20px;border:1px solid var(--line);}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-bottom:12px;border-left:4px solid var(--line);}
.card.harm{border-left-color:var(--harm);}.card.span{border-left-color:var(--span);}.card.konj{border-left-color:var(--konj);}
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:7px;flex-wrap:wrap;}
.card-title{font-weight:700;font-size:15px;}
.card-orb{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold);}
.card p{margin:0 0 8px;font-size:14px;line-height:1.6;color:var(--text-soft);}
.card .rat{margin:0;font-size:13px;line-height:1.55;color:var(--indigo);font-weight:500;}
.dariabox{background:var(--slatebg);border:1px solid #CBD8D8;border-radius:18px;padding:20px 22px;margin-bottom:12px;}
.dariabox h3{margin:0 0 4px;font-size:15px;color:var(--slate);}
.dariabox .dsub{font-size:12.5px;color:#5E7480;margin-bottom:14px;}
.dcard{background:#F2F4F4;border-radius:12px;padding:12px 16px;margin-bottom:10px;}
.dcard-head{font-weight:700;font-size:13.5px;color:var(--slate);margin-bottom:4px;display:flex;justify-content:space-between;gap:8px;}
.dcard p{margin:0;font-size:13px;line-height:1.55;color:#5E7480;}
.drat{font-size:13.5px;line-height:1.6;color:#22333B;background:#E9EEEE;border-radius:12px;padding:12px 16px;}
.footer-note{margin-top:36px;padding-top:20px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--text-soft);line-height:1.6;}"""

def kat(nm):
    return {'Trigon':'harm','Sextil':'harm','Konjunktion':'konj','Quadrat':'span','Opposition':'span'}.get(nm,'')

sky_html = '<div class="sky">' + ' · '.join(f"{GL[n]} {sp(d)}" + (RSPAN if r else '') for n,(d,r) in sky.items()) + '</div>'

cards=[]
for o,tn,nm,g,nn,retro in hits[:8]:
    txt,rat = deute(tn,nm,nn)
    r = ' '+RSPAN if retro else ''
    cards.append(f'''<div class="card {kat(nm)}"><div class="card-head"><span class="card-title">{GL.get(tn,tn)} {tn}{r} {g} {GL.get(nn,nn)} {nn}</span><span class="card-orb">{o:.2f}°</span></div><p>{txt}</p><p class="rat">→ {rat}</p></div>''')
cards_html='\n'.join(cards) if cards else '<div class="card"><p>Heute keine engen Transite - ein freier Tag ohne kosmischen Druck.</p></div>'

tun_html=''.join(f'<li>{t}</li>' for t in tun) or '<li>Heute keine besonders begünstigten Bereiche - neutraler Tag.</li>'
lassen_html=''.join(f'<li>{l}</li>' for l in lassen) or '<li>Keine besonderen Warnungen heute.</li>'

daria_html=f'''<div class="dariabox"><h3>🌊 Daria heute - euer Beziehungswetter</h3>
<div class="dsub">Was gerade in ihr arbeitet und wie du ihr heute am besten begegnest</div>
{''.join(daria_cards)}
<div class="drat">{rat_daria}</div></div>'''

datum = f"{WD[now.weekday()]}, {now.day:02d}.{now.month:02d}.{now.year}"
html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Deine Transite heute</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="sign-header"><div class="sign-glyph">🌤️</div><div>
<div class="eyebrow">Astro Charlie · Heute</div><div class="sub">{datum} · Berlin</div></div></div>
<h1>Dein Tag, gedeutet.</h1>
<a class="back-link" href="../index.html">← zur Startseite</a>
<div class="mood"><div class="mood-label">Das Fazit für heute</div>
<div class="mood-moon">☽ Mond in {moon_sign} · dein {moon_house}. Haus</div>
<div class="mood-text">{fazit}</div></div>
<div class="dolass">
<div class="dobox"><h3>✓ Heute begünstigt</h3><ul>{tun_html}</ul></div>
<div class="lassbox"><h3>✕ Heute lieber lassen</h3><ul>{lassen_html}</ul></div>
</div>
<h2>Du & Daria</h2>
{daria_html}
<h2>Deine Transite im Detail</h2>
{cards_html}
<h2>Der ganze Himmel</h2>
{sky_html}
<div class="footer-note">Automatisch berechnet mit Swiss Ephemeris für {datum}, Berlin · Whole Sign. Aktualisiert sich jeden Morgen. Zu jeder Karte: erst was wirkt, dann (→) was du damit machst. Transite beschreiben Zeitqualitäten, keine festen Ereignisse.</div>
</div></body></html>"""
os.makedirs("heute", exist_ok=True)
open("heute/index.html","w",encoding="utf-8").write(html)
print(f"heute/ OK: {datum}, {len(hits)} Transite, Daria-Aspekte: {len(dhits)}")
