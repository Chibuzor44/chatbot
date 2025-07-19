FROM python:3.10-bookworm

WORKDIR /app

# # Install uv via official install script
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy dependency files first to leverage Docker cache
COPY . /app

# Install Python dependencies
RUN uv sync --locked

CMD ["uv", "run", "app.py"]