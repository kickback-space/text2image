# text2image

This Service API will be built using flask, the initial design is to create an API service that utilizes Koala API text to image library and use it and send the appropriate JSON response to an image 1024 X 1024 resolution

## Proposed API Spec

- Request
    - text: string

- Response
  - image: binary?? 1024 X 1024


## Nice to have
- Test the API and make sure the response is as expected
- Create a CI/CD pipeline to improve the overall feature to product workflow

Other decisions
- Will it be deployed as a serverless cloud function?
- Are there any additional requirements?

## Usage
- Clean Up Resources
  ````
  make clean
  ````
- Build the image
  ```
  make build
  ```
- R