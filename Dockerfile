FROM python:3.10-bookworm

WORKDIR /app

# Install uv via official install script
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Add uv to PATH (default install is in ~/.local/bin)
ENV PATH="/root/.local/bin:$PATH"

COPY . /app

RUN uv sync

CMD ["python3", "app.py"]