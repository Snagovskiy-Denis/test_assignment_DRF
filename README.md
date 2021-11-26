
# Introduction

This project realizes [that](https://docs.google.com/document/d/1f3ZGfaYil9Xd8er1-nQazC6jA2wTzzevOGGDqeyfMXo) test assignment

Main Goal: to show that I can implement basic REST API service

Assignment' tasks and technical requirements are listed by link above


# How to run

## Project outside container

1. Create and activate virtual environment, install requirements

```bash
python -m venv ./venv && source ./venv/bin/activate
pip install -r requirements.txt
```

2. Run database:

```bash
docker-compose up -d
```

3. Run Django test-server:

```bash
./manage.py runserver
```


## All infrastructure inside containers

Run following commands one by one from project root directory:

```bash
docker-compose -f docker-compose-project-in-container.yml up -d
docker exec -it test_assignment_drf-app-1 /bin/bash
./manage.py migrate
./manage.py test cityshops/tests/
```
