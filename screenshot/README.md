# URL 截图服务

这个项目提供“输入 URL，输出完整页面截图”的能力，默认目标示例是 https://xailab.com.cn/。它基于 Playwright 打开真实 Chromium 页面，适合需要执行 JavaScript、加载字体图片、处理懒加载和长页面的网站。

## 目录结构

```text
src/
  cli.js          # 命令行入口
  screenshot.js   # 核心截图逻辑
  security.js     # URL 安全校验和 SSRF 防护
  server.js       # HTTP API 服务
output/
  screenshots/    # 默认截图输出目录
```

## 常用命令

```bash
npm install
npm run install:browsers
npm run check
npm run capture
npm run capture:desktop
npm run capture:mobile
```

### 命令行截图

```bash
npm run screenshot -- https://xailab.com.cn/
npm run screenshot -- https://xailab.com.cn/ --output=output/xailab.png --width=1440 --height=900
```

默认输出目录是 `output/screenshots/`。常用参数：

- `--width=1440`：视口宽度。
- `--height=900`：视口高度。
- `--format=png|jpeg|webp`：图片格式。
- `--max-page-height=50000`：页面最大高度，避免无限滚动页面占满资源。
- `--tile-height=8000`：长页面分片高度。

### 批量截图

把统一配置和多个 URL 写到 JSON 文件里：

```json
{
  "outputDir": "output/batch",
  "width": 1440,
  "height": 900,
  "format": "png",
  "maxPageHeight": 50000,
  "tileHeight": 8000,
  "items": [
    { "name": "xailab-home", "url": "https://xailab.com.cn/" },
    { "name": "example", "url": "https://example.com/" }
  ]
}
```

执行：

```bash
npm run screenshot:batch -- --input=batch-screenshots.example.json
```

也可以不写配置文件，直接一次性传多个目标：

```bash
npm run screenshot:batch -- --output-dir=output/batch --width=1440 --height=900 --format=png --max-page-height=50000 --tile-height=8000 --target=xailab-home=https://xailab.com.cn/ --target=example=https://example.com/
```

批量脚本会把 `name` 作为输出文件名，按统一 `format` 生成到 `outputDir`，例如 `output/batch/xailab-home.png`。

### HTTP API

启动服务：

```bash
npm run screenshot:server
```

生成截图并返回 JSON：

```bash
curl -X POST http://localhost:3000/screenshot \
  -H 'content-type: application/json' \
  -d '{"url":"https://xailab.com.cn/","width":1440,"height":900}'
```

也可以直接返回图片：

```bash
curl 'http://localhost:3000/screenshot?url=https%3A%2F%2Fxailab.com.cn%2F' --output xailab.png
```

服务默认保存图片到 `output/screenshots/`，并通过 `/screenshots/<filename>` 暴露本地图片地址。

### 安全与资源限制

默认只允许 `http` 和 `https`，并阻止 `localhost`、内网 IP、链路本地地址和云元数据地址，降低 SSRF 风险。开发环境如果确实要截本机页面，可以临时设置：

```bash
ALLOW_PRIVATE_URLS=1 npm run screenshot:server
```

生产环境常用环境变量：

- `PORT=3000`：服务端口。
- `HOST=0.0.0.0`：监听地址。
- `SCREENSHOT_OUTPUT_DIR=output/screenshots`：截图保存目录。
- `PUBLIC_BASE_URL=https://example.com`：返回给客户端的公开访问基准地址。
- `SCREENSHOT_MAX_CONCURRENCY=2`：最大并发截图数。
- `SCREENSHOT_MAX_QUEUE_SIZE=20`：等待队列长度。

### Docker 部署

```bash
docker build -t url-screenshot-service .
docker run --rm -p 3000:3000 url-screenshot-service
```
