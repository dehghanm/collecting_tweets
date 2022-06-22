FROM python:3.9.13
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Tehran
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


RUN                                                     \
       apt install tzdata                               \
    && apt-get update                                   \
    && apt install --no-install-recommends -y           \
            nano                                        \
            cron                                        \
    && pip install --upgrade pip                        \
    && mkdir -p /work

WORKDIR /work

COPY ./twitterAPI/ /work/

RUN pip install -r requirements.txt  

RUN pip install git+https://github.com/dehghanm/twint

