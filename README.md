[![Build Status](https://travis-ci.org/oyekanmiayo/recipe-app-api.svg?branch=master)](https://travis-ci.org/oyekanmiayo/recipe-app-api)

# recipe-app-api
I have built this API because I want an easy way to store all the recipes I'm currently learning.

To build Dockerfile:
- `docker build .`

To build Dockerfile using docker-compose:
- `docker-compose build`

To run application:
- `docker-compose run app sh -c "python manage.py runserver 0.0.0.0:8000"`
- `docker-compose up`

To Create Django Project:
- `docker-compose run app sh -c "django-admin.py startproject <project_name> ."`

To Create Django App
- `docker-compose run app sh -c "python manage.py startapp <app_name>"`

To Run Tests and Linting:
- `docker-compose run app sh -c "python manage.py test && flake8"`

To Make Migrations:
- `docker-compose run app sh -c "python manage.py makemigrations <app_name>"`

To Create Superuser:
- `docker-compose run app sh -c "python manage.py createsuperuser"`

Remember:
- Anytime a requirement is added, `docker-compose build` must be executed
- To ensure contains don't linger after any docker-compose command use --rm as an argument \
in the call like: `docker-compose run --rm app sh -c "<command>""`
