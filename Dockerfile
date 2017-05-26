FROM ubuntu:latest

MAINTAINER Sebastian Estenssoro

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
  apt-utils \
  sudo \
  python2.7 \
  python-pip \
  virtualenv \
  wget \
  python-tk \
  sqlite3 \
  libsqlite3-dev \
  python-scipy \
  zip \
  unzip

RUN useradd -m docker && echo "docker:docker" | chpasswd
RUN adduser docker sudo

RUN virtualenv /home/docker/venv
WORKDIR /home/docker
ADD ./requirements.txt /home/docker/
RUN /bin/bash -c "source venv/bin/activate && pip install --upgrade pip"
RUN /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"
RUN echo "source venv/bin/activate" >>.bashrc
USER docker
ENTRYPOINT /bin/bash -c "source venv/bin/activate && cd tendril_exercise && ./start.sh"
