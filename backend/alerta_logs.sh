#!/bin/bash
LOGS=$(logcli query '{namespace="default"} |= "error"' --addr="http://localhost:3100" --since=5m --limit=10)
if [[ $LOGS == *"error"* ]]; then
    echo -e "Subject: Erro detectado nos pods!\n\n$LOGS" | msmtp henriqueslopes99@gmail.com
fi