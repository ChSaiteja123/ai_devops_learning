.PHONY: help build up down logs shell test migrate makemigrations collectstatic lint format

help:
	@echo "Available commands:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start all services"
	@echo "  down           - Stop all services"
	@echo "  logs           - Follow service logs"
	@echo "  shell          - Open Django shell"
	@echo "  test           - Run tests"
	@echo "  migrate        - Run database migrations"
	@echo "  makemigrations - Create new migrations"
	@echo "  collectstatic  - Collect static files"
	@echo "  lint           - Run linter"
	@echo "  format         - Format code"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

test:
	docker-compose exec web python manage.py test

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

lint:
	flake8 .

format:
	black .
	isort .
