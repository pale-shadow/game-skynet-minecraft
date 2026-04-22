VENV = .venv
PYTHON = $(VENV)/bin/python3
HUB01_NODE = skynet
HUB06_NODE = edge-t

.PHONY: python test remote-audit backup clean lint stargate edge-t

# Project: game-chonk-minecraft (bitsmasher.net)
# Environment: Paper 1.21.11
# Infrastructure: The Bit-Stream Flux-Rail (BSFR)

lint: python
	@echo "==> Formatting BSFR Python Modules..."
	$(VENV)/bin/isort .
	$(VENV)/bin/black .

python:
	@echo "==> Synchronizing Stargate Python Environment..."
	test -d $(VENV) || python3 -m venv $(VENV)
	$(VENV)/bin/python3 -m pip install -r requirements.txt pytest pytest-asyncio

stargate: python
	@echo "==> Deploying Stargate MCP Services..."
	$(PYTHON) -m pip install -r src/servers/stargate/requirements-stargate.txt

edge-t: python
	@echo "==> Deploying Edge-T Vision Services..."
	$(PYTHON) -m pip install -r src/servers/edge-t/requirements-edge-t.txt

test: python
	@echo "==> Initiating BSFR Distributed Test Suite..."
	PYTHONPATH=./src $(PYTHON) -m pytest test/test_gemini_link.py \
			test/test_brain.py \
			test/test_hardware.py \
			test/test_neural_vault_logging_persistence.py \
			test/test_hailo_npu_decoding_validity.py \
			test/test_schematic_boundary_safety.py \
			test/test_schematic_metadata_integrity.py \
			test/test_rcon.py \
			test/test_builders.py
	@echo "==> Auditing Hub 01 (Inference Nexus) NPU & Thermal State..."
	ssh $(HUB01_NODE) "hailortcli fw-control identify && vcgencmd measure_temp"

remote-audit:
	@echo "==> Auditing Hub 01 Logic Logs & Hub 06 Vision Daemon..."
	ssh $(HUB01_NODE) "tail -n 50 /home/minecraft/logs/skynet_daemon.log"
	ssh mendel@$(HUB06_NODE) "systemctl status edge-t-daemon.service --no-pager"

backup:
	@echo "==> Synchronizing BSFR Technical Ledger to GitHub..."
	./bin/backup_to_git.sh

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
