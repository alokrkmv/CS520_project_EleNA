# Pulling the alpine image
FROM python:3.8-slim



COPY ./docker_requirements.txt /app/requirements.txt

WORKDIR /app


RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD ["src/main/server/server.py" ]

