set -e

docker compose build
docker compose stop
docker compose up -d

docker compose logs -f
