# Dockerfile.chonk
FROM eclipse-temurin:25-jre-jammy

LABEL maintainer="admin@bitsmasher.net"
LABEL role="chonk-execution-layer"

# Install Git LFS, jq (for JSON parsing), and RCON utilities
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    jq \
    netcat \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

WORKDIR /opt/minecraft

# Expose Minecraft server and RCON ports
EXPOSE 25565/tcp
EXPOSE 25575/tcp

# Copy server assets (RCON script, properties, plugins folder)
COPY ./rcon.sh /usr/local/bin/rcon
RUN chmod +x /usr/local/bin/rcon

# Pre-flight hydration script to enforce raw binary conversion
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Start the Paper JVM
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["java", "-Xms16G", "-Xmx16G", "-XX:+UseZGC", "-jar", "paper-26.1.5.jar", "nogui"]
