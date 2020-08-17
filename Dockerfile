FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN pip install --user -r requirements.txt
EXPOSE 8080
CMD [ "python", "manage.py", "runserver", "8080" ]
