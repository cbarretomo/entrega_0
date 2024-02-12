FROM alpine:3.10

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
CMD ["sh", "-c", "cd flaskr && python3 -m flask run --host=0.0.0.0"]







