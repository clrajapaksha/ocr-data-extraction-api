# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /code

ENV PORT=8000

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN --mount=type=secret,id=api_key,env=API_KEY
RUN --mount=type=secret,id=azure_storage_account,env=AZURE_STORAGE_ACCOUNT
RUN --mount=type=secret,id=azure_storage_account_key,env=AZURE_STORAGE_ACCOUNT_KEY
RUN --mount=type=secret,id=azure_storage_connection_string,env=AZURE_STORAGE_CONNECTION_STRING
RUN --mount=type=secret,id=container_name,env=CONTAINER_NAME

COPY ./ /code/

EXPOSE 8000

CMD ["gunicorn", "main:app"]