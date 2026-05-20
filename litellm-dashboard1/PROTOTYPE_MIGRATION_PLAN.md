# LiteLLM Dashboard → 前端高保真原型：AI 逐步执行计划

> **文档用途**：供 AI Agent 或开发者按任务 ID 顺序执行，在 **`litellm-dashboard1/`** 目录构建**不依赖 LiteLLM Proxy 后端**、仅通过 Mock 数据驱动的高保真原型项目。  
> **执行原则**：每完成一个任务必须跑验收命令；未通过不得进入下一任务；改 UI 组件前先 Mock API 边界。

---

## 0. 元信息

| 项 | 值 |
|---|---|
| **本项目根目录** | `litellm-dashboard1/`（本目录） |
| **上游 UI 源码** | `../ui/litellm-dashboard/`（LiteLLM monorepo，复制来源） |
| 主 API 层 | `src/components/networking.tsx`（~280 导出、~348 处 fetch） |
| 数据 Hooks | `src/app/(dashboard)/hooks/`（44 个子目录） |
| 构建 | Next.js 16，`output: "export"`（`next.config.mjs`） |
| 目标模式 | `NEXT_PUBLIC_MOCK_MODE=true` 时 MSW 拦截全部 API |
| 预估 MVP | 2–3 周（1 人）；全量 6–10 周 |

### 0.1 给 AI 的执行约定

1. **一次只做一个任务 ID**（如 `P1-03`），完成后在 `MOCK_PROGRESS.md` 打勾。
2. **所有命令默认在 `litellm-dashboard1/` 下执行**（`cd litellm-dashboard1`）。
3. **禁止**在未启用 Mock 时大规模改 UI 逻辑；优先加 `src/mocks/` 与 handler。
4. **禁止**把 access token / API key 写入 `localStorage`（沿用 `sessionStorage` 规则）。
5. 新 UI 组件使用 **antd**（勿新增 `@tremor/react`）。
6. 提交前执行：`npm run format`（若有）、`npm run test:dot`、`npm run build`。
7. 每个任务末尾必须有 **验收标准** 与 **验证命令**。

### 0.2 范围开关（执行前由人确认）

在 `MOCK_PROGRESS.md` 填写：

- [ ] **模式 A — 只读演示**：列表/详情/图表可浏览，写操作 toast「原型模式」
- [ ] **模式 B — 假 CRUD**（推荐）：内存 MockStore，创建/编辑/删除在会话内生效
- [ ] **是否保留连接真实 Proxy**：`NEXT_PUBLIC_MOCK_MODE=false` + `NEXT_PUBLIC_PROXY_URL`

---

## 1. 目标架构

```
┌─────────────────────────────────────────────────────────┐
│  Pages / Components（尽量不改）                          │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│  hooks (TanStack Query) + networking.tsx                 │
└───────────────────────────┬─────────────────────────────┘
                            │ fetch()
┌───────────────────────────▼─────────────────────────────┐
│  MSW (browser) — when NEXT_PUBLIC_MOCK_MODE=true         │
│    handlers/*.ts → fixtures/*.json → mockStore.ts        │
└─────────────────────────────────────────────────────────┘
```

**不采用**：重写 280 个 `*Call` 函数。  
**采用**：MSW 按 URL path 通配拦截 `fetch`。

---

## 2. 最终目录结构（计划结束时存在）

```text
litellm-dashboard1/
├── PROTOTYPE_MIGRATION_PLAN.md          # 本文档
├── MOCK_PROGRESS.md
├── README.md
├── .env.mock.example
├── package.json
├── next.config.mjs
├── public/
│   └── mockServiceWorker.js             # MSW（P2-01）
├── docs/
│   ├── networking-calls.txt             # P0-02 生成
│   └── networking-paths.txt
└── src/
    ├── mocks/
    │   ├── README.md
    │   ├── index.ts
    │   ├── browser.ts
    │   ├── config.ts
    │   ├── mockStore.ts
    │   ├── utils.ts
    │   ├── unhandled-requests.md
    │   ├── auth/
    │   ├── fixtures/
    │   └── handlers/
    ├── components/dev/MockRoleSwitcher.tsx
    └── app/MockProvider.tsx
```

---

## 3. 阶段总览

| 阶段 | 名称 | 任务 ID 前缀 | 预估 |
|------|------|--------------|------|
| 0 | 范围与基线 | `P0-` | 0.5d |
| 1 | 源码迁入与配置 | `P1-` | 1–2d |
| 2 | Mock 基础设施 | `P2-` | 3–5d |
| 3 | 认证与壳子 | `P3-` | 2–3d |
| 4 | P0 页面 Mock | `P4-` | 1–2w |
| 5 | P1 页面 Mock | `P5-` | 1–2w |
| 6 | 特殊流与交付 | `P6-` | 3–7d |

---

## 4. 阶段 0：范围与基线（P0）

### P0-01 创建进度跟踪文件

**操作**：确认 `MOCK_PROGRESS.md` 存在，§12 任务全部 `[ ]`。

**验收**：文件在本目录根下且表格完整。

---

### P0-02 生成 API 清单（自动化）

**前置**：已完成 **P1-00**（`src/components/networking.tsx` 已存在）。

**操作**：在 **`litellm-dashboard1/`** 执行：

```bash
cd litellm-dashboard1
mkdir -p docs
rg "^export const (\w+Call)" src/components/networking.tsx -o -r '$1' | sort -u > docs/networking-calls.txt
rg 'url = proxyBaseUrl \? `\$\{proxyBaseUrl\}([^`]+)`' src/components/networking.tsx -o -r '$1' | sort -u > docs/networking-paths.txt
```

**验收**：`docs/networking-calls.txt` 行数 ≥ 150。

---

### P0-03 确认 MVP 页面矩阵

**MVP（P0）页面** — 必须 Mock：

| 路由/入口 | 主要 networking 函数 | 优先级 |
|-----------|---------------------|--------|
| `/ui/login` | `getUiConfig`, `loginCall` | P0 |
| `/ui` 壳子 | `getUiConfig`, `getProxyUISettings`, `userGetInfoV2`, `modelAvailableCall` | P0 |
| Virtual Keys | `keyListCall`, `keyInfoV1Call`, `keyCreateCall`, `keyDeleteCall` | P0 |
| Teams | `v2TeamListCall`, `teamInfoCall`, `teamCreateCall` | P0 |
| Users | `userListCall`, `userInfoCall` | P0 |
| Models & Endpoints | `modelAvailableCall`, `modelInfoCall`, `credentialListCall` | P0 |
| Usage | `userDailyActivityCall`, `adminGlobalActivity`, `tagsSpendLogsCall` | P0 |
| Logs | `uiSpendLogsCall`, `keyInfoCall` | P0 |
| Model Hub 公开 | `modelHubPublicModelsCall`, `getPublicModelHubInfo` | P0 |
| Settings（只读） | `getProxyUISettings`, `alertingSettingsCall` | P0 |

**P1**：MCP、Guardrails、Playground、Organizations、API Reference。  
**P2**：Policies、Projects、Access Groups、Cost Tracking、CloudZero、Workflow Runs。

**验收**：MVP 列表已写入 `MOCK_PROGRESS.md` 决策记录。

---

## 5. 阶段 1：源码迁入与配置（P1）

### P1-00 从 monorepo 复制前端源码（首要任务）

**操作**：在 LiteLLM 仓库根目录执行：

```bash
# 在 litellm 仓库根：/Users/chailishen/Documents/Project/litellm
rsync -a --exclude node_modules --exclude .next --exclude out \
  ui/litellm-dashboard/ litellm-dashboard1/
```

**说明**：
- 保留本目录已有的 `PROTOTYPE_MIGRATION_PLAN.md`、`MOCK_PROGRESS.md`、`.env.mock.example`（rsync 后用计划文档覆盖或合并 README）。
- 复制后删除 `litellm-dashboard1` 内与 monorepo 发布相关的脚本引用（若有 `build_release_ui.sh` 指向 proxy 的，可删或改注释）。

**验收**：
- [ ] `litellm-dashboard1/package.json` 存在
- [ ] `litellm-dashboard1/src/app/page.tsx` 存在
- [ ] `cd litellm-dashboard1 && npm install` 成功

---

### P1-01 添加 Mock 环境变量模板

**确认/更新** 根目录 `.env.mock.example`（已提供则核对字段）。

**本地**：`cp .env.mock.example .env.local`

**验收**：`grep MOCK_MODE .env.mock.example` 成功。

---

### P1-02 调整 Next 配置（独立原型项目）

**修改** `next.config.mjs`：

- 本项目为独立原型，默认：
  - `assetPrefix: ""`（或 `"/"`）
  - 保留 `output: "export"`
- 删除或注释仅用于 monorepo 内嵌 Proxy 的 `assetPrefix: "/litellm-asset-prefix"`，除非仍需嵌回 Proxy。

**验收**：`npm run build` 生成 `out/index.html` 且静态资源路径正确。

---

### P1-03 更新 README

**修改** `README.md`：

- 标明本项目为 **LiteLLM Dashboard 高保真原型**（无后端）
- 链接 `PROTOTYPE_MIGRATION_PLAN.md`、`MOCK_PROGRESS.md`
- Mock 启动：`cp .env.mock.example .env.local && npm run dev:mock`

**验收**：README 含原型说明与计划链接。

---

### P1-04 添加 npm scripts

**修改** `package.json`：

```json
"dev:mock": "NEXT_PUBLIC_MOCK_MODE=true next dev",
"build:mock": "NEXT_PUBLIC_MOCK_MODE=true next build",
"build:standalone": "NEXT_PUBLIC_MOCK_MODE=true next build"
```

**验收**：`npm run dev:mock` 进程可启动。

---

### P1-05 独立仓库 .gitignore（可选）

**创建/核对** `.gitignore`：`.env.local`、`node_modules/`、`.next/`、`out/`。

**验收**：`git status` 不跟踪敏感与构建产物。

---

## 6. 阶段 2：Mock 基础设施（P2）

### P2-01 安装 MSW

```bash
cd litellm-dashboard1
npm install -D msw@latest
npx msw init public/ --save
```

**验收**：`public/mockServiceWorker.js` 存在。

---

### P2-02 创建 mocks 骨架

**创建**：

- `src/mocks/config.ts`
- `src/mocks/mockStore.ts`
- `src/mocks/browser.ts`
- `src/mocks/handlers/index.ts`
- `src/mocks/index.ts`
- `src/mocks/README.md`（可覆盖占位内容）

**`config.ts` 模板**：

```typescript
export const isMockMode = (): boolean =>
  process.env.NEXT_PUBLIC_MOCK_MODE === "true";

export const mockLatency = (): number => {
  const min = Number(process.env.NEXT_PUBLIC_MOCK_LATENCY_MS_MIN ?? 200);
  const max = Number(process.env.NEXT_PUBLIC_MOCK_LATENCY_MS_MAX ?? 600);
  return min + Math.random() * (max - min);
};

export const mockDefaultRole = (): string =>
  process.env.NEXT_PUBLIC_MOCK_DEFAULT_ROLE ?? "proxy_admin";
```

**验收**：`npm run build` 通过（暂不挂 layout）。

---

### P2-03 Mock JWT 与 auth fixtures

**创建** `src/mocks/auth/tokens.ts`、`src/mocks/fixtures/ui-config.json`（见原 §2-03 字段）。

**验收**：`jwt-decode` 解码 `MOCK_ACCESS_TOKEN` 不抛错。

---

### P2-04 实现 mockStore（模式 B）

**职责**：keys/teams 增删改；`resetMockStore()`；单测 `src/mocks/mockStore.test.ts`。

**验收**：`npm run test:dot -- src/mocks/mockStore.test.ts` 通过。

---

### P2-05 实现全局 handlers

**文件** `src/mocks/handlers/global.ts`：

| Method | Path 模式 | 响应 |
|--------|-----------|------|
| GET | `getUiConfig` 实际 path | `fixtures/ui-config.json` |
| GET | `*/sso/get/ui_settings` | `fixtures/proxy-ui-settings.json` |
| POST | `*/v2/login`, `*/v3/login` | mock token |
| GET | `userGetInfoV2` 实际 path | `fixtures/user-info.json` |

**核对 path**：`rg "getUiConfig|loginCall|userGetInfoV2" src/components/networking.tsx`

**验收**：MSW 下 `fetch` 登录接口返回 200。

---

### P2-06 MockProvider 与 layout 集成

**创建** `src/app/MockProvider.tsx`，**修改** `src/app/layout.tsx` 包裹子节点。

**验收**：`npm run dev:mock` 控制台 `[MSW] Mocking enabled`。

---

### P2-07 通用 handler 工具

**创建** `src/mocks/utils.ts`：`jsonResponse`、`requireAuth`、`parseBearer`。

**验收**：handlers 无重复样板。

---

## 7. 阶段 3：认证与壳子（P3）

### P3-01 登录流程 Mock

扩展 `global.ts`；`LoginPage.tsx` 可加「Prototype Mode」Tag。

**验收**：`http://localhost:3000/ui/login` → 任意凭据 → `/ui` + Sidebar。

---

### P3-02 壳子启动数据

Fixtures：`user-info.json`、`models-available.json`、`proxy-ui-settings.json`、`in-product-nudges.json`。

**验收**：刷新 `/ui` 无 401 洪流。

---

### P3-03 Mock 角色切换器

`src/components/dev/MockRoleSwitcher.tsx` 挂到 `navbar.tsx`。

**验收**：切换角色后菜单权限变化正确。

---

### P3-04 防踢回登录

Mock token 长效；`getUiConfig` 始终成功。

**验收**：Mock 模式 10 分钟不被踢回 login。

---

## 8. 阶段 4：P0 页面 Mock（P4）

### P4-01 Virtual Keys

`handlers/keys.ts` + `fixtures/keys-list.json`（≥15 条）。

**验收**：列表、详情 Drawer、创建 Key（模式 B）。

---

### P4-02 Teams

`handlers/teams.ts` + fixtures。

**验收**：列表、详情、创建 Team。

---

### P4-03 Users

`handlers/users.ts`。

**验收**：用户表与详情侧栏。

---

### P4-04 Models & Endpoints

`handlers/models.ts` + 多 provider fixtures。

**验收**：模型列表、详情、添加向导前两步。

---

### P4-05 Usage

`handlers/usage.ts` + 30 天时间序列 fixtures。

**验收**：图表有数据、改日期不报错。

---

### P4-06 Logs

`handlers/logs.ts` + `logs-list.json`（≥50 条）。

**验收**：表格、筛选、LogDetailsDrawer。

---

### P4-07 Model Hub

`handlers/hub-public.ts`。

**验收**：公开 Hub 页有卡片。

---

### P4-08 Settings（只读）

`handlers/settings.ts`；写操作返回 200 + 原型提示。

**验收**：各 Tab 可开、保存不 404。

---

### P4-09 合并 handlers

`handlers/index.ts` 导出数组；`browser.ts` 注册。

**验收**：P0 页面 MSW unhandled = 0。

---

### P4-10 未处理请求清单

记录到 `src/mocks/unhandled-requests.md`。

**验收**：P0 无未记录的红字请求。

---

## 9. 阶段 5：P1 页面 Mock（P5）

| 任务 | 内容 |
|------|------|
| P5-01 | MCP Servers |
| P5-02 | Guardrails |
| P5-03 | Playground 假 SSE 流式 |
| P5-04 | Organizations |
| P5-05 | API Reference + openapi fixture |

（各任务验收标准同 P4：页面可浏览、核心交互不 404。）

---

## 10. 阶段 6：特殊流与交付（P6）

| 任务 | 内容 |
|------|------|
| P6-01 | Onboarding mock |
| P6-02 | MCP OAuth callback 静态成功页 |
| P6-03 | Chat 页 mock 或 Banner |
| P6-04 | Playwright `baseURL: localhost:3000` + mock storageState |
| P6-05 | CI：`npm run build:mock` + 静态产物 |
| P6-06 | 更新 `src/mocks/README.md` 与交接说明 |

---

## 11. 测试策略

| 层级 | 命令 |
|------|------|
| 单元 | `npm run test:dot` |
| 构建 | `npm run build:mock` |
| 手动 | `npm run dev:mock` |

**Vitest + MSW（可选）**：`setupServer` 于 `vitest.setup.ts`。

---

## 12. 进度跟踪表

见 **`MOCK_PROGRESS.md`**（与本计划同步更新）。

---

## 13. 附录 A：Hooks → Handler 映射

| Hook 目录 | 关键 Call |
|-----------|-----------|
| `hooks/keys/` | `keyListCall`, `keyInfoV1Call` |
| `hooks/teams/` | `v2TeamListCall`, `teamInfoCall` |
| `hooks/users/` | `userListCall`, `userInfoCall` |
| `hooks/models/` | `modelAvailableCall`, `modelInfoCall` |
| `hooks/mcpServers/` | MCP CRUD calls |
| `hooks/login/` | `loginCall` |

```bash
rg "from \"@/components/networking\"" src/app/(dashboard)/hooks -l
```

---

## 14. 附录 B：常见陷阱

1. MSW 用 `*/path` 通配，不写死 host。  
2. `getGlobalLitellmHeaderName()` 默认 `Authorization`。  
3. `user_dashboard.tsx` 的 sessionStorage 缓存：改 fixture 后清缓存或版本 key。  
4. **勿再依赖** `../litellm/proxy/_experimental/out` 发布 UI。  
5. Playground WebSocket：原型可禁用并提示。

---

## 15. 附录 C：AI 单任务执行模板

```markdown
## 正在执行：<TASK_ID>
### 工作目录
litellm-dashboard1/
### 输入
- 前置：<已完成 ID>
- 模式：A 只读 / B 假 CRUD
### 步骤
1. ...
### 验收
- [ ] `cd litellm-dashboard1 && npm run dev:mock`
- [ ] `npm run test:dot -- <paths>`
### 完成后
- 更新 MOCK_PROGRESS.md
```

---

## 16. 快速命令参考

```bash
cd litellm-dashboard1

# 首次迁入源码（仅一次）
rsync -a --exclude node_modules --exclude .next --exclude out \
  ../ui/litellm-dashboard/ ./

cp .env.mock.example .env.local
npm install
npm run dev:mock

npm run test:dot
npm run build:mock
npx serve out
```

---

*文档版本：1.1 | 项目根目录：litellm-dashboard1 | 上游：../ui/litellm-dashboard*
