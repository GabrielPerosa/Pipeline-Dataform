FROM python:3.9

WORKDIR /app

ADD . /app

RUN pip install -r dataform/requirements.txt

ENV PORT=8080

EXPOSE 8080

CMD ["python", "regex-py/program/main.py"]
