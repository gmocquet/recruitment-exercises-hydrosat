ARG PYTHON_IMAGE=python:3.13.3-slim-bookworm
ARG UV_VERSION=0.7.2

ARG PYTHONUNBUFFERED=1
ARG VENV_PATH=/opt/.venv

# ----------- STAGE 1: UV Installer -----------

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-installer

# ----------- STAGE 2: Builder -----------

FROM ${PYTHON_IMAGE} AS builder

ARG PYTHONUNBUFFERED
ARG VENV_PATH

ENV PYTHONUNBUFFERED=${PYTHONUNBUFFERED} \
    VENV_PATH=${VENV_PATH} \
    VIRTUAL_ENV=${VENV_PATH} \
    PATH="${VENV_PATH}/bin:$PATH"

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv-installer /uv /usr/local/bin/uv
COPY --from=uv-installer /uvx /usr/local/bin/uvx

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv venv ${VENV_PATH}

# Assuming the dev server is OK for testing purposes
# For production, add the --no-dev flag
RUN . ${VENV_PATH}/bin/activate && uv sync --locked --no-editable --active

COPY ./ndvi_monitoring/ ./ndvi_monitoring

# ----------- STAGE 3: Runtime -----------

FROM ${PYTHON_IMAGE}

ARG PYTHONUNBUFFERED
ARG VENV_PATH

ENV PYTHONUNBUFFERED=${PYTHONUNBUFFERED} \
    VENV_PATH=${VENV_PATH} \
    VIRTUAL_ENV=${VENV_PATH} \
    PATH="${VENV_PATH}/bin:$PATH"

WORKDIR /app

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder $VENV_PATH $VENV_PATH
COPY --from=builder /app/ndvi_monitoring/ ./ndvi_monitoring
COPY --from=builder /app/pyproject.toml ./pyproject.toml
COPY --from=builder /app/.python-version ./

RUN gdalinfo --version \
    && python -c "import rasterio; print(rasterio.__gdal_version__)"

EXPOSE 80

# Assuming the dev server is OK for testing purposes
CMD ["dagster", "dev"]
