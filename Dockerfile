FROM ubuntu:20.04

ENV SOURCES=/usr/project

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    cmake \
    make \
    python3 \
    python3-pip \
    wget

# install arm-none-eabi toolchain for big endian targets.
RUN wget -O gcc-arm-none-eabi.tar.bz2 https://github.com/paoloteti/armeb-none-eabi-gcc-buildpatch/releases/download/v8-2019-q3-update/gcc-armeb-none-eabi-8-2019-q3-update-linux.tar.bz2 && \
    mkdir /usr/local/bin/armeb-none-eabi-gcc && \
    tar xf gcc-arm-none-eabi.tar.bz2 --strip-components=1 -C /usr/local/bin/armeb-none-eabi-gcc && \
    rm gcc-arm-none-eabi.tar.bz2

# install arm-none-eabi toolchain for little endian targets.
RUN wget -O gcc-arm-none-eabi.tar.bz2 https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2019q3/RC1.1/gcc-arm-none-eabi-8-2019-q3-update-linux.tar.bz2?revision=c34d758a-be0c-476e-a2de-af8c6e16a8a2?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,8-2019-q3-update && \
    mkdir /usr/local/bin/armel-none-eabi-gcc && \
    tar xf gcc-arm-none-eabi.tar.bz2 --strip-components=1 -C /usr/local/bin/armel-none-eabi-gcc && \
    rm gcc-arm-none-eabi.tar.bz2

COPY requirements.txt requirements.txt
COPY requirements-test.txt requirements-test.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade build && \
    python3 -m pip install -r requirements.txt && \
    python3 -m pip install -r requirements-test.txt

WORKDIR $SOURCES
VOLUME ["$SOURCES"]
