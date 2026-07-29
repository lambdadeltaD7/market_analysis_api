FROM python:alpine

WORKDIR /app

COPY ./requirements.txt .
COPY ./funcs.py .
COPY ./main.py .

RUN pip install -r requirements.txt

CMD python3 -m uvicorn main:app  --host 0.0.0.0 --port 8080