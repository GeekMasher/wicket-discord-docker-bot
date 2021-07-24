FROM python:3.9-slim-buster

LABEL Maintainer="GeekMasher"

RUN apt-get update -y

WORKDIR /app

COPY . /app

RUN python3 -m pip install pipenv && \
    python3 -m pipenv install --system

# Remove all unnecessary libraries and tools
RUN apt-get remove -y \
    dpkg-dev gcc make wget \
    libbluetooth-dev libbz2-dev libc6-dev libexpat1-dev libffi-dev libgdbm-dev \
    liblzma-dev libncursesw5-dev \libreadline-dev libsqlite3-dev libssl-dev \
    tk-dev uuid-dev xz-utils zlib1g-dev

RUN apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

CMD [ "python3", "-m", "wicket" ]
