export const C = {
  ink: "#2D3340",
  muted: "#667A83",
  teal: "#17C8B5",
  tealDark: "#128D85",
  mint: "#E9FFFB",
  cyan: "#47B7F4",
  blue: "#5D87E9",
  line: "#A5E4DD",
  pale: "#F3FFFD",
  white: "#FFFFFF",
};

export function addBg(slide, ctx) {
  ctx.addShape(slide, {
    x: 0,
    y: 0,
    w: ctx.W,
    h: ctx.H,
    fill: {
      type: "gradient",
      gradientKind: "linear",
      angleDeg: 20,
      stops: [
        { offset: 0, color: "#F6FFFD" },
        { offset: 55000, color: "#ECFEFA" },
        { offset: 100000, color: "#D7FAF4" },
      ],
    },
  });
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: -170,
    y: 545,
    w: 520,
    h: 230,
    fill: "#7DE9D955",
  });
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 970,
    y: -110,
    w: 340,
    h: 250,
    fill: "#93EFE655",
  });
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 420,
    y: 596,
    w: 440,
    h: 92,
    fill: "#B8F4EF55",
  });
  for (let i = 0; i < 12; i += 1) {
    ctx.addShape(slide, {
      geometry: "ellipse",
      x: 1115 + (i % 4) * 18,
      y: 560 + Math.floor(i / 4) * 18,
      w: 4,
      h: 4,
      fill: "#7EDBD255",
    });
  }
}

export function text(slide, ctx, value, frame, opts = {}) {
  return ctx.addText(slide, {
    text: value,
    x: frame.x,
    y: frame.y,
    w: frame.w,
    h: frame.h,
    fontSize: opts.size ?? 22,
    color: opts.color ?? C.ink,
    bold: opts.bold ?? false,
    typeface: opts.face ?? "PingFang SC",
    align: opts.align ?? "left",
    valign: opts.valign ?? "middle",
    fill: opts.fill ?? "#00000000",
    line: opts.line ?? { style: "solid", fill: "#00000000", width: 0 },
    insets: opts.insets ?? { left: 6, right: 6, top: 3, bottom: 3 },
    name: opts.name,
  });
}

export function title(slide, ctx, main, sub = "") {
  text(slide, ctx, main, { x: 72, y: 44, w: 860, h: 56 }, {
    size: 31,
    bold: true,
    color: C.tealDark,
  });
  if (sub) {
    text(slide, ctx, sub, { x: 76, y: 94, w: 760, h: 28 }, {
      size: 14,
      color: C.muted,
    });
  }
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: 48,
    y: 65,
    w: 10,
    h: 10,
    fill: C.teal,
  });
}

export function card(slide, ctx, frame, opts = {}) {
  return ctx.addShape(slide, {
    geometry: "roundRect",
    x: frame.x,
    y: frame.y,
    w: frame.w,
    h: frame.h,
    fill: opts.fill ?? "#FFFFFFCC",
    line: { style: "solid", fill: opts.line ?? C.line, width: opts.width ?? 1.2 },
    name: opts.name,
  });
}

export function pill(slide, ctx, frame, value, opts = {}) {
  card(slide, ctx, frame, { fill: opts.fill ?? "#FFFFFFB8", line: opts.line ?? C.line, width: 1 });
  return text(slide, ctx, value, frame, {
    size: opts.size ?? 15,
    bold: opts.bold ?? true,
    color: opts.color ?? C.tealDark,
    align: "center",
    valign: "middle",
  });
}

export function iconCircle(slide, ctx, x, y, size, icon, opts = {}) {
  ctx.addShape(slide, {
    geometry: "ellipse",
    x,
    y,
    w: size,
    h: size,
    fill: opts.fill ?? "#DDFBF6",
    line: { style: "solid", fill: opts.line ?? "#B4ECE4", width: 1 },
  });
  return ctx.addLucideIcon(slide, {
    icon,
    x: x + size * 0.24,
    y: y + size * 0.24,
    w: size * 0.52,
    h: size * 0.52,
    color: opts.color ?? C.tealDark,
    strokeWidth: 2.2,
  });
}

export function arrow(slide, ctx, x1, y1, x2, y2, opts = {}) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.max(1, Math.hypot(dx, dy));
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  const body = ctx.addShape(slide, {
    x: x1,
    y: y1 - (opts.width ?? 2) / 2,
    w: len,
    h: opts.width ?? 2,
    fill: opts.color ?? C.line,
  });
  body.position.rotation = angle;
  ctx.addShape(slide, {
    geometry: "triangle",
    x: x2 - 8,
    y: y2 - 6,
    w: 12,
    h: 12,
    fill: opts.color ?? C.line,
    line: { style: "solid", fill: "#00000000", width: 0 },
  }).position.rotation = angle + 90;
}

export function mascot(slide, ctx, x, y, scale = 1) {
  ctx.addShape(slide, {
    geometry: "ellipse",
    x: x - 22 * scale,
    y: y + 82 * scale,
    w: 230 * scale,
    h: 34 * scale,
    fill: "#49D6C655",
  });
  const head = ctx.addShape(slide, {
    geometry: "roundRect",
    x,
    y,
    w: 180 * scale,
    h: 118 * scale,
    fill: {
      type: "gradient",
      gradientKind: "linear",
      angleDeg: 35,
      stops: [
        { offset: 0, color: "#58E8D4" },
        { offset: 100000, color: "#09BFAE" },
      ],
    },
    line: { style: "solid", fill: "#8EF5EA", width: 1 },
  });
  head.position.rotation = -14;
  const eye1 = ctx.addShape(slide, {
    geometry: "roundRect",
    x: x + 45 * scale,
    y: y + 40 * scale,
    w: 22 * scale,
    h: 46 * scale,
    fill: C.white,
  });
  eye1.position.rotation = -14;
  const eye2 = ctx.addShape(slide, {
    geometry: "roundRect",
    x: x + 113 * scale,
    y: y + 24 * scale,
    w: 22 * scale,
    h: 46 * scale,
    fill: C.white,
  });
  eye2.position.rotation = -14;
}

export function smallFooter(slide, ctx, n) {
  text(slide, ctx, `WorkBuddy 产品家族全景图  |  ${n}/5`, { x: 970, y: 682, w: 210, h: 20 }, {
    size: 10,
    color: "#7B9D9A",
    align: "right",
  });
}
