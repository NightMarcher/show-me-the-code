FROM python:3.12.9-slim-bookworm

# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

EXPOSE 80

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple jupyterlab

WORKDIR /app

COPY lab.ipynb /app

CMD jupyter lab --ip=0.0.0.0 --port=80 --no-browser --allow-root --NotebookApp.token=
# docker run -dit -p 8080:80 --name jpy -v /home/bryan/data:/lab/data jpy:dev
