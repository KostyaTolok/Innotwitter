FROM python:3.9

RUN mkdir /microservice
WORKDIR /microservice

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY . ./

EXPOSE 3000