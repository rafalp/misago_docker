# 1.0 (2023-06-10)

- Upgraded PostgreSQL service to 15.3.
- Renamed PostgreSQL service from `postgres` to `postgres-15`.
- Upgraded Redis service to 6.2.
- Renamed Redis service from `redis` to `redis-6`.
- Renamed `misago-celery` service to `celery-worker`.
- Renamed `misago-database` volume to `misago-postgres-15`
- Renamed `misago-redis` volume to `misago-redis-6`
- Removed `postgres.env` dependency.
- Removed `postgres` wizard step.


# 0.2 (2023-06-10)

- Added support for both `docker-compose` and `docker compose`.
- Added `majorupgrade` that updates `misago-docker` setup to v1.0


# 0.1 (2023-05-30)

- Moved backup logic inside the `misago` container (#98).
- Added `resetcron` command to `./appctl`.