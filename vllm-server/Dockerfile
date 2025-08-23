FROM python:3.11-slim

# System deps (only what we really need)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
# Force CPU build of PyTorch
RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu
# Install app requirements (includes vllm==0.10.1.1)
RUN pip install --no-cache-dir -r requirements.txt

# Expose default vLLM port
EXPOSE 8001

# Default envs (Railway can override at runtime)
ENV MODEL_NAME=facebook/opt-1.3b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_LOGGING_LEVEL=INFO

# Run vLLM serve with model from env in CPU mode
CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8001 --device cpu $MODEL_NAME"]
