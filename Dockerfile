FROM python:3-slim AS builder
ADD . /app
WORKDIR /app
RUN ["python3", "--no-cache-dir", "-m", "pip", "install", "cffi"]
RUN pip install --target=/app boto3 PyGithub

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

CMD ["/app/main.py"]