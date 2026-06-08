import path from "node:path";
import { C, addBg, card, text } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  text(slide, ctx, "WorkBuddy 共创生态伙伴", { x: 250, y: 50, w: 780, h: 52 }, {
    size: 36,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "全面开放 WorkBuddy 产品能力，首批加入共创生态伙伴", { x: 220, y: 104, w: 840, h: 34 }, {
    size: 19,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  card(slide, ctx, { x: 96, y: 150, w: 1088, h: 262 }, { fill: "#FFFFFFC8", line: "#A7E7DF" });
  await ctx.addImage(slide, {
    path: path.join(ctx.assetDir, "partner-logos.png"),
    x: 122,
    y: 170,
    w: 1038,
    h: 218,
    fit: "contain",
    alt: "WorkBuddy partner logo matrix",
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 150,
    y: 452,
    w: 980,
    h: 96,
    fill: "#6FE0D54D",
  });
  card(slide, ctx, { x: 252, y: 448, w: 256, h: 232 }, { fill: "#FFFFFFD8", line: "#B6EDE7" });
  card(slide, ctx, { x: 772, y: 448, w: 256, h: 232 }, { fill: "#FFFFFFD8", line: "#B6EDE7" });

  await ctx.addImage(slide, {
    path: path.join(ctx.assetDir, "qr-public.png"),
    x: 316,
    y: 466,
    w: 140,
    h: 140,
    fit: "contain",
    alt: "WorkBuddy official account QR code",
  });
  await ctx.addImage(slide, {
    path: path.join(ctx.assetDir, "qr-miniapp.png"),
    x: 836,
    y: 466,
    w: 140,
    h: 140,
    fit: "contain",
    alt: "WorkBuddy mini app QR code",
  });

  text(slide, ctx, "扫码关注", { x: 270, y: 610, w: 220, h: 28 }, {
    size: 20,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "WorkBuddy 公众号", { x: 260, y: 638, w: 240, h: 30 }, {
    size: 18,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "扫码体验", { x: 790, y: 610, w: 220, h: 28 }, {
    size: 20,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  text(slide, ctx, "WorkBuddy 小程序", { x: 780, y: 638, w: 240, h: 30 }, {
    size: 18,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  return slide;
}
