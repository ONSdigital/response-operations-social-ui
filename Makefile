build:
	pipenv install --dev

lint:
	pipenv run flake8 --exclude ./response_operations_social_ui/logger_config.py ./response_operations_social_ui ./tests
	pipenv check ./response_operations_social_ui ./tests

test: lint
	pipenv run python run_tests.py

start:
	pipenv run python run.py

docker: test
	docker build -t sdcplatform/response-operations-social-ui:latest .
