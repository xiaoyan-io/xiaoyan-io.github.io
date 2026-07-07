---
title: Alan Cloud Agent Hub — 架构解析与使用方法
date: 2026-07-05 14:30:00
updated: 2026-07-05 14:30:00
tags:
  - Alan
  - Agent
  - Telegram
  - Docker
  - 自动化
categories:
  - Alan
---

> 这是我给自己和团队整理的「Alan Cloud Agent Hub」完整架构文档和使用手册。

## 一、系统概述

Alan Cloud Agent Hub 是一个**分布式节点管理平台**，通过 Telegram Bot + HTTP API 实现远程节点的统一管理和监控。

### 核心能力

- **节点心跳监控** — 远程节点（Pi5、WSL、PC）定期上报状态
- **Telegram 管理** — 通过 Telegram 命令管理节点、任务、日志
- **自动超时检测** — Cron 定时扫描离线节点
- **JWT 认证** — 节点间通信使用 JWT Token 鉴权
- **Docker 化部署** — 支持一键容器化运行

### 架构总览

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Telegram   │────▶│  Hub (VPS)        │◀────│  节点 Agent │
│  管理员     │     │                  │     │             │
│  发送命令   │     │  ┌────────────┐  │     │ Pi5 / WSL   │
│             │     │  │Telegram Bot│  │     │ / Main PC   │
│             │     │  └────────────┘  │     │             │
│             │     │                  │     │  POST       │
│             │     │  ┌────────────┐  │     │ heartbeat   │
│             │     │  │ Node API   │  │     │ (JWT)       │
│             │     │  │ :8082      │  │     │             │
│             │     │  └────────────┘  │     │             │
│             │     │                  │     │             │
│             │     │  ┌────────────┐  │     │             │
│             │     │  │ 超时检测   │  │     │             │
│             │     │  │ (Cron 10m) │  │     │             │
│             │     │  └────────────┘  │     │             │
└─────────────┘     └──────────────────┘     └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ nodes.json  │
                   │ 节点注册表   │
                   └─────────────┘
```

## 二、文件结构

```
/opt/alan-cloud-agent/
├── bots/
│   └── telegram_bot.py          # Telegram 管理 Bot
├── src/
│   ├── node_api.py              # Node HTTP API (FastAPI, 端口 8082)
│   └── node_agent.py            # 节点心跳 Agent
├── scripts/
│   └── check_node_timeout.py    # 节点超时检测脚本
├── configs/
│   ├── nodes.json               # 节点注册表
│   └── .jwt_secret              # JWT 签名密钥
├── tasks/                       # 任务队列目录
├── logs/                        # 日志目录
├── docs/
│   └── USER_MANUAL.md           # 完整使用手册
├── docker-compose.yml           # Docker 编排
├── Dockerfile.bot               # Bot 镜像
├── Dockerfile.api               # API 镜像
├── Dockerfile.agent             # Agent 镜像
└── .env                         # 环境变量配置
```

## 三、Telegram 命令参考

所有 `/node` 命令仅限管理员使用。

### 节点管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `/node status` | 查看所有注册节点 | `/node status` |
| `/node heartbeat <name> <ip>` | 手动更新节点心跳 | `/node heartbeat Pi5 192.168.1.50` |
| `/node register <name> <type>` | 注册新节点 | `/node register MyServer development` |
| `/node renew-token <name>` | 轮换节点 Token | `/node renew-token Pi5` |

#### `/node status`

显示所有节点的详细信息：

```
🖥️ Registered Nodes:

🟢 Pi5 Edge (edge)
   IP: 192.168.1.50 | Last seen: 2026-07-05 14:30

🔴 WSL Development (development)
   IP: 192.168.1.100 | Last seen: 2026-07-05 12:15
```

- 🟢 = online（最近有心跳）
- 🔴 = offline（超时未响应）

#### `/node register <name> <type>`

注册新节点并自动生成 JWT Token：

```
/node register MyServer development
```

支持的节点类型：
- `development` — 开发环境（代码、测试、仓库）
- `file` — 文件存储（磁盘、NAS、项目文件）
- `edge` — 边缘计算（IoT、传感器、网关）
- `compute` — 计算节点（GPU、批量处理）
- `monitor` — 监控节点（网络扫描、健康检查）

注册成功后返回：
```
✅ Node registered

Name: MyServer
Node ID: myserver-a1b2
Type: development
Token: eyJhbG...NiIs...

⚠️ Save the token — it won't be shown again.
Deploy node_agent.py on the new node with this token.
```

**重要：Token 只显示一次！请妥善保存。**

#### `/node heartbeat <name> <ip>`

手动更新指定节点的心跳时间，适用于节点 Agent 暂时无法运行时的应急操作。

#### `/node renew-token <name>`

轮换指定节点的 JWT Token（旧 Token 立即失效），用于 Token 可能泄露或定期安全轮换。

### 任务管理

| 命令 | 说明 |
|------|------|
| `/task list` | 查看任务队列 |
| `/task create <title> <type> <command>` | 创建新任务 |
| `/task status <task_id>` | 查看任务详情 |
| `/task complete <task_id>` | 标记任务完成（管理员） |
| `/task fail <task_id> [reason]` | 标记任务失败（管理员） |

### 系统信息

| 命令 | 说明 |
|------|------|
| `/status` | Hub 健康检查 + 进程状态 + 任务统计 |
| `/brief` | 今日摘要（日志、任务、Cron、进程） |
| `/logs` | 最近 20 条日志 |
| `/logs tail <N>` | 最近 N 条日志 |
| `/logs filter <keyword>` | 搜索日志 |
| `/help` | 完整命令列表 |

## 四、HTTP API 参考

### 节点心跳

```
POST /api/node/heartbeat
Content-Type: application/json

{
  "node_id": "pi5-edge",
  "name": "Pi5 Edge",
  "type": "edge",
  "address": "192.168.1.50",
  "capabilities": ["homeassistant", "growatt"],
  "token": "<jwt-token>"
}
```

**成功响应 (200)：**
```json
{
  "status": "ok",
  "node_id": "pi5-edge",
  "updated_fields": ["name", "type", "address", "capabilities", "last_heartbeat", "status"],
  "last_heartbeat": "2026-07-05 14:30",
  "node_status": "online"
}
```

### 查询节点状态

```
GET /api/node/status
```

### 健康检查

```
GET /health
```

## 五、节点部署指南

### 前置条件

在每台远程节点（Pi5、WSL、Main PC）上安装依赖：

```bash
pip install requests python-jose[cryptography]
```

### 配置 .env

在节点上创建 `.env` 文件：

```env
HUB_URL=http://<hub-ip>:8082
NODE_ID=pi5-edge
NODE_TOKEN=<从 /node register 获取的 token>
INTERVAL=60
NODE_NAME=Pi5 Edge
NODE_TYPE=edge
NODE_ADDRESS=192.168.1.50
CAPABILITIES=homeassistant,growatt,network_scan
```

### 运行模式

**前台调试：**
```bash
python3 node_agent.py --once    # 发送一次心跳后退出
python3 node_agent.py           # 持续心跳模式
```

**后台运行（systemd）：**

创建 `/etc/systemd/system/alan-node-agent.service`：
```ini
[Unit]
Description=Alan Cloud Agent Hub — Node Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/node_agent_dir
ExecStart=/usr/bin/python3 /path/to/node_agent.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动：
```bash
systemctl daemon-reload
systemctl enable alan-node-agent
systemctl start alan-node-agent
```

## 六、节点状态流转

```
未注册 ──(/node register)──▶ 已注册(offline)
                                │
                        (首次心跳成功)
                                │
                                ▼
                          在线(online)
                                │
                        (> 超时阈值无心跳)
                                │
                                ▼
                          离线(offline)
```

### 超时检测机制

- **检测频率**：每 10 分钟执行一次（Cron）
- **超时阈值**：5 分钟（可配置）
- **触发条件**：仅当节点当前状态为 `online` 且超时才会标记为 `offline`
- **恢复条件**：节点发送心跳后自动恢复为 `online`

## 七、安全说明

- **Telegram Bot**：仅管理员 ID 可执行 `/node` 管理命令
- **Node API**：所有心跳请求需携带有效 JWT Token
- **JWT Token**：HS256 算法，24 小时有效期
- **MVP 阶段无 TLS** — 仅在可信局域网内使用
- **节点 Agent 不执行远程命令**

## 八、Docker 部署

### 构建镜像

```bash
cd /opt/alan-cloud-agent
docker compose build
```

### 启动服务

```bash
docker compose up -d
docker compose ps
docker compose logs -f bot
```

## 九、故障排查

### 节点显示 offline 但实际在线

```bash
# 1. 检查节点 Agent 进程
ps aux | grep node_agent

# 2. 手动测试心跳
python3 node_agent.py --once

# 3. 检查 Hub API 可达性
curl http://<hub-ip>:8082/health

# 4. 手动更新心跳
/node heartbeat <name> <ip>
```

### Telegram Bot 无响应

```bash
# 查看进程
ps aux | grep telegram_bot

# 查看日志
tail -50 /opt/alan-cloud-agent/logs/hub.log

# 重启 Bot
pkill -f telegram_bot.py
cd /opt/alan-cloud-agent
python3 bots/telegram_bot.py --real
```

### Node API 无法连接

```bash
# 查看 systemd 状态
systemctl status alan-node-api

# 测试 API
curl http://localhost:8082/health
curl http://localhost:8082/api/node/status

# 重启 API
systemctl restart alan-node-api
```

## 十、常用命令速查

```bash
# Hub 管理
systemctl status alan-node-api
systemctl restart alan-node-api
python3 bots/telegram_bot.py --real

# 节点管理
curl http://localhost:8082/health
curl http://localhost:8082/api/node/status
python3 scripts/check_node_timeout.py

# 日志查看
tail -f /opt/alan-cloud-agent/logs/hub.log
tail -f /opt/alan-cloud-agent/logs/node_timeout.log
```

---

> 本文档最后更新：2026-07-05 | 版本：0.3.0-MVP
