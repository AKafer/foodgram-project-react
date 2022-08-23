FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 

COPY foodgram/ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]