FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Install dependencies in one single command/layer
RUN apt-get update && \
    apt-get install -y \
      vim \
      libffi-dev \
      libssl-dev \
      libjpeg-dev \
      libopenjp2-7-dev \
      locales \
      cron \
      postgresql-client \
      gettext && \
    apt-get clean

# Install requirements file
ADD requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make current directory available as "Misago" within docker
ADD . /misago
WORKDIR /misago

# Expose port 80 from Docker
EXPOSE 80

# Call entrypoint script to setup 
CMD ["uwsgi", "--ini", "uwsgi.ini"]
