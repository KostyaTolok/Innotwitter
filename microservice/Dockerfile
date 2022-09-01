FROM python:3.9

WORKDIR /microservice

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 3000

COPY . ./

RUN pip install pipenv

RUN pipenv install --deploy --system