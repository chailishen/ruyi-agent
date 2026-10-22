\pset pager off
BEGIN READ ONLY;
SET LOCAL TIME ZONE 'Asia/Shanghai';

-- 最近 7 天新增人员（含后来被删除的账号）
SELECT
    a.created_at::timestamptz AS "操作时间",
    COALESCE(u.display_name, a.actor_id) AS "操作人",
    a.target_id AS "人员ID",
    a.target_snapshot::jsonb->>'display_name' AS "人员姓名",
    a.result AS "结果"
FROM audit_events a
LEFT JOIN users u ON u.id = a.actor_id
WHERE a.action = 'member.create'
  AND a.created_at::timestamptz >= now() - interval '7 days'
ORDER BY a.created_at::timestamptz;

COMMIT;
