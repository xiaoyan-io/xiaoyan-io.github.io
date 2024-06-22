#Proxmox创建和编辑自动扩容脚本

##首先，创建一个脚本文件 `auto_resize_lxc.sh`：

```bash
nano /root/auto_resize_lxc.sh
```

将以下内容粘贴到脚本文件中：

```bash
#!/bin/bash

# 日志文件路径
LOGFILE="/var/log/lxc_auto_resize.log"

# 获取所有LXC容器ID和状态
CT_LIST=$(pct list | awk 'NR>1 {print $1, $2}')

# 设置触发扩容的阈值（比如80%）
THRESHOLD=80

{
    echo "开始检查 LXC 容器磁盘使用率: $(date)"

    echo "$CT_LIST" | while read -r CTID STATUS; do
        if [ "$STATUS" != "running" ]; then
            echo "容器 $CTID 未运行。跳过。"
            continue
        fi

        # 获取当前的磁盘使用率
        USAGE=$(pct exec $CTID -- df / --output=pcent / | tail -n1 | tr -dc '0-9')

        if [ -z "$USAGE" ]; then
            echo "容器 $CTID 获取磁盘使用率失败。"
            continue
        fi

        if [ "$USAGE" -gt "$THRESHOLD" ]; then
            echo "容器 $CTID 磁盘使用率达到 $THRESHOLD%。正在扩容..."
            # 扩容磁盘（增加10G）
            pct resize $CTID rootfs +10G
            echo "容器 $CTID 磁盘已增加10G"
            echo "容器 $CTID 磁盘已增加10G" | mail -s "LXC 容器扩容通知" your-email@example.com
        else
            echo "容器 $CTID 磁盘使用率低于阈值。无操作。"
        fi
    done

    echo "检查结束: $(date)"
} >> "$LOGFILE" 2>&1
```

保存并关闭文件。

### 赋予脚本执行权限

```bash
chmod +x /root/auto_resize_lxc.sh
```

### 安装邮件工具

安装 `mailutils` 以便发送邮件通知：

```bash
apt-get update
apt-get install mailutils -y
```

### 创建日志轮转配置文件

创建或编辑 `/etc/logrotate.d/lxc_auto_resize` 文件：

```bash
nano /etc/logrotate.d/lxc_auto_resize
```

在文件中添加以下内容：

```plaintext
/var/log/lxc_auto_resize.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 640 root root
    sharedscripts
    postrotate
        /usr/sbin/service cron reload > /dev/null
    endscript
}
```

保存并关闭文件。

### 添加定时任务

使用 `crontab` 添加定时任务，让脚本每小时运行一次：

```bash
crontab -e
```

在crontab文件中添加一行：

```bash
0 * * * * /root/auto_resize_lxc.sh
### 手动测试脚本

手动运行脚本以确保其工作正常：

bash
/root/auto_resize_lxc.sh


### 查看日志

查看日志文件，确保脚本运行正常并记录了所有操作：

bash
cat /var/log/lxc_auto_resize.log


通过这些步骤，你的Proxmox VE系统将能够自动扩容LXC容器的磁盘空间，并且所有操作都有详细的日志记录和邮件通知。这样可以确保你在磁盘空间不足时能够及时得到通知并采取相应措施。