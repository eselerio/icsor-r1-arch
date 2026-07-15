"""Generate the journal graphical abstract as a deterministic vector PDF.

The composition deliberately separates invariant-aware *training* from the
hard correction used for deployed outputs.  Run this file from any directory:

    .venv/Scripts/python.exe tools/generate_graphical_abstract.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import (
    Circle,
    FancyArrowPatch,
    FancyBboxPatch,
    PathPatch,
    Polygon,
    Rectangle,
)
from matplotlib.path import Path as MplPath


REPO_ROOT = Path(__file__).resolve().parents[1]
PATHS_CONFIG = json.loads((REPO_ROOT / "config" / "paths.json").read_text(encoding="utf-8"))
OUTPUT_PATH = REPO_ROOT / PATHS_CONFIG["submission_asset_dir"] / "graphical_abstract.pdf"

FIGURE_WIDTH = 13.3333333333
FIGURE_HEIGHT = 6.0

NAVY = "#173F67"
LIGHT_BLUE = "#A9CDED"
PLUM = "#5A124E"
LIGHT_PLUM = "#EBC8E9"
MID_PLUM = "#D98CD4"
GREEN = "#3FA34D"
LIGHT_GREEN = "#8BD36A"
INK = "#263442"
MUTED = "#647381"
CYAN = "#17DDE0"
PALE_GREEN = "#F0F8EC"
WHITE = "#FFFFFF"


def rounded_panel(
    ax: Axes, x: float, y: float, width: float, height: float, color: str
) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.72",
            linewidth=5.2,
            edgecolor=color,
            facecolor=WHITE,
            joinstyle="round",
            zorder=2,
        )
    )


def check_mark(ax: Axes, x: float, y: float, radius: float = 0.23) -> None:
    ax.add_patch(Circle((x, y), radius, facecolor=GREEN, edgecolor="none", zorder=8))
    ax.plot(
        [x - 0.12, x - 0.035, x + 0.14],
        [y - 0.005, y - 0.105, y + 0.105],
        color=WHITE,
        linewidth=3.6,
        solid_capstyle="round",
        solid_joinstyle="round",
        zorder=9,
    )


def draw_cstr(ax: Axes) -> None:
    """Draw the steady-state reactor and a compact nitrogen-pathway inset."""
    vessel_vertices = [
        (0.67, 3.45),
        (0.67, 3.72),
        (1.08, 3.82),
        (1.54, 3.82),
        (2.30, 3.82),
        (2.30, 3.45),
        (2.30, 1.12),
        (2.30, 0.91),
        (1.93, 0.80),
        (1.50, 0.80),
        (1.05, 0.80),
        (0.67, 0.94),
        (0.67, 1.12),
        (0.67, 3.45),
    ]
    vessel_codes = [
        MplPath.MOVETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.LINETO,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CLOSEPOLY,
    ]
    vessel_path = MplPath(vessel_vertices, vessel_codes)
    vessel_fill = PathPatch(vessel_path, facecolor=WHITE, edgecolor="none", zorder=3)
    ax.add_patch(vessel_fill)
    liquid = Rectangle((0.67, 2.01), 1.63, 1.72, facecolor=CYAN, edgecolor="none", zorder=4)
    liquid.set_clip_path(vessel_fill)
    ax.add_patch(liquid)
    ax.plot([0.68, 2.29], [2.01, 2.01], color="#0BA8B0", linewidth=1.3, zorder=5)
    ax.add_patch(PathPatch(vessel_path, facecolor="none", edgecolor="#111111", linewidth=1.3, zorder=6))

    # Feed, effluent, shaft, and impeller.
    ax.plot([0.43, 1.08, 1.08], [4.06, 4.06, 3.58], color="#111111", linewidth=1.4, zorder=7)
    ax.add_patch(
        FancyArrowPatch(
            (1.08, 3.83),
            (1.08, 3.44),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.2,
            color="#111111",
            zorder=7,
        )
    )
    ax.plot([2.30, 2.68], [1.87, 1.87], color="#111111", linewidth=1.3, zorder=7)
    ax.add_patch(
        FancyArrowPatch(
            (2.55, 1.87),
            (2.72, 1.87),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.2,
            color="#111111",
            zorder=7,
        )
    )
    ax.plot([1.49, 1.49], [4.43, 1.24], color="#111111", linewidth=1.35, zorder=7)
    ax.add_patch(Polygon([(1.49, 1.24), (1.10, 1.48), (1.10, 1.02)], closed=True, color="#111111", zorder=7))
    ax.add_patch(Polygon([(1.49, 1.24), (1.88, 1.48), (1.88, 1.02)], closed=True, color="#111111", zorder=7))

    ax.text(0.43, 4.18, r"$\mathbf{u},\,\mathbf{c}_{in}$", color=NAVY, fontsize=12.5, fontweight="bold")
    ax.text(2.48, 2.02, r"$\hat{\mathbf{c}}$", color=NAVY, fontsize=12.5, fontweight="bold")
    ax.text(1.49, 0.98, "ASM2d-TSN", ha="center", va="bottom", color=NAVY, fontsize=11.7, fontweight="bold", zorder=8)

    ax.text(
        2.45,
        4.53,
        "20 states\n28 reactions\n10,000 samples",
        ha="left",
        va="top",
        color=NAVY,
        fontsize=12.2,
        fontweight="bold",
        linespacing=1.34,
        zorder=8,
    )

    # Nitrogen-removal pathway inset: a simplified vector counterpart to the
    # biological illustration in the earlier abstract.
    cx, cy, radius = 3.34, 1.27, 0.78
    ax.add_patch(Circle((cx, cy), radius, facecolor=WHITE, edgecolor="#111111", linewidth=1.2, zorder=7))
    ax.text(cx, cy + 0.60, "N-removal pathways", ha="center", fontsize=6.8, fontweight="bold", color=INK, zorder=8)
    nodes = {
        r"NH$_4^+$": (3.09, 1.66),
        r"NO$_2^-$": (2.91, 1.08),
        r"NO$_3^-$": (3.16, 0.72),
        r"N$_2$": (3.72, 0.80),
        "Organic N": (3.68, 1.56),
    }
    for label, (nx, ny) in nodes.items():
        ax.add_patch(Circle((nx, ny), 0.045, facecolor=PLUM, edgecolor=WHITE, linewidth=0.6, zorder=9))
        offset_y = 0.10 if label != "Organic N" else 0.09
        ax.text(nx, ny + offset_y, label, ha="center", va="center", fontsize=5.7, color=INK, zorder=9)
    pathway_edges = [
        ((3.08, 1.58), (2.95, 1.17), "#2A9D4B"),
        ((2.98, 1.00), (3.12, 0.79), "#2A9D4B"),
        ((3.23, 0.71), (3.63, 0.79), "#BC5A16"),
        ((3.65, 1.50), (3.20, 1.64), "#BC5A16"),
    ]
    for start, end, color in pathway_edges:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                connectionstyle="arc3,rad=0.15",
                mutation_scale=7,
                linewidth=1.7,
                color=color,
                zorder=8,
            )
        )


def card(ax: Axes, x: float, y: float, width: float, height: float) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=0,
            facecolor=LIGHT_PLUM,
            zorder=6,
        )
    )


def draw_icsor_pipeline(ax: Axes) -> None:
    x, width = 5.02, 3.40
    # A central spine makes the sequence readable before the individual labels.
    ax.add_patch(Rectangle((6.58, 4.83), 0.39, 0.20, facecolor=PLUM, edgecolor="none", zorder=3))
    ax.add_patch(Rectangle((6.65, 1.04), 0.25, 3.88, facecolor=PLUM, edgecolor="none", zorder=3))
    ax.add_patch(Polygon([(6.42, 1.18), (7.13, 1.18), (6.775, 0.79)], closed=True, facecolor=PLUM, edgecolor="none", zorder=3))

    card(ax, x, 4.22, width, 0.62)
    ax.text(
        x + width / 2,
        4.53,
        r"Inputs: $\mathbf{u},\,\mathbf{c}_{in},\,\phi(\mathbf{u},\mathbf{c}_{in})$",
        ha="center",
        va="center",
        fontsize=12.0,
        color=PLUM,
        zorder=7,
    )

    card(ax, x, 3.49, width, 0.60)
    ax.text(x + width / 2, 3.88, "Coupled driver", ha="center", va="center", fontsize=10.6, color=PLUM, zorder=7)
    ax.text(
        x + width / 2,
        3.66,
        r"$\mathbf{d}=\mathbf{B}\phi,\quad \mathbf{R}=\mathbf{I}-\mathbf{\Gamma}$",
        ha="center",
        va="center",
        fontsize=12.0,
        color=PLUM,
        fontweight="bold",
        zorder=7,
    )

    card(ax, x, 2.65, width, 0.70)
    ax.text(
        x + width / 2,
        3.08,
        "Invariant-aware regression head",
        ha="center",
        va="center",
        fontsize=11.5,
        color=PLUM,
        fontweight="bold",
        zorder=7,
    )
    ax.text(
        x + width / 2,
        2.82,
        "soft training penalties",
        ha="center",
        va="center",
        fontsize=10.0,
        color=PLUM,
        fontstyle="italic",
        zorder=7,
    )

    card(ax, x, 1.74, width, 0.76)
    ax.text(
        x + width / 2,
        2.25,
        "Hard deployment correction:",
        ha="center",
        va="center",
        fontsize=10.6,
        color=PLUM,
        fontweight="bold",
        zorder=7,
    )
    ax.text(
        x + width / 2,
        1.97,
        "Raw → Affine → LP",
        ha="center",
        va="center",
        fontsize=13.2,
        color=PLUM,
        fontweight="bold",
        zorder=7,
    )

    card(ax, x, 1.02, width, 0.58)
    ax.text(
        x + width / 2,
        1.31,
        r"Physically admissible state $\hat{\mathbf{c}}$",
        ha="center",
        va="center",
        fontsize=11.2,
        color=PLUM,
        zorder=7,
    )

    check_mark(ax, 5.34, 0.63, radius=0.22)
    ax.text(5.64, 0.78, "Mass conservation", ha="left", va="center", fontsize=8.8, color=PLUM, fontweight="bold", zorder=9)
    ax.text(5.64, 0.50, r"$\mathbf{A}\hat{\mathbf{c}}=\mathbf{A}\mathbf{c}_{in}$", ha="left", va="center", fontsize=10.2, color=PLUM, zorder=9)

    check_mark(ax, 7.28, 0.63, radius=0.22)
    ax.text(7.58, 0.78, "Non-negativity", ha="left", va="center", fontsize=8.8, color=PLUM, fontweight="bold", zorder=9)
    ax.text(7.58, 0.50, r"$\hat{\mathbf{c}}\geq\mathbf{0}$", ha="left", va="center", fontsize=10.2, color=PLUM, zorder=9)


def draw_benchmark_plot(fig: Figure) -> None:
    """Draw the three fixed-split RMSE values discussed in the revised Abstract."""
    chart = fig.add_axes([9.63 / FIGURE_WIDTH, 2.64 / FIGURE_HEIGHT, 3.13 / FIGURE_WIDTH, 1.82 / FIGURE_HEIGHT])
    model_labels = ["MLP", "LightGBM", "ICSOR"]
    rmse_values = np.array([4.38, 5.30, 5.98], dtype=float)
    colors = ["#577590", "#2A9D8F", PLUM]
    positions = np.arange(len(model_labels))
    bars = chart.barh(positions, rmse_values, color=colors, height=0.55, edgecolor=INK, linewidth=0.45)
    for bar, value in zip(bars, rmse_values, strict=True):
        chart.text(
            value + 0.10,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}",
            va="center",
            ha="left",
            fontsize=7.1,
            color=INK,
            fontweight="bold",
        )
    chart.set_title("Aggregate test RMSE (lower is better)", fontsize=8.2, pad=4, color=INK)
    chart.set_xlabel("RMSE", fontsize=7.2, labelpad=2)
    chart.set_xlim(0, 6.7)
    chart.set_yticks(positions, labels=model_labels)
    chart.invert_yaxis()
    chart.tick_params(axis="both", labelsize=6.8, colors=MUTED, length=2)
    chart.grid(True, axis="x", color="#DDE5EA", linestyle=":", linewidth=0.55)
    chart.set_axisbelow(True)
    chart.spines[["top", "right"]].set_visible(False)
    chart.spines[["left", "bottom"]].set_color("#9DAAB4")
    chart.spines[["left", "bottom"]].set_linewidth(0.7)


def draw_deployment_summary(ax: Axes) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (9.46, 1.20),
            3.28,
            1.18,
            boxstyle="round,pad=0.03,rounding_size=0.16",
            facecolor=PALE_GREEN,
            edgecolor="#C8E8BE",
            linewidth=0.9,
            zorder=4,
        )
    )
    ax.text(9.62, 2.16, "Final deployed outputs:", ha="left", va="center", fontsize=11.2, color="#245E1D", fontweight="bold", zorder=7)
    check_mark(ax, 9.69, 1.79, radius=0.16)
    ax.text(9.94, 1.79, "0% conservation violations", ha="left", va="center", fontsize=10.8, color="#245E1D", fontweight="bold", zorder=7)
    check_mark(ax, 9.69, 1.43, radius=0.16)
    ax.text(9.94, 1.43, "0% non-negativity violations", ha="left", va="center", fontsize=10.8, color="#245E1D", fontweight="bold", zorder=7)

    check_mark(ax, 9.72, 0.71, radius=0.22)
    ax.text(10.03, 0.71, "Interpretable", ha="left", va="center", fontsize=10.6, color="#245E1D", fontweight="bold", zorder=7)
    check_mark(ax, 11.43, 0.71, radius=0.22)
    ax.text(
        11.74,
        0.71,
        "Moderate RMSE\ntradeoff",
        ha="left",
        va="center",
        fontsize=9.8,
        color="#245E1D",
        fontweight="bold",
        linespacing=1.05,
        zorder=7,
    )


def build_figure() -> Figure:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "mathtext.fontset": "dejavusans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "savefig.facecolor": WHITE,
        }
    )
    fig = plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIGURE_WIDTH)
    ax.set_ylim(0, FIGURE_HEIGHT)
    ax.axis("off")

    # Broad process arrows sit behind the three panels.
    ax.add_patch(Polygon([(4.22, 2.54), (4.58, 2.54), (4.58, 2.25), (5.00, 2.85), (4.58, 3.45), (4.58, 3.15), (4.22, 3.15)], closed=True, facecolor=LIGHT_BLUE, edgecolor="none", zorder=1))
    ax.add_patch(Polygon([(8.71, 2.54), (9.07, 2.54), (9.07, 2.25), (9.49, 2.85), (9.07, 3.45), (9.07, 3.15), (8.71, 3.15)], closed=True, facecolor=MID_PLUM, edgecolor="none", zorder=1))

    rounded_panel(ax, 0.15, 0.31, 4.20, 5.00, LIGHT_BLUE)
    rounded_panel(ax, 4.60, 0.31, 4.20, 5.00, MID_PLUM)
    rounded_panel(ax, 9.05, 0.31, 4.13, 5.00, LIGHT_GREEN)

    ax.text(2.25, 5.58, "Steady-State CSTR Simulation", ha="center", va="center", color=NAVY, fontsize=15.2, fontweight="bold")
    ax.text(6.70, 5.58, "ICSOR Framework", ha="center", va="center", color=PLUM, fontsize=15.2, fontweight="bold")
    ax.text(11.115, 5.58, "Benchmark Comparison", ha="center", va="center", color="#245E1D", fontsize=15.2, fontweight="bold")

    draw_cstr(ax)
    draw_icsor_pipeline(ax)
    draw_benchmark_plot(fig)
    draw_deployment_summary(ax)
    return fig


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = build_figure()
    fixed_date = datetime(2026, 7, 16, tzinfo=timezone.utc)
    figure.savefig(
        OUTPUT_PATH,
        format="pdf",
        dpi=300,
        metadata={
            "Title": "ICSOR graphical abstract",
            "Author": "ICSOR authors",
            "Subject": "Invariant-aware regression with hard deployment correction",
            "Creator": "tools/generate_graphical_abstract.py",
            "Producer": "Matplotlib",
            "CreationDate": fixed_date,
            "ModDate": fixed_date,
        },
    )
    plt.close(figure)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
