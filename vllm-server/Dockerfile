FROM ubuntu:22.04

# install build & runtime deps
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      git build-essential gcc-12 g++-12 libtcmalloc-minimal4 libnuma-dev jq \
      libsm6 libxext6 libgl1 ca-certificates wget && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 10 \
      --slave /usr/bin/g++ g++ /usr/bin/g++-12 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install Python & pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3.11 python3.11-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# install CPU torch & supporting libs
RUN pip3 install --no-cache-dir \
    torch --extra-index-url https://download.pytorch.org/whl/cpu \
    torchvision --extra-index-url https://download.pytorch.org/whl/cpu \
    pyarrow

# clone & install vLLM CPU backend
RUN git clone https://github.com/vllm-project/vllm.git /vllm && \
    cd /vllm && \
    VLLM_TARGET_DEVICE=cpu python3 setup.py install && \
    cd /app && rm -rf /vllm

# expose & defaults
EXPOSE 8001
ENV MODEL_NAME=openai/gpt-oss-20b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_LOGGING_LEVEL=INFO

CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8001 --device cpu $MODEL_NAME"]
