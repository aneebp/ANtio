#this describe, how we build our django app,
# Dockerfile is a blueprint for creating Docker images

FROM python:3.12

#common python dockerfile commmand
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR / app

#. used as the workdir /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#COPY source(from our code) to dest(app)
COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]