FROM public.ecr.aws/lambda/python:3.9
ENV AWS_DEFAULT_REGION ap-northeast-1

# install build libs
RUN yum groupinstall -y "Development Tools" \
    && yum install -y which openssl

RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install gzip

# install TA-Lib
WORKDIR /tmp
RUN wget --quiet http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O ta-lib-0.4.0-src.tar.gz && \
    tar -zxvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr/local/ && \
    make && \
    make check && \
    make install && \
    cd .. && \
    python3 -m pip install TA-Lib && \
    rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN cp -pa /usr/local/lib/libta_lib.so.0* /var/task/

RUN python3 -m pip install --upgrade TA-Lib --user --global-option='build_ext' --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib"

RUN python3 -m pip install numpy

COPY ./requirements.txt /opt/
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /opt/requirements.txt -t /var/task

WORKDIR /var/task
COPY handler.py .
# COPY slack.py .
# COPY twitter.py .

CMD [ "handler.lambdahandler" ]
