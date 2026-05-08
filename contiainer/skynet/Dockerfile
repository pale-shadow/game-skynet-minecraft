# Dockerfile.skynet
FROM ubuntu:26.04

LABEL maintainer="admin@bitsmasher.net"
LABEL role="skynet-ai-orchestration"

# Prevent interactive prompts during apt installations
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and HailoRT dependencies
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3-pip \
    python3-venv \
    build-essential \
    cmake \
    git \
    wget \
    pciutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/skynet

# Establish Python virtual environment for the T2BM pipeline
RUN python3 -m venv /opt/skynet/.venv
ENV PATH="/opt/skynet/.venv/bin:$PATH"

# Install HailoRT and project requirements
# (Assuming hailo_rt wheels are available locally or via specific repo)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy schematic validation vectors and pipeline logic
COPY ./src /opt/skynet/src
COPY ./test /opt/skynet/test

# Verify metadata and boundary safety on build
RUN pytest test/test_schematic_metadata_integrity.py && \
    pytest test/test_schematic_boundary_safety.py

CMD ["python", "src/skynet/orchestrator.py"]
