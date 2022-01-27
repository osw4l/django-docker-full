FROM ubuntu:20.04

ADD requirements.txt /app/requirements.txt

WORKDIR /app/

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:ubuntugis/ppa -y
RUN apt-get update -y

RUN apt-get install -y wget build-essential libpq-dev \
	python3-dev libffi-dev python3-pip wget \
	pkg-config libpng-dev

RUN apt-get install -y binutils libproj-dev gdal-bin

RUN apt-get install -y python3-setuptools python3-wheel python3-cffi libcairo2 \
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    libffi-dev shared-mime-info

RUN apt-get install -y libpq-dev gdal-bin libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install GDAL
RUN pip3 install --upgrade setuptools

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN export LC_ALL=es_ES.UTF-8

RUN adduser --disabled-password --gecos '' app
RUN chown -R app:app /app && chmod -R 755 /app

ENV HOME /home/app
USER app