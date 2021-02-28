FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# RUN apk add --no-cache  build-base libffi-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run","--host=0.0.0.0"]