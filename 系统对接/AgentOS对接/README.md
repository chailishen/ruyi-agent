# AgentOS 对接 — 00 一体机主库

00 一体机 AgentOS 主库为 **PostgreSQL 17**，宿主机未对外开放 `5432`，需经 **SSH 隧道** 访问。

## 当前状态

| 项 | 状态 |
| --- | --- |
| 连接方式 | SSH 隧道 → 本地 `127.0.0.1:15432` |
| 业务库 | `agentos_bff` |
| 本机密钥 | 已配置 `~/.ssh/agentos-prod`（ED25519，`ws00-access`） |
| SSH Host | `agentos-prod` → `ws00-access@192.168.2.10:22` |
| 网络 | 本机直连 `192.168.2.10:22` **超时**（需在一体机同网段或先开 VPN） |
| 库表探查 | 跳板可达后：`./scripts/tunnel.sh` + `python3 scripts/inspect_db.py` |

## 前置条件

1. 私钥：`~/.ssh/agentos-prod`（`chmod 600`）。粘贴时勿去掉换行；若 `ssh-keygen -y -f ~/.ssh/agentos-prod` 报 invalid format，多半是换行丢失。
2. SSH config：已写入 `Host agentos-prod`（见 [`ssh/config.snippet`](ssh/config.snippet)）。
3. 网络：能访问 `192.168.2.10:22`（办公室内网 / VPN）。
4. 环境变量：

```bash
cp .env.example .env   # 若尚无 .env
```

## 一、建立 SSH 隧道

保持终端窗口打开：

```bash
./scripts/tunnel.sh
```

等价手写命令：

```bash
ssh -N \
  -o HostKeyAlias=ws00-frp-audit \
  -i ~/.ssh/agentos-prod \
  -o ProxyCommand='ssh agentos-prod -W 127.0.0.1:6022' \
  -L 127.0.0.1:15432:172.23.0.6:5432 \
  ubuntu@127.0.0.1
```

说明：

- `172.23.0.6` 为当前数据库容器内网 IP，**容器重建后可能变化**，连不上时先找运维确认最新 IP。
- 隧道成功后，本机 `127.0.0.1:15432` 即转发到 PG 的 `5432`。

## 二、客户端连接（Navicat / DBeaver）

| 配置 | 值 |
| --- | --- |
| 主机 | `127.0.0.1` |
| 端口 | `15432` |
| 数据库 | `agentos_bff` |
| 用户名 | `agentos` |
| 密码 | 见 `.env` 中 `PGPASSWORD` |
| SSL | 禁用 |

## 三、命令行探库

隧道开着时，另开终端：

```bash
cd 系统对接/AgentOS对接
python3 -m pip install -r scripts/requirements.txt
python3 scripts/inspect_db.py
```

会输出：

- 服务器版本 / 当前库
- schema 列表
- 表清单与行数估算
- 结果写入 `schema/tables.json`、`schema/overview.md`

## 目录结构

```
系统对接/AgentOS对接/
├── README.md
├── .env.example          # 连接参数模板
├── .env                  # 本地密钥（勿提交）
├── ssh/config.snippet    # 本机 SSH config 片段
├── scripts/
│   ├── tunnel.sh         # 建立 SSH 隧道
│   ├── inspect_db.py     # 探库并导出 schema 摘要
│   └── requirements.txt
└── schema/               # inspect_db 输出（有数据后再提交）
```

## 安全注意

- 生产业务账号，仅用于对接排查；勿写入公开文档或提交到 Git。
- 仓库 `.gitignore` 已忽略本目录下的 `.env`。
- 若密码轮换，只改 `.env`，并同步通知相关同学。
