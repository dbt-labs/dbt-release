FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests packaging

ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]
