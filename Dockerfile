FROM alpine:latest
ARG APP_BRANCH=basic-weather-app
ARG APP_ID
LABEL maintainer "amuawiakhan@gmail.com"
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN apk --update add python3 git python3-dev libstdc++ \
    libffi-dev build-base

RUN git checkout ${APP_VERSION} \
    && pip3 install .

# When developing with Python in a docker container, we are using PYTHONBUFFERED
# to force stdin, stdout and stderr to be totally unbuffered and to capture logs/outputs
ENV PYTHONUNBUFFERED 0
ENV WEATHER_APP_ID ${APP_ID}

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["/usr/src/app/run.py"]
