# 泛微 Open API 本地文档库

本目录用于沉淀泛微开放平台 API 文档，便于人工查阅、持续跟进和 AI 编程。

## 推荐格式（三层结构）

| 层级 | 目录/文件 | 用途 | 适合谁 |
| --- | --- | --- | --- |
| 索引层 | `manifest.json`、`ALL_APIS.md`、`modules/*.md` | 快速检索、按业务模块浏览 | 人 + AI |
| 结构化层 | `parsed/**/*.json` | 程序读取、生成表单/插件/SDK | 代码 / AI 编程 |
| 原文层 | `raw/**/*.json` | 与线上完全一致的 ProseMirror 源数据 | 对账、重新解析 |
| 阅读层 | `markdown/**/*.md` | 人类阅读、直接喂给 AI 对话 | 人 + AI |

**结论：不要只存一种格式。**

- 给 AI 写代码：优先看 `parsed/*.json` + `manifest.json`
- 给 AI 理解业务：优先看 `markdown/*.md` 或 `ALL_APIS.md`
- 需要完整还原线上文档：看 `raw/*.json`

## 目录说明

```
docs/fanwei-openapi/
├── README.md              # 本说明
├── meta.json              # 同步元信息（来源、时间、统计）
├── manifest.json          # 全量索引（机器友好）
├── catalog.json           # 原始目录树
├── ALL_APIS.md            # 全量 API 索引（AI 友好）
├── modules/               # 按业务模块的索引页
├── raw/zh_cn/{id}.json    # 线上原始文档（ProseMirror JSON）
├── parsed/{module}/{name}.json  # 解析后的结构化 API 定义
└── markdown/{module}/{name}.md  # Markdown 可读文档
```

## 结构化 JSON 示例

`parsed/` 中每个文件包含：

```json
{
  "id": "949479748799578113",
  "name": "同步分部",
  "module": "部门",
  "module_path": ["部门"],
  "is_api": true,
  "url": "/api/hrm/restful/syncSubcompany",
  "url_template": "{OpenApiOrigin}/api/hrm/restful/syncSubcompany",
  "method": "POST",
  "content_type": "application/json",
  "parameters": [
    { "name": "...", "required": "是", "type": "string", "description": "..." }
  ],
  "response_example": "{ ... }"
}
```

## 如何更新

```bash
python3 scripts/sync_fanwei_openapi_docs.py
```

可选参数：

```bash
python3 scripts/sync_fanwei_openapi_docs.py \
  --base-url https://zhxz-test.xasp.com.cn \
  --version 10.0.2026.0201.01 \
  --locale zh_cn \
  --out docs/fanwei-openapi
```

## 来源

- 文档门户：`https://zhxz-test.xasp.com.cn/sp/opendoc/freepass/10.0.2026.0201.01/zh_cn/949862795428020225`
- 目录数据：`/build/opendoc/docs/{version}/categorys/zh_cn.json`
- 文档内容：`/build/opendoc/docs/{version}/files/f{docId}.zh_cn.json`
