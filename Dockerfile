FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN chown -R $USER: /code/

RUN pip install -r requirements.txt
#python manage.py migrate

COPY . /code/

#CMD ['python', 'manage.py', 'migrate']