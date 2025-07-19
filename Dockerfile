FROM python:3.10-bookworm

WORKDIR /app

# Install uv via official install script
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Add uv to PATH (default install is in ~/.local/bin)
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync

# Now copy the rest of the application
COPY . .

# Expose the port used in app.py
EXPOSE 8080

CMD ["python3", "app.py"]