# 数据交付方案（本地项目）

这是给 **Cursor 桌面** 用的本地项目，不依赖云端 Agent。克隆后用桌面版打开本文件夹即可继续改方案、查历史材料。

## 在本机打开（Cursor 桌面）

1. 安装 [Cursor 桌面版](https://cursor.com/download)。
2. 克隆本仓库并切到本分支：

```bash
git clone https://github.com/Leo123456789011/hello-world.git
cd hello-world
git checkout cursor/local-data-schemes-ad6c
```

3. 用 Cursor 打开这个文件夹：`File → Open Folder…`，选中 `hello-world`。
4. 预览页面（任选一种）：
   - 终端执行 `./scripts/preview.sh`，浏览器打开 http://127.0.0.1:8080
   - 或直接在 Cursor 里打开根目录 `index.html`

之后在本地对话里改方案即可，不必再开云端项目。

## 内容

| 方案 | 说明 | 打开 |
|---|---|---|
| 数据元素商场 | 客户选品入口，参考报价后交销售 | [docs/ai-data-marketplace-workflow/index.html](docs/ai-data-marketplace-workflow/index.html) |
| 数据集成 | 内部履约：标准数据项，可 API 交付 | [docs/ai-data-integration-workflow/index.html](docs/ai-data-integration-workflow/index.html) |
| 数据加工 | 内部履约：分析师生产，线下交付 | [docs/ai-data-processing-workflow/index.html](docs/ai-data-processing-workflow/index.html) |
| 定义 | 商城 / 集成 / 加工协作台 | [docs/definitions.md](docs/definitions.md) |
| 正式客户优惠 | 数据集成 3 折规则与两套方案 | [docs/数据集成正式客户优惠方案.md](docs/数据集成正式客户优惠方案.md) |
| 历史上传 PDF | 评估汇报、红期介绍、销售画像、调研要点 | [docs/source-pdfs/README.md](docs/source-pdfs/README.md) |
| 内部汇报邮件 | 邀约稿 | [docs/internal-briefing/email-invite.md](docs/internal-briefing/email-invite.md) |

总览页：[index.html](index.html)

每套方案目录里都有：

- `index.html`：鱼骨图 + 节点原型
- `edit.html` / `prototypes-editable.md`：可改文案

## 目录

```
index.html                          总览
scripts/preview.sh                  本地预览
docs/definitions.md                 三套方案定义
docs/数据集成正式客户优惠方案.md     正式客户优惠
docs/ai-data-marketplace-workflow/  数据元素商场
docs/ai-data-integration-workflow/  数据集成
docs/ai-data-processing-workflow/   数据加工
docs/source-pdfs/                   历史上传 PDF
docs/internal-briefing/             汇报邮件
```
