FROM python:3.9

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

COPY . /app

RUN python3 -m pip install pipenv && python3 -m pipenv install --system

CMD [ "python3", "-m", "wicket" ]
