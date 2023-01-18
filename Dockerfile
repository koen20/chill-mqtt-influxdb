FROM python:3.10-slim

COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt
WORKDIR /src
COPY ./ /src
CMD [ "python", "./app.py"]
