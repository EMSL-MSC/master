FROM gitlab.emsl.pnl.gov:4567/msc_ops/build/kitchen-kubernetes-images/yarm9
LABEL org.opencontainers.image.authors="evan.felix@pnl.gov"

RUN yum install -y postgresql-server python3-ply python3-pip gcc python3-devel libffi-devel openssl-devel postgresql-devel python3-psycopg2
RUN pip3 install --upgrade pip
RUN pip3 install service_identity
RUN pip3 install Twisted
RUN pip3 install python-hostlist
# fix for bad interpeter
RUN pip3 install setuptools\<76

COPY . /app

RUN cd /app && python3 setup.py install --root=/

CMD master
