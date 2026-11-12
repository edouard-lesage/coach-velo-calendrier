"""Génère seances.json (structure des séances Zwift) pour le tableau de bord.

Usage : python3 zwo_to_json.py [--out seances.json]
Une ligne par segment : seance, ordre, min, debut_pct, fin_pct, cadence.
"""
import argparse, glob, json, os
from render_zwo import parse, HERE

ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join(HERE, "seances.json"))
out = ap.parse_args().out
rows = []
for f in sorted(glob.glob(os.path.join(HERE, "zwo", "*.zwo"))):
    name, segs, _ = parse(f)
    for i, (d, a, b, cad) in enumerate(segs):
        rows.append({"seance": name, "ordre": i, "min": d, "debut_pct": a, "fin_pct": b, "cadence": cad})
json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, len(rows))
