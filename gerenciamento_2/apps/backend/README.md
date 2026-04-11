Dentro de apps/backend:

1. crie um .env e configure usando o .env.example

2. suba os containers
docker compose up -d --build

3. popule o banco
docker compose exec app python src/scripts/seed.py

4. acesse:
  http://localhost:5000/apidocs/
