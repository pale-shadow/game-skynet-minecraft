# Dockerfile.jetson03_surveyor
FROM nvcr.io/nvidia/l4t-base:r32.7.1

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3-pip python3-dev git git-lfs build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/gpu-bridge/surveyor

COPY requirements-surveyor.txt .
# Install Numba and PyCUDA for parallel AABB checks
RUN pip3 install --no-cache-dir fastapi uvicorn redis numba pycuda numpy

COPY . /opt/gpu-bridge/surveyor/

EXPOSE 8003

CMD ["uvicorn", "surveyor_service:app", "--host", "0.0.0.0", "--port", "8003"]