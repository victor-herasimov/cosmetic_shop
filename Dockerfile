FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN useradd -s /bin/sh -u 1234 appuser

WORKDIR /usr/src/app

RUN apt update && apt install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir media

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

RUN chmod +x /usr/src/app/entrypoint.sh
RUN chown -R appuser:appuser /usr/src/app/media

USER appuser

ENTRYPOINT [ "./entrypoint.sh" ]