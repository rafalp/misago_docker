FROM python:3.7

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Install dependencies in one single command/layer
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >> /etc/apt/sources.list.d/pgdg.list' && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated \
      vim \
      libffi-dev \
      libssl-dev \
      libjpeg-dev \
      libopenjp2-7-dev \
      locales \
      cron \
      postgresql-client-10 \
      gettext && \
    apt-get clean

# Make current directory available as "Misago" within docker
ADD . /misago
WORKDIR /misago

# Install requirements files
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN [ -f requirements-plugins.txt ] && pip install -r requirements-plugins.txt || true

# Expose port 3031 from Docker
EXPOSE 3031

# Call entrypoint script to setup 
CMD ["uwsgi", "--ini", "uwsgi.ini"]
