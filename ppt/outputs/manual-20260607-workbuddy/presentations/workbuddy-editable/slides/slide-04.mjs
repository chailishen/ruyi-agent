import { C, addBg, card, iconCircle, pill, smallFooter, text } from "./common.mjs";

function ecoCard(slide, ctx, x, y, icon, heading, body) {
  card(slide, ctx, { x, y, w: 300, h: 126 }, { fill: "#FFFFFFD0", line: "#B5E9E4" });
  iconCircle(slide, ctx, x + 24, y + 32, 64, icon, { fill: "#E3FCF8" });
  text(slide, ctx, heading, { x: x + 98, y: y + 28, w: 170, h: 30 }, {
    size: 20,
    bold: true,
    color: C.tealDark,
  });
  text(slide, ctx, body, { x: x + 98, y: y + 62, w: 176, h: 48 }, {
    size: 12,
    color: C.muted,
    valign: "top",
  });
}

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  text(slide, ctx, "Buddy AI 共创生态", { x: 290, y: 52, w: 700, h: 62 }, {
    size: 38,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  ctx.addShape(slide, { geometry: "ellipse", x: 270, y: 82, w: 7, h: 7, fill: "#6A8BD9" });
  ctx.addShape(slide, { geometry: "ellipse", x: 1004, y: 82, w: 7, h: 7, fill: "#6A8BD9" });
  text(slide, ctx, "提升用户体验，加速 AI 普惠，让 AI 无处不在", { x: 260, y: 116, w: 760, h: 34 }, {
    size: 21,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  ecoCard(slide, ctx, 98, 214, "DoorOpen", "场景入口", "让 AI Agent 拥有更多真实世界交互入口与触点");
  ecoCard(slide, ctx, 490, 214, "Boxes", "能力协同", "让软件服务、专业知识和方法论成为可调能力");
  ecoCard(slide, ctx, 882, 214, "ChartNoAxesCombined", "商业交付", "让获客解决方案可复用、可分发、可商业化");

  [246, 640, 1034].forEach((x) => {
    ctx.addShape(slide, { x, y: 352, w: 3, h: 74, fill: "#96E3DA" });
    ctx.addShape(slide, {
      geometry: "triangle",
      x: x - 7,
      y: 416,
      w: 16,
      h: 16,
      fill: "#96E3DA",
      line: { style: "solid", fill: "#00000000", width: 0 },
    }).position.rotation = 180;
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 330,
    y: 510,
    w: 620,
    h: 100,
    fill: "#60E0D566",
  });
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 410,
    y: 462,
    w: 460,
    h: 106,
    fill: "#DFFFFBE6",
    line: { style: "solid", fill: "#A8ECE5", width: 1.2 },
  });
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 450,
    y: 492,
    w: 380,
    h: 54,
    fill: "#FFFFFFE8",
    line: { style: "solid", fill: "#C9F0EC", width: 1 },
  });
  text(slide, ctx, "WorkBuddy", { x: 506, y: 454, w: 260, h: 52 }, {
    size: 36,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "AI 能力与智能体底座", { x: 500, y: 507, w: 274, h: 32 }, {
    size: 19,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  pill(slide, ctx, { x: 190, y: 632, w: 900, h: 38 }, "全面开放 WorkBuddy 产品能力，首批加入共创生态伙伴", {
    size: 19,
    fill: "#FFFFFFC8",
  });

  smallFooter(slide, ctx, 4);
  return slide;
}
