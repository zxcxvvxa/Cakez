#!/bin/bash
set -e

echo "[+] Starting container initialization..."

# 1. File Descriptor Limits
ulimit -n 65535 2>/dev/null || true

# 2. Kernel & TCP Socket Tuning (fails silently in restricted container environments like Cloud Run)
echo "[+] Attempting Kernel & TCP Socket Tuning..."
sysctl -w net.core.default_qdisc=fq 2>/dev/null || true
sysctl -w net.ipv4.tcp_congestion_control=bbr 2>/dev/null || true

sysctl -w net.core.rmem_max=16777216 2>/dev/null || true
sysctl -w net.core.wmem_max=16777216 2>/dev/null || true
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216" 2>/dev/null || true
sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216" 2>/dev/null || true

sysctl -w net.ipv4.tcp_fin_timeout=15 2>/dev/null || true
sysctl -w net.ipv4.tcp_tw_reuse=1 2>/dev/null || true
sysctl -w net.ipv4.tcp_fastopen=3 2>/dev/null || true

echo "[+] Generating SSH Host Keys..."
ssh-keygen -A
mkdir -p /run/sshd /var/run/sshd

echo "[+] Handing over process management to Supervisor..."
exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
