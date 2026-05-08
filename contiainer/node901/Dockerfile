# Dockerfile.jetson02_clerk
FROM python:3.14-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git git-lfs \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /opt/gpu-bridge/clerk

COPY requirements-clerk.txt .
# Requires nbtlib for deep-scanning NBT headers
RUN pip install --no-cache-dir fastapi uvicorn redis nbtlib

# Pull in the validation scripts
COPY test_schematic_metadata_integrity.py /opt/gpu-bridge/clerk/
COPY . /opt/gpu-bridge/clerk/

EXPOSE 8002

CMD ["uvicorn", "clerk_service:app", "--host", "0.0.0.0", "--port", "8002"]