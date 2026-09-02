# 数据交付方案（本地项目）

本仓库在本地使用。用 Cursor 桌面打开即可，不依赖云端 Agent。

## 内容

| 方案 | 说明 | 打开 |
|---|---|---|
| 数据集成 | 内部履约：标准数据项，可 API 交付 | [docs/ai-data-integration-workflow/index.html](docs/ai-data-integration-workflow/index.html) |
| 数据加工 | 内部履约：分析师生产，线下交付 | [docs/ai-data-processing-workflow/index.html](docs/ai-data-processing-workflow/index.html) |
| 数据元素商场 | 客户选品入口，下单后交销售 | [docs/ai-data-marketplace-workflow/index.html](docs/ai-data-marketplace-workflow/index.html) |
| 历史上传 PDF | 评估汇报、红期介绍、销售画像、调研要点 | [docs/source-pdfs/README.md](docs/source-pdfs/README.md) |
| 内部汇报邮件 | 邀约稿 | [docs/internal-briefing/email-invite.md](docs/internal-briefing/email-invite.md) |

总览页：[index.html](index.html)

## 本地打开

```bash
git clone https://github.com/Leo123456789011/hello-world.git
cd hello-world
git checkout cursor/data-element-mall-fishbone-5430
./scripts/preview.sh
```

浏览器访问 http://127.0.0.1:8080

也可在 Cursor 中打开仓库，直接打开各目录下的 `index.html`。

## 目录

```
index.html                          总览
scripts/preview.sh                  本地预览
docs/ai-data-integration-workflow/  数据集成
docs/ai-data-processing-workflow/   数据加工
docs/ai-data-marketplace-workflow/  数据元素商场
docs/source-pdfs/                   历史上传 PDF
docs/internal-briefing/             汇报邮件
```
