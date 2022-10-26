FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
