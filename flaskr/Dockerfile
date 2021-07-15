FROM python:3.7

WORKDIR usr/src/flaskr

COPY Pipfile* .
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system
RUN pipenv install importlib-metadata

COPY . .
RUN chmod +x ./boot.sh

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
