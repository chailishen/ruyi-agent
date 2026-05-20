# litellm-dashboard1

LiteLLM 管理端 UI 的**独立高保真原型**（MSW Mock 数据，无需 LiteLLM Proxy）。

## 文档

| 文件 | 说明 |
|------|------|
| [PROTOTYPE_MIGRATION_PLAN.md](./PROTOTYPE_MIGRATION_PLAN.md) | 完整迁移与扩展计划 |
| [MOCK_PROGRESS.md](./MOCK_PROGRESS.md) | 任务进度 |

## 快速开始

```bash
cd litellm-dashboard1
cp .env.mock.example .env.local
npm install
npm run dev:mock
```

浏览器打开 **[http://localhost:3000/login](http://localhost:3000/login)**（独立原型用 `/login`，不是 `:4000/ui/login`），任意凭据登录。

> 若被跳到 `localhost:4000`，说明未开 Mock 或需重启 `npm run dev:mock`；勿单独启动 LiteLLM Proxy。

### 主要原型页面

| 功能 | 路径 |
|------|------|
| MCP Servers | `/tools/mcp-servers` |
| Guardrails | `/guardrails` |
| Playground | `/playground` |
| API Reference | `/api-reference` |
| Onboarding | `/onboarding?invitation_id=demo` |

## 脚本

| 命令 | 说明 |
|------|------|
| `npm run dev:mock` | Mock 模式开发 |
| `npm run build:mock` | Mock 模式静态构建 |
| `npm run build:standalone` | 独立部署（无 asset 前缀） |
| `npm run test:dot` | 单元测试 |
| `npm run e2e:mock` | E2E（需先 `dev:mock`，Mock 登录态） |

## 上游源码

初始 UI 来自 `../ui/litellm-dashboard/`。重新同步：

```bash
rsync -a --exclude node_modules --exclude .next --exclude out \
  ../ui/litellm-dashboard/ ./
```

保留本目录的 `src/mocks/` 与计划文档。
