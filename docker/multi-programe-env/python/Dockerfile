FROM python as pydev
WORKDIR /data/

RUN apt-get update \
    && apt-get install -y git \
    && apt-get install -y net-tools \
    && apt-get install -y vim \
    && apt-get install -y inetutils-ping \
    && apt-get install -y telnet \
    && apt-get install -y net-tools 
