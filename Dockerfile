#Streamlit app

# Base image
FROM python:3.8-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install libpq-dev
RUN apt-get update && apt-get install -y libpq-dev gcc

FROM base as builder

ENV POSTGRES_USER=$POSTGRES_USER \
 POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 POSTGRES_DB=$POSTGRES_DB \
 POSTGRES_HOST=$POSTGRES_HOST \
 POSTGRES_PORT=$POSTGRES_PORT \
 PIP_DEFAULT_TIMEOUT=100 \
 PIP_DISABLE_PIP_VERSION_CHECK=1 \
 PIP_NO_CACHE_DIR=1 \
 POETRY_VERSION=1.3.0

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock README.md ./

COPY rightmove_scrape ./rightmove_scrape

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root && \
    poetry build

FROM base as final

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .

RUN ./.venv/bin/pip install *.whl

COPY app ./app
COPY rightmove_scrape ./rightmove_scrape

# Make port 8501 available to the world outside this container
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Activate .venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["streamlit", "run", "./app/main_page.py", "--server.port=8501", "--server.address=0.0.0.0"]
# ENTRYPOINT ["python", "-m", "streamlit", "run", "./rightmove-scrape/app/main_page.py", "--server.port=8501", "--server.address=0.0.0.0"]
