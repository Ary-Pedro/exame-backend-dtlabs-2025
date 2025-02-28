run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

venv:
	python -m venv venv && source venv/bin/activate

install:
	pip install -r requirements.txt

test:
	pytest -v

docker-up:
	docker-compose up -d --build
