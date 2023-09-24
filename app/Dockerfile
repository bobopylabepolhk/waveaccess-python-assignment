FROM python:3.11.5-alpine3.17

WORKDIR /code

RUN pip install poetry==1.6.1

COPY ./pyproject.toml ./poetry.lock* /code/
RUN poetry config virtualenvs.create false
RUN poetry install --no-cache --without test

COPY /src /code/

CMD uvicorn main:app --reload --host 0.0.0.0 --port ${FASTAPI_PORT}
