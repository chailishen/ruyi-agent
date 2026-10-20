#!/usr/bin/env python3
"""探查 AgentOS PostgreSQL（需先运行 scripts/tunnel.sh）。

读取同目录上级的 .env，连接后写出 schema/overview.md 与 schema/tables.json。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
SCHEMA_DIR = ROOT / "schema"


def load_env(path: Path) -> None:
    if not path.exists():
        print(f"缺少 {path}，请先：cp .env.example .env", file=sys.stderr)
        sys.exit(1)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def connect():
    try:
        import psycopg
    except ImportError:
        print("请先安装依赖：python3 -m pip install -r scripts/requirements.txt", file=sys.stderr)
        sys.exit(1)

    conninfo = (
        f"host={os.environ['PGHOST']} "
        f"port={os.environ['PGPORT']} "
        f"dbname={os.environ['PGDATABASE']} "
        f"user={os.environ['PGUSER']} "
        f"password={os.environ['PGPASSWORD']} "
        f"sslmode={os.environ.get('PGSSLMODE', 'disable')} "
        f"connect_timeout=10"
    )
    try:
        return psycopg.connect(conninfo)
    except Exception as exc:
        print(f"连接失败：{exc}", file=sys.stderr)
        print(
            "请确认：1) scripts/tunnel.sh 已打开；2) .env 密码正确；"
            "3) 容器 IP 未变更（见 README）。",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> int:
    load_env(ENV_PATH)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version(), current_database(), current_user, now()")
            version, db, user, now = cur.fetchone()

            cur.execute(
                """
                SELECT nspname
                FROM pg_namespace
                WHERE nspname NOT IN ('pg_catalog', 'information_schema')
                  AND nspname NOT LIKE 'pg_toast%'
                  AND nspname NOT LIKE 'pg_temp%'
                ORDER BY nspname
                """
            )
            schemas = [r[0] for r in cur.fetchall()]

            cur.execute(
                """
                SELECT
                  n.nspname AS schema,
                  c.relname AS table,
                  c.relkind,
                  COALESCE(s.n_live_tup, 0) AS approx_rows,
                  obj_description(c.oid, 'pg_class') AS comment
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_stat_user_tables s
                  ON s.schemaname = n.nspname AND s.relname = c.relname
                WHERE n.nspname = ANY(%s)
                  AND c.relkind IN ('r', 'p', 'v', 'm')
                ORDER BY n.nspname, c.relname
                """,
                (schemas,),
            )
            kind_map = {"r": "table", "p": "partitioned", "v": "view", "m": "matview"}
            tables = [
                {
                    "schema": row[0],
                    "name": row[1],
                    "kind": kind_map.get(row[2], row[2]),
                    "approx_rows": int(row[3]),
                    "comment": row[4],
                }
                for row in cur.fetchall()
            ]

            # 每张普通表采一列样本字段名（前 20 列）
            for t in tables:
                if t["kind"] not in ("table", "partitioned"):
                    t["columns"] = []
                    continue
                cur.execute(
                    """
                    SELECT a.attname, pg_catalog.format_type(a.atttypid, a.atttypmod),
                           NOT a.attnotnull AS nullable
                    FROM pg_attribute a
                    JOIN pg_class c ON c.oid = a.attrelid
                    JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE n.nspname = %s AND c.relname = %s
                      AND a.attnum > 0 AND NOT a.attisdropped
                    ORDER BY a.attnum
                    LIMIT 40
                    """,
                    (t["schema"], t["name"]),
                )
                t["columns"] = [
                    {"name": r[0], "type": r[1], "nullable": bool(r[2])} for r in cur.fetchall()
                ]

    payload = {
        "inspected_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "database": db,
        "user": user,
        "server_time": str(now),
        "schemas": schemas,
        "tables": tables,
    }

    tables_json = SCHEMA_DIR / "tables.json"
    tables_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# AgentOS 库表概览",
        "",
        f"- 探查时间（UTC）：`{payload['inspected_at']}`",
        f"- 数据库：`{db}`",
        f"- 用户：`{user}`",
        f"- 版本：`{version}`",
        "",
        "## Schemas",
        "",
    ]
    for s in schemas:
        lines.append(f"- `{s}`")
    lines += ["", "## 对象清单", "", "| Schema | Name | Kind | Approx rows | Comment |", "| --- | --- | --- | ---: | --- |"]
    for t in tables:
        comment = (t.get("comment") or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{t['schema']}` | `{t['name']}` | {t['kind']} | {t['approx_rows']} | {comment} |"
        )
    lines.append("")
    overview = SCHEMA_DIR / "overview.md"
    overview.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK  库={db}  schemas={len(schemas)}  objects={len(tables)}")
    print(f"写入 {tables_json.relative_to(ROOT)}")
    print(f"写入 {overview.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
