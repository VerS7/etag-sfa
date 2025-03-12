include .env

.PHONY: stop
stop:
	docker compose down

.PHONY: clean 
clean: stop
	-docker rm etag-backend
	-docker rm etag-frontend
	-docker rmi etag-backend-i
	-docker rmi etag-frontend-i

.PHONY: run
run:
	docker compose up -d

.PHONY: build-run
build-run: clean
	docker compose up --build -d
