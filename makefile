.PHONY: build
build:
	docker build -t text2image .

.PHONY: run
run:
	docker run -p 5000:5000 text2image
