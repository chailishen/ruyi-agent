#!/usr/bin/env python3
"""从教师端整理.docx中提取图片，按一级菜单分目录存放。"""

import os
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

DOCX_PATH = Path(__file__).parent.parent / "教师端整理.docx"
OUTPUT_DIR = Path(__file__).parent.parent / "实训项目截图" / "教师端"


def sanitize_filename(name: str) -> str:
    """替换文件名中的非法字符。"""
    return re.sub(r'[\\/:*?"<>|]', '_', name).strip()


def get_images_from_paragraph(para_element, doc_part):
    """从段落 XML 中提取所有图片的二进制数据和扩展名。"""
    images = []
    blips = para_element.findall('.//' + qn('a:blip'))
    for blip in blips:
        embed_id = blip.get(qn('r:embed'))
        if not embed_id:
            continue
        rel = doc_part.rels[embed_id]
        image_part = rel.target_part
        ext = os.path.splitext(image_part.partname)[1]
        images.append((image_part.blob, ext))
    return images


def normalize_category(name: str) -> str:
    """将分类名称归一化，修正 Word 中的拼写错误。"""
    first_part = name.split('-')[0].strip()
    # 修正 "AI" 和 "AI；课件" 等变体 → "AI课件"
    if first_part in ('AI', 'AI；课件'):
        return 'AI课件'
    return first_part


def extract_images():
    doc = Document(str(DOCX_PATH))
    doc_part = doc.part

    current_name = None
    img_seq = 0  # 同名下的图片序号
    extracted = 0
    skipped = 0

    for para in doc.paragraphs:
        text = para.text.strip()

        if para.style.name.startswith('Heading'):
            continue

        # 有文字的段落 → 记录为下一张图片的名称，重置序号
        if text:
            current_name = text
            img_seq = 0
            continue

        # 无文字段落，检查是否含图片
        blips = para._element.findall('.//' + qn('a:blip'))
        if not blips:
            continue

        if current_name is None:
            skipped += 1
            continue

        category = normalize_category(current_name)
        filename = sanitize_filename(current_name)

        images = get_images_from_paragraph(para._element, doc_part)
        if not images:
            skipped += 1
            continue

        for data, ext in images:
            out_dir = OUTPUT_DIR / category
            out_dir.mkdir(parents=True, exist_ok=True)

            # 同一名称下多张图片时加序号后缀
            img_seq += 1
            if img_seq == 1:
                out_path = out_dir / f"{filename}{ext}"
            else:
                out_path = out_dir / f"{filename}-{img_seq}{ext}"

            with open(out_path, 'wb') as f:
                f.write(data)
            extracted += 1

    print(f"提取完成: {extracted} 张图片已导出")
    if skipped:
        print(f"跳过: {skipped} 张（无法关联名称或提取失败）")

    # 打印目录结构
    print(f"\n输出目录: {OUTPUT_DIR}")
    for d in sorted(OUTPUT_DIR.iterdir()):
        if d.is_dir():
            count = len(list(d.glob('*')))
            print(f"  {d.name}/  ({count} 张)")


if __name__ == '__main__':
    extract_images()
