FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import vllm.server.openai_serving_chat"

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

EXPOSE 8001
CMD ["python", "server.py"]
