FROM python:3.10-bookworm

WORKDIR /app

# Install uv via official install script
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Add uv to PATH (default install is in ~/.cargo/bin)
ENV PATH="/root/.cargo/bin:${PATH}"

COPY . /app

RUN uv sync

CMD ["python3", "app.py"]