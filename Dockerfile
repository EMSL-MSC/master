FROM centos:7
LABEL org.opencontainers.image.authors="evan.felix@pnl.gov"

RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum install -y postgresql-server python36-ply python36-pip gcc python36-devel libffi-devel openssl-devel postgresql-devel python36-psycopg2
RUN pip3 install --upgrade pip
RUN pip3 install service_identity
RUN pip3 install Twisted
RUN pip3 install python-hostlist

COPY . /app

RUN cd /app && python3 setup.py install --root=/


CMD master
