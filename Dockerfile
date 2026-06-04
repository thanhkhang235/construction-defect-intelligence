FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV HF_HOME=/app/.cache/huggingface
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/app/streamlit_app.py"]
