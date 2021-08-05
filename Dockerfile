FROM public.ecr.aws/lambda/python:3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

# install build libs
RUN yum groupinstall -y "Development Tools" \
    && yum install -y which openssl

RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install gzip

RUN pip3 install --upgrade pip
# RUN pip3 install TA-Lib
# RUN python3 setup.py install


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
    python3 -m pip install --force-reinstall ta-lib && \
    rm -R ta-lib ta-lib-0.4.0-src.tar.gz

# RUN python3 -m pip install ta-lib --user --global-option='build_ext' --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib"

# RUN python3 -m pip install --upgrade ta-lib --user --global-option='build_ext' --global-option="-I/usr/local/include" --global-option="-L/etc/ld.so.conf"


# RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/lib:

RUN pip3 install numpy

RUN echo "include /usr/local/lib" >> /etc/ld.so.conf

COPY ./requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt -t /var/task

COPY handler.py /var/task/
# COPY init.py /tmp
# RUN python3 /tmp/init.py

CMD [ "handler.lambdahandler" ]
