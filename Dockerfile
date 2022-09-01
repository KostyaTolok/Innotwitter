FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /core

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

EXPOSE 5000

COPY . ./

RUN pip install pipenv

RUN pipenv install --deploy --system