#!/usr/bin/env bash
set -e

source .venv/bin/activate

echo "Starting Research Agent..."
uvicorn agents.research_agent:app --host 0.0.0.0 --port 8001 > research.log 2>&1 &
R_PID=$!

echo "Starting Writer Agent..."
uvicorn agents.writer_agent:app --host 0.0.0.0 --port 8002 > writer.log 2>&1 &
W_PID=$!

echo "Starting Supervisor..."
uvicorn supervisor.app:app --host 0.0.0.0 --port 8000 > supervisor.log 2>&1 &
S_PID=$!

trap 'kill $R_PID $W_PID $S_PID' EXIT
echo "All services started."
echo "Supervisor: http://127.0.0.1:8000"
echo "Research Agent Card: http://127.0.0.1:8001/.well-known/agent-card.json"
echo "Writer Agent Card: http://127.0.0.1:8002/.well-known/agent-card.json"

wait
