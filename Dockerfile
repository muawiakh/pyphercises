FROM alpine:latest
ARG APPVERSION=v1.0.0
LABEL maintainer "amuawiakhan@gmail.com"
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apk --update add python3 git python3-dev libstdc++ \
    libffi-dev build-base \
    && git clone https://github.com/muawiakh/pyphercises.git

WORKDIR /usr/src/app/pyphercises

RUN git checkout tags/${APPVERSION} -b ${APPVERSION} \
    && python3 setup.py install

# When developing with Python in a docker container, we are using PYTHONBUFFERED
# to force stdin, stdout and stderr to be totally unbuffered and to capture logs/outputs
ENV PYTHONUNBUFFERED 0

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["/usr/src/app/pyphercises/pyphercises/app.py"]