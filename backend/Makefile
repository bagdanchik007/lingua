.PHONY: install run seed test docker-up docker-down migrate

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

seed:
	@echo "Call POST /api/v1/admin/seed with a valid token"

test:
	pytest -q

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

migrate:
	alembic upgrade head
