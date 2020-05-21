# recipe-app-api
I have built this API because I want an easy way to store all the recipes I'm currently learning.

To build Dockerfile:
- `docker build .`

To build Dockerfile using docker-compose:
- `docker-compose build`

To run application:
- `docker-compose run <service_name> sh -c <django_or_python_command>"`

To create Django App:
- `docker-compose run app sh -c "django-admin.py startproject <app_name> ."`