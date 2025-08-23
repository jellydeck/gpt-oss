# Use the official vLLM image (replace tag with latest stable)
FROM vllm/vllm:latest

# Set working directory (optional)
WORKDIR /app

# Expose the default port for vLLM server
EXPOSE 8001

# Default environment variables; override MODEL_NAME when deploying or building
ENV MODEL_NAME=openai/gpt-oss-20b
ENV VLLM_LOGGING_LEVEL=INFO

# Entrypoint to run vLLM serve on CPU with model from env var
CMD ["sh", "-c", "vllm serve --host 0.0.0.0 --port 8001 --device cpu $MODEL_NAME"]
