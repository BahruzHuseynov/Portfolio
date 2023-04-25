# URL Status Checker
In this project, we will be using asynchronous requests to get the status codes of the urls defined by each user. 

# Used Technologies
- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Asyncio](https://docs.python.org/3/library/asyncio.html)


## Setup
In order to get ready to run the code, we need to install the required dependencies.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## How to run the application

Simple enough:

```bash
$ docker-compose -f _development/docker-compose.yml up --build -d
```

You can run the code in 2 modes:
1. Normal mode:
    ```python3 manage.py runserver```
2. async mode:
    ```uvicorn --reload url_status_checker.asgi:application```

`uvicorn` is a single-threaded server that can be used to run Django application as an ASGI instead of WSGI. It is used to send asynchronous requests to the defined urls.

## Project dependencies

The project dependency management is based on `pip`. All the required packages are stored in the `requirements.txt` file.
