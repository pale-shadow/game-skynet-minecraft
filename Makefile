python:
	eval "$(ssh-agent -s)" && ssh-add
	python3 -m venv .venv

