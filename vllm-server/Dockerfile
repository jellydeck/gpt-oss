FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
# Force CPU build of PyTorch + vLLM
RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir vllm[all] --extra-index-url https://download.pytorch.org/whl/cpu

# Expose default vLLM port
EXPOSE 8000

# Healthcheck uses vLLM's built-in OpenAI endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/v1/models || exit 1

# Default envs (Railway will override at runtime if provided)
ENV MODEL_NAME=facebook/opt-1.3b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_LOGGING_LEVEL=INFO

# Run vLLM serve with model from env
CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8000 --device cpu $MODEL_NAME"]
