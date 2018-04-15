FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

# Install dependencies in one single command/layer
RUN apt-get update && \
    apt-get install -y \
      vim \
      libffi-dev \
      libssl-dev \
      sqlite3 \
      libjpeg-dev \
      libopenjpeg-dev \
      locales \
      cron \
      postgresql-client
      gettext && \
    apt-get clean

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD . /misago
WORKDIR /misago

EXPOSE 80

CMD ./entrypoint.sh
