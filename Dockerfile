FROM python:2.7
MAINTAINER Brent Payne <brent.payne@gmail.com>
RUN apt-get update
RUN apt-get -qqy install binutils libproj-dev gdal-bin
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt  # v2
ADD esdjhs /esdjhs
WORKDIR /esdjhs
EXPOSE 8000
# EXPOSE 9200
ENV PYTHONPATH .:/esdjhs
ENV DJANGO_SETTINGS_MODULE esdjhs.settings
CMD django-admin runserver 0.0.0.0:8000
