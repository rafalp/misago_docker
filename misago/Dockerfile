FROM python:3.11 as app-build

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" >> /etc/apt/sources.list.d/pgdg.list' && \
    apt-get update && \
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

ADD . /misago

RUN pip install --upgrade pip && pip install -r requirements.txt

# Build final (slim) image
FROM python:3.11-slim

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Copy build files from previous image
COPY --from=app-build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=app-build /usr/local/bin/ /usr/local/bin/

# Update apt and install postgresql-client
RUN apt-get update && apt-get install -y postgresql-client-15

# Re-add misago
ADD . /misago
WORKDIR /misago

# Expose port 3031 from Docker
EXPOSE 3031

# Call entrypoint script to setup 
CMD ["uwsgi", "--ini", "uwsgi.ini"]
