FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN python -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN ["chmod", "+x", "./docker-entrypoint.sh"]

EXPOSE 8000

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]