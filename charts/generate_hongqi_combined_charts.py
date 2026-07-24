#!/usr/bin/env python3
"""Generate combined 红期 total performance chart (PC / APP breakdown)."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

YEARS = [
    "2016", "2017", "2018", "2019", "2020", "2021",
    "2022", "2023", "2024", "2025", "2026H1",
]

# 红期 PC 业绩（元）：新签 + 续签
PC_NEW = [
    111300.00, 527055.00, 1009218.00, 1212705.00, 2703844.38,
    3050670.47, 1266860.30, 880884.97, 790413.56, 536071.35, 556261.47,
]
PC_RENEW = [
    12000.00, 290444.00, 359775.00, 913888.99, 1810475.79,
    3834631.49, 4214655.46, 2762539.59, 2649938.74, 2816055.69, 945589.66,
]
PC_PERF = [n + r for n, r in zip(PC_NEW, PC_RENEW)]

# 红期APP 业绩（元），2021 年起
APP_NEW = [343011.59, 248420.07, 375485.63, 495536.32, 521432.18, 253378.83]
APP_RENEW_BASE = [447103.98, 499671.84, 456856.52, 476033.57, 361719.57, 221220.72]
APP_RENEW_EXTRA = [0, 8020.00, 4351.00, 13389.28, 113844.44, 6025.97]
APP_RENEW = [b + e for b, e in zip(APP_RENEW_BASE, APP_RENEW_EXTRA)]
APP_PERF_BY_YEAR = {year: n + r for year, n, r in zip(YEARS[5:], APP_NEW, APP_RENEW)}

APP_PERF = [APP_PERF_BY_YEAR.get(year, 0) for year in YEARS]
TOTAL_PERF = [pc + app for pc, app in zip(PC_PERF, APP_PERF)]

COLOR_PC = "#4472C4"
COLOR_APP = "#70AD47"
COLOR_TOTAL = "#1F1F1F"

OUTPUT_DIR = Path(__file__).parent


def draw_combined_chart(ax):
    x = np.arange(len(YEARS))
    width = 0.62
    scale = 10000

    pc_scaled = np.array(PC_PERF) / scale
    app_scaled = np.array(APP_PERF) / scale
    totals = pc_scaled + app_scaled

    ax.bar(x, pc_scaled, width, label="PC", color=COLOR_PC, zorder=2)
    ax.bar(x, app_scaled, width, bottom=pc_scaled, label="APP", color=COLOR_APP, zorder=2)

    ax.plot(
        x,
        totals,
        color=COLOR_TOTAL,
        linestyle="--",
        linewidth=1.8,
        marker="o",
        markersize=6,
        markerfacecolor=COLOR_TOTAL,
        markeredgecolor=COLOR_TOTAL,
        label="总业绩",
        zorder=3,
    )

    ymax = max(totals.max(), 1) * 1.18
    ax.set_ylim(0, ymax)
    ax.set_ylabel("业绩（万元）", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(YEARS, fontsize=10)
    ax.set_title("红期 2016-2026H1 总业绩走势（PC / APP）", fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)

    for i, (total, pc, app) in enumerate(zip(totals, pc_scaled, app_scaled)):
        if total <= 0:
            continue
        ax.annotate(
            f"{total:.0f}",
            xy=(x[i], total),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=COLOR_TOTAL,
        )
        if app > 0:
            app_pct = app / total * 100
            ax.text(
                x[i],
                pc + app / 2,
                f"APP\n{app_pct:.0f}%",
                ha="center",
                va="center",
                fontsize=7.5,
                color="white",
                fontweight="bold",
            )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    draw_combined_chart(ax)
    fig.tight_layout()

    output = OUTPUT_DIR / "hongqi_total_pc_app.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {output}")

    print("\n总业绩明细（万元）：")
    for year, pc, app, total in zip(YEARS, PC_PERF, APP_PERF, TOTAL_PERF):
        app_pct = app / total * 100 if total else 0
        print(
            f"{year}: PC {pc/10000:.1f} + APP {app/10000:.1f} = {total/10000:.1f}"
            f"（APP占比 {app_pct:.1f}%）"
        )


if __name__ == "__main__":
    main()
