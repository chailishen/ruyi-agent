# Mock 原型迁移进度

> **项目目录**：`litellm-dashboard1/`

模式选择：**[x] 假 CRUD（推荐）**

最后更新：2026-05-20

---

## 阶段 0：基线

- [x] P0-01 进度文件
- [x] P0-02 API 清单（`docs/networking-calls.txt`，134 条）
- [x] P0-03 MVP 矩阵确认

## 阶段 1：源码迁入与配置

- [x] P1-00 ~ P1-05

## 阶段 2–3：Mock 基础与认证

- [x] P2-01 ~ P2-07
- [x] P3-01 ~ P3-04

## 阶段 4：P0 页面

- [x] P4-01 ~ P4-09
- [x] P4-10 常见 API 已补 `common.ts`（手测各页仍可能有遗漏）

## 阶段 5–6：P1 与交付

- [x] P5-01 MCP Servers
- [x] P5-02 Guardrails
- [x] P5-03 Playground（`/v1/chat/completions` 假流式）
- [x] P5-04 Organizations（list + info）
- [x] P5-05 API Reference（`openapi.json`）
- [x] P6-01 Onboarding
- [x] P6-02 MCP OAuth callback（沿用现有页，redirect 至 `/`）
- [x] P6-03 Chat（复用 Playground chat completions mock）
- [x] P6-04 E2E（`globalSetup.mock.ts` + `npm run e2e:mock`）
- [x] P6-05 CI（`.github/workflows/litellm-dashboard1-prototype.yml`）
- [x] P6-06 文档（`src/mocks/README.md`、本文件）

---

## 本地验证

```bash
cd litellm-dashboard1
npm run dev:mock
# http://localhost:3000/login
```

| 页面 | 路径（独立原型） |
|------|------------------|
| 登录 | `/login` |
| 主页 | `/` |
| Virtual Keys | `/?page=api-keys` 或 `/virtual-keys` |
| MCP | `/tools/mcp-servers` |
| Guardrails | `/guardrails` |
| Playground | `/playground` |
| API Reference | `/api-reference` |
| Onboarding | `/onboarding?invitation_id=demo-invite` |

```bash
npm run build:mock
npm run test:dot -- src/mocks/mockStore.test.ts
PLAYWRIGHT_MOCK_MODE=true npm run e2e:mock   # 需先 dev:mock
```

---

## 决策记录

| 日期 | 决策 | 说明 |
|------|------|------|
| 2026-05-20 | 模式 B | mockStore Key 假 CRUD |
| 2026-05-20 | 登录不重定向 :4000 | `isMockMode()` + `proxyBaseUrl=null` |
| 2026-05-20 | Playground SSE | MSW `ReadableStream` 模拟流式 |
