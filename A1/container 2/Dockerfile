FROM python:3.10-slim

WORKDIR /usr/src/app

COPY container2.py /usr/src/app/container2.py

RUN pip install flask

EXPOSE 5100

CMD [ "python", "container2.py" ]