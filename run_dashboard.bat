@echo off
title Py12 Bot Admin Dashboard
echo Starting Py12 Admin Dashboard...
start "" "http://localhost:5000"
.\venv\Scripts\python.exe dashboard.py
pause

