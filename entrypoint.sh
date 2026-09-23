#!/bin/bash
set -e

echo "[+] Starting container initialization..."

# 1. File Descriptor Limits
ulimit -n 65535 2>/dev/null || true

# 2. Network & Kernel Tuning (Execute only if privileged/writeable)
if [ -w /proc/sys/net/core/default_qdisc ]; then
    echo "[+] Applying Kernel & TCP Socket Tuning..."
    sysctl -w net.core.default_qdisc=fq 2>/dev/null || true
    sysctl -w net.ipv4.tcp_congestion_control=bbr 2>/dev/null || true
    sysctl -w net.core.rmem_max=16777216 2>/dev/null || true
    sysctl -w net.core.wmem_max=16777216 2>/dev/null || true
    sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216" 2>/dev/null || true
    sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216" 2>/dev/null || true
    sysctl -w net.ipv4.tcp_fin_timeout=15 2>/dev/null || true
    sysctl -w net.ipv4.tcp_tw_reuse=1 2>/dev/null || true
    sysctl -w net.ipv4.tcp_fastopen=3 2>/dev/null || true
else
    echo "[!] Container lacks sysctl write permissions (e.g. Cloud Run). Skipping kernel tuning."
fi

# 3. SSH Setup (Generate host keys only if missing)
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    echo "[+] Generating missing SSH Host Keys..."
    ssh-keygen -A
fi

mkdir -p /run/sshd /var/run/sshd
chmod 0755 /run/sshd /var/run/sshd

# 4. Hand over process management to Supervisor
echo "[+] Handing over process management to Supervisor..."
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
