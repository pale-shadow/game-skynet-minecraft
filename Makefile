VENV = .venv
PYTHON = $(VENV)/bin/python3
REMOTE_NODE = skynet

.PHONY: python test remote-audit clean

lint: python
	@echo "==> Formatting and Ordering Python Modules..."
	$(VENV)/bin/isort .
	$(VENV)/bin/black .

python:
	@echo "==> Synchronizing Stargate Python Environment..."
	test -d $(VENV) || python3 -m venv $(VENV)
	$(VENV)/bin/python3 -m pip install -r requirements.txt pytest pytest-asyncio

test: python
	@echo "==> Initiating Distributed Test Suite with Coverage..."
	$(PYTHON) -m pytest test/test_gemini_link.py test/test_brain.py test/test_hardware.py test/test_neural_vault_logging_persistence.py test/test_hailo_npu_decoding_validity.py test/test_schematic_boundary_safety.py
	$(PYTHON) -m pytest test/test_rcon.py test/test_builders.py
	# $(PYTHON) -m pytest --cov=schematics/ 
	ssh $(REMOTE_NODE) "hailortcli fw-control identify && vcgencmd measure_temp"

remote-audit:
	@echo "==> Auditing Skynet NPU & Thermal State..."
	ssh $(REMOTE_NODE) "tail -n 50 /home/minecraft/logs/skynet_daemon.log"	
