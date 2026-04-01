VENV = .venv
PYTHON = $(VENV)/bin/python3
REMOTE_NODE = skynet

.PHONY: python test remote-audit clean

python:
	@echo "==> Synchronizing Stargate Python Environment..."
	test -d $(VENV) || python3 -m venv $(VENV)
	$(VENV)/bin/python3 -m pip install -r requirements.txt pytest pytest-asyncio

test: python
	@echo "==> Initiating Distributed Test Suite..."
	$(PYTHON) -m pytest test/test_gemini_link.py test/test_brain.py
	$(PYTHON) -m pytest test/test_rcon.py
	ssh $(REMOTE_NODE) "hailortcli fw-control identify && vcgencmd measure_temp"

remote-audit:
	@echo "==> Auditing Skynet NPU & Thermal State..."
	ssh $(REMOTE_NODE) "tail -n 50 /home/minecraft/logs/skynet_daemon.log"	
