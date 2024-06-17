FROM tiangolo/uvicorn-gunicorn:python3.11

RUN pip3 install pipfile-requirements==0.3.0

COPY ./app /sample_api/app

WORKDIR /sample_api

ARG GIT_TOKEN

# Point to the location of our API for uvicorn
ENV APP_MODULE="app.main:app"

COPY Pipfile.lock /sample_api/
RUN pipfile2req ./Pipfile.lock -s > requirements.txt
RUN pip3 install -r requirements.txt
