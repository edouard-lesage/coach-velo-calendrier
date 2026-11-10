import datetime as dt
ev=[("2026-11-11","🧪 Ramp test Zwift + mobilité 10 min après","Poids 92,5 kg à jour dans Zwift. Aller jusqu'à l'échec. Noter la FC max atteinte. Objectif : mesurer la FTP. Vigilance : bien reposé, ventilateur, hydratation.\\nPas d'étirements statiques avant le test. Après : routine Post-vélo 10 min (Recover)."),
("2026-11-12","🟢 Récup 45 min Z1 (facultatif) + mobilité 10 min","< 140 W, cadence 85–95 rpm. Repos possible.\\nRoutine Post-vélo 10 min (Recover)."),
("2026-11-13","🧘 Mobilité + gainage ≈ 23 min (Recover)","Recover : 1) Quick loosen up with Nikki Hiltz (8 min) puis 2) Core with Heather Maclean (15 min : bird dog, dead bug, body hold, shoulder taps, shifting front planks)."),
("2026-11-14","🚴 Endurance facile ≤ 2 h + mobilité 10 min","Allure conversationnelle, FC < ~150, pas de chasse aux segments.\\nAprès : routine Post-vélo 10 min (Recover)."),
("2026-11-16","🧘 Mobilité douce 20 min (Recover)","Recover : Post ride full body stretch and roll (20 min, rouleau). Aucun renfo : test LTHR le lendemain."),
("2026-11-17","🧪 Test LTHR vélo 30 min + mobilité 10 min après","Échauffement 15 min : 10 min progressif 120→170 W, 3×30 s @ ~100 rpm/200 W (r30 s), 3 min facile.\\n30 min effort max régulier, départ à 95 % de la FTP du ramp test, accélérer après 20 min, 85–95 rpm, ERG off.\\nRetour au calme 10 min Z1.\\nRésultat : LTHR = FC moyenne des 20 dernières minutes.\\nPas d'étirements statiques avant. Après : routine Post-vélo 10 min."),
("2026-11-18","🟢 Récup 30–40 min Z1 (facultatif) + mobilité 10 min","Très facile ou repos.\\nRoutine Post-vélo 10 min (Recover)."),
("2026-11-20","🧪 Test FC max course à pied (côte) + mobilité 10 min après","Échauffement 15 min + 3 accélérations de 20 s. Côte de 2–3 min : montée 1 ≈ 80 %, montée 2 ≈ 90 %, montée 3 à fond avec sprint final de 30 s. Retour au calme 10 min.\\nVigilance : arrêt immédiat si douleur thoracique, vertige ou palpitations.\\nAprès : mobilité 10 min (mollets, ischios, psoas).")]
now=dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Amedee Railleur//Coach cycliste//FR","CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:Coach vélo – Amédée","X-WR-TIMEZONE:Europe/Paris"]
for d,s,desc in ev:
    d0=dt.date.fromisoformat(d); d1=d0+dt.timedelta(days=1)
    L+=["BEGIN:VEVENT",f"UID:{d.replace('-','')}-coach@amedee-coach",f"DTSTAMP:{now}",f"DTSTART;VALUE=DATE:{d0:%Y%m%d}",f"DTEND;VALUE=DATE:{d1:%Y%m%d}",f"SUMMARY:{s}",f"DESCRIPTION:{desc}","TRANSP:TRANSPARENT","END:VEVENT"]
L.append("END:VCALENDAR")
# fold lines >75 octets
out=[]
for l in L:
    b=l.encode()
    while len(b)>75:
        cut=75
        while (b[cut]&0xC0)==0x80: cut-=1
        out.append(b[:cut].decode()); b=b" "+b[cut:]
    out.append(b.decode())
open("coach-velo.ics","w",newline="").write("\r\n".join(out)+"\r\n")
