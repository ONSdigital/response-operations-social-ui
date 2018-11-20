FROM python:3.6-slim

WORKDIR /app
COPY . /app
EXPOSE 8086
RUN apt-get update -y && apt-get install -y python-pip
RUN pip3 install pipenv && pipenv install --deploy --system

ENTRYPOINT ["python3"]
CMD ["run.py"]