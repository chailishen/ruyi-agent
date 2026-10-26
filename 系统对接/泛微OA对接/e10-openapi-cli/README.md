# 泛微 E10 OpenAPI CLI

供技能 / Agent 调用的命令行封装。当前版本只做**流程查询**。

## 对应官方 API

| 命令 | 官方接口 | 路径 |
|---|---|---|
| `workflow list-all` | 所有流程列表 | `POST /api/workflow/list/paService/v1/getAllWorkflowRequestList` |
| `workflow count-all` | 所有流程数量 | `POST /api/workflow/list/paService/v1/getAllWorkflowRequestCount` |
| `workflow list-monitor` | 监控列表数据 | `POST /api/workflow/list/paService/v1/getMonitorWorkflowRequestList` |
| `workflow count-monitor` | 监控列表数量 | `POST /api/workflow/list/paService/v1/getMonitorWorkflowRequestCount` |

文档来源：`../fanwei-openapi/markdown/工作流程/`

### 范围说明（重要）

- `list-all` / `count-all`：官方写明**默认返回当前 userid 参与的流程**，不是系统全库。
- 若要查「有监控权限可见的更多单据」，用 `list-monitor` / `count-monitor`（需该用户具备流程监控权限）。

## 认证

标准链路：`authorize` 拿 code → `access_token`（约 2 小时）→ 调业务接口。  
可选：`refresh_token` 续期。凭证与令牌缓存到本地 `state/`，勿提交仓库。

```bash
cp config.example.env config.env   # 填入 corpid / app_key / app_secret / userid / openapi origin
pip install -r requirements.txt
python e10_openapi.py auth code
python e10_openapi.py auth token --code <上一步返回的code>
python e10_openapi.py auth status
```

## 流程查询示例

```bash
# 第 1 页，默认 20 条
python e10_openapi.py workflow list-all

# 数量
python e10_openapi.py workflow count-all

# 按标题、工作流、状态、发起时间筛选
python e10_openapi.py workflow list-all \
  --title 会议申请 \
  --workflow-id 1302788388361633792 \
  --status 1,3 \
  --create-start "2026-10-01 00:00:00" \
  --create-end "2026-10-22 23:59:59" \
  --page 1 --size 50

# 自动翻页拉完（有 max-pages 保护）
python e10_openapi.py workflow list-all --all-pages --max-pages 20

# 监控视角
python e10_openapi.py workflow list-monitor --page 1 --size 50
```

所有命令 stdout 输出**单个 JSON 对象**，便于技能解析。

## 配置项

见 `config.example.env`。也可用同名环境变量覆盖（前缀 `E10_`）。
