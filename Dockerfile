FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN python -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000:8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn" "core.wsgi"]