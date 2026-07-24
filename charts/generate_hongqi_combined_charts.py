#!/usr/bin/env python3
"""Generate combined 红期 + 红期APP performance trend chart."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

YEARS = [
    "2016", "2017", "2018", "2019", "2020", "2021",
    "2022", "2023", "2024", "2025", "2026H1",
]

COLOR_NEW = "#4472C4"
COLOR_RENEW = "#ED7D31"
COLOR_TOTAL = "#1F1F1F"
OUTPUT_DIR = Path(__file__).parent

# 红期 业绩（元）
HQ_NEW = [
    111300.00, 527055.00, 1009218.00, 1212705.00, 2703844.38,
    3050670.47, 1266860.30, 880884.97, 790413.56, 536071.35, 556261.47,
]
HQ_RENEW = [
    12000.00, 290444.00, 359775.00, 913888.99, 1810475.79,
    3834631.49, 4214655.46, 2762539.59, 2649938.74, 2816055.69, 945589.66,
]

# 红期APP 业绩（元），2021 年起
APP_NEW = [0, 0, 0, 0, 0, 343011.59, 248420.07, 375485.63, 495536.32, 521432.18, 253378.83]
APP_RENEW_BASE = [0, 0, 0, 0, 0, 447103.98, 499671.84, 456856.52, 476033.57, 361719.57, 221220.72]
APP_RENEW_EXTRA = [0, 0, 0, 0, 0, 0, 8020.00, 4351.00, 13389.28, 113844.44, 6025.97]
APP_RENEW = [b + e for b, e in zip(APP_RENEW_BASE, APP_RENEW_EXTRA)]

PERF_NEW = [h + a for h, a in zip(HQ_NEW, APP_NEW)]
PERF_RENEW = [h + a for h, a in zip(HQ_RENEW, APP_RENEW)]


def format_label(value: float) -> str:
    return f"{value:.0f}"


def draw_stacked_chart(ax, title: str, new_values: list[float], renew_values: list[float]):
    x = np.arange(len(YEARS))
    width = 0.62
    scale = 10000

    new_scaled = np.array(new_values) / scale
    renew_scaled = np.array(renew_values) / scale
    totals = new_scaled + renew_scaled

    ax.bar(x, new_scaled, width, label="新签", color=COLOR_NEW, zorder=2)
    ax.bar(x, renew_scaled, width, bottom=new_scaled, label="续签", color=COLOR_RENEW, zorder=2)
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
        label="总计",
        zorder=3,
    )

    ymax = max(totals.max(), 1) * 1.15
    ax.set_ylim(0, ymax)
    ax.set_ylabel("业绩（万元）", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(YEARS, fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)

    for i, total in enumerate(totals):
        if total <= 0:
            continue
        ax.annotate(
            format_label(total),
            xy=(x[i], total),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=COLOR_TOTAL,
        )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    draw_stacked_chart(
        ax,
        "红期 + 红期APP 2016-2026H1 总业绩走势（新签 / 续签）",
        PERF_NEW,
        PERF_RENEW,
    )
    fig.tight_layout()
    output = OUTPUT_DIR / "hongqi_combined_performance.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {output}")

    for year, new_v, renew_v in zip(YEARS, PERF_NEW, PERF_RENEW):
        total = new_v + renew_v
        print(f"{year}: 新签{new_v:,.0f} + 续签{renew_v:,.0f} = {total:,.0f}元 ({total/10000:.1f}万)")


if __name__ == "__main__":
    main()
