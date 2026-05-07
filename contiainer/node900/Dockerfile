# Dockerfile.jetson01_architect
FROM nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git git-lfs libopenblas-dev \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /opt/gpu-bridge/architect

# Install FastAPI, Redis, and Transformer dependencies
COPY requirements-architect.txt .
RUN pip3 install --no-cache-dir fastapi uvicorn redis transformers numpy

COPY . /opt/gpu-bridge/architect/

# Expose FastAPI port
EXPOSE 8001

# Start the ViT validation worker
CMD ["uvicorn", "architect_service:app", "--host", "0.0.0.0", "--port", "8001"]