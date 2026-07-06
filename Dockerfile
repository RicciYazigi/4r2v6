# 4R2 Coherence Guardrail v7.0 "Frontier" — reproducible self-testing image.
# Build:  docker build -t 4r2:v7 .
# Verify: docker run --rm 4r2:v7 --self-test    # exits 0 iff all checks pass
# (Full pytest suite runs in CI: .github/workflows/ci.yml. This image is the
# minimal self-testing kernel+frontier artifact; self-test is its contract.)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Minimal, pinned runtime + test deps (numpy is the only kernel dependency).
RUN pip install --no-cache-dir "numpy>=1.23" "pytest>=7.0"

# Copy the workspace (kernel, frontier, scripts, tests, evidence, config).
COPY core/ ./core/
COPY scripts/ ./scripts/
COPY 4R2-MASTER-DELIVERY/ ./4R2-MASTER-DELIVERY/
COPY evidence/ ./evidence/
COPY pyproject.toml self_test.py ./

# Make kernel + frontier importable and default to the self-test.
ENV PYTHONPATH=/app/core:/app/scripts:/app/antigravity_wings
ENTRYPOINT ["python", "self_test.py"]
