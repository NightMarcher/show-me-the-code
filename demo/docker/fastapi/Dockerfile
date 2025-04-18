FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY gunicorn.conf.py .

COPY app app

ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=1s --retries=3 CMD curl --fail http://localhost/health || exit 1
