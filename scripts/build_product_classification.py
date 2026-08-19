#!/usr/bin/env python3
"""Generate Excel: map products to 事业部 / 产业群 / 项目经理 in Image-1 order."""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BU_FILL = {
    "橡塑": "D6EAF8",
    "能化": "FDEBD0",
}
GROUP_FILL = {
    "聚烯烃及下游": "AED6F1",
    "C2C3及下游": "85C1E9",
    "橡胶及下游": "5DADE2",
    "芳烃及下游": "F5CBA7",
    "煤化": "EDBB99",
    "炼油": "E59866",
    "新能源新材料": "F0B27A",
    "农资-能化": "F9E79F",
}

# 图一原顺序逐条对应，不合并
# (商品, 事业部, 产业群, 项目经理)
ROWS = [
    ("原油（布伦特）", "能化", "炼油", "王能"),
    ("原油 (WTI)", "能化", "炼油", "王能"),
    ("原料煤", "能化", "煤化", "李春燕"),
    ("动力煤", "能化", "煤化", "李春燕"),
    ("天然气 (LNG)", "能化", "炼油", "王能"),
    ("乙烷", "橡塑", "C2C3及下游", "孙伟卓"),
    ("丙烷", "橡塑", "C2C3及下游", "孙伟卓"),
    ("双氧水（27.5%）", "能化", "农资-能化", "李春燕"),
    ("外购环己酮", "能化", "芳烃及下游", "李春燕"),
    ("DMAC", "能化", "芳烃及下游", "李春燕"),
    ("环己酮", "能化", "芳烃及下游", "李春燕"),
    ("液氨", "能化", "农资-能化", "李春燕"),
    ("100%标准硫酸", "能化", "农资-能化", "李春燕"),
    ("液碱", "能化", "煤化", "李春燕"),
    ("煤炭", "能化", "煤化", "李春燕"),
    ("己内酰胺", "能化", "芳烃及下游", "李春燕"),
    ("硫磺", "能化", "农资-能化", "李春燕"),
    ("苯", "能化", "芳烃及下游", "李春燕"),
    ("外购98%酸", "能化", "农资-能化", "李春燕"),
    ("环己烷", "能化", "芳烃及下游", "李春燕"),
    ("硫酸铵", "能化", "农资-能化", "李春燕"),
    ("聚己内酰胺 (PA6)", "能化", "芳烃及下游", "李春燕"),
    ("高纯氢氧化钠 (32%) 优等品", "能化", "煤化", "李春燕"),
    ("煤炭", "能化", "煤化", "李春燕"),
    ("丙烯 一等品", "橡塑", "C2C3及下游", "孙伟卓"),
    ("液氨 一等品", "能化", "农资-能化", "李春燕"),
    ("硫酸 优等品", "能化", "农资-能化", "李春燕"),
    ("主产氢氟酸", "能化", "新能源新材料", "王能"),
    ("丁二烯 聚合级", "橡塑", "橡胶及下游", "王媛媛"),
    ("己二腈", "橡塑", "橡胶及下游", "王媛媛"),
    ("甲基戊二腈", "橡塑", "橡胶及下游", "王媛媛"),
    ("己二胺", "橡塑", "橡胶及下游", "王媛媛"),
    ("己二酸 优等品", "能化", "芳烃及下游", "李春燕"),
    ("丙烯腈", "橡塑", "C2C3及下游", "孙伟卓"),
    ("乙腈", "橡塑", "C2C3及下游", "孙伟卓"),
    ("硫酸铵", "能化", "农资-能化", "李春燕"),
    ("甲基戊二胺", "橡塑", "橡胶及下游", "王媛媛"),
    ("尼龙66", "橡塑", "橡胶及下游", "王媛媛"),
    ("环氧丙烷", "橡塑", "C2C3及下游", "孙伟卓"),
    ("丙二醇", "橡塑", "C2C3及下游", "孙伟卓"),
    ("丙二醇单甲醚", "橡塑", "C2C3及下游", "孙伟卓"),
    ("丙二醇异单甲醚", "橡塑", "C2C3及下游", "孙伟卓"),
    ("双氧水 (27.5%)", "能化", "农资-能化", "李春燕"),
    ("双氧水 (50%)", "能化", "农资-能化", "李春燕"),
    ("二乙基蒽醌", "能化", "农资-能化", "李春燕"),
    ("丙烯", "橡塑", "C2C3及下游", "孙伟卓"),
    ("甲醇", "能化", "煤化", "李春燕"),
    ("燃料煤", "能化", "煤化", "李春燕"),
    ("原料煤", "能化", "煤化", "李春燕"),
    ("硝酸", "能化", "农资-能化", "李春燕"),
    ("氢氧化钠", "能化", "煤化", "李春燕"),
    ("液氨", "能化", "农资-能化", "李春燕"),
    ("硫磺", "能化", "农资-能化", "李春燕"),
    ("碳酸二甲酯 (精DMC)", "能化", "新能源新材料", "王能"),
    ("聚酯级乙二醇", "橡塑", "C2C3及下游", "孙伟卓"),
    ("工业级乙二醇", "橡塑", "C2C3及下游", "孙伟卓"),
    ("硫酸铵 (一型)", "能化", "农资-能化", "李春燕"),
    ("1,4-丁二醇 (BDO)", "能化", "煤化", "李春燕"),
    ("对苯二甲酸 (PTA)", "能化", "芳烃及下游", "李春燕"),
    ("己二酸 (AA)", "能化", "芳烃及下游", "李春燕"),
    ("聚对苯二甲酸-己二酸丁二酯 (PBAT)", "能化", "新能源新材料", "王能"),
    ("聚对苯二甲酸丁二醇酯 (PBT)", "橡塑", "聚烯烃及下游", "韩永"),
    ("四氢呋喃 (THF)", "能化", "煤化", "李春燕"),
    ("18%氟硅酸", "能化", "新能源新材料", "王能"),
    ("38%氟硅酸", "能化", "新能源新材料", "王能"),
    ("98%硫酸", "能化", "农资-能化", "李春燕"),
    ("无水氯化氢", "能化", "新能源新材料", "王能"),
    ("甲醇", "能化", "煤化", "李春燕"),
    ("二氧化碳", "能化", "新能源新材料", "王能"),
    ("一甲基三甲氧基硅烷", "能化", "新能源新材料", "王能"),
    ("硝酸", "能化", "农资-能化", "李春燕"),
    ("氨水", "能化", "农资-能化", "李春燕"),
    ("硫酸", "能化", "农资-能化", "李春燕"),
    ("六甲基二硅氮烷", "能化", "新能源新材料", "王能"),
    ("硅粉", "能化", "新能源新材料", "王能"),
    ("中高温气凝胶毡", "能化", "新能源新材料", "王能"),
    ("深冷气凝胶毡", "能化", "新能源新材料", "王能"),
    ("工业气凝胶毡", "能化", "新能源新材料", "王能"),
    ("新能源气凝胶毡", "能化", "新能源新材料", "王能"),
    ("气凝胶涂料", "能化", "新能源新材料", "王能"),
    ("气凝胶粉", "能化", "新能源新材料", "王能"),
    ("硅酸酯", "能化", "新能源新材料", "王能"),
    ("超高分子量聚乙烯", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (C200)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (C300)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (C400)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (C600)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (CX300)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (CX400)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (CF50)", "橡塑", "聚烯烃及下游", "韩永"),
    ("超高分子量聚乙烯 (CF100)", "橡塑", "聚烯烃及下游", "韩永"),
]


def font(name="微软雅黑", size=11, bold=False, color="000000"):
    return Font(name=name, size=size, bold=bold, color=color)


def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)


def border():
    s = Side(style="thin", color="7F8C8D")
    return Border(left=s, right=s, top=s, bottom=s)


def align(h="center", wrap=True):
    return Alignment(horizontal=h, vertical="center", wrap_text=wrap)


MANAGER_ORDER = ["韩永", "孙伟卓", "王媛媛", "李春燕", "王能"]
MANAGER_HEADER = {
    "韩永": "1F4E79",
    "孙伟卓": "1A5276",
    "王媛媛": "154360",
    "李春燕": "922B21",
    "王能": "6E2C00",
}
HEADERS = ["商品名称", "事业部", "产业群", "项目经理"]


def write_table(ws, start_row, rows, header_color):
    title_cell = ws.cell(start_row, 1, f"项目经理：{rows[0][3]}（{len(rows)}项）")
    ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=4)
    title_cell.font = font(size=12, bold=True, color="FFFFFF")
    title_cell.fill = fill(header_color)
    title_cell.alignment = align()
    for col in range(1, 5):
        cell = ws.cell(start_row, col)
        cell.fill = fill(header_color)
        cell.border = border()
        cell.alignment = align()
    ws.row_dimensions[start_row].height = 26

    header_row = start_row + 1
    for col, header in enumerate(HEADERS, 1):
        cell = ws.cell(header_row, col, header)
        cell.font = font(size=11, bold=True, color="FFFFFF")
        cell.fill = fill(header_color)
        cell.alignment = align()
        cell.border = border()
    ws.row_dimensions[header_row].height = 22

    for i, (name, bu, group, pm) in enumerate(rows, 1):
        r = header_row + i
        values = [name, bu, group, pm]
        for col, val in enumerate(values, 1):
            cell = ws.cell(r, col, val)
            if col == 1:
                bg = "F8F9F9" if i % 2 == 0 else "FFFFFF"
            elif col == 3:
                bg = GROUP_FILL.get(group, "FFFFFF")
            else:
                bg = BU_FILL.get(bu, "FFFFFF")
            cell.font = font(bold=(col == 4))
            cell.alignment = align(h="left" if col == 1 else "center")
            cell.border = border()
            cell.fill = fill(bg)
        ws.row_dimensions[r].height = 22
    return header_row + len(rows)


def style_widths(ws):
    for i, width in enumerate([36, 12, 20, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = width


def main():
    grouped = {pm: [] for pm in MANAGER_ORDER}
    for row in ROWS:
        grouped[row[3]].append(row)

    wb = Workbook()

    overview = wb.active
    overview.title = "按项目经理分表"
    row_cursor = 1
    for pm in MANAGER_ORDER:
        rows = grouped[pm]
        row_cursor = write_table(overview, row_cursor, rows, MANAGER_HEADER[pm])
        row_cursor += 2
    style_widths(overview)

    for i, pm in enumerate(MANAGER_ORDER):
        ws = wb.create_sheet(pm)
        write_table(ws, 1, grouped[pm], MANAGER_HEADER[pm])
        style_widths(ws)
        ws.freeze_panes = "A3"
        ws.sheet_properties.tabColor = MANAGER_HEADER[pm]

    out = "/workspace/商品分类_事业部产业群项目经理.xlsx"
    wb.save(out)
    print("saved", out)
    for pm in MANAGER_ORDER:
        print(pm, len(grouped[pm]))


if __name__ == "__main__":
    main()
