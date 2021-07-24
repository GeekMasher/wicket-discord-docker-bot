FROM python:3.9

WORKDIR /app

COPY . /app

RUN python3 -m pip install pipenv && python3 -m pipenv install --system

CMD [ "python3", "-m", "wicket" ]
