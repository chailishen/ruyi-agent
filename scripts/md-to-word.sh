#!/bin/bash
# 将操作手册MD文件转换为Word格式
# 用法：
#   ./scripts/md-to-word.sh                    # 转换所有MD文件
#   ./scripts/md-to-word.sh 学生端_我的课程.md  # 转换指定文件

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$PROJECT_ROOT/操作手册"
OUTPUT_DIR="$PROJECT_ROOT/操作手册/word"

if ! command -v pandoc &> /dev/null; then
    echo "错误：pandoc 未安装"
    echo "请运行：brew install pandoc"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

convert_file() {
    local md_file="$1"
    local basename=$(basename "$md_file" .md)
    local output_file="$OUTPUT_DIR/${basename}.docx"

    echo "转换：$basename.md → $basename.docx"

    pandoc "$md_file" \
        -f markdown \
        -t docx \
        --resource-path="$PROJECT_ROOT" \
        -o "$output_file"

    echo "  → $output_file"
}

if [ -n "$1" ]; then
    TARGET="$INPUT_DIR/$1"
    if [ ! -f "$TARGET" ]; then
        echo "错误：找不到 $TARGET"
        exit 1
    fi
    convert_file "$TARGET"
else
    count=0
    for md_file in "$INPUT_DIR"/*.md; do
        [ -f "$md_file" ] || continue
        convert_file "$md_file"
        count=$((count + 1))
    done

    if [ $count -eq 0 ]; then
        echo "没有找到MD文件。请先生成操作手册。"
        exit 1
    fi

    echo ""
    echo "完成！共转换 $count 个文件到 $OUTPUT_DIR/"
fi
