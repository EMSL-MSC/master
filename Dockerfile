FROM centos:7
MAINTAINER evan.felix@pnl.gov

RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum install -y postgresql-server python-ply python-pip gcc python-devel PyGreSQL libffi-devel openssl-devel
RUN pip install --upgrade "pip < 21.0"
RUN pip install idna==2.10 cryptography==3.3.1
RUN pip install service_identity
RUN pip install Twisted
RUN pip install python-hostlist

COPY . /app

RUN cd /app && python setup.py install --root=/


CMD master
