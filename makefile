.PHONY: build
build:
	docker build -t text2image .

.PHONY: run
run:
	docker run --name text_2_image --gpus all -d -p 5000:5000 text2image

.PHONY: logs
logs:
	docker logs -f text_2_image

.PHONY: remove
remove:
	docker stop $$(docker ps -a --filter ancestor=text2image -q) && docker rm $$(docker ps -a --filter ancestor=text2image -q)
