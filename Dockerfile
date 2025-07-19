FROM python:3.10-bookworm

WORKDIR /app


WORKDIR /app

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:$PATH"

# Copy just dependency files first
COPY pyproject.toml uv.lock* /app/

# Make sure we're still in /app
WORKDIR /app

# Install Python dependencies
RUN uv sync

# Copy the rest of your source files
COPY . /app

EXPOSE 8080

CMD ["python3", "app.py"]