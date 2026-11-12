# Coach vélo – calendrier

Abonnement iCal : webcal://raw.githubusercontent.com/edouard-lesage/coach-velo-calendrier/main/coach-velo.ics

Les scripts se lancent depuis n'importe quel dossier : ils lisent et écrivent les données à la racine du repo.

## Calendrier d'activités
- `calendrier/generate_ics.py` : génère `coach-velo.ics` à la racine (le fichier doit y rester, l'abonnement iCal pointe dessus). `python3 calendrier/generate_ics.py`

## Séances Zwift
- `zwo/` : fichiers .zwo des séances structurées (copie de référence de ceux installés dans Zwift).
- `zwift/zwo_to_json.py` : génère `seances.json` (structure des séances) pour le profil au survol du tableau de bord. À relancer après chaque ajout de séance .zwo, puis remplacer le fichier « seances.json » du tableau de bord.

## Images d'activités
- `images/render_zwo.py` : rend une séance en image façon Zwift. `python3 images/render_zwo.py "AR B1 - Endurance cadence 68" --ftp 205 --out seance.png` (nécessite matplotlib).

## Récupération intervals.icu
- `intervals/get_intervals_wellnes.py` : exporte les données bien-être en CSV (90 derniers jours par défaut). Identifiants dans `.env` (non versionné) : `INTERVALS_ATHLETE_ID`, `INTERVALS_API_KEY`. `python3 intervals/get_intervals_wellnes.py`
