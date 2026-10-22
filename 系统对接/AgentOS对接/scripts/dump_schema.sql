-- 导出 agentos_bff 全库表结构（只读）
\pset pager off
\pset tuples_only off
BEGIN READ ONLY;
SET LOCAL TIME ZONE 'Asia/Shanghai';

\echo '=== META ==='
SELECT current_database() AS db, current_user AS db_user, version() AS version, now() AS dumped_at;

\echo '=== SCHEMA_COUNTS ==='
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
GROUP BY n.nspname
ORDER BY n.nspname;

\echo '=== OBJECTS ==='
SELECT n.nspname AS schema,
       c.relname AS name,
       CASE c.relkind
         WHEN 'r' THEN 'table'
         WHEN 'p' THEN 'partitioned'
         WHEN 'v' THEN 'view'
         WHEN 'm' THEN 'matview'
       END AS kind,
       obj_description(c.oid, 'pg_class') AS comment
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
  AND n.nspname NOT LIKE 'pg_toast%'
  AND c.relkind IN ('r','v','m','p')
ORDER BY n.nspname, c.relname;

\echo '=== COLUMNS ==='
SELECT
  n.nspname AS schema,
  c.relname AS table_name,
  a.attnum AS ordinal,
  a.attname AS column_name,
  pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
  NOT a.attnotnull AS nullable,
  pg_get_expr(ad.adbin, ad.adrelid) AS column_default,
  col_description(c.oid, a.attnum) AS comment
FROM pg_attribute a
JOIN pg_class c ON c.oid = a.attrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_attrdef ad ON ad.adrelid = c.oid AND ad.adnum = a.attnum
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
  AND n.nspname NOT LIKE 'pg_toast%'
  AND c.relkind IN ('r','p','v','m')
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY n.nspname, c.relname, a.attnum;

\echo '=== PRIMARY_KEYS ==='
SELECT
  n.nspname AS schema,
  c.relname AS table_name,
  con.conname AS constraint_name,
  string_agg(a.attname, ', ' ORDER BY u.ord) AS columns
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
WHERE con.contype = 'p'
  AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname
ORDER BY n.nspname, c.relname;

\echo '=== FOREIGN_KEYS ==='
SELECT
  n.nspname AS schema,
  c.relname AS table_name,
  con.conname AS constraint_name,
  string_agg(a.attname, ', ' ORDER BY u.ord) AS columns,
  fn.nspname AS ref_schema,
  fc.relname AS ref_table,
  string_agg(fa.attname, ', ' ORDER BY u.ord) AS ref_columns,
  CASE con.confupdtype
    WHEN 'a' THEN 'NO ACTION' WHEN 'r' THEN 'RESTRICT'
    WHEN 'c' THEN 'CASCADE' WHEN 'n' THEN 'SET NULL' WHEN 'd' THEN 'SET DEFAULT'
  END AS on_update,
  CASE con.confdeltype
    WHEN 'a' THEN 'NO ACTION' WHEN 'r' THEN 'RESTRICT'
    WHEN 'c' THEN 'CASCADE' WHEN 'n' THEN 'SET NULL' WHEN 'd' THEN 'SET DEFAULT'
  END AS on_delete
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_class fc ON fc.oid = con.confrelid
JOIN pg_namespace fn ON fn.oid = fc.relnamespace
JOIN LATERAL unnest(con.conkey, con.confkey) WITH ORDINALITY AS u(attnum, fattnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
JOIN pg_attribute fa ON fa.attrelid = fc.oid AND fa.attnum = u.fattnum
WHERE con.contype = 'f'
  AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname, fn.nspname, fc.relname, con.confupdtype, con.confdeltype
ORDER BY n.nspname, c.relname, con.conname;

\echo '=== UNIQUE_CONSTRAINTS ==='
SELECT
  n.nspname AS schema,
  c.relname AS table_name,
  con.conname AS constraint_name,
  string_agg(a.attname, ', ' ORDER BY u.ord) AS columns
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, ord) ON true
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = u.attnum
WHERE con.contype = 'u'
  AND n.nspname NOT IN ('pg_catalog','information_schema')
GROUP BY n.nspname, c.relname, con.conname
ORDER BY n.nspname, c.relname;

\echo '=== INDEXES ==='
SELECT
  n.nspname AS schema,
  t.relname AS table_name,
  i.relname AS index_name,
  ix.indisunique AS is_unique,
  ix.indisprimary AS is_primary,
  pg_get_indexdef(ix.indexrelid) AS index_def
FROM pg_index ix
JOIN pg_class i ON i.oid = ix.indexrelid
JOIN pg_class t ON t.oid = ix.indrelid
JOIN pg_namespace n ON n.oid = t.relnamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
  AND n.nspname NOT LIKE 'pg_toast%'
ORDER BY n.nspname, t.relname, i.relname;

COMMIT;
