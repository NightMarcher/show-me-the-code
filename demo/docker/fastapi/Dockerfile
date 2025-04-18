FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY ./app ./app

EXPOSE 80

ENTRYPOINT ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:80", "--workers", "4"]

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost/health || exit 1
