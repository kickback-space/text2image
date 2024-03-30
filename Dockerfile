FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Install the C compiler (GCC) in the Docker image
RUN apt-get update && apt-get install -y gcc

CMD ["gunicorn", "-b", "0.0.0.0", "app:app"]
