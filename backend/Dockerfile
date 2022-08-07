FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN pip install -U setuptools

RUN pip install ez_setup

RUN pip3 install -r requirements.txt 

COPY foodgram/ /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]