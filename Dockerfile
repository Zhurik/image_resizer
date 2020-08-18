FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install --user -r requirements.txt
EXPOSE 8080
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]
