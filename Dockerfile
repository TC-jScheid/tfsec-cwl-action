FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM python:3-slim
RUN pip3 --no-cache-dir install --upgrade boto3 
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
RUN ["chmod", "+x", "/app/main.py"]
CMD ["/app/main.py"]
