FROM python:3.7.6
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt