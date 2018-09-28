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
      postgresql-client \
      gettext && \
    apt-get clean

# Install requirements file
ADD requirements.txt /
RUN pip install -r requirements.txt

# Make current directory available as "Misago" within docker
ADD . /misago
WORKDIR /misago

# Expose port 80 from Docker
EXPOSE 80

# Call entrypoint script to setup 
CMD ["uwsgi" "--ini uwsgi.ini"]
