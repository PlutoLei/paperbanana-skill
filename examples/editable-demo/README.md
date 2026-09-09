# Editable PowerPoint example

[Home](../../README.md) · [中文说明](#中文说明) · [Download PPTX](editable-demo.pptx) · [Source spec](slide-spec.json)

[![Rendered example of native text, workflow shapes, connectors, table and chart](../previews/editable-demo.webp)](editable-demo.pptx)

This one-slide example is built by the repository's existing renderer. It contains native text, shapes, connectors, a table and a chart; the chart values **2, 4, 3 are arbitrary demonstration data**. It makes no research or model-quality claim. No image API was called to build it.

## Rebuild

From the repository root:

```bash
cd plugins/paperbanana-slide-deck
bun install --frozen-lockfile
bun scripts/build-deck.ts --mode editable ../../examples/editable-demo \
  --output ../../examples/editable-demo/editable-demo.pptx
```

The checked-in `slide-spec.json` is the source. The PPTX is generated with PptxGenJS 4.0.1 through this repository's renderer. The preview is rendered from that PPTX with LibreOffice, then encoded as WebP. No slide screenshot was used as the deck's contents.

## Check editability

Open the PPTX in PowerPoint. Select and change the title, change a workflow box's fill, select a table cell, then use the chart's Edit Data command. Each is a native object. A static preview alone does not prove editability; the downloadable file and source let you inspect it.

To change the generated example, edit the spec and rebuild. [Authoring contract](../../plugins/paperbanana-slide-deck/references/editable-slide-spec.md).

## 中文说明

这个单页示例由仓库自带的渲染器生成，包含原生文本、形状、连接线、表格和图表。**2、4、3 只是演示数值，不是实验结果**，生成过程不调用图片 API。

下载 PPTX 后，可在 PowerPoint 中分别选中标题、流程框、表格单元格，并打开图表的“编辑数据”。预览图仅用于展示效果，实际可编辑能力应以 PPTX 对象为准。

需要重建时，在仓库根目录执行上方命令。修改内容通过 `slide-spec.json` 完成；源文件、生成文件与预览各自保留，方便复查。
