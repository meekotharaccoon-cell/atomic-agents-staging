@echo off
echo Starting Atomic Agents...
cd C:\atomic-agents
powershell -ExecutionPolicy Bypass -File start-agent.ps1
pause
