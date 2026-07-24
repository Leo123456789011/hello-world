#!/usr/bin/env python3
"""Generate 红期APP performance charts (2021-2026H1)."""

import matplotlib.pyplot as plt
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
# 续签业绩基础值 + 2022-2026H1 追加业绩
PERF_RENEW_BASE = [447103.98, 499671.84, 456856.52, 476033.57, 361719.57, 221220.72]
PERF_RENEW_EXTRA = [0, 8020.00, 4351.00, 13389.28, 23844.44, 6025.97]
PERF_RENEW = [b + e for b, e in zip(PERF_RENEW_BASE, PERF_RENEW_EXTRA)]


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


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150)
    draw_stacked_chart(
        ax,
        "红期APP 2021-2026H1 业绩走势（新签 / 续签）",
        "业绩（万元）",
        PERF_NEW,
        PERF_RENEW,
        "wan",
        10000,
    )
    fig.tight_layout()
    output = OUTPUT_DIR / "hongqi_app_performance.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {output}")

    for year, extra, renew, total in zip(YEARS, PERF_RENEW_EXTRA, PERF_RENEW, PERF_NEW):
        print(f"{year}: 续签+{extra:,.2f} → 续签{renew:,.2f}, 总计{(total + renew):,.2f}元 ({(total + renew) / 10000:.1f}万)")


if __name__ == "__main__":
    main()
