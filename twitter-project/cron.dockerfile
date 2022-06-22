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


# RUN apt-get update && apt-get install -y cron && which cron && \
    # rm -rf /etc/cron.*/*

# RUN apt-get update && apt-get install -y cron
RUN rm -rf /etc/cron.*/*
COPY ./cron/crontab /etc/crontab
RUN touch /var/log/cron.log && chmod 0644 /etc/crontab && crontab /etc/crontab
RUN service cron restart


COPY ./cron/entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]

CMD ["cron","-f", "-l", "2"]

