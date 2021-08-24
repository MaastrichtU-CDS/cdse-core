# CDSE - Core
A backend application that allows you to run prediction models.


##Getting started
To get started with CDSE run the following commands (if possible in a virtual environment):
- pipenv install
- pipenv run python manage.py migrate
- pipenv run python manage.py createsuperuser (and follow the instructions)
- set the minimal env settings:
    - DJANGO_ALLOWED_HOSTS=localhost;
    - INVOCATION_HOST=192.168.3.42;
    - INVOCATION_PORT=8000
- pipenv run python manage.py runserver 0.0.0.0:8000

Now you have started the application in local development mode.
This mode uses only the local SQL-lite database to start. This mode uses no external authentication mechanism like 
Keycloak. Of course this is not suitable for production. This mode can be used for local testing and development.
In order to run prediction models you need Docker running and configure an active FHIR-endpoint for use.

Please keep in mind that the docker containers need to know the ip of the host (CDSE itself) and be able to reach them.
To make this accessible, specify you local network ip + port in environment variables and add the suffix 
"0.0.0.0:8000" to the runserver command. 0.0.0.0 will allow connections from any local IP.

##Compatibility
CDSE-core is compatible and tested with the following versions:
- postgresSQL 12.3
- Python 3.8.10
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
To run end-to-end testing, you need to run: 
- docker-compose -f docker-compose.end-to-end-testing.yml up 
  
This will start a selenium hub and firfox docker container. After that check the script in end-to-end-test/mainflow.
py and point it to you local IP. after that run the script with: 

  - pipenv run python end-to-end-test/mainflow.py

If you go to http://<your-ip>:4444 you can see all the active selenium sessions.
Please check the selenium script before running. It requires a certain application state like configured datasource 
and available prediction model te pass. Please edit accordingly to your own setup.

##Linting
To provide a check for PEP8 compliance please run
- pipenv run black .

This will reformat your code conform PEP8 styleguide.

#Running in production mode
The most easy way to get started in production mode, is to run it in docker containers.
First set the environment variables like the provided .env files.
You will see there are some variables you cannot fill yet. 
These will become available after you run the script and configured keycloak.

The project provides a docker-compose file. To use it, install docker-compose and run the command:
- docker-compose up

This will start:
- Postgres database
- Nginx
- Keycloak

It will run migrations and create the needed groups within the django application.
The only thing left is configuration of keycloak. This you will find in the section below.
After you configured keycloak please fill in the right variables and restart the CDSE-core container.
Now the application is running in production mode and will use the external services accordingly.


#Configure Keycloak

For instructions how to set up the system please follow. 
[intro to keycloak](https://www.youtube.com/watch?v=duawSV69LDI)

Steps take for connection with CDSE:
- Create a new realm
- Add a new client
  - Set jwt key to rs256
  - set access type to confidential
  - get client_secret from Credentials tab
- In client-scope configure roles to be include in token scope
- Set roles to be included in token
    - Under realm roles enable: "add to ID token" and "Add to userinfo"
  
- Create groups and roles with the following names
    - super_admin, it_administrator, mdr_regulator,	medical_professional
  
- Add the role to the corresponding group
- Create user with complete details and assign a group
- Add right keys to env variable
  - Point to the right url
  - Set client_secret

