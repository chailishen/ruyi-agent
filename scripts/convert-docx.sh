#!/bin/bash
# 一次性脚本：将建设方案.docx转换为Markdown
# 依赖：pandoc (brew install pandoc)

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT="$PROJECT_ROOT/实训项目截图/建设方案.docx"
OUTPUT="$PROJECT_ROOT/实训项目截图/建设方案.md"
MEDIA_DIR="$PROJECT_ROOT/实训项目截图/建设方案_media"

if ! command -v pandoc &> /dev/null; then
    echo "错误：pandoc 未安装"
    echo "请运行：brew install pandoc"
    exit 1
fi

if [ ! -f "$INPUT" ]; then
    echo "错误：找不到 $INPUT"
    exit 1
fi

echo "正在转换 建设方案.docx → 建设方案.md ..."
echo "文件大小：$(du -h "$INPUT" | cut -f1)"

mkdir -p "$MEDIA_DIR"

pandoc "$INPUT" \
    -f docx \
    -t markdown \
    --extract-media="$MEDIA_DIR" \
    --wrap=none \
    -o "$OUTPUT"

echo "转换完成！"
echo "输出文件：$OUTPUT"
echo "媒体文件：$MEDIA_DIR/"
echo "文件大小：$(du -h "$OUTPUT" | cut -f1)"
