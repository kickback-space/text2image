# text2image

This Service API will be built using flask, the initial design is to create an API service that utilizes Koala API text to image library and use it and send the appropriate JSON response to an image 1024 X 1024 resolution

## Proposed API Spec

- Request
    - text: string

- Response
  - image: binary?? 1024 X 1024


## Build
```
docker build --pull -f Dockerfile -t text2image:latest .
```

## Run
```
docker-compose up
```
tip: to run in background
```
docker-compose up -d
```