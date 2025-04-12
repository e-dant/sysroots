FROM debian
COPY sysroots /etc/sysroots
RUN apt-get update \
 && apt-get install -y \
   build-essential \
   cmake \
   meson \
   git \
   pkg-config \
   python3 \
   python3-pip \
   wget \
   g++-aarch64-linux-gnu \
   g++-arm-linux-gnueabi \
   g++-arm-linux-gnueabihf \
   g++-x86-64-linux-gnu \
   g++-x86-64-linux-gnux32 \
   && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /tmp/musltoolchains \
 && cd /tmp/musltoolchains \
 && wget https://musl.cc/aarch64-linux-musl-cross.tgz \
 && wget https://musl.cc/aarch64_be-linux-musl-cross.tgz \
 && wget https://musl.cc/arm-linux-musleabihf-cross.tgz \
 && wget https://musl.cc/armv7l-linux-musleabihf-cross.tgz \
 && wget https://musl.cc/x86_64-linux-musl-cross.tgz \
 && wget https://musl.cc/x86_64-linux-muslx32-cross.tgz \
 && mkdir -p /etc/musltoolchains \
 && cd /etc/musltoolchains \
 && tar xf /tmp/musltoolchains/aarch64-linux-musl-cross.tgz \
 && tar xf /tmp/musltoolchains/aarch64_be-linux-musl-cross.tgz \
 && tar xf /tmp/musltoolchains/arm-linux-musleabihf-cross.tgz \
 && tar xf /tmp/musltoolchains/armv7l-linux-musleabihf-cross.tgz \
 && tar xf /tmp/musltoolchains/x86_64-linux-musl-cross.tgz \
 && tar xf /tmp/musltoolchains/x86_64-linux-muslx32-cross.tgz \
 && rm -rf /tmp/musltoolchains
ENV PATH=$PATH:/etc/musltoolchains/aarch64-linux-musl-cross/bin:/etc/musltoolchains/aarch64_be-linux-musl-cross/bin:/etc/musltoolchains/arm-linux-musleabihf-cross/bin:/etc/musltoolchains/armv7l-linux-musleabihf-cross/bin:/etc/musltoolchains/x86_64-linux-musl-cross/bin:/etc/musltoolchains/x86_64-linux-muslx32-cross/bin
