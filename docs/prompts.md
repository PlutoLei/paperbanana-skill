# Starter prompts / 起步提示词

[Home / 首页](../README.md) · [Gallery / 图库](gallery.md)

These recipes were written for this documentation refresh. They are **not the original prompts** for the archived gallery images and do not guarantee identical outputs. Substitute your own method, labels and data; ask the agent to preserve your chosen provider.

以下模板是本次整理新写的起步示例，并非历史配图的原始提示词。请替换成自己的方法、标签和数据，预期得到新的结果，而不是原图复刻。

## Scientific figure

> Use paperbanana with Gemini to draw a game-theory influence diagram for this specified model: two players each choose Cooperate or Defect; a shared payoff node depends on both choices. Distinguish decision nodes from outcomes, label every arrow, use a white background and a restrained palette. Do not invent probabilities or numerical payoffs. Return the image and review status.

> 用 paperbanana 和 Gemini 绘制一个指定模型的博弈论影响图：两名参与者各自选择合作或背叛，共同收益节点依赖两人的选择。区分决策与结果，标清箭头，使用白底和克制配色，不虚构概率或收益数值。返回图片及评审状态。

## Research slide

> Use paperbanana-slide-deck in image mode to make one slide introducing a single-cell RNA-seq analysis workflow: quality control, normalization, dimensionality reduction, clustering, and annotation. Mark it as an illustrative workflow. Do not add results or dataset claims. Use a scientific style and report the chosen image provider and review status.

> 用 paperbanana-slide-deck 的图片模式制作一页单细胞 RNA 测序分析流程介绍，包含质控、归一化、降维、聚类与注释。注明“流程示意”，不添加实验结果或数据集结论。采用科研风格，交付时说明生图提供商与评审状态。

## Consistent deck

> Use paperbanana-slide-deck in image mode to plan a four-slide introduction to a learning cycle: goal, practice, feedback, reflection. Use the same warm paper background, type treatment and diagram language throughout. First propose the outline and preserve the selected provider for every slide. Include the per-slide prompts in the delivery.

> 用 paperbanana-slide-deck 的图片模式规划四页“学习循环”介绍，依次讲目标、练习、反馈与反思。整套沿用暖纸色背景、同一字体处理和图示规则。先给出大纲，各页使用同一已选提供商，并在交付时保留逐页提示词。

## Editable deck

For a deterministic example with no image API calls, [build the included slide spec](../examples/editable-demo/README.md). Its arbitrary chart values are labeled as demonstration data.

要直接验证原生可编辑对象，可[构建随仓库提供的示例](../examples/editable-demo/README.md#中文说明)。该示例不调用生图 API，图表中的数值仅用于演示。
