#!/usr/bin/env python3
"""经 SSH + docker exec 导出 agentos_bff 全库表结构说明。

输出：
  schema/overview.md     人类可读总览
  schema/tables.json     结构化全量
  schema/tables/*.md     分表说明（每表一页）
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
TABLES_MD_DIR = SCHEMA_DIR / "tables"
SQL_FILE = Path(__file__).resolve().parent / "dump_schema.sql"
SSH_PSQL = Path(__file__).resolve().parent / "ssh_psql.sh"


def run_dump() -> str:
    if not SSH_PSQL.exists():
        raise SystemExit(f"缺少 {SSH_PSQL}")
    sql = SQL_FILE.read_text(encoding="utf-8")
    proc = subprocess.run(
        [str(SSH_PSQL)],
        input=sql,
        text=True,
        capture_output=True,
        timeout=180,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "dump failed\n")
        raise SystemExit(proc.returncode or 1)
    return proc.stdout


def split_sections(raw: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "_preamble"
    sections[current] = []
    for line in raw.splitlines():
        if line.startswith("=== ") and line.endswith(" ==="):
            current = line.strip("= ").strip()
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def parse_psql_table(block: str) -> list[dict[str, str]]:
    """解析默认对齐的 psql 文本表（含表头与 --- 分隔）。"""
    lines = [ln for ln in block.splitlines() if ln.strip()]
    # 跳过 BEGIN/SET/COMMIT 等
    start = None
    for i, ln in enumerate(lines):
        if set(ln.replace(" ", "")) <= {"-", "+"} and "-" in ln:
            start = i
            break
    if start is None or start == 0:
        return []
    header = lines[start - 1]
    # 用分隔行估算列边界
    sep = lines[start]
    # 简单按 | 分割
    if "|" not in header:
        return []
    cols = [c.strip() for c in header.split("|")]
    rows: list[dict[str, str]] = []
    for ln in lines[start + 1 :]:
        if ln.startswith("(") and "row" in ln:
            break
        if "|" not in ln:
            continue
        vals = [c.strip() for c in ln.split("|")]
        if len(vals) != len(cols):
            # 右端可能缺列
            while len(vals) < len(cols):
                vals.append("")
            vals = vals[: len(cols)]
        rows.append(dict(zip(cols, vals)))
    return rows


def build_payload(sections: dict[str, str]) -> dict:
    objects = parse_psql_table(sections.get("OBJECTS", ""))
    columns = parse_psql_table(sections.get("COLUMNS", ""))
    pks = parse_psql_table(sections.get("PRIMARY_KEYS", ""))
    fks = parse_psql_table(sections.get("FOREIGN_KEYS", ""))
    uniques = parse_psql_table(sections.get("UNIQUE_CONSTRAINTS", ""))
    indexes = parse_psql_table(sections.get("INDEXES", ""))
    meta_rows = parse_psql_table(sections.get("META", ""))
    counts = parse_psql_table(sections.get("SCHEMA_COUNTS", ""))

    by_table: dict[str, dict] = {}
    for obj in objects:
        key = f"{obj.get('schema')}.{obj.get('name')}"
        by_table[key] = {
            "schema": obj.get("schema"),
            "name": obj.get("name"),
            "kind": obj.get("kind"),
            "comment": obj.get("comment") or None,
            "columns": [],
            "primary_key": None,
            "foreign_keys": [],
            "unique_constraints": [],
            "indexes": [],
        }

    for col in columns:
        key = f"{col.get('schema')}.{col.get('table_name')}"
        if key not in by_table:
            continue
        by_table[key]["columns"].append(
            {
                "ordinal": int(col["ordinal"]) if col.get("ordinal", "").isdigit() else col.get("ordinal"),
                "name": col.get("column_name"),
                "type": col.get("data_type"),
                "nullable": (col.get("nullable") or "").lower() in ("t", "true", "yes"),
                "default": col.get("column_default") or None,
                "comment": col.get("comment") or None,
            }
        )

    for pk in pks:
        key = f"{pk.get('schema')}.{pk.get('table_name')}"
        if key in by_table:
            by_table[key]["primary_key"] = {
                "name": pk.get("constraint_name"),
                "columns": [c.strip() for c in (pk.get("columns") or "").split(",") if c.strip()],
            }

    for fk in fks:
        key = f"{fk.get('schema')}.{fk.get('table_name')}"
        if key in by_table:
            by_table[key]["foreign_keys"].append(
                {
                    "name": fk.get("constraint_name"),
                    "columns": [c.strip() for c in (fk.get("columns") or "").split(",") if c.strip()],
                    "ref_table": f"{fk.get('ref_schema')}.{fk.get('ref_table')}",
                    "ref_columns": [c.strip() for c in (fk.get("ref_columns") or "").split(",") if c.strip()],
                    "on_update": fk.get("on_update"),
                    "on_delete": fk.get("on_delete"),
                }
            )

    for uq in uniques:
        key = f"{uq.get('schema')}.{uq.get('table_name')}"
        if key in by_table:
            by_table[key]["unique_constraints"].append(
                {
                    "name": uq.get("constraint_name"),
                    "columns": [c.strip() for c in (uq.get("columns") or "").split(",") if c.strip()],
                }
            )

    for ix in indexes:
        key = f"{ix.get('schema')}.{ix.get('table_name')}"
        if key in by_table:
            by_table[key]["indexes"].append(
                {
                    "name": ix.get("index_name"),
                    "unique": (ix.get("is_unique") or "").lower() in ("t", "true"),
                    "primary": (ix.get("is_primary") or "").lower() in ("t", "true"),
                    "definition": ix.get("index_def"),
                }
            )

    return {
        "dumped_at": datetime.now(timezone.utc).isoformat(),
        "meta": meta_rows[0] if meta_rows else {},
        "schema_counts": counts,
        "tables": sorted(by_table.values(), key=lambda t: (t["schema"] or "", t["name"] or "")),
        "raw_sections_present": sorted(sections.keys()),
    }


def write_markdown(payload: dict) -> None:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_MD_DIR.mkdir(parents=True, exist_ok=True)

    tables = payload["tables"]
    lines = [
        "# agentos_bff 表结构说明",
        "",
        f"- 导出时间（UTC）：`{payload['dumped_at']}`",
        f"- 数据库：`{payload.get('meta', {}).get('db', 'agentos_bff')}`",
        f"- 对象数：{len(tables)}",
        "",
        "## Schema 统计",
        "",
        "| Schema | Tables | Partitioned | Views | Matviews |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in payload.get("schema_counts") or []:
        lines.append(
            f"| `{row.get('schema')}` | {row.get('tables')} | {row.get('partitioned')} | {row.get('views')} | {row.get('matviews')} |"
        )

    lines += ["", "## 对象目录", "", "| Schema | Name | Kind | Columns | Comment |", "| --- | --- | --- | ---: | --- |"]
    for t in tables:
        comment = (t.get("comment") or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{t['schema']}` | [`{t['name']}`](tables/{t['schema']}.{t['name']}.md) | {t['kind']} | {len(t['columns'])} | {comment} |"
        )
    lines.append("")
    (SCHEMA_DIR / "overview.md").write_text("\n".join(lines), encoding="utf-8")

    for t in tables:
        path = TABLES_MD_DIR / f"{t['schema']}.{t['name']}.md"
        body = [
            f"# {t['schema']}.{t['name']}",
            "",
            f"- 类型：`{t['kind']}`",
            f"- 注释：{t.get('comment') or '（无）'}",
            "",
            "## 字段",
            "",
            "| # | 字段 | 类型 | 可空 | 默认 | 注释 |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
        for c in t["columns"]:
            body.append(
                f"| {c['ordinal']} | `{c['name']}` | `{c['type']}` | {'是' if c['nullable'] else '否'} | {c.get('default') or ''} | {c.get('comment') or ''} |"
            )
        if t.get("primary_key"):
            pk = t["primary_key"]
            body += ["", "## 主键", "", f"- `{pk['name']}`: {', '.join(f'`{c}`' for c in pk['columns'])}"]
        if t.get("foreign_keys"):
            body += ["", "## 外键", ""]
            for fk in t["foreign_keys"]:
                body.append(
                    f"- `{fk['name']}`: ({', '.join(fk['columns'])}) → `{fk['ref_table']}` ({', '.join(fk['ref_columns'])}) ON UPDATE {fk.get('on_update')} ON DELETE {fk.get('on_delete')}"
                )
        if t.get("unique_constraints"):
            body += ["", "## 唯一约束", ""]
            for uq in t["unique_constraints"]:
                body.append(f"- `{uq['name']}`: {', '.join(f'`{c}`' for c in uq['columns'])}")
        if t.get("indexes"):
            body += ["", "## 索引", ""]
            for ix in t["indexes"]:
                body.append(f"- `{ix['name']}`: `{ix.get('definition')}`")
        body.append("")
        path.write_text("\n".join(body), encoding="utf-8")


def main() -> int:
    print("正在经 SSH 导出 schema（TSV）…", flush=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        payload = dump_tsv_mode()
    except Exception as exc:
        print(f"TSV 导出失败：{exc}", file=sys.stderr)
        print("回退尝试对齐文本 dump …", file=sys.stderr)
        raw = run_dump()
        (SCHEMA_DIR / "dump_raw.txt").write_text(raw, encoding="utf-8")
        payload = build_payload(split_sections(raw))
        if not payload["tables"]:
            raise SystemExit("未能解析到任何表，请检查 SSH / docker 连通性") from exc

    (SCHEMA_DIR / "tables.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_markdown(payload)
    print(f"完成：{len(payload['tables'])} 个对象")
    print(f"  - {SCHEMA_DIR / 'overview.md'}")
    print(f"  - {SCHEMA_DIR / 'tables.json'}")
    print(f"  - {TABLES_MD_DIR}/")
    return 0


def dump_tsv_mode() -> dict:
    """更稳的解析：对每段查询用 -A -F \\t。"""
    queries = {
        "meta": "SELECT current_database() AS db, current_user AS db_user, version() AS version, now() AS dumped_at;",
        "schema_counts": """
SELECT n.nspname AS schema,
       COUNT(*) FILTER (WHERE c.relkind = 'r') AS tables,
       COUNT(*) FILTER (WHERE c.relkind = 'p') AS partitioned,
       COUNT(*) FILTER (WHERE c.relkind = 'v') AS views,
       COUNT(*) FILTER (WHERE c.relkind = 'm') AS matviews
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
  AND n.nspname NOT LIKE 'pg_toast%'
  AND c.relkind IN ('r','v','m','p')
GROUP BY n.nspname ORDER BY n.nspname;
""",
        "objects": """
SELECT n.nspname AS schema, c.relname AS name,
       CASE c.relkind WHEN 'r' THEN 'table' WHEN 'p' THEN 'partitioned' WHEN 'v' THEN 'view' WHEN 'm' THEN 'matview' END AS kind,
       obj_description(c.oid, 'pg_class') AS comment
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%'
  AND c.relkind IN ('r','v','m','p')
ORDER BY n.nspname, c.relname;
""",
        "columns": """
SELECT n.nspname AS schema, c.relname AS table_name, a.attnum AS ordinal, a.attname AS column_name,
       pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
       NOT a.attnotnull AS nullable,
       pg_get_expr(ad.adbin, ad.adrelid) AS column_default,
       col_description(c.oid, a.attnum) AS comment
FROM pg_attribute a
JOIN pg_class c ON c.oid = a.attrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_attrdef ad ON ad.adrelid = c.oid AND ad.adnum = a.attnum
WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%'
  AND c.relkind IN ('r','p','v','m') AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY n.nspname, c.relname, a.attnum;
""",
        "primary_keys": """
SELECT n.nspname AS schema, c.relname AS table_name, con.conname AS constraint_name,
       string_agg(a.attname, ', ' ORDER BY u.ord) AS columns
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
WHERE con.contype = 'p' AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname ORDER BY n.nspname, c.relname;
""",
        "foreign_keys": """
SELECT n.nspname AS schema, c.relname AS table_name, con.conname AS constraint_name,
       string_agg(a.attname, ', ' ORDER BY u.ord) AS columns,
       fn.nspname AS ref_schema, fc.relname AS ref_table,
       string_agg(fa.attname, ', ' ORDER BY u.ord) AS ref_columns,
       CASE con.confupdtype WHEN 'a' THEN 'NO ACTION' WHEN 'r' THEN 'RESTRICT' WHEN 'c' THEN 'CASCADE' WHEN 'n' THEN 'SET NULL' WHEN 'd' THEN 'SET DEFAULT' END AS on_update,
       CASE con.confdeltype WHEN 'a' THEN 'NO ACTION' WHEN 'r' THEN 'RESTRICT' WHEN 'c' THEN 'CASCADE' WHEN 'n' THEN 'SET NULL' WHEN 'd' THEN 'SET DEFAULT' END AS on_delete
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_class fc ON fc.oid = con.confrelid
JOIN pg_namespace fn ON fn.oid = fc.relnamespace
JOIN LATERAL unnest(con.conkey, con.confkey) WITH ORDINALITY AS u(attnum, fattnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
JOIN pg_attribute fa ON fa.attrelid = fc.oid AND fa.attnum = u.fattnum
WHERE con.contype = 'f' AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname, fn.nspname, fc.relname, con.confupdtype, con.confdeltype
ORDER BY n.nspname, c.relname, con.conname;
""",
        "unique_constraints": """
SELECT n.nspname AS schema, c.relname AS table_name, con.conname AS constraint_name,
       string_agg(a.attname, ', ' ORDER BY u.ord) AS columns
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
WHERE con.contype = 'u' AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname ORDER BY n.nspname, c.relname;
""",
        "indexes": """
SELECT n.nspname AS schema, t.relname AS table_name, i.relname AS index_name,
       ix.indisunique AS is_unique, ix.indisprimary AS is_primary,
       pg_get_indexdef(ix.indexrelid) AS index_def
FROM pg_index ix
JOIN pg_class i ON i.oid = ix.indexrelid
JOIN pg_class t ON t.oid = ix.indrelid
JOIN pg_namespace n ON n.oid = t.relnamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%'
ORDER BY n.nspname, t.relname, i.relname;
""",
    }

    def tsv_query(sql: str) -> list[dict[str, str]]:
        full = "BEGIN READ ONLY;\n" + sql + "\nCOMMIT;\n"
        proc = subprocess.run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-o",
                "ConnectTimeout=20",
                "agentos-prod",
                "sudo -n docker exec -i agentos-postgres psql -U agentos -d agentos_bff -v ON_ERROR_STOP=1 -P pager=off -A -F '\\t'",
            ],
            input=full,
            text=True,
            capture_output=True,
            timeout=180,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr or proc.stdout)
        lines = [ln for ln in proc.stdout.splitlines() if ln and not ln.startswith(("BEGIN", "SET", "COMMIT", "CREATE", "WARNING"))]
        # 找表头：第一行含 tab 且下一行不是数字行数
        # psql -A 输出：header \\t ... \\n rows... \\n (N rows)
        header = None
        rows: list[dict[str, str]] = []
        for ln in lines:
            if ln.startswith("(") and ln.endswith("rows)") or ln.endswith("row)"):
                continue
            if "\t" not in ln and header is None:
                continue
            if header is None:
                header = ln.split("\t")
                continue
            vals = ln.split("\t")
            while len(vals) < len(header):
                vals.append("")
            rows.append({h: vals[i] if i < len(vals) else "" for i, h in enumerate(header)})
        return rows

    objects = tsv_query(queries["objects"])
    columns = tsv_query(queries["columns"])
    pks = tsv_query(queries["primary_keys"])
    fks = tsv_query(queries["foreign_keys"])
    uniques = tsv_query(queries["unique_constraints"])
    indexes = tsv_query(queries["indexes"])
    meta = tsv_query(queries["meta"])
    counts = tsv_query(queries["schema_counts"])

    by_table: dict[str, dict] = {}
    for obj in objects:
        key = f"{obj['schema']}.{obj['name']}"
        by_table[key] = {
            "schema": obj["schema"],
            "name": obj["name"],
            "kind": obj["kind"],
            "comment": obj.get("comment") or None,
            "columns": [],
            "primary_key": None,
            "foreign_keys": [],
            "unique_constraints": [],
            "indexes": [],
        }
    for col in columns:
        key = f"{col['schema']}.{col['table_name']}"
        if key not in by_table:
            continue
        by_table[key]["columns"].append(
            {
                "ordinal": int(col["ordinal"]) if str(col.get("ordinal", "")).isdigit() else col.get("ordinal"),
                "name": col["column_name"],
                "type": col["data_type"],
                "nullable": str(col.get("nullable")).lower() in ("t", "true"),
                "default": col.get("column_default") or None,
                "comment": col.get("comment") or None,
            }
        )
    for pk in pks:
        key = f"{pk['schema']}.{pk['table_name']}"
        if key in by_table:
            by_table[key]["primary_key"] = {
                "name": pk["constraint_name"],
                "columns": [c.strip() for c in pk.get("columns", "").split(",") if c.strip()],
            }
    for fk in fks:
        key = f"{fk['schema']}.{fk['table_name']}"
        if key in by_table:
            by_table[key]["foreign_keys"].append(
                {
                    "name": fk["constraint_name"],
                    "columns": [c.strip() for c in fk.get("columns", "").split(",") if c.strip()],
                    "ref_table": f"{fk['ref_schema']}.{fk['ref_table']}",
                    "ref_columns": [c.strip() for c in fk.get("ref_columns", "").split(",") if c.strip()],
                    "on_update": fk.get("on_update"),
                    "on_delete": fk.get("on_delete"),
                }
            )
    for uq in uniques:
        key = f"{uq['schema']}.{uq['table_name']}"
        if key in by_table:
            by_table[key]["unique_constraints"].append(
                {
                    "name": uq["constraint_name"],
                    "columns": [c.strip() for c in uq.get("columns", "").split(",") if c.strip()],
                }
            )
    for ix in indexes:
        key = f"{ix['schema']}.{ix['table_name']}"
        if key in by_table:
            by_table[key]["indexes"].append(
                {
                    "name": ix["index_name"],
                    "unique": str(ix.get("is_unique")).lower() in ("t", "true"),
                    "primary": str(ix.get("is_primary")).lower() in ("t", "true"),
                    "definition": ix.get("index_def"),
                }
            )

    return {
        "dumped_at": datetime.now(timezone.utc).isoformat(),
        "meta": meta[0] if meta else {},
        "schema_counts": counts,
        "tables": sorted(by_table.values(), key=lambda t: (t["schema"], t["name"])),
        "mode": "tsv",
    }


if __name__ == "__main__":
    raise SystemExit(main())
