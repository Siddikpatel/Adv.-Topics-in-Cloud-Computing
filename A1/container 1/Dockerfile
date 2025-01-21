FROM python:3.10-slim

WORKDIR /usr/src/app

COPY container1.py /usr/src/app/container1.py

RUN pip install flask requests

EXPOSE 6000

CMD [ "python", "container1.py" ]