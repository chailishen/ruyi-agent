# AgentOS 对接 — 00 一体机主库

00 一体机 AgentOS 主库为 **PostgreSQL 17**（容器 `agentos-postgres`，内网 IP 当前为 `172.23.0.6`，**不对外暴露 5432**）。

推荐访问方式：**SSH 登录一体机 → `sudo docker exec` 进库**（已验证可用）。不必再开本地 15432 隧道。

## 当前状态（2026-10-21 已通）

| 项 | 值 |
| --- | --- |
| 主机 | `192.168.2.10:22` |
| 账号 | `ws00-access`（已 sudo 免密） |
| 私钥路径 | `~/.config/hqzyai/ws00-access/id_ed25519`（本机软链到 `~/.ssh/agentos-prod`） |
| SSH Host | `agentos-prod`（见 `ssh/config.snippet`） |
| 数据库容器 | `agentos-postgres` |
| 库 / 用户 | `agentos_bff` / `agentos` |

## 登录一体机

```bash
ssh -i ~/.config/hqzyai/ws00-access/id_ed25519 ws00-access@192.168.2.10
# 或（已配 Host 别名后）
ssh agentos-prod

# 需要完整 root 环境时
sudo -i
```

## 进入数据库

```bash
sudo docker exec -it agentos-postgres psql -U agentos -d agentos_bff
```

只读会话建议：

```sql
\pset pager off
BEGIN READ ONLY;
SET LOCAL TIME ZONE 'Asia/Shanghai';
-- 查询...
COMMIT;
```

本机一条命令跑 SQL：

```bash
./scripts/ssh_psql.sh < scripts/query_member_create_7d.sql
```

导出全库表结构说明（字段 / 主键 / 外键 / 索引 → `schema/`）：

```bash
python3 scripts/dump_schema.py
```

## 示例：最近 7 天新增人员（含已删除）

见 [`scripts/query_member_create_7d.sql`](scripts/query_member_create_7d.sql)，最近一次结果：[`queries/member_create_7d_2026-10-21.md`](queries/member_create_7d_2026-10-21.md)。

## 备选：SSH 隧道 + 本地客户端

PG 未映射宿主机端口时，可隧道到容器 IP（重建容器后 IP 可能变）：

```bash
./scripts/tunnel.sh
# 然后 Navicat：127.0.0.1:15432 / agentos_bff / agentos / 见 .env
```

业务账号密码仅存本地 `.env`（已 gitignore）。

## 目录

```
系统对接/AgentOS对接/
├── README.md
├── .env.example / .env
├── ssh/config.snippet
├── scripts/
│   ├── ssh_psql.sh              # SSH + docker exec psql
│   ├── query_member_create_7d.sql
│   ├── tunnel.sh                # 可选本地隧道
│   └── inspect_db.py            # 隧道探库（可选）
└── queries/                     # 查询结果存档
```
