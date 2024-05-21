#
FROM python:3.9

#
WORKDIR /code

#
COPY ./back/ECM_system/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./back/ECM_system /code/app

EXPOSE 8000

#
CMD ["uvicorn", "app.main:app",  "--port", "8000"]