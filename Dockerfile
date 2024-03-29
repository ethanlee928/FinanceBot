FROM python:3.11

ARG GROUP_ID
ARG USER_ID
ARG USERNAME

RUN getent group ${GROUP_ID} || addgroup --gid ${GROUP_ID} ${USERNAME} \
    && adduser --disabled-password --gecos "" --uid ${USER_ID} --gid ${GROUP_ID} ${USERNAME}\
    && passwd -d ${USERNAME}

RUN apt-get update
RUN pip3 install --upgrade pip && \
    pip3 install numpy paho-mqtt matplotlib mplfinance \
    pandas overrides polygon-api-client requests \
    slack_bolt slackclient

RUN apt-get install -y --no-install-recommends tzdata
RUN TZ=Asia/Hong_Kong \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

USER ${USERNAME}
