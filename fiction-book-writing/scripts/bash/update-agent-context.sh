#!/usr/bin/env bash
AGENT_TYPE=$1
if [ -z "$AGENT_TYPE" ]; then
    echo "Error: No agent type provided."
    exit 1
fi

echo "Updating agent context for $AGENT_TYPE..."
mkdir -p .specify/memory
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Agent context refreshed for $AGENT_TYPE" >> .specify/memory/agent-status.log
