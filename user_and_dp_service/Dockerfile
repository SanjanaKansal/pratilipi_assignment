FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y netcat
RUN mkdir /user_and_dp_service
WORKDIR /user_and_dp_service
ADD . /user_and_dp_service/
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
