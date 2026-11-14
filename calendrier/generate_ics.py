import datetime as dt
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo
ev=[("2026-11-11","🚴 Sortie entre amis 75 km / 780 m D+ (Versailles)","Parcours Komoot « Versailles - Chez Cedric » (≈ 3h30). Rester majoritairement en Z2 (115–155 W), montées sous ~175 W, laisser filer les accélérations du groupe.\\nManger toutes les 45 min dès le départ : 2 bidons dont 1 glucidique + 2 barres/gels.\\nAprès : routine Post-vélo 10 min (Recover)."),
("2026-11-12","🧘 Gainage 15 min (Recover) – pas de vélo","Recover : Core with Heather Maclean (15 min, intensité modérée) + routine Post-vélo (11 min).\\nVélo retiré après la sortie du 11/11 (récupération)."),
("2026-11-13","🧘 Mobilité douce 20 min (Recover)","Recover : Post ride full body stretch and roll (20 min, rouleau). Aucun renfo ni gainage intense : ramp test le lendemain. Coucher tôt."),
("2026-11-14","🧪 Ramp test Zwift + mobilité 10 min après","Poids à jour dans Zwift. Aller jusqu'à l'échec. Noter la FC max atteinte. Objectif : mesurer la FTP.\\nJambes encore lourdes de la sortie du 11 : décaler au 15/11.\\nPas d'étirements statiques avant le test. Après : routine Post-vélo 10 min (Recover)."),
("2026-11-16","🧘 Mobilité douce 20 min (Recover)","Recover : Post ride full body stretch and roll (20 min, rouleau). Aucun renfo : test LTHR le lendemain."),
("2026-11-17","🧪 Test LTHR vélo 30 min + mobilité 10 min après","Échauffement 15 min : 10 min progressif 120→170 W, 3×30 s @ ~100 rpm/200 W (r30 s), 3 min facile.\\n30 min effort max régulier, départ à 95 % de la FTP du ramp test, accélérer après 20 min, 85–95 rpm, ERG off.\\nRetour au calme 10 min Z1.\\nRésultat : LTHR = FC moyenne des 20 dernières minutes.\\nPas d'étirements statiques avant. Après : routine Post-vélo 10 min."),
("2026-11-18","🟢 Récup 30–40 min Z1 (facultatif) + mobilité 10 min","Très facile ou repos.\\nRoutine Post-vélo 10 min (Recover)."),
("2026-11-20","🧪 Test FC max course à pied (côte) + mobilité 10 min après","Échauffement 15 min + 3 accélérations de 20 s. Côte de 2–3 min : montée 1 ≈ 80 %, montée 2 ≈ 90 %, montée 3 à fond avec sprint final de 30 s. Retour au calme 10 min.\\nVigilance : arrêt immédiat si douleur thoracique, vertige ou palpitations.\\nAprès : mobilité 10 min (mollets, ischios, psoas)."),
("2026-11-23","🧘 Mobilité 20 min (Recover)","Recover : Post ride full body stretch and roll (20 min)."),
("2026-11-24","🚴 HT 60 min – AR B1 Endurance cadence 68","Zwift > Custom Workouts : AR B1 - Endurance cadence 68.\\n10 min échauffement 50→65 %, 40 min à 68 % FTP avec 6 × 1 min à 100–110 rpm, 10 min retour au calme.\\nAprès : routine Post-vélo 10 min (Recover).\\nNutrition : repas 2–3 h avant ou collation 1 h avant. Pendant : 750 ml eau + électrolytes ; 1 pâte de fruits vers 25 min si dernier repas > 3 h. Après : protéines + glucides dans l'heure."),
("2026-11-25","🚴 HT 75 min – AR B1 Force-endurance 4x6","Zwift > Custom Workouts : AR B1 - Force-endurance 4x6.\\n15 min échauffement, 4 × 6 min à 80 % FTP à 60–65 rpm assis (récup 4 min à 60 %), 10 min Z2, 10 min retour au calme.\\nAprès : routine Post-vélo 10 min (Recover).\\nNutrition : repas 2–3 h avant ou collation 1 h avant. Pendant : 750 ml avec 30 g de glucides, ou eau + électrolytes + 1 gel à la 2e récup. Après : protéines + glucides dans l'heure."),
("2026-11-26","🚴 Sortie longue 2h15 Z2 (extérieur)","Avancée du samedi (déplacement le 28, vendredi indisponible). Z2 stricte : 56–75 % FTP, soit 138–185 W avec la FTP provisoire de 246 W. Pas de chasse aux segments, montées en petit braquet. Lendemain de force-endurance : si jambes lourdes, rester en bas de Z2.\\nNutrition : 40–60 g de glucides/h dès le départ (1 bidon glucidique + 1 barre ou gel par heure).\\nSi pluie : 1h15 HT Z2 + 30 min footing facile ou marche.\\nAprès : routine Post-vélo 10 min (Recover)."),
("2026-11-27","💪 Renfo 20 min – Glute and Core Strength (Recover)","Séance renfo A, créneau de midi avant le train."),
("2026-11-28","🧘 Gainage 15 min + footing facile optionnel (canal du Midi)","En déplacement. Recover : Core with Heather Maclean (15 min, faisable à l'hôtel).\\nFooting optionnel 30–40 min sur le plat, allure conversationnelle, arrêt si douleur.\\nAprès : routine Post-vélo 10 min (Recover)."),
("2026-11-30","🧘 Mobilité 20 min (Recover)","Recover : Post ride full body stretch and roll (20 min)."),
("2026-12-01","🚴 HT 60 min – AR B1 Endurance cadence 70","Zwift > Custom Workouts : AR B1 - Endurance cadence 70.\\n40 min à 70 % FTP avec 6 × 1 min à 100–110 rpm.\\nAprès : routine Post-vélo 10 min (Recover).\\nNutrition : repas 2–3 h avant ou collation 1 h avant. Pendant : 750 ml eau + électrolytes ; 1 pâte de fruits vers 25 min si dernier repas > 3 h. Après : protéines + glucides dans l'heure."),
("2026-12-02","💪 Renfo 20 min – Bodyweight strength for cyclists (Recover)","Séance renfo B."),
("2026-12-03","🚴 HT 75 min – AR B1 Force-endurance 4x8","Zwift > Custom Workouts : AR B1 - Force-endurance 4x8.\\n15 min échauffement, 4 × 8 min à 80 % FTP à 60–65 rpm assis (récup 4 min à 60 %), 12 min retour au calme.\\nAprès : routine Post-vélo 10 min (Recover).\\nNutrition : repas 2–3 h avant ou collation 1 h avant. Pendant : 750 ml avec 30 g de glucides, ou eau + électrolytes + 1 gel à la 2e récup. Après : protéines + glucides dans l'heure."),
("2026-12-04","🧘 Gainage 15 min – Core with Heather Maclean (Recover)","Gainage sans jambes."),
("2026-12-05","🚴 Sortie longue 2h45 Z2 (extérieur)","Z2 stricte. Manger toutes les 45 min dès le départ.\\nSi pluie : 1h15 HT Z2 + 30 min footing facile ou marche.\\nAprès : routine Post-vélo 10 min (Recover)."),
("2026-12-06","🚴 HT 45 min – AR B1 Z2 continu 45","Zwift > Custom Workouts : AR B1 - Z2 continu 45.\\n30 min à 65 % FTP, cadence libre.\\nAprès : routine Post-vélo 10 min (Recover).\\nNutrition : jamais à jeun. Pendant : 500–750 ml eau + électrolytes, pas de glucides. Après : protéines + glucides dans l'heure.")]
now=dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Amedee Railleur//Coach cycliste//FR","CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:Coach vélo – Amédée","X-WR-TIMEZONE:Europe/Paris","REFRESH-INTERVAL;VALUE=DURATION:PT1H","X-PUBLISHED-TTL:PT1H"]
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
open(os.path.join(ROOT, "coach-velo.ics"),"w",newline="").write("\r\n".join(out)+"\r\n")
