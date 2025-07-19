FROM python:3.10-bookworm

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]