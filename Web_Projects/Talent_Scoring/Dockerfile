FROM python:3.9

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code

# Gettext
RUN apt-get update && apt-get install -y gettext libgettextpo-dev \
  locales \
  locales-all \
  python3.9-dev

# Copy in your requirements file
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN pip install virtualenvwrapper
RUN python3 -m venv /venv
RUN /venv/bin/pip install -U pip
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
ADD . ${APP_ROOT}
COPY mime.types /etc/mime.types

# uWSGI will listen on this port
EXPOSE 8000

# Start uWSGI
#CMD [ "/venv/bin/uwsgi", "--ini", "/code/uwsgi.ini"]
#CMD [ "/venv/bin/daphne", "-b", "0.0.0.0", "-p", "8030", "dr_agro.asgi:application"]
CMD [ "/venv/bin/uwsgi", "--ini", "/code/uwsgi.ini"]
