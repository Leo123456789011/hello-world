#!/usr/bin/env python3
"""Generate 红期 performance charts (2016-2026H1)."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

YEARS = [
    "2016", "2017", "2018", "2019", "2020", "2021",
    "2022", "2023", "2024", "2025", "2026H1",
]

# 业绩（元）
PERF_NEW = [
    111300.00, 527055.00, 1009218.00, 1212705.00, 2703844.38,
    3050670.47, 1266860.30, 880884.97, 790413.56, 536071.35, 556261.47,
]
PERF_RENEW = [
    12000.00, 290444.00, 359775.00, 913888.99, 1810475.79,
    3834631.49, 4214655.46, 2762539.59, 2649938.74, 2816055.69, 945589.66,
]

# 客户数
CUST_NEW = [16, 61, 87, 112, 314, 270, 118, 116, 113, 93, 69]
CUST_RENEW = [3, 22, 33, 65, 104, 203, 204, 196, 202, 168, 83]

# 客单价（元）
AOV_NEW = [
    6956.25, 8640.25, 11600.21, 10827.72, 8610.97,
    11298.78, 10736.10, 7593.84, 6994.81, 5764.21, 8061.76,
]
AOV_RENEW = [
    4000.00, 13202.00, 10902.27, 14059.83, 17408.42,
    18889.81, 20660.08, 14094.59, 13118.51, 16762.24, 11392.65,
]

COLOR_NEW = "#4472C4"
COLOR_RENEW = "#ED7D31"
COLOR_TOTAL = "#1F1F1F"

OUTPUT_DIR = Path(__file__).parent


def format_label(value: float, unit: str) -> str:
    if unit == "wan":
        return f"{value:.0f}"
    if unit == "count":
        return f"{int(round(value))}"
    return f"{value:,.0f}"


def draw_stacked_chart(
    ax,
    title: str,
    ylabel: str,
    new_values: list[float],
    renew_values: list[float],
    unit: str,
    scale: float = 1.0,
):
    """Stacked bar + total trend line, matching reference chart style."""
    x = np.arange(len(YEARS))
    width = 0.62

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

    ymax = totals.max() * 1.18
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(YEARS, fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)

    for i, total in enumerate(totals):
        ax.annotate(
            format_label(total, unit),
            xy=(x[i], total),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=COLOR_TOTAL,
        )


def draw_aov_chart(ax, title: str):
    """Grouped bars for 新签/续签 客单价 + weighted average line."""
    x = np.arange(len(YEARS))
    width = 0.34

    totals_perf = np.array(PERF_NEW) + np.array(PERF_RENEW)
    totals_cust = np.array(CUST_NEW) + np.array(CUST_RENEW)
    weighted_aov = totals_perf / totals_cust

    ax.bar(x - width / 2, AOV_NEW, width, label="新签", color=COLOR_NEW, zorder=2)
    ax.bar(x + width / 2, AOV_RENEW, width, label="续签", color=COLOR_RENEW, zorder=2)
    ax.plot(
        x,
        weighted_aov,
        color=COLOR_TOTAL,
        linestyle="--",
        linewidth=1.8,
        marker="o",
        markersize=6,
        markerfacecolor=COLOR_TOTAL,
        markeredgecolor=COLOR_TOTAL,
        label="综合客单价",
        zorder=3,
    )

    ymax = max(max(AOV_NEW), max(AOV_RENEW), weighted_aov.max()) * 1.18
    ax.set_ylim(0, ymax)
    ax.set_ylabel("客单价（元）", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(YEARS, fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

    for i, total in enumerate(weighted_aov):
        ax.annotate(
            f"{total:,.0f}",
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

    charts = [
        (
            "红期 2016-2026H1 业绩走势（新签 / 续签）",
            "业绩（万元）",
            PERF_NEW,
            PERF_RENEW,
            "wan",
            10000,
            "hongqi_performance.png",
        ),
        (
            "红期 2016-2026H1 客户数走势（新签 / 续签）",
            "客户数（家）",
            CUST_NEW,
            CUST_RENEW,
            "count",
            1,
            "hongqi_customers.png",
        ),
    ]

    for title, ylabel, new_vals, renew_vals, unit, scale, filename in charts:
        fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
        draw_stacked_chart(ax, title, ylabel, new_vals, renew_vals, unit, scale)
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"Saved: {OUTPUT_DIR / filename}")

    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    draw_aov_chart(ax, "红期 2016-2026H1 客单价走势（新签 / 续签）")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hongqi_aov.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_DIR / 'hongqi_aov.png'}")

    # Combined overview slide
    fig, axes = plt.subplots(3, 1, figsize=(12, 16), dpi=150)
    draw_stacked_chart(
        axes[0],
        "红期 2016-2026H1 业绩走势（新签 / 续签）",
        "业绩（万元）",
        PERF_NEW,
        PERF_RENEW,
        "wan",
        10000,
    )
    draw_stacked_chart(
        axes[1],
        "红期 2016-2026H1 客户数走势（新签 / 续签）",
        "客户数（家）",
        CUST_NEW,
        CUST_RENEW,
        "count",
        1,
    )
    draw_aov_chart(axes[2], "红期 2016-2026H1 客单价走势（新签 / 续签）")
    fig.tight_layout(h_pad=2.0)
    fig.savefig(OUTPUT_DIR / "hongqi_overview.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_DIR / 'hongqi_overview.png'}")


if __name__ == "__main__":
    main()
