FROM python:alpine

WORKDIR /app

RUN mkdir endpoints

COPY ./requirements.txt ./
COPY ./*.py ./
COPY ./endpoints/*.py ./endpoints/

RUN pip install -r requirements.txt

CMD python3 -m uvicorn server:app --host 0.0.0.0 --port 8080