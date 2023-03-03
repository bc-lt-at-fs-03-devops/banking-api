from python:3.11.2-slim-buster

WORKDIR /python-docker

COPY . /python-docker

RUN pip install -r requirements_api.txt

EXPOSE 9000

CMD [ "python", "bank_api/api.py"]