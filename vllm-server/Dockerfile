FROM python:3.11-slim

# System dependencies (curl needed for healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Expose vLLM server port
EXPOSE 8001

# Healthcheck uses vLLM's /v1/models endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8001/v1/models || exit 1

# Run vLLM server (use MODEL_NAME env to control model)
# Example: MODEL_NAME=meta-llama/Llama-2-7b-chat-hf
ENV MODEL_NAME=facebook/opt-1.3b
CMD ["vllm", "serve", "--host", "0.0.0.0", "--port", "8001", "${MODEL_NAME}"]
