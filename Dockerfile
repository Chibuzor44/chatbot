FROM python:3.10-bookworm

WORKDIR /app

COPY . /app

RUN uv sync

CMD ["python3", "app.py"]