FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install -r requirements/production.txt

CMD ["gunicorn", "--bind", ":8000", "--chdir", "backend", "arkandha.wsgi:application"]
