# Stage 1: install dependencies
FROM python:3.12 AS builder

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV COUNTER_FILE=/data/visits.txt

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

RUN groupadd --system app && \
    useradd --system --gid app app && \
    mkdir -p /data && \
    chown app:app /data

COPY --chown=app:app app.py ./

USER app

EXPOSE 8080

CMD ["python", "app.py"]
