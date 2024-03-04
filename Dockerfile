FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN export POETRY_HOME=/opt/poetry \
  && curl -sSL https://install.python-poetry.org | python - --version 1.6.1 \
  && $POETRY_HOME/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --upgrade pip setuptools \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --user -r requirements.txt

COPY main.py main.py
EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health

ENTRYPOINT ["python", "-m", "streamlit", "run", "main.py", "--server.port=8502", "--server.address=0.0.0.0"]