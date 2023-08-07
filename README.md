# Menu

clone repository or download zip.

create an environment and install requirements.txt (optional).

create .env and .env.test file in parent folder and add

DATABASE_PORT=5432 POSTGRES_USER={POSTGRES_USER} POSTGRES_PASSWORD={POSTGRES_PASSWORD} POSTGRES_HOST={POSTGRES_HOST} POSTGRES_DB={POSTGRES_DB} POSTGRES_HOSTNAME=postgres REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

DATABASE_PORT=5432 POSTGRES_USER={POSTGRES_USER} POSTGRES_PASSWORD={POSTGRES_PASSWORD} POSTGRES_HOST={POSTGRES_HOST} POSTGRES_DB={POSTGRES_DB} POSTGRES_HOSTNAME=postgres REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

Run docker-compose -f docker-compose-app.yml up --build to start app.
Run docker-compose -f docker-compose-test.yml up --build to start test.
