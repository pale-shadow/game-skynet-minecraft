# Dockerfile.edget
FROM debian:bookworm-slim

LABEL maintainer="admin@bitsmasher.net"
LABEL role="edge-t-vision"

# Add Google Coral repository and install Mendel Development Tool (MDT)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    python3 \
    python3-pip \
    python3-venv \
    openssh-client \
    && echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update \
    && apt-get install -y mdt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/edge-t

# Setup mdt-keymaster for secure SSH communications
RUN mkdir -p /root/.config/mdt \
    && mkdir -p /root/.ssh

# Copy vision pipeline and decoration placement logic
COPY ./src/vision /opt/edge-t/src
COPY requirements.txt .

RUN python3 -m venv /opt/edge-t/.venv
ENV PATH="/opt/edge-t/.venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Ensure mdt-keymaster enforces cluster topology auth before starting the pipeline
CMD ["/bin/bash", "-c", "mdt wait && python src/telemetry_edge.py"]
