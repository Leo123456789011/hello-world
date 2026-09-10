#!/usr/bin/env python3
"""Generate searchable PDFs from recovered source markdown."""
from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1] / "docs" / "source-pdfs"
FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FILES = [
    "量化决策项目评估汇报-20260827.md",
    "红期-专业级期货基本面数据终端.md",
    "销售部工作职责与用户画像.md",
    "20260704-客户调研总结-要点.md",
]


class Doc(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_x(self.l_margin)
        self.set_font("wqy", size=9)
        self.set_text_color(120)
        self.cell(0, 8, f"{self.page_no()}", align="C")


def write(pdf: Doc, size: int, h: float, text: str) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_text_color(20)
    pdf.set_font("wqy", size=size)
    pdf.multi_cell(w=pdf.epw, h=h, text=text)


def render(md_name: str) -> None:
    text = (ROOT / md_name).read_text(encoding="utf-8")
    pdf = Doc(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("wqy", fname=FONT)
    pdf.add_page()
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            write(pdf, 16, 9, line[2:].strip())
            pdf.ln(2)
        elif line.startswith("## "):
            pdf.ln(2)
            write(pdf, 13, 8, line[3:].strip())
        elif line.startswith("### "):
            pdf.ln(1)
            write(pdf, 11, 7, line[4:].strip())
        elif line.startswith("- "):
            write(pdf, 10, 6, "- " + line[2:].strip())
        elif line.startswith("|"):
            cells = [
                c.strip()
                for c in line.strip().strip("|").split("|")
                if c.strip() and set(c.strip()) != {"-"}
            ]
            if cells:
                write(pdf, 10, 6, " | ".join(cells))
        elif not line:
            pdf.ln(2)
        else:
            write(pdf, 10, 6, line)
    out = ROOT / md_name.replace(".md", ".pdf")
    pdf.output(out)
    print(out)


if __name__ == "__main__":
    for name in FILES:
        render(name)
