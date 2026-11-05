FROM python:3.10-slim
WORKDIR /app
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY api api
COPY models models
COPY scripts scripts
COPY data_manifest.json .
RUN python scripts/download_data.py
ENV PORT=8080
CMD ["sh", "-c", "exec python -m uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080} --no-access-log"]
