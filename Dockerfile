FROM python:3-slim AS builder
ADD . /app
WORKDIR /app
RUN pip install --target=/app boto3 requests

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
RUN ls /app
ENV PYTHONPATH /app

CMD ["/app/main.py"]