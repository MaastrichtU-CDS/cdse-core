# CDSE - Core
A backend application that allows you to run prediction models in a generic way.


##Getting started
To get started with CDSE run the following commands (if possible in a virtual environment):
- pipenv install
- pipenv run python manage.py migrate
- pipenv run python manage.py createsuperuser (and follow the instructions)
- pipenv run python manage.py runserver

Now you have started the application in local development mode.
This mode uses only the local SQL-lite database to start. This mode uses no external authentication mechanism like 
Keycloak. Of course this is not suitable for production. This mode can be used for local testing and development.
In order to run prediction models and connect data-sources you need Docker running and have access to a active 
FHIR-endpoint.

##Compatibility
CDSE-core is compatible and tested with the following versions:
- postgresSQL 12.3
- Python 3.6
- Django 3.2.x
- Keycloak 13.0
- Docker CE 2.10
- FHIR 4.x
- Nginx 1.19.x

##Unit and Integration testing
These tests have been made with django's test suite. You can run them with the command:
- pipenv run python manage.py test

This will start unit and integration tests and provide a report in result.xml.

##End-To-End testing
--TODO--

##Linting
To provide a check for PEP8 compliance please run
- pipenv run black .

This will clean reformat your code conform PEP8 styleguide.

#Running in production mode
The most easy way to get started in production mode, is to run it in docker containers.
First set the environment variables like the provided .env files.
You will see there are some variables you cannot fill jet. These will become available after we run the script and 
configured keycloak.

The project provides a docker-compose file. To use it, install docker compose and run the command:
- docker-compose up

This will start:
- Postgres database
- Nginx
- Keycloak

It will run migrations and create the needed groups within the django application.
The only thing left is configuration of keycloak. This you will find in the section below.
After you configured keycloak please fill in the right variables and restart the CDSE-core container.
Now the application is running in production mode and will use the external services.


#Configure Keycloak

For detailed instructions how to set up the system please follow. [intro to keycloak](https://www.youtube.
com/watch?
v=duawSV69LDI)

- Create a new realm
- Add a new client
- Set jwt key to rs256
- Set on confidential
- set roles to be incuded in token
- Create user with complete details
- Create roles
- Add right keys to env variable

