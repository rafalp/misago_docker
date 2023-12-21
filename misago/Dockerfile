FROM python:3.12

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1
ENV MISAGO_PLUGINS "/misago/plugins"

# Install dependencies in one single command/layer
RUN apt-get update && \
    apt-get install -y --allow-unauthenticated \
      vim \
      libffi-dev \
      libssl-dev \
      libjpeg-dev \
      libopenjp2-7-dev \
      locales \
      cron \
      postgresql-client-15 \
      gettext && \
    apt-get clean

# Make current directory available as "Misago" within docker
ADD . /misago
WORKDIR /misago

# Install requirements files
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Bootstrap plugins
RUN ./.run bootstrap_plugins

# Expose port 3031 from Docker
EXPOSE 3031

# Call entrypoint script to setup 
CMD ["uwsgi", "--ini", "uwsgi.ini"]