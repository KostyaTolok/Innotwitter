FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /core
WORKDIR /core

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

EXPOSE 5000

COPY . ./