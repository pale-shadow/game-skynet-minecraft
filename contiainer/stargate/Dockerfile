# Dockerfile.stargate
FROM python:3.14-slim-bookworm

LABEL maintainer="admin@bitsmasher.net"
LABEL role="stargate-control-plane"

RUN apt-get update && apt-get install -y \
    iproute2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/stargate

# Install MCP hub dependencies and routing logic
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bridging logic and telemetry schemas
COPY ./src/stargate /opt/stargate/src

# Telemetry listener port
EXPOSE 5005/tcp

# Run the Stargate MCP Hub
CMD ["python", "src/hub.py"]
