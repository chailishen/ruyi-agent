import { C, addBg, card, smallFooter, text } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  text(slide, ctx, "腾讯效率智能体 “Buddy” 家族产品图谱", { x: 210, y: 56, w: 860, h: 58 }, {
    size: 34,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  ctx.addShape(slide, { geometry: "ellipse", x: 190, y: 82, w: 6, h: 6, fill: "#6A8BD9" });
  ctx.addShape(slide, { geometry: "ellipse", x: 1080, y: 82, w: 6, h: 6, fill: "#6A8BD9" });
  ctx.addShape(slide, { x: 124, y: 91, w: 68, h: 1, fill: "#B7D9DD" });
  ctx.addShape(slide, { x: 1088, y: 91, w: 68, h: 1, fill: "#B7D9DD" });

  const x = 84;
  const y = 150;
  const w = 1112;
  const headerH = 58;
  const rowH = 70;
  const col = [0, 430, 735, 1112];
  card(slide, ctx, { x, y, w, h: headerH + rowH * 6 }, { fill: "#FFFFFFD8", line: "#A7E7DF" });
  const headers = [
    ["智能体名称", "#26C9BA"],
    ["主要场景", "#22C6BA"],
    ["适用人群", "#6E91F0"],
  ];
  headers.forEach((h, i) => {
    ctx.addShape(slide, {
      geometry: "roundRect",
      x: x + col[i],
      y,
      w: col[i + 1] - col[i] - 8,
      h: headerH,
      fill: {
        type: "gradient",
        gradientKind: "linear",
        angleDeg: 0,
        stops: [
          { offset: 0, color: i === 2 ? "#3FBEF2" : "#19C7BA" },
          { offset: 100000, color: h[1] },
        ],
      },
      line: { style: "solid", fill: "#00000000", width: 0 },
    });
    text(slide, ctx, h[0], { x: x + col[i], y: y + 8, w: col[i + 1] - col[i] - 8, h: 42 }, {
      size: 21,
      bold: true,
      color: C.white,
      align: "center",
    });
  });

  const rows = [
    ["WorkBuddy通用智能体", "办公学习", "办公人群、学生、OPC等"],
    ["WorkBuddy企业版", "企业组织提效", "企业管理员及员工"],
    ["WorkBuddy国际版", "面向全球用户", "职场及办公提效人群"],
    ["CodeBuddy编码智能体", "开发与运维", "程序员或独立开发者"],
    ["Miora创意智能体", "创意内容生产", "平面、视频与3D等创意资产创作者"],
    ["Ardot交互设计智能体", "专业交互设计", "UI/UX等交互设计师"],
  ];

  rows.forEach((row, r) => {
    const top = y + headerH + r * rowH;
    if (r % 2 === 0) {
      ctx.addShape(slide, { x, y: top, w, h: rowH, fill: "#F8FFFD99" });
    }
    ctx.addShape(slide, { x: x + 12, y: top, w: w - 24, h: 1, fill: "#B7E8E1" });
    row.forEach((value, c) => {
      text(slide, ctx, value, { x: x + col[c] + 20, y: top + 8, w: col[c + 1] - col[c] - 44, h: rowH - 14 }, {
        size: c === 0 ? 18 : 17,
        color: C.ink,
        align: "center",
      });
    });
  });
  [col[1], col[2]].forEach((cx) => {
    ctx.addShape(slide, { x: x + cx, y: y + headerH + 4, w: 1, h: rowH * 6 - 8, fill: "#C5ECE8" });
  });

  text(slide, ctx, "从个人办公提效到企业组织提效，再到开发、创意和交互设计垂类场景", { x: 210, y: 624, w: 860, h: 34 }, {
    size: 17,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  smallFooter(slide, ctx, 3);
  return slide;
}
