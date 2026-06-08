import { C, addBg, card, iconCircle, pill, smallFooter, text, title } from "./common.mjs";

function stack(slide, ctx, x, y, heading, items) {
  card(slide, ctx, { x, y, w: 174, h: 336 }, { fill: "#FFFFFFC8" });
  text(slide, ctx, heading, { x: x + 16, y: y + 18, w: 142, h: 26 }, {
    size: 17,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  items.forEach((item, i) => {
    const top = y + 62 + i * 48;
    pill(slide, ctx, { x: x + 24, y: top, w: 126, h: 33 }, item.main, {
      size: 13,
      color: C.ink,
      fill: "#FFFFFFE8",
      line: "#C6EDE9",
    });
    if (item.sub) {
      text(slide, ctx, item.sub, { x: x + 24, y: top + 26, w: 126, h: 18 }, {
        size: 8,
        color: C.muted,
        align: "center",
      });
    }
  });
}

function miniArrow(slide, ctx, x, y, w = 30) {
  ctx.addShape(slide, { x, y, w, h: 3, fill: "#9BE7DF" });
  ctx.addShape(slide, {
    geometry: "triangle",
    x: x + w - 4,
    y: y - 5,
    w: 12,
    h: 12,
    fill: "#9BE7DF",
    line: { style: "solid", fill: "#00000000", width: 0 },
  }).position.rotation = 90;
}

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);
  title(slide, ctx, "WorkBuddy 企业 AI 工作台架构", "从智能体套件到数字员工，再到企业级资产与治理平台");

  stack(slide, ctx, 50, 160, "智能体套件", [
    { main: "腾讯文档" },
    { main: "腾讯网盘" },
    { main: "腾讯乐享" },
    { main: "研发智能体", sub: "CodeBuddy" },
    { main: "设计智能体", sub: "Ardot" },
    { main: "创意智能体", sub: "Miora" },
  ]);

  stack(slide, ctx, 1056, 160, "企业 AI 资产", [
    { main: "企业知识", sub: "组织记忆" },
    { main: "Skills", sub: "技能封装" },
    { main: "专家", sub: "经验沉淀" },
    { main: "连接器", sub: "系统接入" },
    { main: "大模型", sub: "模型能力底座" },
  ]);

  card(slide, ctx, { x: 282, y: 150, w: 666, h: 426 }, { fill: "#FFFFFFB8" });
  pill(slide, ctx, { x: 342, y: 170, w: 545, h: 38 }, "WorkBuddy · 企业 AI 工作台", {
    size: 18,
    fill: "#FFFFFFDD",
  });

  const left = card(slide, ctx, { x: 326, y: 244, w: 260, h: 96 }, { fill: "#F7FFFD" });
  const right = card(slide, ctx, { x: 650, y: 244, w: 260, h: 96 }, { fill: "#F7FFFD" });
  iconCircle(slide, ctx, 352, 270, 46, "UserRound");
  iconCircle(slide, ctx, 676, 270, 46, "UsersRound");
  text(slide, ctx, "超级个体（个人提效）", { x: 410, y: 258, w: 160, h: 28 }, {
    size: 17,
    bold: true,
    color: C.tealDark,
  });
  text(slide, ctx, "发挥 WorkBuddy 办公应用能力\n完成任务与知识沉淀", { x: 410, y: 288, w: 165, h: 42 }, {
    size: 11,
    color: C.muted,
  });
  text(slide, ctx, "超级团队（组织提效）", { x: 734, y: 258, w: 170, h: 28 }, {
    size: 17,
    bold: true,
    color: C.tealDark,
  });
  text(slide, ctx, "通过一组智能体协同员工\n完成跨职能任务", { x: 734, y: 288, w: 170, h: 42 }, {
    size: 11,
    color: C.muted,
  });
  miniArrow(slide, ctx, 604, 290, 30);

  ctx.addShape(slide, {
    geometry: "roundRect",
    x: 426,
    y: 356,
    w: 382,
    h: 70,
    line: { style: "solid", fill: C.teal, width: 1.6 },
    fill: "#00000000",
  });
  text(slide, ctx, "数字员工可由人或组织指挥", { x: 430, y: 376, w: 364, h: 26 }, {
    size: 16,
    bold: true,
    color: C.tealDark,
    align: "center",
  });

  pill(slide, ctx, { x: 370, y: 428, w: 490, h: 32 }, "智能体创建", { size: 14 });
  card(slide, ctx, { x: 326, y: 484, w: 584, h: 74 }, { fill: "#FBFFFE" });
  text(slide, ctx, "7*24 小时在线的数字员工", { x: 430, y: 494, w: 370, h: 22 }, {
    size: 15,
    bold: true,
    color: C.tealDark,
    align: "center",
  });
  const rolesA = ["前端开发", "项目经理", "营销顾问", "招聘经理"];
  const rolesB = ["一人公司（OPC）", "软件开发团队", "内容创作团队"];
  text(slide, ctx, "专家", { x: 344, y: 526, w: 46, h: 20 }, { size: 12, bold: true, color: C.tealDark });
  rolesA.forEach((role, i) => pill(slide, ctx, { x: 400 + i * 126, y: 524, w: 106, h: 22 }, role, { size: 10, bold: false, color: C.muted }));
  text(slide, ctx, "专家团", { x: 344, y: 548, w: 46, h: 20 }, { size: 12, bold: true, color: C.tealDark });
  rolesB.forEach((role, i) => pill(slide, ctx, { x: 400 + i * 156, y: 548, w: 132, h: 22 }, role, { size: 10, bold: false, color: C.muted }));

  pill(slide, ctx, { x: 76, y: 612, w: 1088, h: 38 }, "智能体与资产治理 · WorkBuddy 企业管理平台（Agent 治理可见、可控、可管）", {
    size: 18,
    fill: "#FFFFFFC8",
  });

  smallFooter(slide, ctx, 2);
  return slide;
}
