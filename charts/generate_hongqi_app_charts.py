#!/usr/bin/env python3
"""Generate 红期APP performance charts (2021-2026H1)."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

YEARS = ["2021", "2022", "2023", "2024", "2025", "2026H1"]

COLOR_NEW = "#4472C4"
COLOR_RENEW = "#ED7D31"
COLOR_TOTAL = "#1F1F1F"

OUTPUT_DIR = Path(__file__).parent

PERF_NEW = [343011.59, 248420.07, 375485.63, 495536.32, 521432.18, 253378.83]
PERF_RENEW = [447103.98, 499671.84, 456856.52, 476033.57, 361719.57, 221220.72]

CUST_NEW = [85, 90, 154, 202, 191, 108]
CUST_RENEW = [52, 64, 102, 125, 120, 64]

AOV_NEW = [4035.43, 2760.22, 2438.22, 2453.15, 2730.01, 2346.10]
AOV_RENEW = [8598.15, 7807.37, 4478.99, 3808.27, 3014.33, 3456.57]


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

    ymax = max(totals.max(), 1) * 1.18
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
        if total <= 0:
            continue
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


def draw_aov_chart(
    ax,
    title: str,
    perf_new: list[float],
    perf_renew: list[float],
    cust_new: list[float],
    cust_renew: list[float],
    aov_new: list[float],
    aov_renew: list[float],
):
    x = np.arange(len(YEARS))
    width = 0.34

    totals_perf = np.array(perf_new) + np.array(perf_renew)
    totals_cust = np.array(cust_new) + np.array(cust_renew)
    with np.errstate(divide="ignore", invalid="ignore"):
        weighted_aov = np.where(totals_cust > 0, totals_perf / totals_cust, 0)

    ax.bar(x - width / 2, aov_new, width, label="新签", color=COLOR_NEW, zorder=2)
    ax.bar(x + width / 2, aov_renew, width, label="续签", color=COLOR_RENEW, zorder=2)
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

    active = weighted_aov[weighted_aov > 0]
    ymax = max(active.max(), max(aov_new), max(aov_renew)) * 1.18
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
        if total <= 0:
            continue
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
    prefix = "hongqi_app"

    charts = [
        (
            "红期APP 2021-2026H1 业绩走势（新签 / 续签）",
            "业绩（万元）",
            PERF_NEW,
            PERF_RENEW,
            "wan",
            10000,
            f"{prefix}_performance.png",
        ),
        (
            "红期APP 2021-2026H1 客户数走势（新签 / 续签）",
            "客户数（家）",
            CUST_NEW,
            CUST_RENEW,
            "count",
            1,
            f"{prefix}_customers.png",
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
    draw_aov_chart(
        ax,
        "红期APP 2021-2026H1 客单价走势（新签 / 续签）",
        PERF_NEW,
        PERF_RENEW,
        CUST_NEW,
        CUST_RENEW,
        AOV_NEW,
        AOV_RENEW,
    )
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{prefix}_aov.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_DIR / f'{prefix}_aov.png'}")

    fig, axes = plt.subplots(3, 1, figsize=(12, 16), dpi=150)
    draw_stacked_chart(
        axes[0],
        "红期APP 2021-2026H1 业绩走势（新签 / 续签）",
        "业绩（万元）",
        PERF_NEW,
        PERF_RENEW,
        "wan",
        10000,
    )
    draw_stacked_chart(
        axes[1],
        "红期APP 2021-2026H1 客户数走势（新签 / 续签）",
        "客户数（家）",
        CUST_NEW,
        CUST_RENEW,
        "count",
        1,
    )
    draw_aov_chart(
        axes[2],
        "红期APP 2021-2026H1 客单价走势（新签 / 续签）",
        PERF_NEW,
        PERF_RENEW,
        CUST_NEW,
        CUST_RENEW,
        AOV_NEW,
        AOV_RENEW,
    )
    fig.tight_layout(h_pad=2.0)
    fig.savefig(OUTPUT_DIR / f"{prefix}_overview.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT_DIR / f'{prefix}_overview.png'}")


if __name__ == "__main__":
    main()
