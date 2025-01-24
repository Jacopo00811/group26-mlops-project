# Change from latest to a specific version if your requirements.txt
FROM python:3.11-slim AS base

EXPOSE 8080

WORKDIR /app

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY src src/
COPY requirements_backend.txt requirements_backend.txt
COPY README.md README.md
COPY models/ models/
COPY pyproject.toml pyproject.toml

RUN pip install -r requirements_backend.txt --no-cache-dir --verbose
RUN pip install . --no-deps --no-cache-dir --verbose
RUN pip install --no-cache-dir -e .

CMD exec python src/danish_to_english_llm/api.py
#ENTRYPOINT ["uvicorn", "src/danish_to_english_llm/api:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
