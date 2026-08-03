#!/usr/bin/env python3
"""客户一级/二级分类脚本。

按 PDF 要求：
- 一级：金融客户、产业客户、个人客户、其他
- 二级（仅金融/产业）：见 FINANCE_RULES / INDUSTRY_RULES
- 输出：按年份分 sheet 的 Excel（公司名称、一级分类、二级分类）
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

FINANCE_RULES: list[tuple[str, list[str]]] = [
    ("保险", ["保险", "人寿", "财险", "太保", "泰康"]),
    ("基金", ["基金", "私募", "股权投资", "创投"]),
    ("期货", ["期货"]),
    ("券商", ["证券", "投行", "研究所", "券商"]),
    ("融资租赁", ["融资租赁", "金租", "融租"]),
    ("商品交易所", ["交易所", "交易中心", "上期所", "大商所", "郑商所", "中金所", "广期所"]),
    ("银行", ["银行", "农商行", "农信", "信用社", "村镇银行"]),
]

INDUSTRY_RULES: list[tuple[str, list[str]]] = [
    ("采矿业", ["矿业", "煤矿", "煤炭", "铁矿", "有色金属矿", "黄金矿", "稀土", "采掘", "油田", "石油", "天然气", "矿山", "采矿"]),
    ("建筑业", ["建筑", "建设", "工程", "施工", "路桥", "隧道", "市政", "装饰", "园林", "基建", "中铁", "中建", "中交", "中冶", "电建", "能建", "城建", "城投", "房地产", "置业", "物业"]),
    ("贸易业", ["贸易", "商贸", "进出口", "外贸", "供应链", "批发", "零售", "经销", "国贸", "物产", "建发", "象屿", "物流", "货代", "港口", "码头", "航运", "快递"]),
    ("农林牧渔业", ["农业", "农林", "牧业", "渔业", "养殖", "种植", "粮油", "饲料", "种业", "种子", "化肥", "农药", "农机", "农产品", "畜牧", "生猪", "禽业", "乳业", "水产", "林业", "木材", "造纸", "农场", "合作社"]),
    ("制造业", ["制造", "工业", "工厂", "生产", "加工", "机械", "设备", "装备", "汽车", "零部件", "电子", "电器", "半导体", "芯片", "光伏", "新能源", "电池", "储能", "电机", "线缆", "钢铁", "有色", "化工", "化纤", "塑料", "橡胶", "玻璃", "水泥", "陶瓷", "纺织", "服装", "食品", "饮料", "医药", "生物", "制药", "材料", "冶金", "铸造", "模具"]),
    ("服务业", ["服务", "咨询", "顾问", "人力", "劳务", "外包", "客服", "会展", "广告", "传媒", "营销", "策划", "设计", "文化", "旅游", "酒店", "餐饮", "娱乐", "体育", "健身", "美容", "医疗", "医院", "诊所", "药店", "体检", "康复", "护理", "养老", "家政", "保洁", "保安", "维修", "检测", "认证", "评估", "审计", "会计", "税务", "法律", "律所", "软件", "信息", "科技", "互联网", "数据", "云计算", "人工智能"]),
]

COMPANY_SUFFIXES = ("有限公司", "有限责任公司", "股份有限公司", "集团公司", "集团", "公司", "企业", "厂", "中心", "院", "所", "期货", "证券", "银行", "保险", "基金", "信托", "租赁", "交易所")
PERSON_PATTERN = re.compile(r"^[\u4e00-\u9fa5]{2,3}$")


def _match_subcategory(name: str, rules: list[tuple[str, list[str]]]) -> str:
    for sub, keywords in rules:
        if any(kw in name for kw in keywords):
            return sub
    return "其他"


def _has_finance_signal(name: str) -> bool:
    return any(kw in name for _, kws in FINANCE_RULES for kw in kws)


def _has_industry_signal(name: str) -> bool:
    return any(kw in name for _, kws in INDUSTRY_RULES for kw in kws)


def classify_company(name: str) -> tuple[str, str]:
    name = str(name).strip()
    if not name:
        return "其他", ""

    if _has_finance_signal(name):
        return "金融客户", _match_subcategory(name, FINANCE_RULES)

    if _has_industry_signal(name):
        return "产业客户", _match_subcategory(name, INDUSTRY_RULES)

    if any(s in name for s in COMPANY_SUFFIXES):
        return "其他", ""

    if PERSON_PATTERN.match(name):
        return "个人客户", ""

    return "其他", ""


def load_companies(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path, header=None)
    elif suffix == ".csv":
        df = pd.read_csv(path, header=None)
    elif suffix == ".txt":
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        raise ValueError(f"不支持的文件格式: {path}")

    col = df.iloc[:, 0].dropna().astype(str).str.strip()
    skip = {"公司名称", "公司名字", "名称", "客户名称", "客户"}
    return [x for x in col if x and x not in skip]


def build_dataframe(companies: list[str]) -> pd.DataFrame:
    rows = []
    for name in companies:
        level1, level2 = classify_company(name)
        rows.append({"公司名称": name, "一级分类": level1, "二级分类": level2})
    return pd.DataFrame(rows, columns=["公司名称", "一级分类", "二级分类"])


def write_excel(output: Path, year_data: dict[str, list[str]]) -> None:
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for year, companies in sorted(year_data.items()):
            build_dataframe(companies).to_excel(writer, sheet_name=year, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="客户一级/二级分类")
    parser.add_argument("--input-dir", type=Path, help="输入目录，包含 2024/2025/2026 的 xlsx/csv/txt")
    parser.add_argument("--output", type=Path, default=Path("客户分类结果.xlsx"), help="输出 Excel 路径")
    parser.add_argument("--demo", action="store_true", help="生成示例模板")
    args = parser.parse_args()

    if args.demo:
        demo = {
            "2024": ["永安期货", "中信证券", "张三", "宝钢股份", "某某贸易有限公司"],
            "2025": ["中信期货", "中国人寿", "李四", "中国建筑", "紫金矿业"],
            "2026": ["南华期货", "招商银行", "王五", "海尔智家", "无法识别公司"],
        }
        write_excel(args.output, demo)
        print(f"已生成示例: {args.output}")
        return

    if not args.input_dir:
        parser.error("请提供 --input-dir 或使用 --demo")

    year_data: dict[str, list[str]] = {}
    for year in ("2024", "2025", "2026"):
        matched = sorted(args.input_dir.glob(f"{year}*"))
        if matched:
            year_data[year] = load_companies(matched[0])

    if not year_data:
        parser.error(f"在 {args.input_dir} 未找到 2024/2025/2026 数据文件")

    write_excel(args.output, year_data)
    print(f"已输出: {args.output}")
    for year, companies in year_data.items():
        print(f"  {year}: {len(companies)} 家公司")


if __name__ == "__main__":
    main()
