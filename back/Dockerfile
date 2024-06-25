FROM python:3.10


WORKDIR /code


COPY ./back/requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libpq-dev build-essential


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./back /code/

CMD ["uvicorn", "main:app",  "--reload"]