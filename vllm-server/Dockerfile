FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "vllm[all]" huggingface_hub

# Expose vLLM port
EXPOSE 8000

# Healthcheck for Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/v1/models || exit 1

# Hugging Face cache path (mount volume here on Railway)
ENV HF_HOME=/root/.cache/huggingface
ENV MODEL_NAME=openai/gpt-oss-20b
ENV VLLM_DEVICE=cpu

# Run vLLM serve with GPT-OSS 20B
CMD ["sh", "-c", "vllm serve $MODEL_NAME --host 0.0.0.0 --port 8000 --device cpu"]
