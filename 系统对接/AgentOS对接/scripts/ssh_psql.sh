#!/usr/bin/env bash
# 经 SSH 在一体机上 docker exec 进 agentos-postgres，执行 SQL（stdin）或交互。
# 用法：
#   ./scripts/ssh_psql.sh                 # 交互 psql
#   ./scripts/ssh_psql.sh < query.sql     # 执行文件
#   echo 'SELECT 1' | ./scripts/ssh_psql.sh

set -euo pipefail

SSH_HOST="${SSH_HOST:-agentos-prod}"
CONTAINER="${PG_CONTAINER:-agentos-postgres}"
PGUSER="${PGUSER:-agentos}"
PGDATABASE="${PGDATABASE:-agentos_bff}"

exec ssh -o BatchMode=yes -o ConnectTimeout=15 "${SSH_HOST}" \
  "sudo -n docker exec -i ${CONTAINER} psql -U ${PGUSER} -d ${PGDATABASE} -v ON_ERROR_STOP=1 -P pager=off" \
  "$@"
