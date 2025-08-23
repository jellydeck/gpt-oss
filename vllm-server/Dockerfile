# Dockerfile
FROM python:3.11-slim

# install build tools and dependencies for vLLM CPU backend
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential git curl wget ca-certificates \
      gcc-12 g++-12 libtcmalloc-minimal4 libnuma-dev \
      libffmpeg-dev libsm6 libxext6 libgl1 jq lsof && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 --slave /usr/bin/g++ g++ /usr/bin/g++-12 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements
COPY requirements.txt .

# install Python deps
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# clone and build vLLM CPU backend
RUN git clone https://github.com/vllm-project/vllm.git /vllm_source && \
    cd /vllm_source && \
    VLLM_TARGET_DEVICE=cpu python setup.py install && \
    cd /app && rm -rf /vllm_source

# expose port and set env defaults
EXPOSE 8001
ENV MODEL_NAME=openai/gpt-oss-20b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_LOGGING_LEVEL=INFO

# launch vLLM server on CPU
CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8001 --device cpu $MODEL_NAME"]
