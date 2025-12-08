"""Generate a Circle Packing PNG from `data.json`.

This script creates `rawgraphs_repo/chart.png` (512x512) by packing circles
with sizes proportional to `investment`. It uses a simple greedy circle
placement algorithm to avoid overlaps. The visual styling uses a qualitative
colormap and places labels on circles when space allows.
"""

import json
import math
import os
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


def load_and_prepare(json_path, min_rows=15, seed=42):
    with open(json_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    rows = []
    for r in data:
        sector = r.get("sector", "Other")
        asset = r.get("asset", "Asset")
        invest = r.get("investment", 0)
        try:
            invest = int(invest)
        except Exception:
            invest = 0
        rows.append({"sector": sector, "asset": asset, "investment": invest})

    # Aggregate duplicates
    agg = defaultdict(int)
    for r in rows:
        key = (r["sector"], r["asset"])
        agg[key] += r["investment"]

    rows = [{"sector": k[0], "asset": k[1], "investment": v} for k, v in agg.items()]

    # Ensure at least min_rows by adding synthetic assets sampled from distribution
    random.seed(seed)
    if len(rows) < min_rows:
        investments = [r["investment"] for r in rows] or [1_000_000]
        mean = int(sum(investments) / len(investments))
        std = max(1, int(np.std(investments)))
        sectors = list({r["sector"] for r in rows}) or ["Other"]
        i = 1
        while len(rows) < min_rows:
            sector = random.choice(sectors)
            asset = f"{sector} Synthetic {i}"
            invest = max(50_000, int(random.gauss(mean, std)))
            rows.append({"sector": sector, "asset": asset, "investment": invest})
            i += 1

    # Sort descending by investment
    rows.sort(key=lambda x: x["investment"], reverse=True)
    return rows


def pack_circles(radii):
    """Greedy circle packing: place largest first, then place each new circle
    tangent to an existing circle at various angles until it doesn't overlap.
    Returns list of (x, y) positions matching radii order.
    """
    positions = []
    if not radii:
        return positions

    # Place first at origin
    positions.append((0.0, 0.0))

    for i in range(1, len(radii)):
        r = radii[i]
        placed = False
        # Try placing tangent to each existing circle
        for j, (xj, yj) in enumerate(positions):
            rj = radii[j]
            dist = r + rj
            # sample angles
            for theta in np.linspace(0, 2 * math.pi, 60, endpoint=False):
                xi = xj + dist * math.cos(theta)
                yi = yj + dist * math.sin(theta)
                ok = True
                for k, (xk, yk) in enumerate(positions):
                    rk = radii[k]
                    d = math.hypot(xi - xk, yi - yk)
                    if d < (r + rk) - 1e-6:
                        ok = False
                        break
                if ok:
                    positions.append((xi, yi))
                    placed = True
                    break
            if placed:
                break

        # Fallback: random jitter search expanding outward
        if not placed:
            angle_steps = np.linspace(0, 2 * math.pi, 90, endpoint=False)
            radius_step = max(1.5, max(radii) * 0.1)
            attempt = 1
            while not placed and attempt < 200:
                for theta in angle_steps:
                    dist = (max(radii) + r) * (1 + attempt * 0.05)
                    xi = dist * math.cos(theta)
                    yi = dist * math.sin(theta)
                    ok = True
                    for k, (xk, yk) in enumerate(positions):
                        rk = radii[k]
                        d = math.hypot(xi - xk, yi - yk)
                        if d < (r + rk) - 1e-6:
                            ok = False
                            break
                    if ok:
                        positions.append((xi, yi))
                        placed = True
                        break
                attempt += 1

        if not placed:
            # As last resort, place far away
            positions.append((len(positions) * (r * 2.5), 0.0))

    return positions


def draw_circle_packing(rows, out_path, size_px=512):
    investments = [r["investment"] for r in rows]
    # Radii proportional to sqrt(investment)
    areas = np.array(investments, dtype=float)
    radii = np.sqrt(areas)
    # Normalize radii to fit into canvas
    max_dim = size_px * 0.4
    if radii.max() > 0:
        radii = radii / radii.max() * max_dim
    else:
        radii[:] = 10

    # Pack circles
    pos = pack_circles(radii.tolist())
    xs = np.array([p[0] for p in pos])
    ys = np.array([p[1] for p in pos])

    # Center positions
    minx, maxx = xs.min() - radii.max(), xs.max() + radii.max()
    miny, maxy = ys.min() - radii.max(), ys.max() + radii.max()
    spanx = maxx - minx
    spany = maxy - miny
    # scale to image coords
    margin = 20
    scale = (size_px - 2 * margin) / max(spanx, spany)
    xs = (xs - minx) * scale + margin
    ys = (ys - miny) * scale + margin
    radii = radii * scale

    # Color mapping by sector
    sectors = [r["sector"] for r in rows]
    unique_sectors = sorted(set(sectors))
    cmap = plt.get_cmap("tab20")
    color_map = {s: cmap(i % cmap.N) for i, s in enumerate(unique_sectors)}

    fig, ax = plt.subplots(figsize=(size_px / 100, size_px / 100), dpi=100)
    ax.set_xlim(0, size_px)
    ax.set_ylim(0, size_px)
    ax.set_aspect("equal")
    ax.axis("off")

    for i, r in enumerate(rows):
        x, y = xs[i], ys[i]
        rad = radii[i]
        circ = plt.Circle(
            (x, y), rad, color=color_map[r["sector"]], ec="white", lw=1.2, alpha=0.95
        )
        ax.add_patch(circ)
        # label if enough space
        label = r["asset"]
        if rad > 18:
            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=max(6, int(rad / 4)),
                weight="bold",
                color="black",
            )

    # Legend (small)
    handles = [
        plt.Line2D(
            [0], [0], marker="o", color="w", markerfacecolor=color_map[s], markersize=8
        )
        for s in unique_sectors
    ]
    ax.legend(handles, unique_sectors, fontsize=6, loc="lower left", frameon=False)

    plt.tight_layout(pad=0)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "data.json")
    out_path = os.path.join(base_dir, "chart.png")
    out_path = os.path.normpath(out_path)

    if not os.path.exists(json_path):
        print("data.json not found in q6; cannot generate chart.")
        return

    rows = load_and_prepare(json_path, min_rows=15)
    draw_circle_packing(rows, out_path, size_px=512)
    print(f"Wrote circle-packing PNG to: {out_path}")


if __name__ == "__main__":
    main()
