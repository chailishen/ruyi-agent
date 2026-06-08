import { C, addBg, card, iconCircle, mascot, pill, smallFooter, text } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  text(slide, ctx, "WorkBuddy", { x: 82, y: 102, w: 370, h: 70 }, {
    size: 52,
    bold: true,
    color: C.teal,
  });
  text(slide, ctx, "企业版及", { x: 430, y: 108, w: 240, h: 62 }, {
    size: 42,
    bold: true,
    color: C.ink,
  });
  text(slide, ctx, "Buddy", { x: 82, y: 180, w: 250, h: 66 }, {
    size: 51,
    bold: true,
    color: C.teal,
  });
  text(slide, ctx, "产品家族全景图", { x: 300, y: 186, w: 520, h: 62 }, {
    size: 42,
    bold: true,
    color: C.ink,
  });

  mascot(slide, ctx, 875, 96, 1.05);

  pill(slide, ctx, { x: 83, y: 308, w: 220, h: 42 }, "企业 AI 工作台", {
    size: 17,
    fill: "#FFFFFFAA",
  });
  pill(slide, ctx, { x: 322, y: 308, w: 220, h: 42 }, "智能体与数字员工", {
    size: 17,
    fill: "#FFFFFFAA",
  });
  pill(slide, ctx, { x: 561, y: 308, w: 220, h: 42 }, "Buddy 产品图谱", {
    size: 17,
    fill: "#FFFFFFAA",
  });
  pill(slide, ctx, { x: 800, y: 308, w: 220, h: 42 }, "AI 共创生态", {
    size: 17,
    fill: "#FFFFFFAA",
  });

  card(slide, ctx, { x: 82, y: 405, w: 1000, h: 132 }, { fill: "#FFFFFFBA" });
  const items = [
    ["智能体套件", "腾讯文档 / 腾讯网盘 / 腾讯乐享", "Files"],
    ["垂类智能体", "CodeBuddy / Ardot / Miora", "Sparkles"],
    ["企业 AI 资产", "企业知识 / 技能套件 / 专家经验", "Database"],
    ["企业管理平台", "Agent 治理可见、可控、可管", "ShieldCheck"],
  ];
  items.forEach((item, i) => {
    const x = 118 + i * 235;
    iconCircle(slide, ctx, x, 435, 48, item[2]);
    text(slide, ctx, item[0], { x: x + 60, y: 426, w: 160, h: 28 }, {
      size: 19,
      bold: true,
      color: C.tealDark,
    });
    text(slide, ctx, item[1], { x: x + 60, y: 458, w: 170, h: 54 }, {
      size: 12,
      color: C.muted,
      valign: "top",
    });
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 396,
    y: 590,
    w: 400,
    h: 54,
    fill: "#74E5DD66",
  });
  card(slide, ctx, { x: 438, y: 560, w: 316, h: 84 }, { fill: "#FFFFFFD8", line: "#B7ECE7" });
  text(slide, ctx, "WorkBuddy", { x: 478, y: 572, w: 238, h: 38 }, {
    size: 32,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "AI 能力与智能体底座", { x: 478, y: 612, w: 238, h: 24 }, {
    size: 16,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  smallFooter(slide, ctx, 1);
  return slide;
}
