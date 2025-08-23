# Dockerfile
FROM public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:latest

WORKDIR /app

# expose vLLM server port
EXPOSE 8000

# default environment variables (override in Railway)
ENV MODEL_NAME=openai/gpt-oss-20b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_CPU_KVCACHE_SPACE=40
ENV VLLM_CPU_OMP_THREADS_BIND=auto
ENV VLLM_LOGGING_LEVEL=INFO

# serve on CPU
CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8000 --model $MODEL_NAME --device cpu --dtype=bfloat16"]
