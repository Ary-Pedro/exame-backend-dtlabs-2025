API_URL=http://127.0.0.1:8000/
SERVER_ULID=01JN4HCDW7ZF0TFMXWKRFV06GG

docker:
	docker compose up -d

start-server: 
	uvicorn app.main:app --reload

seed-db:
	python -m app.script.seed

run: docker start-server seed-db