# Dockerfile.jetson04_engineer
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git git-lfs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/gpu-bridge/engineer

COPY requirements-engineer.txt .
RUN pip install --no-cache-dir fastapi uvicorn redis networkx

COPY . /opt/gpu-bridge/engineer/

EXPOSE 8004

CMD ["uvicorn", "engineer_service:app", "--host", "0.0.0.0", "--port", "8004"]