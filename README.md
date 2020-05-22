[![Build Status](https://travis-ci.org/oyekanmiayo/recipe-app-api.svg?branch=master)](https://travis-ci.org/oyekanmiayo/recipe-app-api)

# recipe-app-api
I have built this API because I want an easy way to store all the recipes I'm currently learning.

To build Dockerfile:
- `docker build .`

To build Dockerfile using docker-compose:
- `docker-compose build`

To run application:
- `docker-compose run <service_name> sh -c <django_or_python_command>"`

To create Django App:
- `docker-compose run app sh -c "django-admin.py startproject <project_name> ."`
- `docker-compose run app sh -c "python manage.py startapp <app_name>"`

To run tests and linting:
- `docker-compose run app sh -c "python manage.py test && flake8"`

Remember:
- Anytime a requirement is added, `docker-compose build` must be executed

To make migrations:
- `docker-compose run app sh -c "python manage.py makemigrations <app_name>"`
