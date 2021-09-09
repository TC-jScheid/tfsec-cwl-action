FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM python:3-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]
