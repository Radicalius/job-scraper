FROM python:3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app

WORKDIR /app

CMD /bin/bash start.sh
