FROM public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.1

WORKDIR /app

# remove the existing entrypoint
ENTRYPOINT []

# expose port
EXPOSE 8000

ENV MODEL_NAME=openai/gpt-oss-20b
ENV HF_HOME=/root/.cache/huggingface
ENV VLLM_CPU_KVCACHE_SPACE=40
ENV VLLM_CPU_OMP_THREADS_BIND=auto
ENV VLLM_LOGGING_LEVEL=INFO

# default command uses the vllm CLI directly
CMD ["sh", "-c", "vllm serve $MODEL_NAME --host 0.0.0.0 --port 8000 --dtype bfloat16"]
