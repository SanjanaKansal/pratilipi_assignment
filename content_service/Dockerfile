FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y netcat
RUN mkdir /content_service
WORKDIR /content_service
ADD . /content_service/
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["sh", "docker-entrypoint.sh"]