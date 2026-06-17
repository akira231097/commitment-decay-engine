# Commitment Decay Engine — minimal image.
# Pure-Python, standard-library-only runtime (no system packages required).
FROM python:3.12-slim

# Avoid .pyc files and force unbuffered stdout for clean container logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project metadata and source, then install the package (installs the
# `cde` console script defined in pyproject.toml [project.scripts]).
COPY pyproject.toml README.md ./
COPY commitment_decay_engine/ ./commitment_decay_engine/
COPY examples/ ./examples/
RUN pip install --no-cache-dir .

# `cde demo` reads examples/ via relative paths, so run from /app.
ENTRYPOINT ["cde"]
CMD ["demo"]