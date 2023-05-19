FROM python:3.9

RUN mkdir /task

WORKDIR /task

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --system --deploy

COPY app /task/app

EXPOSE 8000
