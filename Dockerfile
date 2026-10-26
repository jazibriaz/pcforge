FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# Dependencies first so this layer is cached when only app code changes
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/

# Never run as root inside the container
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin pcforge
USER 10001

# CI passes the git SHA here; it shows in the page footer and /version
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

# 8080 = app (behind the Ingress), 9100 = Prometheus metrics (cluster-internal only)
ENV METRICS_PORT=9100
EXPOSE 8080 9100

# One worker + threads: prometheus_client counters live in process memory,
# so multiple workers would each report partial numbers. Scale with replicas instead.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", \
     "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "app:app"]
