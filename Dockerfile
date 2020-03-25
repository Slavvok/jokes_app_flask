FROM python:3
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /app/
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip-tools && pip-sync requirements.txt
RUN flask db init && flask db migrate -m "" && flask db upgrade
