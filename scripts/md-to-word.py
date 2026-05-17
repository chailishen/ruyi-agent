#!/usr/bin/env python3
"""将 Markdown 文件转换为 Word (.docx)，依赖 pandoc。"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def convert(md_path: Path) -> Path:
    output = md_path.with_suffix(".docx")
    cmd = [
        "pandoc",
        str(md_path),
        "-f", "markdown",
        "-t", "docx",
        "--resource-path", str(md_path.parent),
        "-o", str(output),
    ]
    subprocess.run(cmd, check=True)
    return output


def main():
    parser = argparse.ArgumentParser(description="将 Markdown 转换为 Word 文档")
    parser.add_argument("files", nargs="+", type=Path, help="要转换的 .md 文件路径")
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        print("错误：pandoc 未安装，请运行 brew install pandoc", file=sys.stderr)
        sys.exit(1)

    for md in args.files:
        if not md.exists():
            print(f"跳过：{md} 不存在", file=sys.stderr)
            continue
        out = convert(md.resolve())
        print(f"{md} → {out}")


if __name__ == "__main__":
    main()
