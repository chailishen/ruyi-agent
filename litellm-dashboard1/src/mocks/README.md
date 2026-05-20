# Mock 层（MSW）

`NEXT_PUBLIC_MOCK_MODE=true` 时拦截 API，无需 LiteLLM Proxy。

## 结构

| 路径 | 说明 |
|------|------|
| `handlers/` | 按领域划分的 MSW handlers |
| `fixtures/` | 静态 JSON 样例 |
| `mockStore.ts` | 会话内 Key 假 CRUD |
| `auth/tokens.ts` | Mock JWT |

## 已覆盖

global、keys、teams、users、organizations、models、usage、logs、hub、settings、**mcp**、**guardrails**、**playground**（含流式 chat）、**openapi**、**onboarding**、**common**

## 新增端点

1. `fixtures/<name>.json`
2. `handlers/<domain>.ts` 内 `http.get/post`
3. 写操作 → `mockStore.ts`
4. 注册到 `handlers/index.ts`
