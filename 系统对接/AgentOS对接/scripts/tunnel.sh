#!/usr/bin/env bash
# 建立到 00 一体机 AgentOS PostgreSQL 的本地隧道。
# 用法：在「系统对接/AgentOS对接」目录执行 ./scripts/tunnel.sh
# 成功后保持本窗口打开；客户端连 127.0.0.1:15432

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/.env"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  set -a
  # 仅加载 KEY=VALUE，忽略注释与空行
  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -z "${line}" || "${line}" =~ ^[[:space:]]*# ]] && continue
    export "${line?}"
  done < "${ENV_FILE}"
  set +a
fi

SSH_KEY="${SSH_KEY:-~/.ssh/agentos-prod}"
SSH_KEY="${SSH_KEY/#\~/$HOME}"
SSH_PROXY_HOST="${SSH_PROXY_HOST:-agentos-prod}"
SSH_JUMP_LOCAL="${SSH_JUMP_LOCAL:-127.0.0.1}"
SSH_JUMP_PORT="${SSH_JUMP_PORT:-6022}"
SSH_REMOTE_USER="${SSH_REMOTE_USER:-ubuntu}"
SSH_REMOTE_HOST="${SSH_REMOTE_HOST:-127.0.0.1}"
SSH_HOST_KEY_ALIAS="${SSH_HOST_KEY_ALIAS:-ws00-frp-audit}"
PG_CONTAINER_IP="${PG_CONTAINER_IP:-172.23.0.6}"
PG_CONTAINER_PORT="${PG_CONTAINER_PORT:-5432}"
LOCAL_BIND="${LOCAL_BIND:-127.0.0.1:15432}"

if [[ ! -f "${SSH_KEY}" ]]; then
  cat >&2 <<EOF
缺少私钥：${SSH_KEY}

本机尚未配置 AgentOS 生产 SSH 密钥，无法建隧道。
请向运维索取 agentos-prod 私钥后：
  1. 保存为 ${SSH_KEY} 并 chmod 600
  2. 将 ssh/config.snippet 合并进 ~/.ssh/config（补全 Host agentos-prod）
  3. 再重新执行本脚本
EOF
  exit 1
fi

if ! grep -qE '^[[:space:]]*Host[[:space:]]+agentos-prod([[:space:]]|$)' "${HOME}/.ssh/config" 2>/dev/null; then
  echo "警告：~/.ssh/config 中未找到 Host agentos-prod，ProxyCommand 可能失败。" >&2
  echo "请参考 ${ROOT}/ssh/config.snippet 补全配置。" >&2
fi

echo "隧道：${LOCAL_BIND} -> ${PG_CONTAINER_IP}:${PG_CONTAINER_PORT}"
echo "经 ProxyCommand: ssh ${SSH_PROXY_HOST} -W ${SSH_JUMP_LOCAL}:${SSH_JUMP_PORT}"
echo "按 Ctrl+C 结束隧道。"
echo

exec ssh -N \
  -o HostKeyAlias="${SSH_HOST_KEY_ALIAS}" \
  -i "${SSH_KEY}" \
  -o "ProxyCommand=ssh ${SSH_PROXY_HOST} -W ${SSH_JUMP_LOCAL}:${SSH_JUMP_PORT}" \
  -L "${LOCAL_BIND}:${PG_CONTAINER_IP}:${PG_CONTAINER_PORT}" \
  "${SSH_REMOTE_USER}@${SSH_REMOTE_HOST}"
