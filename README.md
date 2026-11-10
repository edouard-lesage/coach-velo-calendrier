# Coach vélo – calendrier

Abonnement iCal : webcal://raw.githubusercontent.com/edouard-lesage/coach-velo-calendrier/main/coach-velo.ics

## Séances Zwift
- `zwo/` : fichiers .zwo des séances structurées (copie de référence de ceux installés dans Zwift).
- `render_zwo.py` : rend une séance en image façon Zwift. `python3 render_zwo.py "AR B1 - Endurance cadence 68" --ftp 205 --out seance.png` (nécessite matplotlib).
- `zwo_to_json.py` : génère `seances.json` (structure des séances) pour le profil au survol du tableau de bord. À relancer après chaque ajout de séance .zwo, puis remplacer le fichier « seances.json » du tableau de bord.
