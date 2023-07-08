FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
USER root
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y vim tmux git cmake wget clang
RUN apt install -y libgl1-mesa-dev libx11-dev libxrandr-dev libxi-dev mesa-utils libglu1-mesa-dev libpython3.11-dev python3-pip libopenmpi-dev
RUN apt install -y curl libssl-dev zlib1g-dev
RUN apt install -y patchelf freeglut3

ARG USERNAME=user
ARG GROUPNAME=user
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME
USER $USERNAME

RUN curl https://pyenv.run | bash
RUN ~/.pyenv/bin/pyenv install 3.11.4
RUN ~/.pyenv/bin/pyenv global 3.11.4
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 以下を設定しないとトレーニング中に 'Read -1, expected <someNumber>, errno = 1' というエラーが出てしまう
# 参考: https://github.com/open-mpi/ompi/issues/4948
RUN echo 'export OMPI_MCA_btl_vader_single_copy_mechanism=none' >> ~/.bashrc

WORKDIR /home/$USERNAME/DeepMimic
COPY requirements.txt /home/$USERNAME/DeepMimic
RUN ~/.pyenv/shims/pip install -r requirements.txt
RUN echo "export LD_LIBRARY_PATH=\"/home/$USERNAME/DeepMimic/DeepMimicCore/third/glew-2.1.0/lib:/home/$USERNAME/DeepMimic/DeepMimicCore/third/freeglut-3.0.0/lib\"" >> ~/.bashrc
