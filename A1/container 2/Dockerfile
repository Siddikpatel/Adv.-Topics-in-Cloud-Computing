FROM python:3

WORKDIR /usr/src/app

COPY container2.py /usr/src/app/container2.py

RUN pip install flask

EXPOSE 7000

CMD [ "python", "container2.py" ]