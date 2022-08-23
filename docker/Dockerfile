FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y vim tmux git cmake wget clang
RUN apt install -y libgl1-mesa-dev libx11-dev libxrandr-dev libxi-dev mesa-utils libglu1-mesa-dev libpython3.8-dev python3-pip libopenmpi-dev
RUN git clone https://github.com/wakewakame/DeepMimic.git
WORKDIR /root/DeepMimic/DeepMimicCore
RUN ./build.sh

