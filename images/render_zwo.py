"""Rend une séance Zwift (.zwo) en image PNG façon Zwift.

Usage : python3 images/render_zwo.py <fichier.zwo | nom de séance> [--ftp 205] [--out seance.png]
Le nom de séance (ex. « AR B1 - Endurance cadence 68 ») est cherché dans le dossier zwo/.
"""
import argparse, glob, os, sys
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du repo
ZONES = [("Z1", 55, "#8a8a8a"), ("Z2", 75, "#3b82f6"), ("Z3", 90, "#4caf50"),
         ("Z4", 105, "#f4c430"), ("Z5", 120, "#f26b3a"), ("Z6", 999, "#e53935")]


def zone(p):
    for z in ZONES:
        if p <= z[1]:
            return z
    return ZONES[-1]


def find(arg):
    if os.path.isfile(arg):
        return arg
    for f in glob.glob(os.path.join(ROOT, "zwo", "*.zwo")):
        n = ET.parse(f).getroot().findtext("name") or ""
        if n.strip().lower() == arg.strip().lower():
            return f
    sys.exit(f"Séance introuvable : {arg}")


def parse(path):
    root = ET.parse(path).getroot()
    segs, groups = [], []  # segs: (min, from, to, cad)
    for e in root.find("workout"):
        a = e.attrib
        cad = int(a["Cadence"]) if "Cadence" in a else None
        if e.tag in ("Warmup", "Cooldown", "Ramp"):
            d = int(a["Duration"]) / 60
            s = (d, round(float(a["PowerLow"]) * 100, 1), round(float(a["PowerHigh"]) * 100, 1), cad)
            segs.append(s); groups.append((1, [s]))
        elif e.tag == "SteadyState":
            d = int(a["Duration"]) / 60
            s = (d, round(float(a["Power"]) * 100, 1), round(float(a["Power"]) * 100, 1), cad)
            segs.append(s); groups.append((1, [s]))
        elif e.tag == "IntervalsT":
            n = int(a["Repeat"])
            on = (int(a["OnDuration"]) / 60, round(float(a["OnPower"]) * 100, 1), round(float(a["OnPower"]) * 100, 1),
                  int(a["Cadence"]) if "Cadence" in a else None)
            off = (int(a["OffDuration"]) / 60, round(float(a["OffPower"]) * 100, 1), round(float(a["OffPower"]) * 100, 1),
                   int(a["CadenceResting"]) if "CadenceResting" in a else None)
            for _ in range(n):
                segs += [on, off]
            groups.append((n, [on, off]))
    return root.findtext("name"), segs, groups


def fmt(m):
    return f"{m:g} min"


def render(path, ftp, out):
    name, segs, groups = parse(path)
    W = lambda p: round(p * ftp / 100)
    total = sum(s[0] for s in segs)
    zmin = {z[0]: 0.0 for z in ZONES}
    tss = 0.0
    for d, a, b, _ in segs:
        n = int(d * 4)
        for k in range(n):
            p = a + (b - a) * (k + 0.5) / n
            zmin[zone(p)[0]] += 0.25
            tss += 0.25 / 60 * (p / 100) ** 2 * 100

    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(10, 5.2), dpi=150)
    fig.text(0.04, 0.94, name, fontsize=15, fontweight="bold", color="#222")
    fig.text(0.04, 0.89, f"Durée {total:g} min · stress ≈ {round(tss)} TSS · FTP {ftp} W",
             fontsize=10, color="#666")

    ax = fig.add_axes([0.04, 0.42, 0.92, 0.42])
    ax.set_xlim(0, total); ax.set_ylim(0, 130); ax.axis("off")
    x = 0
    gap = total * 0.002
    for d, a, b, _ in segs:
        c = zone((a + b) / 2)[2]
        if a == b:
            ax.add_patch(FancyBboxPatch((x + gap, 0), max(d - 2 * gap, 0.05), a,
                                        boxstyle=f"round,pad=0,rounding_size={min(d * 0.3, 1.2)}",
                                        mutation_aspect=4, fc=c, ec="none"))
        else:
            ax.add_patch(Polygon([(x + gap, 0), (x + gap, a), (x + d - gap, b), (x + d - gap, 0)],
                                 closed=True, fc=c, ec="none"))
        x += d
    ax.axhline(100, ls=(0, (4, 4)), color="#999", lw=1)
    ax.text(total, 103, f"FTP {ftp} W", ha="right", va="bottom", fontsize=9, color="#666")
    ax.axhline(0, color="#bbb", lw=1)

    y = 0.33
    for n, gr in groups:
        def one(s):
            d, a, b, cad = s
            t = f"{fmt(d)} @ {W(a)} W" if a == b else f"{fmt(d)} de {W(a)} à {W(b)} W"
            return t + (f" ({cad} rpm)" if cad and a == b else "")
        txt = (f"{n} x " if n > 1 else "") + ", ".join(one(s) for s in gr)
        col = zone(max(max(s[1], s[2]) for s in gr))[2]
        fig.patches.append(FancyBboxPatch((0.04, y - 0.012), 0.006, 0.032, transform=fig.transFigure,
                                          boxstyle="round,pad=0,rounding_size=0.002", fc=col, ec="none"))
        fig.text(0.055, y, txt, fontsize=10, color="#222", va="bottom")
        y -= 0.055

    fig.text(0.70, 0.33, "Temps par zone", fontsize=10, color="#666", va="bottom")
    zmax = max(max(zmin.values()), 1)
    for i, (z, _, c) in enumerate(ZONES):
        yy = 0.28 - i * 0.045
        fig.text(0.70, yy, z, fontsize=9, color="#666", va="bottom")
        w = zmin[z] / zmax * 0.16
        if w:
            fig.patches.append(FancyBboxPatch((0.735, yy), w, 0.028, transform=fig.transFigure,
                                              boxstyle="round,pad=0,rounding_size=0.004", fc=c, ec="none"))
        fig.text(0.745 + w, yy, f"{round(zmin[z])} min" if zmin[z] else "–", fontsize=9, color="#222",
                 va="bottom")
    fig.savefig(out, facecolor="white")
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("seance")
    ap.add_argument("--ftp", type=int, default=205)
    ap.add_argument("--out", default="seance.png")
    a = ap.parse_args()
    render(find(a.seance), a.ftp, a.out)
