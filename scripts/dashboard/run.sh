#!/bin/sh
# (Re)start the dashboard on port 8383, detached. Safe to run repeatedly.
cd "$(dirname "$0")/../.."
for p in $(pgrep -f "[d]ashboard/server.py"); do kill "$p" 2>/dev/null; done
sleep 1
mkdir -p logs/dashboard
setsid nohup python3 scripts/dashboard/server.py --port "${1:-8383}" > logs/dashboard/server.out 2>&1 < /dev/null &
sleep 1
echo "dashboard on http://$(hostname -I | cut -d' ' -f1):${1:-8383}"
