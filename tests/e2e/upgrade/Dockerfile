# Test environment for flowspec upgrade-tools functionality
# This provides an isolated environment to test npm/pnpm installs

FROM python:3.11-slim

# Install Node.js and npm (but NOT pnpm to test fallback)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python package management
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY templates/ templates/
COPY memory/ memory/

# Install flowspec CLI from local source
RUN uv tool install .

# Install OLD versions of backlog.md and beads to test upgrade
RUN npm install -g backlog.md@1.20.1 @beads/bd@0.30.2

# Verify installations
RUN flowspec version && backlog --version && bd --version

# Default command runs the upgrade test
CMD ["bash", "-c", "echo '=== Before upgrade ===' && \
    flowspec version && \
    echo '=== Running upgrade-tools ===' && \
    flowspec upgrade-tools && \
    echo '=== After upgrade ===' && \
    flowspec version && \
    backlog --version && \
    bd --version"]
