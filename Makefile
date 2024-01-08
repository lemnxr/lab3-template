run-compose:
	docker-compose up -d

down-compose:
	docker-compose down

delete-all:
	docker rmi postgres:16-alpine ; docker rmi reservation_service ; rm -rf reservation_data ; docker rmi payment_service ; rm -rf payment_data ; docker rmi loyalty_service ; rm -rf loyalty_data ; docker rmi gateway_service

run-tests:
	pytest -vs app/tests/person.py
