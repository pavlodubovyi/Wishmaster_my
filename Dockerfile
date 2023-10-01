FROM python:3.11.3-slim-buster

WORKDIR /wishmaster_docker

COPY . .

EXPOSE 5000

CMD ["python3", "wishmaster.py"]